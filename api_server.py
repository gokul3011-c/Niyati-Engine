from flask import Flask, request, jsonify
from flask_cors import CORS
from core_logic import process_resumes
import pandas as pd
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})  # Enable CORS for frontend communication

@app.route('/api/analyze', methods=['POST'])
def analyze_resumes():
    try:
        # Get job description from form data
        jd = request.form.get('job_description', '')
        cutoff = float(request.form.get('cutoff', 70))
        
        # Get uploaded files
        if 'resumes' not in request.files:
            return jsonify({'error': 'No resumes uploaded'}), 400
            
        files = request.files.getlist('resumes')
        
        if not jd.strip():
            return jsonify({'error': 'Job description is required'}), 400
            
        if len(files) == 0 or all(f.filename == '' for f in files):
            return jsonify({'error': 'At least one resume is required'}), 400
        
        # Filter out empty files and ensure they have filenames
        valid_files = [f for f in files if f.filename and f.filename.strip()]
        
        if len(valid_files) == 0:
            return jsonify({'error': 'Please upload valid resume files'}), 400
        
        # Process resumes using existing core logic
        results = process_resumes(valid_files, jd)
        
        # Sort results by final score
        results = sorted(results, key=lambda x: x["Final Score %"], reverse=True)
        
        # Separate accepted and rejected
        accepted = [r for r in results if r["Final Score %"] >= cutoff]
        rejected = [r for r in results if r["Final Score %"] < cutoff]
        
        # Prepare response
        response_data = {
            'total': len(results),
            'accepted': len(accepted),
            'rejected': len(rejected),
            'accepted_candidates': accepted,
            'rejected_candidates': rejected,
            'all_candidates': results
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_results():
    try:
        data = request.json
        results = data.get('results', [])
        
        # Create DataFrame and convert to CSV
        df = pd.DataFrame(results)
        csv_data = df.to_csv(index=False)
        
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=niyati_results.csv'
        }
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
