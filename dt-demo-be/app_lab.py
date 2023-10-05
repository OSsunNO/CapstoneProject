from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from document import Document
import dbconn

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# TODO: Design document handling flow
did = 1
test_doc = Document(app, did)

# TODO: Design API for saving selected modules
@app.route("/api/filter/modules", methods=["POST"])
def post_selected_modules():
    return "post_selected_modules"

@app.route("/api/filter/detreport", methods=["GET"])
def get_det_report():
    app.logger.info("API request to get detection report")
    db_conn = dbconn.connect_to_db()
    test_doc.fetchDetReportInfo(db_conn)
    db_conn.close()

    return test_doc.getDetReportInfo()

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
    test_doc.fetchConvReportInfo(db_conn, data['option'])
    db_conn.close()

    return test_doc.getConvReportInfo()

if __name__ == '__main__':
    app.run(port='5001', debug=True)