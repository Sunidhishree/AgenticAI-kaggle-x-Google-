"""
Root Orchestrator Agent using Google ADK
"""
from typing import Dict, Any
from .adk_restoration_agent import RestorationAgent
from .adk_data_agent import DataFetcherAgent
from .adk_environmental_agent import EnvironmentalAgent


class RootAgent:
    """Main orchestrator for multi-agent workflow using Google ADK"""
    
    def __init__(self):
        print("🚀 Initializing Root Agent with ADK components...")
        
        # Initialize all sub-agents
        self.restoration_agent = RestorationAgent()
        self.data_agent = DataFetcherAgent()
        self.environmental_agent = EnvironmentalAgent()
        
        print("[OK] Root Agent fully initialized with all sub-agents")
    
    def process_artifact(self, image_path: str, time_span: int = 10) -> Dict[str, Any]:
        """
        Orchestrate complete multi-agent workflow
        
        Args:
            image_path: Path to artifact image
            time_span: Years for environmental prediction
            
        Returns:
            Complete analysis results from all agents
        """
        results = {
            "image_path": image_path,
            "time_span": time_span,
            "workflow_status": "initiated"
        }
        
        print(f"\n{'='*60}")
        print(f"🏛️  ARTIFACT RESTORATION WORKFLOW")
        print(f"{'='*60}")
        print(f"Image: {image_path}")
        print(f"Prediction span: {time_span} years")
        print(f"{'='*60}\n")
        
        # Step 1: Restoration Agent
        print("🔧 STEP 1: Restoration & Analysis")
        restoration_result = self.restoration_agent.analyze_and_restore(image_path)
        results["restoration"] = restoration_result
        
        if restoration_result.get("restored_image_base64"):
            results["restored_image"] = restoration_result["restored_image_base64"]
        
        if restoration_result["status"] != "success":
            results["workflow_status"] = "failed_at_restoration"
            print(f"❌ Restoration failed: {restoration_result.get('message')}")
            return results
        
        print("[OK] Restoration complete")
        
        # Step 2: Data Fetcher Agent
        print("\n📚 STEP 2: Historical Context Retrieval")
        analysis_text = restoration_result.get("analysis", "")
        artifact_identification = restoration_result.get("artifact_identification", "")
        data_result = self.data_agent.fetch_context(analysis_text, artifact_identification)
        results["data_fetcher"] = data_result
        
        if data_result["status"] != "success":
            results["workflow_status"] = "failed_at_data_fetcher"
            print(f"❌ Data fetching failed: {data_result.get('message')}")
            return results
        
        print("[OK] Historical context retrieved")
        
        # Step 3: Environmental Agent
        print(f"\n🌍 STEP 3: Environmental Degradation Analysis ({time_span} years)")
        historical_context = data_result.get("historical_context", "")
        environmental_result = self.environmental_agent.predict_degradation_timeline(
            historical_context, 
            time_span,
            material="canvas"  # Default, could be extracted from analysis
        )
        results["environmental"] = environmental_result
        
        if environmental_result["status"] != "success":
            results["workflow_status"] = "failed_at_environmental"
            print(f"❌ Environmental analysis failed: {environmental_result.get('message')}")
            return results
        
        print("[OK] Environmental analysis complete")
        
        # Workflow complete
        results["workflow_status"] = "completed"
        print(f"\n{'='*60}")
        print("[OK] MULTI-AGENT WORKFLOW COMPLETED SUCCESSFULLY")
        print(f"{'='*60}\n")
        
        return results


if __name__ == "__main__":
    root = RootAgent()
    print("[OK] Root Agent ready for artifact processing")
