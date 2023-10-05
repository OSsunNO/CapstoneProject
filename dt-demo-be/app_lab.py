from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from document import Document
import dbconn

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# TODO: Remove did and created_doc after implementing uploading flow
did = 1
created_doc = Document(app, did)

test_doc = None # This is user-uploaded file

@app.route("/api/filter/upload", methods=["POST"])
def file_upload():
    app.logger.info("API request on upload func: POST")
    uploaded_status = "FAIL"
    isFileExists = 'file' in request.files and request.files['file'] is not None
    if isFileExists:
        file = request.files['file']
        contents = file.read().decode('utf-8')

        db_conn = dbconn.connect_to_db()
        test_doc = Document(app)
        uploaded_status = test_doc.upload(file.filename, contents, db_conn)
        db_conn.close()
        
    return jsonify({'result': uploaded_status})

# TODO: Design API for saving selected modules
@app.route("/api/filter/modules", methods=["POST"])
def post_selected_modules():
    return "post_selected_modules"

@app.route("/api/filter/detreport", methods=["GET"])
def get_det_report():
    app.logger.info("API request to get detection report")
    db_conn = dbconn.connect_to_db()
    # TODO: remove created_doc
    created_doc.fetchDetReportInfo(db_conn)
    db_conn.close()

    return created_doc.getDetReportInfo()

@app.route("/api/filter/convreport", methods=["POST"])
def get_conv_report():
    '''
    TODO: Update option for every errors
    Sample API body1
    {
        "option": "word"
    }

    Sample API body2
    {
        "option": "sentence"
    }
    '''
    data = request.json
    app.logger.info(f"API request to get conversion report with option:{data['option']}")
    db_conn = dbconn.connect_to_db()
    # TODO: remove created_doc
    created_doc.fetchConvReportInfo(db_conn, data['option'])
    db_conn.close()

    return created_doc.getConvReportInfo()

if __name__ == '__main__':
    app.run(port='5001', debug=True)