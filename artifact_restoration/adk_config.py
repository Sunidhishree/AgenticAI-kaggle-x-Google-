"""
Google ADK Configuration with MCP and Context Engineering
"""
import os
from typing import Any, Dict, List
import google.adk as adk
from google.adk import sessions, tools


class ContextManager:
    """Context engineering for multi-agent communication"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.artifact_context: Dict[str, Any] = {}
        self.agent_outputs: Dict[str, Any] = {}
        
    def add_message(self, agent: str, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "agent": agent,
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        })
        
    def set_artifact_context(self, key: str, value: Any):
        """Store artifact-specific context"""
        self.artifact_context[key] = value
        
    def get_artifact_context(self, key: str = None) -> Any:
        """Retrieve artifact context"""
        if key:
            return self.artifact_context.get(key)
        return self.artifact_context
        
    def store_agent_output(self, agent_name: str, output: Any):
        """Store output from an agent for sequential handoff"""
        self.agent_outputs[agent_name] = output
        
    def get_agent_output(self, agent_name: str) -> Any:
        """Get output from previous agent"""
        return self.agent_outputs.get(agent_name)
        
    def build_context_prompt(self, current_agent: str) -> str:
        """Build rich context prompt for current agent"""
        context_parts = []
        
        # Add artifact context
        if self.artifact_context:
            context_parts.append("=== ARTIFACT CONTEXT ===")
            for key, value in self.artifact_context.items():
                context_parts.append(f"{key}: {value}")
            context_parts.append("")
        
        # Add previous agent outputs
        if self.agent_outputs:
            context_parts.append("=== PREVIOUS AGENT OUTPUTS ===")
            for agent, output in self.agent_outputs.items():
                context_parts.append(f"\n--- {agent} Output ---")
                context_parts.append(str(output))
            context_parts.append("")
        
        return "\n".join(context_parts)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
        
    def clear(self):
        """Clear all context"""
        self.conversation_history.clear()
        self.artifact_context.clear()
        self.agent_outputs.clear()


class MCPTools:
    """Model Context Protocol Tools for artifact analysis"""
    
    @staticmethod
    def create_image_analysis_tool():
        """Tool for analyzing artifact images"""
        return {
            "name": "analyze_artifact_image",
            "description": "Analyze an artifact image to identify type, condition, and damage",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the artifact image"
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific areas to focus analysis on"
                    }
                },
                "required": ["image_path"]
            }
        }
    
    @staticmethod
    def create_restoration_tool():
        """Tool for generating restored artifact images"""
        return {
            "name": "generate_restoration",
            "description": "Generate a pristine version of the damaged artifact using DALL-E 3",
            "parameters": {
                "type": "object",
                "properties": {
                    "artifact_description": {
                        "type": "string",
                        "description": "Detailed description of the artifact"
                    },
                    "damage_assessment": {
                        "type": "string",
                        "description": "Assessment of damage and missing parts"
                    },
                    "artifact_type": {
                        "type": "string",
                        "enum": ["painting", "sculpture", "monument", "textile", "pottery"],
                        "description": "Type of artifact"
                    }
                },
                "required": ["artifact_description", "damage_assessment", "artifact_type"]
            }
        }
    
    @staticmethod
    def create_historical_search_tool():
        """Tool for searching historical artifact databases"""
        return {
            "name": "search_artifact_history",
            "description": "Search for historical information about artifacts",
            "parameters": {
                "type": "object",
                "properties": {
                    "artifact_name": {
                        "type": "string",
                        "description": "Name or description of the artifact"
                    },
                    "period": {
                        "type": "string",
                        "description": "Historical period (e.g., Renaissance, Ancient Egypt)"
                    },
                    "culture": {
                        "type": "string",
                        "description": "Cultural origin"
                    }
                },
                "required": ["artifact_name"]
            }
        }
    
    @staticmethod
    def create_degradation_prediction_tool():
        """Tool for predicting environmental degradation"""
        return {
            "name": "predict_degradation",
            "description": "Predict future degradation based on environmental factors",
            "parameters": {
                "type": "object",
                "properties": {
                    "material": {
                        "type": "string",
                        "description": "Primary material of the artifact"
                    },
                    "location": {
                        "type": "string",
                        "description": "Current or intended storage location"
                    },
                    "time_span": {
                        "type": "integer",
                        "description": "Number of years to predict"
                    },
                    "current_condition": {
                        "type": "string",
                        "description": "Current condition assessment"
                    }
                },
                "required": ["material", "time_span"]
            }
        }


class ADKConfig:
    """Central ADK configuration"""
    
    # Model configuration
    MODEL_NAME = "gemini-2.0-flash-exp"
    FALLBACK_MODEL = "gemini-2.0-flash"
    
    # Session configuration
    SESSION_TTL = 3600  # 1 hour
    MAX_CONTEXT_LENGTH = 100000
    
    # Agent names
    AGENT_NAMES = {
        "vision": "VisionAnalysisAgent",
        "restoration": "RestorationAgent", 
        "historical": "HistoricalDataAgent",
        "environmental": "EnvironmentalAgent",
        "orchestrator": "OrchestratorAgent"
    }
    
    # Temperature settings for different tasks
    TEMPERATURES = {
        "vision_analysis": 0.1,  # Low for factual analysis
        "restoration": 0.7,      # Medium-high for creative generation
        "historical": 0.2,       # Low for factual retrieval
        "environmental": 0.3     # Low-medium for predictions
    }
    
    @staticmethod
    def get_api_key() -> str:
        """Get Google API key from environment"""
        key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY must be set")
        return key
    
    @staticmethod
    def get_openai_key() -> str:
        """Get OpenAI API key for DALL-E"""
        return os.getenv('OPENAI_API_KEY', '')
