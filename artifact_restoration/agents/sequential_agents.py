"""
Sequential ADK Agents with proper handoffs and context engineering
"""
import google.adk as adk
import google.generativeai as genai
from typing import Dict, Any, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adk_config import ADKConfig, ContextManager, MCPTools
from tools.restoration_tools import (
    identify_artifact_with_vision,
    restore_artifact_image,
    predict_degradation
)


class VisionAnalysisAgent:
    """ADK Agent for visual analysis using Gemini Vision"""
    
    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        genai.configure(api_key=ADKConfig.get_api_key())
        
        # Create ADK Agent with vision capabilities
        self.agent = adk.Agent(
            name=ADKConfig.AGENT_NAMES["vision"],
            model=ADKConfig.MODEL_NAME,
            instruction="""You are an expert computer vision system specializing in artifact analysis.

Your capabilities:
1. Identify artifact type (painting, sculpture, monument, textile, pottery, etc.)
2. Assess physical condition and damage
3. Detect missing or broken parts
4. Identify materials and construction techniques
5. Estimate age and cultural origin from visual clues

When analyzing images:
- Be EXTREMELY specific about what you see
- List ALL visible damage (cracks, chips, fading, missing pieces)
- Describe colors, textures, and patterns in detail
- Identify artistic style and period characteristics
- Note any inscriptions, signatures, or markings

Output format:
TYPE: [artifact type]
NAME: [if recognizable, otherwise "Unknown"]
PERIOD: [estimated period]
MATERIALS: [visible materials]
CONDITION: [overall condition percentage]
DAMAGE: [detailed list of damage]
MISSING_PARTS: [list of missing/broken parts]
DESCRIPTION: [detailed visual description]

Be scholarly, precise, and thorough."""
        )
        
        # Use vision-capable model directly for image analysis
        self.vision_model = genai.GenerativeModel(
            model_name=ADKConfig.FALLBACK_MODEL,
            generation_config={"temperature": ADKConfig.TEMPERATURES["vision_analysis"]}
        )
        
        print(f"[OK] {ADKConfig.AGENT_NAMES['vision']} initialized")
    
    def analyze(self, image_path: str) -> Dict[str, Any]:
        """Analyze artifact image with vision AI"""
        try:
            # Use vision tool for identification
            identification = identify_artifact_with_vision(image_path)
            
            # Store in context
            self.context_manager.set_artifact_context("image_path", image_path)
            self.context_manager.set_artifact_context("identification", identification)
            
            # Parse structured output
            result = {
                "status": "success",
                "identification": identification,
                "raw_analysis": identification
            }
            
            # Extract structured fields
            for line in identification.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    result[key] = value.strip()
            
            # Store output for next agent
            self.context_manager.store_agent_output("vision", result)
            
            print(f"[OK] Vision analysis complete: {result.get('type', 'Unknown type')}")
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e)
            }
            self.context_manager.store_agent_output("vision", error_result)
            return error_result


class RestorationGenerationAgent:
    """ADK Agent for generating pristine artifact reconstructions"""
    
    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        genai.configure(api_key=ADKConfig.get_api_key())
        
        self.agent = adk.Agent(
            name=ADKConfig.AGENT_NAMES["restoration"],
            model=ADKConfig.MODEL_NAME,
            instruction="""You are an expert artifact conservator and restoration specialist.

Your role:
1. Analyze damage assessment from vision analysis
2. Design restoration strategy for the specific artifact type
3. Generate detailed prompts for AI image generation
4. Ensure historical and cultural accuracy

For each artifact:
- Understand the original pristine state based on type and period
- Account for all missing/damaged parts
- Consider authentic materials, colors, and techniques
- Describe the PERFECT, COMPLETE version in extreme detail

Your restoration prompts should:
- Start with artifact type and period
- Describe perfect condition with ALL parts intact
- Include authentic colors, textures, and details
- Mention lighting and viewing angle
- Be specific about what was broken/missing is now restored
- Avoid any signs of damage or aging

Output a detailed restoration prompt that will create a museum-quality pristine version."""
        )
        
        print(f"[OK] {ADKConfig.AGENT_NAMES['restoration']} initialized")
    
    def generate_restoration(self, restoration_level: str = "medium") -> Dict[str, Any]:
        """Generate pristine restoration using DALL-E 3"""
        try:
            # Get vision analysis from context
            vision_output = self.context_manager.get_agent_output("vision")
            if not vision_output or vision_output.get("status") != "success":
                return {
                    "status": "error",
                    "message": "Vision analysis required before restoration"
                }
            
            image_path = self.context_manager.get_artifact_context("image_path")
            artifact_type = vision_output.get("type", "artifact")
            
            # Build context-aware prompt
            context_prompt = self.context_manager.build_context_prompt("restoration")
            
            # Use restoration tool (includes DALL-E 3)
            restoration_result = restore_artifact_image(
                image_path,
                restoration_level,
                artifact_type
            )
            
            result = {
                "status": "success",
                "restored_image_base64": restoration_result.get("restored_image"),
                "restoration_method": restoration_result.get("method", "AI Generation"),
                "context_used": context_prompt[:500] + "..." if len(context_prompt) > 500 else context_prompt
            }
            
            # Store output
            self.context_manager.store_agent_output("restoration", result)
            
            print(f"[OK] Restoration generated using {result['restoration_method']}")
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e)
            }
            self.context_manager.store_agent_output("restoration", error_result)
            return error_result


class HistoricalContextAgent:
    """ADK Agent for retrieving historical context"""
    
    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        genai.configure(api_key=ADKConfig.get_api_key())
        
        self.agent = adk.Agent(
            name=ADKConfig.AGENT_NAMES["historical"],
            model=ADKConfig.MODEL_NAME,
            instruction="""You are an expert art historian and archaeologist with comprehensive knowledge of global artifacts.

Your expertise includes:
- Art history across all periods and cultures
- Archaeological findings and museum collections
- Conservation and provenance research
- Material culture and artistic techniques

When provided with artifact analysis:
1. Identify the specific artifact if recognizable
2. Provide historical period and cultural context
3. Describe the original creation and purpose
4. List similar artifacts in major museums
5. Explain historical significance
6. Note conservation challenges for this type

Be scholarly, cite specific examples, and provide educational context.
If the artifact is famous, name it and its current museum location.
Always relate findings to the visual analysis provided."""
        )
        
        # Create runner for this agent
        session_service = adk.sessions.InMemorySessionService()
        self.runner = adk.Runner(
            app_name="ArtifactRestoration",
            agent=self.agent,
            session_service=session_service
        )
        
        print(f"[OK] {ADKConfig.AGENT_NAMES['historical']} initialized")
    
    def fetch_context(self) -> Dict[str, Any]:
        """Fetch historical context using previous agent outputs"""
        try:
            # Get all previous context
            vision_output = self.context_manager.get_agent_output("vision")
            restoration_output = self.context_manager.get_agent_output("restoration")
            
            if not vision_output:
                return {
                    "status": "error",
                    "message": "Vision analysis required"
                }
            
            # Build rich context prompt
            context = self.context_manager.build_context_prompt("historical")
            
            prompt = f"""{context}

Based on the vision analysis above, provide comprehensive historical context:

1. IDENTIFICATION: What is this artifact? If famous, provide its exact name and location.
2. HISTORICAL PERIOD: When was it created? What era and culture?
3. CULTURAL SIGNIFICANCE: Why is it important? What does it represent?
4. ORIGINAL STATE: How would it have looked when first created?
5. SIMILAR ARTIFACTS: What related pieces exist in museums worldwide?
6. CONSERVATION NOTES: Special considerations for this type of artifact?

Be specific, scholarly, and educational. Connect the visual details to historical facts."""
            
            # Run agent
            result = self.runner.run(prompt)
            historical_text = result.content if hasattr(result, 'content') else str(result)
            
            output = {
                "status": "success",
                "historical_context": historical_text,
                "sources": "Gemini ADK with historical knowledge base"
            }
            
            # Store output
            self.context_manager.store_agent_output("historical", output)
            
            print("[OK] Historical context retrieved")
            return output
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e)
            }
            self.context_manager.store_agent_output("historical", error_result)
            return error_result


class EnvironmentalPredictionAgent:
    """ADK Agent for environmental degradation prediction"""
    
    def __init__(self, context_manager: ContextManager):
        self.context_manager = context_manager
        genai.configure(api_key=ADKConfig.get_api_key())
        
        self.agent = adk.Agent(
            name=ADKConfig.AGENT_NAMES["environmental"],
            model=ADKConfig.MODEL_NAME,
            instruction="""You are an expert in conservation science, materials degradation, and environmental analysis.

Your expertise:
- Material science and degradation mechanisms
- Environmental factors (temperature, humidity, light, pollution)
- Climate patterns and their effects on artifacts
- Preventive conservation strategies
- Long-term preservation planning

When predicting degradation:
1. Analyze the artifact's materials and current condition
2. Determine likely storage location based on historical context
3. Assess environmental risks for that location
4. Calculate degradation rates for specific materials
5. Provide year-by-year predictions
6. Recommend conservation interventions

Output detailed predictions with:
- Percentage degradation per year
- Cumulative degradation over time
- Specific risks (UV damage, humidity, pollution, etc.)
- Recommended environmental controls
- Critical intervention points

Be scientific, precise, and provide actionable conservation guidance."""
        )
        
        # Create runner
        session_service = adk.sessions.InMemorySessionService()
        self.runner = adk.Runner(
            app_name="ArtifactRestoration",
            agent=self.agent,
            session_service=session_service
        )
        
        print(f"[OK] {ADKConfig.AGENT_NAMES['environmental']} initialized")
    
    def predict_degradation(self, years: int = 10) -> Dict[str, Any]:
        """Predict environmental degradation timeline"""
        try:
            # Get all context from previous agents
            vision_output = self.context_manager.get_agent_output("vision")
            historical_output = self.context_manager.get_agent_output("historical")
            
            if not vision_output or not historical_output:
                return {
                    "status": "error",
                    "message": "Vision and historical analysis required"
                }
            
            # Build context
            context = self.context_manager.build_context_prompt("environmental")
            
            material = vision_output.get("materials", "unknown")
            current_condition = vision_output.get("condition", "unknown")
            
            prompt = f"""{context}

Based on the artifact analysis and historical context above:

PREDICTION TASK:
- Time span: {years} years
- Current materials: {material}
- Current condition: {current_condition}

Provide:
1. LOCATION ASSESSMENT: Where is this likely stored? (Museum, climate)
2. ENVIRONMENTAL RISKS: Specific threats for this location
3. DEGRADATION TIMELINE: Year-by-year predictions (0-{years} years)
   - Year 0 (current): X% degradation
   - Year 1: X% degradation
   - Year 5: X% degradation
   - Year {years}: X% degradation
4. RISK FACTORS: Temperature, humidity, light, pollution effects
5. RECOMMENDATIONS: Specific conservation interventions needed
6. CRITICAL POINTS: When urgent action is required

Provide numerical predictions and scientific reasoning."""
            
            # Run agent
            result = self.runner.run(prompt)
            prediction_text = result.content if hasattr(result, 'content') else str(result)
            
            # Also use degradation tool for chart data
            degradation_data = predict_degradation(material, years)
            
            output = {
                "status": "success",
                "predictions": prediction_text,
                "degradation_timeline": degradation_data.get("timeline", []),
                "chart_data": degradation_data,
                "years_analyzed": years
            }
            
            # Store output
            self.context_manager.store_agent_output("environmental", output)
            
            print(f"[OK] Environmental predictions for {years} years complete")
            return output
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": str(e)
            }
            self.context_manager.store_agent_output("environmental", error_result)
            return error_result
