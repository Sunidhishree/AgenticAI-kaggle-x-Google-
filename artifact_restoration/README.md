# 🏛️ Artifact Restoration Multi-Agent System

**Powered by Google ADK (Agent Development Kit)**

A sophisticated multi-agent AI system for analyzing, restoring, and predicting the degradation of historical artifacts using Google's ADK framework.

## 🎯 Features

- **🔧 Restoration Agent**: Analyzes and restores artifact images using advanced image processing
- **📚 Data Fetcher Agent**: Provides historical context, cultural significance, and conservation knowledge
- **🌍 Environmental Agent**: Predicts degradation timelines and provides preservation recommendations
- **🤖 Multi-Agent Orchestration**: Seamless workflow coordination using Google ADK
- **🖼️ Drag-and-Drop Interface**: Easy image upload with intuitive UI
- **📊 Comprehensive Analysis**: Detailed reports on condition, history, and future preservation

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Root Agent (ADK)              │
│         Orchestrates Workflow           │
└────────────┬────────────────────────────┘
             │
    ┌────────┴─────────┬─────────────┐
    │                  │             │
┌───▼────┐      ┌─────▼─────┐  ┌───▼──────┐
│Restora │      │   Data    │  │Environ   │
│tion    │─────▶│  Fetcher  │─▶│mental    │
│Agent   │      │   Agent   │  │Agent     │
└────────┘      └───────────┘  └──────────┘
    │                │              │
    ▼                ▼              ▼
Image          Historical    Degradation
Restoration    Context       Predictions
```

## 📋 Prerequisites

- Python 3.10 or 3.11 (⚠️ Python 3.12 has compatibility issues with google-adk on Windows)
- Google API Key (Gemini)
- Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd artifact_restoration
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Test Setup

```bash
python test_adk_setup.py
```

### 4. Run Application

```bash
python app.py
```

Open **http://localhost:5000** in your browser!

## 📁 Project Structure

```
artifact_restoration/
├── agents/                         # ADK Agent Implementations
│   ├── adk_restoration_agent.py   # Image restoration & analysis
│   ├── adk_data_agent.py          # Historical data fetcher
│   ├── adk_environmental_agent.py # Degradation predictions
│   └── adk_root_agent.py          # Workflow orchestrator
│
├── tools/
│   └── restoration_tools.py       # Image processing tools
│
├── templates/
│   ├── index.html                 # Upload interface
│   └── dashboard.html             # Results display
│
├── app.py                          # Flask application
├── setup_adk.py                    # ADK initialization
└── test_adk_setup.py              # Setup verification
```

## 🔧 How It Works

### 1. User Uploads Artifact Image
Drag and drop or browse for an artifact image (painting, sculpture, document, etc.)

### 2. Multi-Agent Processing

**Restoration Agent** → Analyzes and restores the image:
- Identifies artifact type and materials
- Applies restoration techniques (sharpening, contrast, color)
- Provides detailed condition assessment

**Data Fetcher Agent** → Retrieves historical context:
- Historical period and cultural origin
- Similar artifacts in museums
- Conservation best practices
- Estimated value and significance

**Environmental Agent** → Predicts degradation:
- Material-specific decay rates
- Environmental threats (temperature, humidity, light)
- Preservation recommendations
- Cost estimates for conservation

### 3. Results Displayed
- Side-by-side original and restored images
- Comprehensive analysis report
- Degradation timeline predictions
- Conservation recommendations

## 🛠️ Key Functions

### Restoration Tools

```python
# Restore artifact image
restore_artifact_image(
    image_path="artifact.jpg",
    restoration_level="medium"  # light, medium, heavy
)

# Predict degradation
predict_degradation(
    material="canvas",  # paper, stone, wood, metal, etc.
    years=10
)
```

### Agent Usage

```python
from agents.adk_root_agent import RootAgent

# Initialize multi-agent system
root = RootAgent()

# Process artifact
results = root.process_artifact(
    image_path="path/to/artifact.jpg",
    time_span=20  # prediction years
)
```

## 📊 API Endpoints

### `POST /process_artifact`

**Request**:
```javascript
FormData {
  image: File,
  time_span: 10  // years
}
```

**Response**:
```json
{
  "success": true,
  "workflow_status": "completed",
  "original_image": "base64...",
  "restored_image": "base64...",
  "restoration": {
    "analysis": "17th century oil painting on canvas...",
    "level": "medium"
  },
  "historical_context": "Dutch Golden Age painting...",
  "environmental": {
    "degradation_percentage": 35.0,
    "condition": "Fair - Noticeable degradation",
    "predictions": "Detailed timeline..."
  }
}
```

## 🐛 Troubleshooting

### Windows Python 3.12 Compatibility

**Error**: `AttributeError: 'WindowsPath' object has no attribute '_str'`

**Solutions**:
1. Use Python 3.10 or 3.11
2. Use WSL (Windows Subsystem for Linux)
3. Disable Flask debug mode reloader:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

### API Quota Exceeded

The system uses `gemini-1.5-flash` to minimize quota usage. If you hit limits:
- Wait for quota reset
- Check Google Cloud Console quotas
- Consider upgrading your plan

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

## 🎓 Example Use Cases

1. **Museum Conservation**: Analyze and plan restoration of historical artworks
2. **Archaeological Documentation**: Assess artifact condition and preservation needs
3. **Art Authentication**: Examine materials and techniques
4. **Collection Management**: Predict maintenance requirements
5. **Educational Tool**: Teach conservation science

## 📝 Material Degradation Rates

| Material | Degradation/Year | 10-Year Impact |
|----------|------------------|----------------|
| Paper    | 4.5%            | 45%            |
| Canvas   | 3.5%            | 35%            |
| Textile  | 4.0%            | 40%            |
| Wood     | 2.8%            | 28%            |
| Metal    | 1.5%            | 15%            |
| Stone    | 0.8%            | 8%             |
| Glass    | 0.5%            | 5%             |

## 🔮 Future Enhancements

- [ ] Support for 3D artifacts
- [ ] Multi-language support
- [ ] PDF report generation
- [ ] Museum database integration
- [ ] Real-time collaboration
- [ ] Mobile app version
- [ ] Advanced material analysis
- [ ] Cost estimation tools

## 📧 Support

- **Google ADK**: [Documentation](https://github.com/google/adk)
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/)
- **Issues**: Open a GitHub issue

---

**Built with ❤️ using Google ADK Multi-Agent Architecture**

🏛️ Preserving history through AI innovation
