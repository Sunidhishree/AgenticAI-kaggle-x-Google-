"""
ADK Orchestrator with Sequential Agent Workflow and Context Engineering
"""
import google.adk as adk
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adk_config import ADKConfig, ContextManager, MCPTools
from agents.sequential_agents import (
    VisionAnalysisAgent,
    RestorationGenerationAgent,
    HistoricalContextAgent,
    EnvironmentalPredictionAgent
)


class ADKOrchestrator:
    """
    Main orchestrator using Google ADK with:
    - Sequential agent execution with handoffs
    - Context engineering and memory management
    - MCP (Model Context Protocol) tool integration
    """
    
    def __init__(self):
        print("\n" + "="*70)
        print("🚀 INITIALIZING GOOGLE ADK MULTI-AGENT SYSTEM")
        print("="*70)
        
        # Initialize context manager for agent communication
        self.context_manager = ContextManager()
        
        # Initialize all sequential agents
        print("\n[INIT] Creating sequential agents with context engineering...")
        self.vision_agent = VisionAnalysisAgent(self.context_manager)
        self.restoration_agent = RestorationGenerationAgent(self.context_manager)
        self.historical_agent = HistoricalContextAgent(self.context_manager)
        self.environmental_agent = EnvironmentalPredictionAgent(self.context_manager)
        
        # MCP Tools registry
        self.mcp_tools = {
            "vision": MCPTools.create_image_analysis_tool(),
            "restoration": MCPTools.create_restoration_tool(),
            "historical": MCPTools.create_historical_search_tool(),
            "environmental": MCPTools.create_degradation_prediction_tool()
        }
        
        print(f"\n[OK] MCP Tools registered: {len(self.mcp_tools)} tools")
        print("[OK] Context Manager initialized")
        print("[OK] Sequential workflow ready")
        
        print("\n" + "="*70)
        print("✅ ADK ORCHESTRATOR FULLY INITIALIZED")
        print("="*70)
        print("\nAgent Sequence:")
        print("  1. VisionAnalysisAgent → Identify & assess artifact")
        print("  2. RestorationGenerationAgent → Generate pristine version")
        print("  3. HistoricalContextAgent → Retrieve historical data")
        print("  4. EnvironmentalPredictionAgent → Predict degradation")
        print("\nContext Engineering: ENABLED")
        print("MCP Integration: ENABLED")
        print("Sequential Handoffs: ENABLED")
        print("="*70 + "\n")
    
    def process_artifact(self, image_path: str, restoration_level: str = "medium", 
                        time_span: int = 10) -> Dict[str, Any]:
        """
        Execute sequential multi-agent workflow with context engineering
        
        Args:
            image_path: Path to artifact image
            restoration_level: Restoration intensity (light/medium/high)
            time_span: Years for degradation prediction
            
        Returns:
            Complete results from all agents with context
        """
        print("\n" + "="*70)
        print("🏛️  SEQUENTIAL AGENT WORKFLOW STARTED")
        print("="*70)
        print(f"Image: {image_path}")
        print(f"Restoration Level: {restoration_level}")
        print(f"Prediction Span: {time_span} years")
        print("="*70 + "\n")
        
        # Clear previous context
        self.context_manager.clear()
        self.context_manager.set_artifact_context("workflow_start", True)
        
        results = {
            "image_path": image_path,
            "restoration_level": restoration_level,
            "time_span": time_span,
            "workflow_status": "running",
            "agents_executed": []
        }
        
        # SEQUENTIAL EXECUTION WITH HANDOFFS
        
        # Step 1: Vision Analysis Agent
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ AGENT 1: Vision Analysis (Gemini Vision + MCP)             │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        vision_result = self.vision_agent.analyze(image_path)
        results["vision_analysis"] = vision_result
        results["agents_executed"].append("VisionAnalysisAgent")
        
        if vision_result.get("status") != "success":
            results["workflow_status"] = "failed_at_vision"
            results["error"] = vision_result.get("message", "Vision analysis failed")
            print(f"\n❌ WORKFLOW FAILED: {results['error']}\n")
            return results
        
        print(f"✓ Artifact identified: {vision_result.get('type', 'Unknown')}")
        print(f"✓ Context stored for next agent\n")
        
        # Step 2: Restoration Generation Agent
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ AGENT 2: Restoration Generation (DALL-E 3 + Context)       │")
        print("└─────────────────────────────────────────────────────────────┘")
        print("→ Receiving context from VisionAnalysisAgent...")
        
        restoration_result = self.restoration_agent.generate_restoration(restoration_level)
        results["restoration"] = restoration_result
        results["agents_executed"].append("RestorationGenerationAgent")
        
        if restoration_result.get("status") == "success":
            results["restored_image"] = restoration_result.get("restored_image_base64")
            print(f"✓ Restoration generated: {restoration_result.get('restoration_method')}")
            print(f"✓ Context updated for next agent\n")
        else:
            print(f"⚠ Restoration had issues: {restoration_result.get('message')}")
            print("→ Continuing with available data...\n")
        
        # Step 3: Historical Context Agent
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ AGENT 3: Historical Context (ADK Runner + Knowledge)       │")
        print("└─────────────────────────────────────────────────────────────┘")
        print("→ Receiving context from VisionAnalysisAgent + RestorationAgent...")
        
        historical_result = self.historical_agent.fetch_context()
        results["historical_context"] = historical_result
        results["agents_executed"].append("HistoricalContextAgent")
        
        if historical_result.get("status") != "success":
            results["workflow_status"] = "failed_at_historical"
            results["error"] = historical_result.get("message", "Historical context retrieval failed")
            print(f"\n❌ WORKFLOW FAILED: {results['error']}\n")
            return results
        
        print("✓ Historical context retrieved")
        print(f"✓ Context enriched for final agent\n")
        
        # Step 4: Environmental Prediction Agent
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ AGENT 4: Environmental Prediction (ADK + Science Models)   │")
        print("└─────────────────────────────────────────────────────────────┘")
        print("→ Receiving full context from all previous agents...")
        
        environmental_result = self.environmental_agent.predict_degradation(time_span)
        results["environmental_prediction"] = environmental_result
        results["agents_executed"].append("EnvironmentalPredictionAgent")
        
        if environmental_result.get("status") != "success":
            results["workflow_status"] = "failed_at_environmental"
            results["error"] = environmental_result.get("message", "Environmental prediction failed")
            print(f"\n❌ WORKFLOW FAILED: {results['error']}\n")
            return results
        
        results["degradation_timeline"] = environmental_result.get("degradation_timeline", [])
        print(f"✓ Degradation predictions for {time_span} years complete")
        print(f"✓ Timeline data ready for visualization\n")
        
        # Workflow complete
        results["workflow_status"] = "completed"
        results["context_summary"] = {
            "total_agents": len(results["agents_executed"]),
            "context_items": len(self.context_manager.artifact_context),
            "agent_outputs": len(self.context_manager.agent_outputs),
            "conversation_length": len(self.context_manager.conversation_history)
        }
        
        print("="*70)
        print("✅ SEQUENTIAL WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Agents executed: {' → '.join(results['agents_executed'])}")
        print(f"Context items tracked: {results['context_summary']['context_items']}")
        print(f"Agent outputs stored: {results['context_summary']['agent_outputs']}")
        print("="*70 + "\n")
        
        return results
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow and context status"""
        return {
            "context_manager": {
                "artifact_context": self.context_manager.artifact_context,
                "agent_outputs_count": len(self.context_manager.agent_outputs),
                "conversation_history_length": len(self.context_manager.conversation_history)
            },
            "mcp_tools": list(self.mcp_tools.keys()),
            "agents": {
                "vision": "VisionAnalysisAgent (Gemini Vision)",
                "restoration": "RestorationGenerationAgent (DALL-E 3)",
                "historical": "HistoricalContextAgent (ADK Runner)",
                "environmental": "EnvironmentalPredictionAgent (ADK Runner)"
            }
        }


if __name__ == "__main__":
    orchestrator = ADKOrchestrator()
    print("[OK] ADK Orchestrator ready for artifact processing")
