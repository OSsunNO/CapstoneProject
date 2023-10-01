import json

modules = ["typo", "slang", "dup", "pdd", "spc"]

class Document:
    def __init__(self, app, did):
        self.app = app                      # Flask app: used for logging
        self.did = did                      # Document id: must be given
        self.dname = ""                     # Document name
        self.active_module = []             # Active module chosen from user
        self.module_count = {}              # Numbers of error detected from active module
        self.contents = ""                  # TODO: delete?
        self.sentences = []                 # List of Sentence objects
        self.error_rate = 0                 # TODO: check if "conversion" has happened.(Currently calculate upon size of detected value.)
        self.conv_contents = ""             # TODO: delete?

    def setDname(self, dbconn):
        self.app.logger.info("class Document - setDname(): "
                            + "Fetching dname ...")
        query = f"SELECT dname FROM doc WHERE did = {self.did}; "
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            self.dname = query_result[0]
            cursor.close()
        except Exception as e:
            self.app.logger.error("class Document - setDname(): "
                                  + "Error fetching dname from database.")
            self.app.logger.error("class Document - setDname():",e)

    def setActiveModule(self, dbconn):
        self.app.logger.info("class Document - setActiveModule(): "
                            + "Fetching active modules ...")
        query = ("SELECT "
                 +", ".join(modules)
                 +f" FROM doc WHERE did = {self.did};")
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()
            for i, q_r in enumerate(query_result[0]):
                if q_r == 1:
                    self.active_module.append(modules[i])
            cursor.close()
        except Exception as e:
            self.app.logger.error("class Document - setActiveModule(): "
                                  + "Error fetching active modules from database.")
            self.app.logger.error("class Document - setActiveModule():",e)

    def setModuleCount(self, dbconn):
        self.app.logger.info("class Document - setModuleCount(): "
                            + "Fetching module counts ...")
        queries = []
        for m in self.active_module:
            query = ""
            if m == "dup":
                query = ("SELECT COUNT(*) FROM sprocessing "
                         +f"WHERE dup = true AND did = {self.did};")
            else:
                query = (f"SELECT CAST(SUM(JSON_LENGTH(JSON_KEYS({m}))) AS SIGNED) "
                        +f"FROM sprocessing WHERE did = {self.did};")
            queries.append(query)
        
        try:
            cursor = dbconn.cursor()

            for i, q in enumerate(queries):
                cursor.execute(q)
                query_result = cursor.fetchone()
                self.module_count[self.active_module[i]] = query_result[0]

            cursor.close()
        except Exception as e:
            self.app.logger.error("class Document - setModuleCount(): "
                                  + "Error fetching module count from database.")
            self.app.logger.error("class Document - setModuleCount():",e)

    def setContents(self, dbconn):
        self.app.logger.info("class Document - setContents(): "
                            + "Fetching original document contents ...")
        query = f"SELECT contents FROM doc WHERE did = {self.did}; "
        try:
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            self.contents = query_result[0]
            cursor.close()
        except Exception as e:
            self.app.logger.error("class Document - setContents(): "
                                  + "Error fetching contents from database.")
            self.app.logger.error("class Document - setContents():",e)

    def setSentences(self, dbconn):
        '''
        This function initializes Sentence object for Detection Report Information.
        Setting error information and highlighting original content part is included.
        '''
        max_sid = 1
        columns = ["sid", "did", "osent"] + modules + ["csent"]

        query = f"SELECT MAX(sid) FROM sprocessing WHERE did = {self.did}; "
        try:
            self.app.logger.info("class Document - setSentences(): "
                                + "Fetching sentence indexes ...")
            cursor = dbconn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchone()
            max_sid = query_result[0]
            cursor.close()
        except Exception as e:
            self.app.logger.error("class Document - setSentences():",e)

        for i in range(1, max_sid+1, 1):
            query = f"SELECT * FROM sprocessing WHERE did = {self.did} AND sid = {i}; "

            try:
                self.app.logger.info("class Document - setSentences(): "
                                    + f"Fetching sentence #{i} ...")
                cursor = dbconn.cursor()
                cursor.execute(query)
                query_result = cursor.fetchall()

                osent = query_result[0][columns.index("osent")]
                sent = Sentence(self.app, self.did, i, osent)
                error_info = {}
                for m in modules:
                    error_info[m] = query_result[0][columns.index(m)]
                sent.setErrorInfo(error_info)
                self.sentences.append(sent)
                cursor.close()
            except Exception as e:
                self.app.logger.error("class Document - setSentences():",e)

        for s in self.sentences:
            s.highlightOriginalContent()

    def fetchDetReportInfo(self, dbconn):
        self.setDname(dbconn)
        if len(self.active_module) == 0:
            self.setActiveModule(dbconn)
        self.setModuleCount(dbconn)
        self.setContents(dbconn)
        if len(self.sentences) == 0:
            self.setSentences(dbconn)

    def getDetReportInfo(self):
        self.app.logger.info("class Document - getDetReportInfo(): "
                            + "Detection report information has been requested.")
        info_dict = {"did": self.did,
                "dname": self.dname,
                "active_module": self.active_module,
                "module_count": self.module_count,
                "contents": self.contents,
                "sentences": [s.getOriginalHighlightedContent() for s in self.sentences]}
        info_json = ""
        try:
            info_json = json.dumps(info_dict, ensure_ascii=False)
        except Exception as e:
            self.app.logger.warning("class Document - getDetReportInfo(): "
                                  + "Json auto generation failed.")
            self.app.logger.warning("class Document - getDetReportInfo(): "
                                  + "Trying to create Json result.")
            info_json = "{"
            for key, value in info_dict.items():
                info_json += f'"{key}": "{value}",'
            info_json = info_json.rstrip(',') 
            info_json += '}'
        self.app.logger.info("class Document - getDetReportInfo(): "
                            + "Returning detection report information.")
        return info_json

    def calculateOverviewRate(self):
        self.app.logger.info("class Document - calculateOverviewRate(): "
                            + "Calculating overall error rate ...")
        total_error_size = 0
        total_original_size = 0
        for s in self.sentences:
            error_size, original_size = s.getErrorSizePerSentence()
            total_error_size += error_size
            total_original_size += original_size
        self.error_rate = round((total_error_size/total_original_size)*100, 2)

    def fetchConvReportInfo(self, dbconn, option):
        # Confirm if necessary data has been prepared:
        if self.dname == "":
            self.app.logger.info("class Document - fetchConvReportInfo(): "
                                + "Conversion report information has not been ready yet.")
            self.fetchDetReportInfo(dbconn)

        # TODO: Process each sentence with different options

        # Contents without highlights
        self.conv_contents = ""
        for s in self.sentences:
            s.setConvertOption(option)
            s.setConvertedContent()
            self.conv_contents += s.getConvertedContent()+"\n" if s.getConvertedContent() != "" else ""

        # fetching conv report information
        self.calculateOverviewRate()
        for s in self.sentences:
            s.highlightConvertedContent()

    # TODO: conv report api request 전에는 무조건 det report api request 있어야 함
    def getConvReportInfo(self):
        self.app.logger.info("class Document - getConvReportInfo(): "
                            + "Conversion report information has been requested.")

        info_dict = {"did": self.did,
                "dname": self.dname,
                "overview_rate": f"{self.error_rate}{'%'}",
                "active_module": self.active_module,
                "module_count": self.module_count,
                "contents": self.contents,
                "converted_dname": self.dname.replace(".txt", "_filtered.txt"),
                "converted_contents": self.conv_contents,
                "details": {}}
        
        # Update details information for table data
        for s in self.sentences:
            # Table contains sentences with error detection
            if len(s.getDetectedErrorTypes()) > 0:
                info_dict["details"][f"{s.getSid()}"] = {}
                info_dict["details"][f"{s.getSid()}"]["type"] = s.getDetectedErrorTypes()
                info_dict["details"][f"{s.getSid()}"]["original_highlighted_sentences"] = s.getOriginalHighlightedContent()
                info_dict["details"][f"{s.getSid()}"]["converted_highlighted_sentences"] = s.getConvertedHighlightedContent()

        info_json = ""
        try:
            info_json = json.dumps(info_dict, ensure_ascii=False)
        except Exception as e:
            self.app.logger.warning("class Document - getConvReportInfo(): "
                                  + "Json auto generation failed.")
            self.app.logger.warning("class Document - getConvReportInfo(): "
                                  + "Trying to create Json result.")
            info_json = "{"
            for key, value in info_dict.items():
                info_json += f'"{key}": "{value}",'
            info_json = info_json.rstrip(',') 
            info_json += '}'
        self.app.logger.info("class Document - getConvReportInfo(): "
                            + "Returning detection report information.")
        return info_json

class Sentence:
    def __init__(self, app, did, sid, original_content):
        self.app = app                              # Flask app: used for logging
        self.did = did                              # document id: must be given
        self.sid = sid                              # sentence id: must be given
        self.original_content = original_content    # original content: must be given
        self.error_info = {}                        # error informatin for every modules(0 or 1 for duplication, json string for others)
        self.original_highlighted_content = ""      # original sentence with highlightings of detected errors
        self.converted_content = ""                 # converted sentence
        self.converted_highlighted_content = ""     # converted sentence with highlightings of converted parts
        self.convert_option = ""

    def isClean(self):
        isClean = True
        for m in modules:
            if m == "dup":
                if self.error_info[m] == 1:
                    isClean = False
            elif self.error_info[m] is not None:
                isClean = False
        return isClean

    def setErrorInfo(self, error_info):
        self.error_info = error_info
    
    def highlightOriginalContent(self):
        '''
        This function returns highlighted sentence with given tag.
        '''
        csent = self.original_content
        
        # Highlight only if error has been detected
        if self.error_info != {}:
            for m in modules:
                error_value = self.error_info[m]
                tag_st = f"<mark id='{m}'>"
                tag_end = "</mark>"

                # Duplication column stores different type of value
                if m == "dup":
                    # Highlight whole sentence if value is 1
                    # For duplication column, True means duplication detected
                    if error_value == 1:
                        csent = tag_st+self.original_content+tag_end

                # Confirm if error value exists
                elif error_value is not None:
                    error_info = json.loads(error_value)

                    # Iterate error information if multiple errors from same module have been detected.
                    for i in error_info:
                        dvalue = error_info[i]["dvalue"]
                        csent = csent.replace(dvalue, tag_st+dvalue+tag_end)

        self.original_highlighted_content = csent
    
    def setConvertOption(self, option):
        '''
        TODO: Remove me,
        TODO: Implement option on every errors.(DB design update needed.)
        Setter for convert opion "word" or "sentence"
        '''
        self.convert_option = option

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

        self.converted_content = self.original_content

        # Confirm this sentence has error_info
        if not self.isClean() :
            if self.convert_option == "remain":
                self.converted_content = self.original_content
            elif self.convert_option == "word":
                for m in modules:
                    if m == "dup":
                        if self.error_info[m]==1:
                            self.converted_content = ""
                    elif self.error_info[m] != None:
                        # type casting to dictionary type(from str)
                        temp_dict = json.loads(self.error_info[m])
                        for index in temp_dict:
                            self.converted_content = self.converted_content.replace(temp_dict[index]["dvalue"], temp_dict[index]["cvalue"])
            elif self.convert_option == "sentence":
                self.converted_content = ""

    def highlightConvertedContent(self):
        csent = self.converted_content

        # Highlight only if error has been detected
        if not self.isClean() :
            if self.convert_option == "word":
                for m in modules:
                    error_value = self.error_info[m]
                    tag_st = f"<mark id='{m}'>"
                    tag_end = "</mark>"

                    # Duplication column stores different type of value
                    if m == "dup":
                        # Highlight whole sentence if value is 1
                        # For duplication column, True means duplication detected
                        if error_value == 1:
                            # Retrun duplicated part with strike(del) tag to visualize elimination
                            csent = tag_st+"<del>"+self.original_content+"</del>"+tag_end

                    # Confirm if error value exists
                    elif error_value is not None:
                        error_info = json.loads(error_value)

                        # Iterate error information if multiple errors from same module have been detected.
                        for i in error_info:
                            dvalue = error_info[i]["cvalue"]
                            csent = csent.replace(dvalue, tag_st+dvalue+tag_end)

            elif self.convert_option == "sentence":

                tag_st = f"<mark id='{','.join(self.getDetectedErrorTypes())}'>"
                tag_end = "</mark>"
                csent = tag_st+"<del>"+self.original_content+"</del>"+tag_end
        
        self.converted_highlighted_content = csent


    def getSid(self):
        return self.sid

    def getOriginalContent(self):
        return self.original_content

    def getOriginalHighlightedContent(self):
        return self.original_highlighted_content
    
    def getDetectedErrorTypes(self):
        detected_error_types = []
        if not self.isClean() :
            for m in modules:
                if m == "dup":
                    if self.error_info[m] == 1:
                        detected_error_types.append(m)
                elif self.error_info[m] is not None:
                    detected_error_types.append(m)
        return detected_error_types
    
    def getErrorSizePerSentence(self):
        '''
        Function to return error size and original sentence size in byte
        '''

        # TODO: case handling: option - "sentence"

        original_size = len(self.original_content.encode('utf-8'))
        error_size = 0

        # Calculate error size only if error has been detected
        if not self.isClean() :
            if self.convert_option == "word":
                for m in modules:
                    # Case handling for duplication module(0 or 1)
                    if m == "dup":
                        # If given sentence is duplicated sentence
                        if self.error_info[m]==1:
                            error_size += original_size
                        # elif self.error_info[m]==0: means clean sentence
                    
                    # If error detected from other modules
                    elif self.error_info[m] != None:
                        temp_dict = json.loads(self.error_info[m])
                        # If given sentence has multiple errors in same module,
                        # index would increase.
                        # Otherwise index is "0"
                        for index in temp_dict:
                            error_size += len(temp_dict[index]["dvalue"].encode('utf-8'))
            elif self.convert_option == "sentence":
                error_size = original_size
        return error_size, original_size

    def getConvertedContent(self):
        return self.converted_content
    
    def getConvertedHighlightedContent(self):
        return self.converted_highlighted_content
    
    def getConvertOption(self):
        return self.convert_option