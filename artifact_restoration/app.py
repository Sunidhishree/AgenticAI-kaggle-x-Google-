"""
Flask Application for Artifact Restoration Multi-Agent System
Using Google ADK (Agent Development Kit) with Sequential Agents, MCP, and Context Engineering
"""

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import traceback
import os
import base64
from werkzeug.utils import secure_filename

# Import setup first to ensure authentication
from setup_adk import GEMINI_API_KEY

# Import new ADK Orchestrator with sequential agents
from adk_orchestrator import ADKOrchestrator

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize ADK Orchestrator with sequential agents, MCP, and context engineering
orchestrator = ADKOrchestrator()
print("[OK] Application ready with ADK Sequential Agents!")


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
        restoration_level = request.form.get('restoration_level', 'medium')
        
        # Process with ADK Orchestrator (sequential agents + context engineering)
        results = orchestrator.process_artifact(filepath, restoration_level, time_span)
        
        # Extract results from sequential agent outputs
        vision_data = results.get('vision_analysis', {})
        restoration_data = results.get('restoration', {})
        historical_data = results.get('historical_context', {})
        environmental_data = results.get('environmental_prediction', {})
        
        # Format response to match frontend expectations
        response_data = {
            'success': results.get('workflow_status') == 'completed',
            'results': {
                'workflow_status': results.get('workflow_status'),
                'agents_executed': results.get('agents_executed', []),
                'context_summary': results.get('context_summary', {}),
                'original_image': original_image_b64,
                'restored_image': results.get('restored_image'),
                'time_span': time_span,
                'restoration': {
                    'status': restoration_data.get('status', 'error'),
                    'message': 'AI-generated pristine restoration completed' if restoration_data.get('status') == 'success' else 'Restoration failed',
                    'response': vision_data.get('identification', ''),
                    'restoration_details': f"Method: {restoration_data.get('restoration_method', 'N/A')} | Level: {restoration_level}",
                    'artifact_type': vision_data.get('type', 'Unknown'),
                    'condition': vision_data.get('condition', 'Unknown')
                },
                'data_fetcher': {
                    'status': historical_data.get('status', 'error'),
                    'message': 'Historical context retrieved via ADK' if historical_data.get('status') == 'success' else 'Historical retrieval failed',
                    'historical_data': historical_data.get('historical_context', '')
                },
                'environmental': {
                    'status': environmental_data.get('status', 'error'),
                    'message': f'Environmental predictions for {time_span} years via ADK' if environmental_data.get('status') == 'success' else 'Environmental prediction failed',
                    'time_span': time_span,
                    'environmental_analysis': environmental_data.get('predictions', '')
                },
                'degradation_predictions': environmental_data.get('degradation_timeline', [])
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
    print("\n" + "="*70)
    print("ARTIFACT RESTORATION SYSTEM")
    print("    Powered by Google ADK Sequential Agents + MCP + Context Engineering")
    print("="*70)
    print("\n[SERVER] Starting Flask server...")
    print("[URL] Open http://localhost:5000 in your browser")
    print("\n[ARCHITECTURE]")
    print("  Sequential Agents: Vision → Restoration → Historical → Environmental")
    print("  Context Engineering: ENABLED (agent-to-agent handoffs)")
    print("  MCP Tools: ENABLED (Model Context Protocol)")
    print("  ADK Runners: ENABLED (Historical + Environmental agents)")
    print("\n[INFO] Debug mode disabled (Windows compatibility)")
    print("\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
