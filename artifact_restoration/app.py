"""
Flask Application for Artifact Restoration Multi-Agent System
Using Google ADK (Agent Development Kit)
"""

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import traceback
import os
import base64
from werkzeug.utils import secure_filename

# Import setup first to ensure authentication
from setup_adk import GEMINI_API_KEY

# Import ADK agents
from agents.adk_root_agent import RootAgent

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize root agent once
print("[INIT] Initializing ADK Multi-Agent System...")
root_agent = RootAgent()
print("[OK] Application ready!")


@app.route('/')
def index():
    """Main page with input form"""
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/process_artifact', methods=['POST'])
def process_artifact():
    """
    Process artifact through multi-agent system
    
    Expected Form Data:
    - image: uploaded file
    - time_span: number (years for environmental analysis)
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read image and convert to base64
        with open(filepath, 'rb') as f:
            image_data = f.read()
            original_image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        time_span = int(request.form.get('time_span', 10))
        
        # Process with multi-agent system
        results = root_agent.process_artifact(filepath, time_span)
        
        # Format response to match frontend expectations
        response_data = {
            'success': True,
            'results': {
                'workflow_status': results.get('workflow_status'),
                'original_image': original_image_b64,
                'restored_image': results.get('restored_image'),
                'time_span': time_span,
                'restoration': {
                    'status': results.get('restoration', {}).get('status'),
                    'message': 'Restoration completed successfully',
                    'response': results.get('restoration', {}).get('analysis', ''),
                    'restoration_details': f"Restoration Level: {results.get('restoration', {}).get('restoration_level', 'medium')}"
                },
                'data_fetcher': {
                    'status': 'success' if results.get('data_fetcher', {}).get('status') == 'success' else 'error',
                    'message': 'Historical data retrieved',
                    'historical_data': results.get('data_fetcher', {}).get('historical_context', '')
                },
                'environmental': {
                    'status': 'success' if results.get('environmental', {}).get('status') == 'success' else 'error',
                    'message': 'Environmental analysis completed',
                    'time_span': time_span,
                    'environmental_analysis': results.get('environmental', {}).get('environmental_predictions', '')
                },
                'degradation_predictions': [
                    {
                        'year': int(time_span * 0.25),
                        'condition': f"{results.get('environmental', {}).get('degradation_data', {}).get('degradation_percentage', 0) * 0.25:.1f}% degradation - Early stage"
                    },
                    {
                        'year': int(time_span * 0.5),
                        'condition': f"{results.get('environmental', {}).get('degradation_data', {}).get('degradation_percentage', 0) * 0.5:.1f}% degradation - Mid stage"
                    },
                    {
                        'year': int(time_span * 0.75),
                        'condition': f"{results.get('environmental', {}).get('degradation_data', {}).get('degradation_percentage', 0) * 0.75:.1f}% degradation - Advanced stage"
                    },
                    {
                        'year': time_span,
                        'condition': results.get('environmental', {}).get('degradation_data', {}).get('condition', 'Unknown')
                    }
                ]
            }
        }
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/dashboard')
def dashboard():
    """Dashboard to display results"""
    response = make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Artifact Restoration Multi-Agent System'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("ARTIFACT RESTORATION SYSTEM")
    print("    Powered by Google ADK Multi-Agent Architecture")
    print("="*60)
    print("\n[SERVER] Starting Flask server...")
    print("[URL] Open http://localhost:5000 in your browser")
    print("[AGENTS] Restoration -> Data Fetcher -> Environmental")
    print("\n[INFO] Debug mode disabled (Windows ADK compatibility)")
    print("\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
