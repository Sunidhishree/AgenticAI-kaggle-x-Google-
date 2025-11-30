# 🏛️ AI-Powered Artifact Restoration System

**Enterprise-Grade Multi-Agent Architecture with Google ADK, MCP & Context Engineering**

A production-ready AI system for artifact restoration, analysis, and preservation planning using Google's Agent Development Kit with sequential agent orchestration, Model Context Protocol (MCP) integration, and advanced context engineering.

##  Features

### Core AI Capabilities
- **Google ADK App Architecture**: Production multi-agent system with proper App, Runner, and session management
- **Sequential Agent Orchestration**: Context-aware agents execute in optimized order with state transfer
- **MCP Tool Integration**: Model Context Protocol tools for advanced image generation and analysis
- **Context Engineering**: Advanced prompt engineering with structured context passing between agents
- **DALL-E 3 Integration**: AI-generated pristine artifact reconstruction (not just enhancement)
- **Gemini Vision API**: Accurate artifact identification via reverse image search capabilities

### Multi-Agent System
- **Vision Agent**: Uses Gemini Vision to identify artifacts with high accuracy (type, name, origin)
- **Restoration Agent**: DALL-E 3 generates pristine versions showing original state with all parts intact
- **Data Agent**: Fetches historical context, cultural significance, and conservation knowledge
- **Environmental Agent**: Predicts degradation timelines and provides preservation recommendations
- **Sequential Coordination**: Agents execute in order, each enriching context for the next

### User Experience
- **Historic UI Theme**: Brownish color scheme with Hampi temple backgrounds, serif fonts
- **Interactive Dashboards**: Chart.js visualizations for degradation predictions
- **Real-time Processing**: Stream-based responses with progress indicators

## Architecture
flowchart TD

A([Start: User Uploads Artifact Image]) 
    --> B[Flask Backend Receives Image<br>Handles API Request & Session]

B --> C{Root Agent Activated<br>Orchestrates All Agents<br>via Google ADK}

C --> D[Image Analysis Agent<br>Detects Materials, Damage, Structure]

D --> E[Restoration Agent<br>Reconstructs Original Colors<br>Generates Restored Image]

E --> F[Historical Data Agent<br>Retrieves References, Records, Notes]

F --> G[Environmental Agent<br>Analyzes Climate & Predicts Degradation]

G --> H[Cost Estimation Agent<br>Calculates Local Restoration & Preservation Costs]

H --> I[Recommendations Agent<br>Suggests Storage Conditions & Risk Mitigation]

I --> J[Report Generator<br>Creates Graphs, Summaries, Outputs]

J --> K[Flask Backend Sends Results Back]

K --> L([End: User Views Restored Image, Predictions, Cost, Recommendations])


## 📋 Prerequisites

- **Python 3.10 or 3.11** (⚠️ Python 3.12 has ADK compatibility issues on Windows)
- **Google API Key** (Gemini/Vertex AI)
- **OpenAI API Key** (for DALL-E 3 pristine image generation)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended for large images)
- **Storage**: 2GB for dependencies and cache

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Sunidhishree/AgenticAI-kaggle-x-Google-.git
cd AgenticAI-kaggle-x-Google-/artifact_restoration
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
# Required: Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Required: OpenAI for DALL-E 3 image generation
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Test ADK Setup

```bash
python test_adk_setup.py
```

Expected output:
```
✓ Google ADK installed
✓ Gemini API configured
✓ OpenAI API configured
✓ MCP tools available
✓ All agents initialized
```

### 4. Run Application

```bash
python app.py
```

Open **http://localhost:5000** in your browser!

## 📁 Project Structure

```
artifact_restoration/
├── adk_orchestrator.py            # ⭐ Main ADK App with sequential agents
│   ├── ADKOrchestrator class
│   ├── Sequential agent execution
│   ├── Context engineering pipeline
│   └── MCP tool integration
│
├── agents/                         # Individual ADK Agents
│   ├── vision_agent.py            # Gemini Vision for identification
│   ├── restoration_agent.py       # DALL-E 3 pristine generation
│   ├── data_agent.py              # Historical context fetcher
│   └── environmental_agent.py     # Degradation predictions
│
├── tools/
│   ├── restoration_tools.py       # Image processing & DALL-E integration
│   └── mcp_tools.py               # Model Context Protocol tools
│
├── templates/
│   ├── index.html                 # Upload interface (brownish theme)
│   └── dashboard.html             # Results with Chart.js graphs
│
├── static/
│   └── images/                    # Hampi temple backgrounds
│
├── app.py                          # Flask application with ADK
├── .env                            # API keys (not in git)
└── requirements.txt                # Dependencies
```

## 🔧 How It Works

### Sequential Multi-Agent Pipeline with Context Engineering

#### 1. User Uploads Artifact Image
Drag-and-drop interface accepts images of paintings, sculptures, monuments, documents, etc.

#### 2. Vision Agent (Gemini Vision API)
```python
# Accurate artifact identification via reverse image search
{
  "artifact_type": "sculpture",
  "artifact_name": "Venus de Milo",
  "period": "Hellenistic (130-100 BCE)",
  "material": "Parian marble",
  "current_location": "Louvre Museum, Paris"
}
```
**Output**: Structured identification → passed to next agent

#### 3. Restoration Agent (DALL-E 3 + Context)
```python
# Context: Receives vision agent's identification
# Action: Generates pristine original-state image
# Key: NOT just enhancement - actual AI reconstruction

prompt = f"Create pristine {artifact_name} from {period}, 
          COMPLETE with ALL original parts intact including 
          {missing_parts}. Show how it looked when first created."

dalle3.generate(prompt) → pristine_image.jpg
```
**Output**: AI-generated pristine image + restoration analysis → passed to next agent

#### 4. Data Agent (Historical Context)
```python
# Context: Receives identification + restoration analysis
# Action: Enriches with historical knowledge

{
  "historical_period": "Hellenistic Greek art movement",
  "cultural_significance": "Represents Aphrodite...",
  "similar_artifacts": ["Louvre: Winged Victory", ...],
  "conservation_practices": "Climate-controlled display...",
  "estimated_value": "$1B+ (priceless)"
}
```
**Output**: Rich historical context → passed to final agent

#### 5. Environmental Agent (Degradation Prediction)
```python
# Context: Receives ALL previous context
# Action: Material science + environmental analysis

{
  "current_condition": "Arms missing, surface weathering",
  "degradation_rate": "0.8% per year (marble in museum)",
  "10_year_prediction": "8% additional surface erosion",
  "preservation_cost": "$50,000-100,000 per decade",
  "recommendations": [
    "Maintain 18-22°C temperature",
    "Keep 45-55% humidity",
    "Limit UV exposure to <75 lux"
  ]
}
```

#### 6. Results Dashboard
- **Side-by-side comparison**: Original damaged vs AI-generated pristine
- **Interactive timeline**: Chart.js degradation graph over decades
- **Comprehensive report**: All agent outputs in brownish historic theme
- **Downloadable**: Both images + full analysis PDF (future)


### MCP Tool Integration

```python
# Model Context Protocol tools
from tools.mcp_tools import (
    dalle3_generate_pristine,
    gemini_vision_identify,
    analyze_material_degradation
)

# Used by agents for specific tasks
pristine_image = dalle3_generate_pristine(
    artifact_description=vision_result,
    generation_params={
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "hd"
    }
)
```


## 🔮 Future Enhancements

### Planned Features
- [ ] **3D Artifact Support**: Point cloud reconstruction for sculptures
- [ ] **Multi-language UI**: Support for 10+ languages
- [ ] **PDF Report Generation**: Downloadable professional reports
- [ ] **Museum API Integration**: Direct connection to Smithsonian, Louvre databases
- [ ] **Real-time Collaboration**: Multiple users working on same artifact
- [ ] **Mobile Apps**: iOS/Android native applications
- [ ] **AR Visualization**: View restored artifacts in augmented reality
- [ ] **Blockchain Provenance**: NFT certificates for digital restorations
- [ ] **Advanced Material Analysis**: XRF/FTIR simulation for composition
- [ ] **Cost Estimation Tools**: ROI calculator for conservation projects

### MCP Enhancements
- [ ] **Additional MCP Servers**: Integration with more specialized tools
- [ ] **Custom Tool Development**: Domain-specific restoration tools
- [ ] **Tool Chaining**: Complex multi-tool workflows
- [ ] **Performance Optimization**: Parallel tool execution

### AI Model Upgrades
- [ ] **GPT-4 Vision**: Alternative to Gemini Vision
- [ ] **Stable Diffusion**: Open-source image generation option
- [ ] **Fine-tuned Models**: Custom models trained on museum data
- [ ] **Multimodal RAG**: Retrieval-augmented generation for artifacts

## 🎓 Use Cases

### Museum & Conservation
- **Digital Archival**: Create pristine digital twins of damaged artifacts
- **Restoration Planning**: Visualize restoration outcomes before physical work
- **Condition Monitoring**: Track degradation over time with predictions
- **Grant Applications**: Generate compelling before/after visuals for funding

### Academic & Research
- **Archaeological Analysis**: Reconstruct fragmentary finds
- **Art History**: Study original appearance of weathered works
- **Conservation Science**: Test degradation hypotheses
- **Student Training**: Teach restoration techniques safely

### Commercial Applications
- **Auction Houses**: Enhanced catalog images showing original state
- **Insurance**: Damage assessment and valuation
- **Galleries**: Marketing materials with restored views
- **Tourism**: Virtual museum exhibits with restored artifacts

## 📧 Support & Resources

### Documentation
- **Google ADK**: [Official Documentation](https://github.com/google/adk)
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/)
- **DALL-E 3**: [OpenAI Platform Docs](https://platform.openai.com/docs/guides/images)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io/)


## 🏆 Acknowledgments

**Built with cutting-edge AI technologies:**
-  **Google ADK** - Multi-agent orchestration framework
-  **Gemini 2.0 Flash** - Vision and language understanding  
-  **DALL-E 3** - Pristine artifact image generation
- **Model Context Protocol** - Advanced tool integration
- **Flask** - Web application framework
-  **Chart.js** - Interactive visualizations

**Special Thanks:**
- Google AI for ADK framework and Gemini API
- OpenAI for DALL-E 3 image generation capabilities
- Museum conservation community for domain expertise
- Open source contributors and testers


**🏛️ Preserving History Through AI Innovation 🏛️**

Built with ❤️ using Google ADK Multi-Agent Architecture


</div>
