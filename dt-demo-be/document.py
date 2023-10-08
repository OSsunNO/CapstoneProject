import json

modules = ["typo", "slang", "dup", "pdd", "spc"]

class Document:
    def __init__(self, app, did=None):
        self.__app = app                      # Flask app: used for logging
        self.__did = 0                        # Document id
        self.__dname = ""                     # Document name
        self.__active_module = []             # Active module chosen from user
        self.__module_count = {}              # Numbers of error detected from active module
        self.__contents = ""                  # TODO: delete?
        self.__sentences = []                 # List of Sentence objects
        self.__conv_contents = ""             # TODO: delete?
        if did:
            # TODO: remove me, did must be created by database(automatically)
            self.__did = did

    def upload(self, name, contents, dbconn):
        # TODO: Discuss Trial limit num
        
        # Insert document on doc table with dname
        # Verify if dname is unique.
        trial_limit = 2
        for i in range(1, trial_limit+1):
            dname = name if i==1 else f"{name.replace('.txt','_{}.txt'.format(i))}"
            self.__app.logger.info("class Document - upload(): "
                                + f"Uploading document on doc table trial#{i} with dname:{dname}...")
            query = f"INSERT INTO doc (dname, contents) VALUES (%s, %s); "
            data = (dname, contents)
            try:
                cursor = dbconn.cursor()
                cursor.execute(query, data)
                dbconn.commit()
                cursor.close()
                # Set member variable: __dname, __contents
                self.__dname = dname
                self.__contents = contents

                if self.__contents == "":
                    self.__app.logger.error("class Document - upload(): "
                                        + "Contents is empty.")
                    return "UPLOAD FAIL"

                # When Query succeed
                break
            except dbconn.Error as e:
                self.__app.logger.error("class Document - upload(): "
                                    + f"Error uploading document with name {dname}")
                self.__app.logger.error(f"class Document - upload(): {e}")

        # get did from db and set self.__did
        if self.__dname != "": 
            self.__app.logger.info("class Document - upload(): "
                        + "Fetching did(auto-generated from database) ...")
            query = f"SELECT did FROM doc WHERE dname = '{self.__dname}'; "
            try:
                cursor = dbconn.cursor()
                cursor.execute(query)
                query_result = cursor.fetchone()
                self.__did = query_result[0]
                cursor.close()
            except dbconn.Error as e:
                self.__app.logger.error("class Document - upload(): "
                                    + "Error fetching did from database.")
                self.__app.logger.error(f"class Document - upload(): {e}")
                return "UPLOAD FAIL"
        else:
            return "UPLOAD FAIL"
        return "SUCCESS"

    def splitContents(self, dbconn):
        '''
        This function splits contents into sentences and stores them into sprocessing table.
        '''
        self.__app.logger.info("class Document - splitContent(): "
                            + "Splitting contents into sentences ...")
        try:
            sentences = self.__contents.split("\n")   # TODO: decide delimiters

            sid = 1
            for sentence in sentences:
                query = ("INSERT INTO sprocessing (sid, did, osent) "
                        +f"VALUES ({sid}, {self.__did}, '{sentence}');")
                cursor = dbconn.cursor()
                cursor.execute(query)
                dbconn.commit()
                cursor.close()
                
                sid += 1
            return "SUCCESS"
        except Exception as e:
            self.__app.logger.error("class Document - splitContent(): "
                                    + "Error splitting contents into sentences.")
            self.__app.logger.error("class Document - splitContent():",e)
            return "SPLIT FAIL"

    def getDname(self):
        return self.__dname
    
    # TODO: remove me
    def __setDname(self, dbconn):
        self.__app.logger.info("class Document - setDname(): "
                            + "Fetching dname ...")
        query = f"SELECT dname FROM doc WHERE did = {self.__did}; "
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            self.__dname = query_result[0]
            cursor.close()
        except Exception as e:
            self.__app.logger.error("class Document - setDname(): "
                                  + "Error fetching dname from database.")
            self.__app.logger.error("class Document - setDname():",e)

    def __setActiveModule(self, dbconn):
        self.__app.logger.info("class Document - setActiveModule(): "
                            + "Fetching active modules ...")
        query = ("SELECT "
                 +", ".join(modules)
                 +f" FROM doc WHERE did = {self.__did};")
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()
            for i, q_r in enumerate(query_result[0]):
                if q_r == 1:
                    self.__active_module.append(modules[i])
            cursor.close()
        except Exception as e:
            self.__app.logger.error("class Document - setActiveModule(): "
                                  + "Error fetching active modules from database.")
            self.__app.logger.error("class Document - setActiveModule():",e)

    def __setModuleCount(self, dbconn):
        self.__app.logger.info("class Document - setModuleCount(): "
                            + "Fetching module counts ...")
        queries = []
        for m in self.__active_module:
            query = ""
            if m == "dup":
                query = ("SELECT COUNT(*) FROM sprocessing "
                         +f"WHERE dup = true AND did = {self.__did};")
            else:
                query = (f"SELECT CAST(SUM(JSON_LENGTH(JSON_KEYS({m}))) AS SIGNED) "
                        +f"FROM sprocessing WHERE did = {self.__did};")
            queries.append(query)
        
        try:
            cursor = dbconn.cursor()

            for i, q in enumerate(queries):
                cursor.execute(q)
                query_result = cursor.fetchone()
                self.__module_count[self.__active_module[i]] = query_result[0]

            cursor.close()
        except Exception as e:
            self.__app.logger.error("class Document - setModuleCount(): "
                                  + "Error fetching module count from database.")
            self.__app.logger.error("class Document - setModuleCount():",e)

    def __setContents(self, dbconn):
        self.__app.logger.info("class Document - setContents(): "
                            + "Fetching original document contents ...")
        query = f"SELECT contents FROM doc WHERE did = {self.__did}; "
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            self.__contents = query_result[0]
            cursor.close()
        except Exception as e:
            self.__app.logger.error("class Document - setContents(): "
                                  + "Error fetching contents from database.")
            self.__app.logger.error("class Document - setContents():",e)

    def __setSentences(self, dbconn):
        '''
        This function initializes Sentence object for Detection Report Information.
        Setting error information and highlighting original content part is included.
        '''
        max_sid = 1
        columns = ["sid", "did", "osent"] + modules + ["csent"]

        query = f"SELECT MAX(sid) FROM sprocessing WHERE did = {self.__did}; "
        try:
            self.__app.logger.info("class Document - setSentences(): "
                                + "Fetching sentence indexes ...")
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            max_sid = query_result[0]
            cursor.close()
        except Exception as e:
            self.__app.logger.error("class Document - setSentences():",e)

        for i in range(1, max_sid+1, 1):
            query = f"SELECT * FROM sprocessing WHERE did = {self.__did} AND sid = {i}; "

            try:
                self.__app.logger.info("class Document - setSentences(): "
                                    + f"Fetching sentence #{i} ...")
                cursor = dbconn.cursor()
                cursor.execute(query)
                query_result = cursor.fetchall()

                osent = query_result[0][columns.index("osent")]
                sent = Sentence(self.__app, self.__did, i, osent)
                error_info = {}
                for m in modules:
                    error_info[m] = query_result[0][columns.index(m)]
                sent.setErrorInfo(error_info)
                self.__sentences.append(sent)
                cursor.close()
            except Exception as e:
                self.__app.logger.error("class Document - setSentences():",e)

        for s in self.__sentences:
            s.highlightOriginalContent()

    def fetchDetReportInfo(self, dbconn):
        self.__setDname(dbconn)
        if len(self.__active_module) == 0:
            self.__setActiveModule(dbconn)
        self.__setModuleCount(dbconn)
        self.__setContents(dbconn)
        if len(self.__sentences) == 0:
            self.__setSentences(dbconn)

    def getDetReportInfo(self):
        self.__app.logger.info("class Document - getDetReportInfo(): "
                            + "Detection report information has been requested.")
        info_dict = {"did": self.__did,
                "dname": self.__dname,
                "active_module": self.__active_module,
                "module_count": self.__module_count,
                "contents": self.__contents,
                "sentences": [s.getOriginalHighlightedContent() for s in self.__sentences]}
        info_json = ""
        try:
            info_json = json.dumps(info_dict, ensure_ascii=False)
        except Exception as e:
            self.__app.logger.warning("class Document - getDetReportInfo(): "
                                  + "Json auto generation failed.")
            self.__app.logger.warning("class Document - getDetReportInfo(): "
                                  + "Trying to create Json result.")
            info_json = "{"
            for key, value in info_dict.items():
                info_json += f'"{key}": "{value}",'
            info_json = info_json.rstrip(',') 
            info_json += '}'
        self.__app.logger.info("class Document - getDetReportInfo(): "
                            + "Returning detection report information.")
        return info_json

    def __calculateOverviewRate(self):
        self.__app.logger.info("class Document - calculateOverviewRate(): "
                            + "Calculating overall error rate ...")
        total_error_size = 0
        total_original_size = 0
        for s in self.__sentences:
            error_size, original_size = s.getErrorSizePerSentence()
            total_error_size += error_size
            total_original_size += original_size
        return round((total_error_size/total_original_size)*100, 2)

    def fetchConvReportInfo(self, dbconn, option):
        # Confirm if necessary data has been prepared:
        if self.__dname == "":
            self.__app.logger.info("class Document - fetchConvReportInfo(): "
                                + "Conversion report information has not been ready yet.")
            self.fetchDetReportInfo(dbconn)

        # TODO: Process each sentence with different options

        # Contents without highlights
        self.__conv_contents = ""
        for s in self.__sentences:
            s.setConvertOption(option)
            s.setConvertedContent()
            s.highlightConvertedContent()

    def getConvReportInfo(self):
        self.__app.logger.info("class Document - getConvReportInfo(): "
                            + "Conversion report information has been requested.")

        info_dict = {"did": self.__did,
                "dname": self.__dname,
                "overview_rate": f"{0}{'%'}",
                "active_module": self.__active_module,
                "module_count": self.__module_count,
                "contents": self.__contents,
                "converted_dname": self.__dname.replace(".txt", "_filtered.txt"),
                "converted_contents": self.__conv_contents,
                "details": {}}
        
        info_dict["overview_rate"] = f"{self.__calculateOverviewRate()}{'%'}"

        # Update details information for table data
        for s in self.__sentences:
            self.__conv_contents += s.getConvertedContent()+"\n" if s.getConvertedContent() != "" else ""
            # Table contains sentences with error detection
            if len(s.getDetectedErrorTypes()) > 0:
                info_dict["details"][f"{s.getSid()}"] = {}
                info_dict["details"][f"{s.getSid()}"]["type"] = s.getDetectedErrorTypes()
                info_dict["details"][f"{s.getSid()}"]["original_highlighted_sentences"] = s.getOriginalHighlightedContent()
                info_dict["details"][f"{s.getSid()}"]["converted_highlighted_sentences"] = s.getConvertedHighlightedContent()

        info_dict["converted_contents"] = self.__conv_contents

        info_json = ""
        try:
            info_json = json.dumps(info_dict, ensure_ascii=False)
        except Exception as e:
            self.__app.logger.warning("class Document - getConvReportInfo(): "
                                  + "Json auto generation failed.")
            self.__app.logger.warning("class Document - getConvReportInfo(): "
                                  + "Trying to create Json result.")
            info_json = "{"
            for key, value in info_dict.items():
                info_json += f'"{key}": "{value}",'
            info_json = info_json.rstrip(',') 
            info_json += '}'
        self.__app.logger.info("class Document - getConvReportInfo(): "
                            + "Returning detection report information.")
        return info_json

class Sentence:
    def __init__(self, app, did, sid, original_content):
        self.__app = app                              # Flask app: used for logging
        self.__did = did                              # document id: must be given
        self.__sid = sid                              # sentence id: must be given
        self.__original_content = original_content    # original content: must be given
        self.__error_info = {}                        # error informatin for every modules(0 or 1 for duplication, json string for others)
        self.__original_highlighted_content = ""      # original sentence with highlightings of detected errors
        self.__converted_content = ""                 # converted sentence
        self.__converted_highlighted_content = ""     # converted sentence with highlightings of converted parts
        self.__convert_option = ""

    def __isClean(self):
        isClean = True
        for m in modules:
            if m == "dup":
                if self.__error_info[m] == 1:
                    isClean = False
            elif self.__error_info[m] is not None:
                isClean = False
        return isClean

    def setErrorInfo(self, error_info):
        self.__error_info = error_info
    
    def setConvertOption(self, option):
        '''
        TODO: Remove me,
        TODO: Implement option on every errors.(DB design update needed.)
        Setter for convert opion "word" or "sentence"
        '''
        self.__convert_option = option

    def highlightOriginalContent(self):
        '''
        This function returns highlighted sentence with given tag.
        '''
        csent = self.__original_content
        
        # Highlight only if error has been detected
        if not self.__isClean():
            for m in modules:
                error_value = self.__error_info[m]
                tag_st = f"<mark id='{m}'>"
                tag_end = "</mark>"

                # Duplication column stores different type of value
                if m == "dup":
                    # Highlight whole sentence if value is 1
                    # For duplication column, True means duplication detected
                    if error_value == 1:
                        csent = tag_st+self.__original_content+tag_end

                # Confirm if error value exists
                elif error_value is not None:
                    error_info = json.loads(error_value)

                    # Iterate error information if multiple errors from same module have been detected.
                    for i in error_info:
                        dvalue = error_info[i]["dvalue"]
                        csent = csent.replace(dvalue, tag_st+dvalue+tag_end)

        self.__original_highlighted_content = csent

    def setConvertedContent(self):
        '''
        convert_option would be word or sentence at the moment
        TODO: add more converting option on each errors
        op1. remain
        op2. converting
        op3. "word" - deleting error part
        op4. "sentence" - deleting whole sentence
        '''

        # TODO: update each sentences' convert_opion on database

        self.__converted_content = self.__original_content

        # Confirm this sentence has error_info
        if not self.__isClean() :
            if self.__convert_option == "remain":
                self.__converted_content = self.__original_content
            elif self.__convert_option == "word":
                for m in modules:
                    if m == "dup":
                        if self.__error_info[m]==1:
                            self.__converted_content = ""
                    elif self.__error_info[m] != None:
                        # type casting to dictionary type(from str)
                        temp_dict = json.loads(self.__error_info[m])
                        for index in temp_dict:
                            self.__converted_content = self.__converted_content.replace(temp_dict[index]["dvalue"], temp_dict[index]["cvalue"])
            elif self.__convert_option == "sentence":
                self.__converted_content = ""

    def highlightConvertedContent(self):
        csent = self.__converted_content

        # Highlight only if error has been detected
        if not self.__isClean() :
            if self.__convert_option == "word":
                for m in modules:
                    error_value = self.__error_info[m]
                    tag_st = f"<mark id='{m}'>"
                    tag_end = "</mark>"

                    # Duplication column stores different type of value
                    if m == "dup":
                        # Highlight whole sentence if value is 1
                        # For duplication column, True means duplication detected
                        if error_value == 1:
                            # Retrun duplicated part with strike(del) tag to visualize elimination
                            csent = tag_st+"<del>"+self.__original_content+"</del>"+tag_end

                    # Confirm if error value exists
                    elif error_value is not None:
                        error_info = json.loads(error_value)

                        # Iterate error information if multiple errors from same module have been detected.
                        for i in error_info:
                            dvalue = error_info[i]["cvalue"]
                            csent = csent.replace(dvalue, tag_st+dvalue+tag_end)

            elif self.__convert_option == "sentence":

                tag_st = f"<mark id='{','.join(self.getDetectedErrorTypes())}'>"
                tag_end = "</mark>"
                csent = tag_st+"<del>"+self.__original_content+"</del>"+tag_end
        
        self.__converted_highlighted_content = csent

    def getSid(self):
        return self.__sid

    def getOriginalContent(self):
        return self.__original_content

    def getOriginalHighlightedContent(self):
        return self.__original_highlighted_content
    
    def getDetectedErrorTypes(self):
        detected_error_types = []
        if not self.__isClean() :
            for m in modules:
                if m == "dup":
                    if self.__error_info[m] == 1:
                        detected_error_types.append(m)
                elif self.__error_info[m] is not None:
                    detected_error_types.append(m)
        return detected_error_types
    
    def getErrorSizePerSentence(self):
        '''
        Function to return error size and original sentence size in byte
        '''

        # TODO: case handling: option - "sentence"

        original_size = len(self.__original_content.encode('utf-8'))
        error_size = 0

        # Calculate error size only if error has been detected
        if not self.__isClean() :
            if self.__convert_option == "word":
                for m in modules:
                    # Case handling for duplication module(0 or 1)
                    if m == "dup":
                        # If given sentence is duplicated sentence
                        if self.__error_info[m]==1:
                            error_size += original_size
                        # elif self.__error_info[m]==0: means clean sentence
                    
                    # If error detected from other modules
                    elif self.__error_info[m] != None:
                        temp_dict = json.loads(self.__error_info[m])
                        # If given sentence has multiple errors in same module,
                        # index would increase.
                        # Otherwise index is "0"
                        for index in temp_dict:
                            error_size += len(temp_dict[index]["dvalue"].encode('utf-8'))
            elif self.__convert_option == "sentence":
                error_size = original_size
        return error_size, original_size

    def getConvertedContent(self):
        return self.__converted_content
    
    def getConvertedHighlightedContent(self):
        return self.__converted_highlighted_content
    
    def getConvertOption(self):
        return self.__convert_option