from flask import Flask, request, jsonify, render_template_string
from ecourts_scraper import ECourtsScraper
import os

app = Flask(__name__)
scraper = ECourtsScraper()

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>eCourts Scraper API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin: 15px 0; }
        input, select, button { padding: 8px; margin: 5px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>eCourts India Case Scraper</h1>
        
        <h3>Search by CNR</h3>
        <form id="cnrForm">
            <div class="form-group">
                <input type="text" id="cnr" placeholder="Enter CNR Number" required>
                <select id="cnrDate">
                    <option value="today">Today</option>
                    <option value="tomorrow">Tomorrow</option>
                </select>
                <button type="submit">Search</button>
            </div>
        </form>
        
        <h3>Search by Case Details</h3>
        <form id="caseForm">
            <div class="form-group">
                <input type="text" id="caseType" placeholder="Case Type" required>
                <input type="text" id="caseNumber" placeholder="Case Number" required>
                <input type="text" id="caseYear" placeholder="Year" required>
                <select id="caseDate">
                    <option value="today">Today</option>
                    <option value="tomorrow">Tomorrow</option>
                </select>
                <button type="submit">Search</button>
            </div>
        </form>
        
        <h3>Download Cause List</h3>
        <button onclick="downloadCauseList()">Download Today's Cause List</button>
        
        <div id="result" class="result" style="display:none;"></div>
    </div>

    <script>
        document.getElementById('cnrForm').onsubmit = function(e) {
            e.preventDefault();
            const cnr = document.getElementById('cnr').value;
            const date = document.getElementById('cnrDate').value;
            searchByCNR(cnr, date);
        };
        
        document.getElementById('caseForm').onsubmit = function(e) {
            e.preventDefault();
            const type = document.getElementById('caseType').value;
            const number = document.getElementById('caseNumber').value;
            const year = document.getElementById('caseYear').value;
            const date = document.getElementById('caseDate').value;
            searchByCase(type, number, year, date);
        };
        
        function searchByCNR(cnr, date) {
            fetch('/api/search/cnr', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({cnr: cnr, date_type: date})
            })
            .then(response => response.json())
            .then(data => displayResult(data));
        }
        
        function searchByCase(type, number, year, date) {
            fetch('/api/search/case', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    case_type: type, 
                    case_number: number, 
                    year: year, 
                    date_type: date
                })
            })
            .then(response => response.json())
            .then(data => displayResult(data));
        }
        
        function downloadCauseList() {
            fetch('/api/causelist')
            .then(response => response.json())
            .then(data => displayResult(data));
        }
        
        function displayResult(data) {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search/cnr', methods=['POST'])
def search_cnr():
    data = request.get_json()
    cnr = data.get('cnr')
    date_type = data.get('date_type', 'today')
    
    if not cnr:
        return jsonify({"error": "CNR number is required"}), 400
    
    result = scraper.search_by_cnr(cnr, date_type)
    return jsonify(result)

@app.route('/api/search/case', methods=['POST'])
def search_case():
    data = request.get_json()
    case_type = data.get('case_type')
    case_number = data.get('case_number')
    year = data.get('year')
    date_type = data.get('date_type', 'today')
    
    if not all([case_type, case_number, year]):
        return jsonify({"error": "Case type, number, and year are required"}), 400
    
    result = scraper.search_by_case_details(case_type, case_number, year, date_type)
    return jsonify(result)

@app.route('/api/causelist', methods=['GET'])
def get_causelist():
    result = scraper.get_cause_list()
    return jsonify(result)

@app.route('/api/download/pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    pdf_url = data.get('pdf_url')
    filename = data.get('filename')
    
    if not pdf_url:
        return jsonify({"error": "PDF URL is required"}), 400
    
    result = scraper.download_pdf(pdf_url, filename)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)