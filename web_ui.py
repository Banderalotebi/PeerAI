#!/usr/bin/env python3
"""
PeerAI Web UI
واجهة الويب لـ PeerAI
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import requests
import json
import os

app = Flask(__name__)

# HTML template for the web UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PeerAI - Decentralized AI Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background-color: #4CAF50;
        }
        
        .status-offline {
            background-color: #f44336;
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .result {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-family: monospace;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .tabs {
            display: flex;
            margin-bottom: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            background: transparent;
            font-size: 1rem;
        }
        
        .tab.active {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 PeerAI</h1>
            <p>Decentralized AI Training & Sharing Platform</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3>📊 System Status</h3>
                <p><span class="status-indicator status-online"></span>PeerAI API: <span id="api-status">Checking...</span></p>
                <p><span class="status-indicator status-online"></span>IPFS Node: <span id="ipfs-status">Checking...</span></p>
                <p><span class="status-indicator status-online"></span>IPFS Gateway: <span id="gateway-status">Checking...</span></p>
                <button class="btn" onclick="checkStatus()">🔄 Refresh Status</button>
            </div>
            
            <div class="card">
                <h3>🔗 Quick Links</h3>
                <a href="http://localhost:8000" target="_blank" class="btn">📡 API Documentation</a>
                <a href="http://localhost:8080" target="_blank" class="btn">🌐 IPFS Gateway</a>
                <a href="http://localhost:5001/api/v0/version" target="_blank" class="btn">🔧 IPFS API</a>
            </div>
            
            <div class="card">
                <h3>📈 Statistics</h3>
                <p>Models Available: <span id="model-count">-</span></p>
                <p>Datasets Available: <span id="dataset-count">-</span></p>
                <p>Node ID: <span id="node-id">-</span></p>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('training')">🎯 Model Training</button>
            <button class="tab" onclick="showTab('prediction')">🔮 Prediction</button>
            <button class="tab" onclick="showTab('nlp')">📝 NLP Tools</button>
            <button class="tab" onclick="showTab('ipfs')">🌐 IPFS Management</button>
        </div>
        
        <div id="training" class="tab-content active">
            <div class="card">
                <h3>🎯 Train a New Model</h3>
                <form id="training-form">
                    <div class="form-group">
                        <label>Dataset Path:</label>
                        <input type="text" name="data_path" value="sample_data/iris.csv" required>
                    </div>
                    <div class="form-group">
                        <label>Target Column:</label>
                        <input type="text" name="target" value="target" required>
                    </div>
                    <div class="form-group">
                        <label>Algorithm:</label>
                        <select name="algorithm" required>
                            <option value="random_forest">Random Forest</option>
                            <option value="svm">SVM</option>
                            <option value="logistic_regression">Logistic Regression</option>
                            <option value="decision_tree">Decision Tree</option>
                            <option value="knn">K-Nearest Neighbors</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Task Type:</label>
                        <select name="task_type" required>
                            <option value="classification">Classification</option>
                            <option value="regression">Regression</option>
                            <option value="clustering">Clustering</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">🚀 Start Training</button>
                </form>
                <div id="training-result" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div id="prediction" class="tab-content">
            <div class="card">
                <h3>🔮 Make Predictions</h3>
                <form id="prediction-form">
                    <div class="form-group">
                        <label>Model Path:</label>
                        <input type="text" name="model_path" value="models/random_forest_classification_model.pkl" required>
                    </div>
                    <div class="form-group">
                        <label>Features (JSON array):</label>
                        <textarea name="features" rows="4" placeholder='[{"feature1": 1.0, "feature2": 2.0}]' required></textarea>
                    </div>
                    <button type="submit" class="btn">🔮 Predict</button>
                </form>
                <div id="prediction-result" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div id="nlp" class="tab-content">
            <div class="card">
                <h3>📝 NLP Analysis</h3>
                <form id="nlp-form">
                    <div class="form-group">
                        <label>Text:</label>
                        <textarea name="text" rows="4" placeholder="Enter text to analyze..." required></textarea>
                    </div>
                    <div class="form-group">
                        <label>Analysis Type:</label>
                        <select name="analysis_type">
                            <option value="sentiment">Sentiment Analysis</option>
                            <option value="entities">Entity Extraction</option>
                            <option value="summary">Text Summary</option>
                            <option value="features">Text Features</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">📊 Analyze</button>
                </form>
                <div id="nlp-result" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div id="ipfs" class="tab-content">
            <div class="card">
                <h3>🌐 IPFS Management</h3>
                <button class="btn" onclick="listModels()">📋 List Models</button>
                <button class="btn" onclick="listDatasets()">📊 List Datasets</button>
                <button class="btn btn-secondary" onclick="uploadToIPFS()">📤 Upload to IPFS</button>
                <div id="ipfs-result" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>PeerAI v2.0 - Built with ❤️ for decentralized AI</p>
        </div>
    </div>
    
    <script>
        // Check system status on page load
        window.onload = function() {
            checkStatus();
            loadStatistics();
        };
        
        function showTab(tabName) {
            // Hide all tab contents
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        async function checkStatus() {
            try {
                // Check PeerAI API
                const apiResponse = await fetch('http://localhost:8000/health');
                document.getElementById('api-status').textContent = apiResponse.ok ? 'Online' : 'Offline';
                
                // Check IPFS API
                const ipfsResponse = await fetch('http://localhost:5001/api/v0/version');
                document.getElementById('ipfs-status').textContent = ipfsResponse.ok ? 'Online' : 'Offline';
                
                // Check IPFS Gateway
                const gatewayResponse = await fetch('http://localhost:8080');
                document.getElementById('gateway-status').textContent = gatewayResponse.ok ? 'Online' : 'Offline';
            } catch (error) {
                document.getElementById('api-status').textContent = 'Offline';
                document.getElementById('ipfs-status').textContent = 'Offline';
                document.getElementById('gateway-status').textContent = 'Offline';
            }
        }
        
        async function loadStatistics() {
            try {
                const response = await fetch('http://localhost:8000/list_models');
                const data = await response.json();
                document.getElementById('model-count').textContent = data.count || 0;
            } catch (error) {
                document.getElementById('model-count').textContent = 'Error';
            }
            
            document.getElementById('node-id').textContent = 'peerai-node-' + Date.now();
        }
        
        // Training form submission
        document.getElementById('training-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('http://localhost:8000/train', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('training-result');
                resultDiv.textContent = JSON.stringify(result, null, 2);
                resultDiv.style.display = 'block';
            } catch (error) {
                const resultDiv = document.getElementById('training-result');
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.style.display = 'block';
            }
        });
        
        // Prediction form submission
        document.getElementById('prediction-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                data.features = JSON.parse(data.features);
                const response = await fetch('http://localhost:8000/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('prediction-result');
                resultDiv.textContent = JSON.stringify(result, null, 2);
                resultDiv.style.display = 'block';
            } catch (error) {
                const resultDiv = document.getElementById('prediction-result');
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.style.display = 'block';
            }
        });
        
        // NLP form submission
        document.getElementById('nlp-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const endpoint = '/nlp/' + data.analysis_type;
                const response = await fetch('http://localhost:8000' + endpoint, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: data.text})
                });
                
                const result = await response.json();
                const resultDiv = document.getElementById('nlp-result');
                resultDiv.textContent = JSON.stringify(result, null, 2);
                resultDiv.style.display = 'block';
            } catch (error) {
                const resultDiv = document.getElementById('nlp-result');
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.style.display = 'block';
            }
        });
        
        async function listModels() {
            try {
                const response = await fetch('http://localhost:8000/list_models');
                const result = await response.json();
                const resultDiv = document.getElementById('ipfs-result');
                resultDiv.textContent = JSON.stringify(result, null, 2);
                resultDiv.style.display = 'block';
            } catch (error) {
                const resultDiv = document.getElementById('ipfs-result');
                resultDiv.textContent = 'Error: ' + error.message;
                resultDiv.style.display = 'block';
            }
        }
        
        async function listDatasets() {
            const resultDiv = document.getElementById('ipfs-result');
            resultDiv.textContent = 'Datasets feature coming soon...';
            resultDiv.style.display = 'block';
        }
        
        async function uploadToIPFS() {
            const resultDiv = document.getElementById('ipfs-result');
            resultDiv.textContent = 'IPFS upload feature coming soon...';
            resultDiv.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "web-ui"})

if __name__ == '__main__':
    port = int(os.environ.get('WEB_PORT', 8001))
    app.run(debug=True, host='0.0.0.0', port=port) 