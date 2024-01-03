from flask import request, jsonify, send_file
import requests
import pandas as pd
from nltk.probability import FreqDist
import matplotlib
matplotlib.use("agg")
from io import BytesIO
import json
from sqlalchemy import text

from utils import tokenize, remove_punctuation,convert_to_lowercase,generate_pdf_report
from charts import graph_dist_len_words, graph_frequent_words

from database import app, db, Report

@app.route('/reports', methods=['GET'])
def reports():
    try:
        reports = Report.query.all()
        reports = [report.name for report in reports]
        return jsonify(reports)
    except:
        return "Error, There are not reports"

@app.route('/reports/<name>', methods=['GET'])
def reportsByName(name):
    try:
        report = Report.query.filter_by(name=name).first()
        data = json.loads(report.data)
        common_words = json.loads(report.common_words) 
        pdf_report = generate_pdf_report(data, common_words, "bar.png", "distribution.png")

        
        return send_file(BytesIO(pdf_report),
                             download_name=f'{report.name}.pdf',
                             mimetype='application/pdf') 
    except:
        return "Error, report not found"
    

@app.route('/')
def index():
    try:
        # Verificar la conexión ejecutando una consulta simple
        db.session.execute(text('SELECT 1'))

        return 'Successfully conection'
    except Exception as e:
        print(f'Conection Error: {e}')
        return "Database not found"


@app.route('/generate-pdf', methods=['POST'])
def generatePdf():
    db.create_all()
    api_url = 'https://baconipsum.com/api/?type=all-meat'
    data = request.json
    size = data["paragraphs"]
    name = data["name"]

    try:
        size = data["paragraphs"]
        name = data["name"]
        response = requests.get(f"{api_url}&paras={size}")
        if response.status_code==200:
            data = response.json()

            #Transform to dataframe
            df = pd.DataFrame(data)

            #Transform data, tokenization, punctuation removal, and converting text to lowercase       
            df["transformed"] = df[0].apply(tokenize)
            df["transformed"] = df["transformed"].apply(remove_punctuation)
            df["transformed"] = df["transformed"].apply(convert_to_lowercase)

            # Frequency words
            all_tokens = [token for sublist in df["transformed"] for token in sublist]
            freq_dist = FreqDist(all_tokens)
            common_words = freq_dist.most_common(10)

            # Visualization: Bar Chart Frequency words
            graph_frequent_words(common_words)

            # Length words distribution
            graph_dist_len_words(df)

            #Generate PDF
            pdf_report = generate_pdf_report(data, common_words, df, "bar.png", "distribution.png")
            
            #Save Report in DB
            report = Report(name=name, data=json.dumps(data), common_words=json.dumps(common_words))
            db.session.add(report)
            db.session.commit()
            
            return send_file(BytesIO(pdf_report),
                             download_name=f'{name}.pdf',
                             mimetype='application/pdf')

        else:
            return jsonify({"Error: Request Error"})
    
    except Exception as e:
        return jsonify({"Error:Request Error"})
    
if __name__ == '__main__':
    app.run(debug=True)