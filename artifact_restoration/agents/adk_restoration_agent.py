"""  
Restoration Agent using Google Gemini API with DALL-E integration
"""
import google.generativeai as genai
import os
from typing import Dict, Any
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.restoration_tools import restore_artifact_image, identify_artifact_with_vision


class RestorationAgent:
    """Gemini-based agent for artifact restoration with AI image generation"""
    
    def __init__(self):
        # Configure API keys
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        # Use Gemini model directly
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.system_prompt = """You are an expert artifact restoration specialist with deep knowledge of art history and conservation.

Your responsibilities:
1. Analyze artifact images for type, age, materials, and condition
2. Provide detailed professional assessments about the artifact's origin, period, and cultural significance
3. Recommend appropriate conservation techniques
4. Assess current condition and restoration needs

Always be thorough, scholarly, and provide specific details about the artifact."""
        
        print("[OK] Restoration Agent initialized (Gemini + DALL-E)")
    
    def analyze_and_restore(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze and restore artifact image using vision identification
        
        Args:
            image_path: Path to artifact image
            
        Returns:
            Dictionary with analysis and restoration results
        """
        try:
            # Step 1: Identify artifact using Vision API
            print("🔍 Identifying artifact with Vision API...")
            identification = identify_artifact_with_vision(image_path)
            
            artifact_info = identification.get('identification', '')
            artifact_type = "unknown"
            
            # Extract artifact type from identification - look for TYPE: line
            import re
            type_match = re.search(r'TYPE:\s*([^\n]+)', artifact_info, re.IGNORECASE)
            if type_match:
                type_text = type_match.group(1).strip().lower()
                
                # Map the identified type
                if 'sculpt' in type_text or 'statue' in type_text:
                    artifact_type = "sculpture"
                elif 'monument' in type_text or 'architecture' in type_text:
                    artifact_type = "monument"
                elif 'paint' in type_text:
                    artifact_type = "painting"
                elif 'pottery' in type_text or 'ceramic' in type_text or 'vase' in type_text:
                    artifact_type = "pottery"
                elif 'relief' in type_text or 'carving' in type_text:
                    artifact_type = "sculpture"
                elif 'bronze' in type_text or 'metal' in type_text:
                    artifact_type = "sculpture"
                elif 'textile' in type_text or 'fabric' in type_text:
                    artifact_type = "textile"
                else:
                    artifact_type = type_text.split()[0]  # Use first word
            else:
                # Fallback: search in full text
                if 'sculpt' in artifact_info.lower() or 'statue' in artifact_info.lower():
                    artifact_type = "sculpture"
                elif 'monument' in artifact_info.lower():
                    artifact_type = "monument"
                elif 'paint' in artifact_info.lower() and 'canvas' in artifact_info.lower():
                    artifact_type = "painting"
                elif 'pottery' in artifact_info.lower() or 'ceramic' in artifact_info.lower():
                    artifact_type = "pottery"
            
            print(f"[OK] Identified as: {artifact_type}")
            
            # Step 2: Restore the image with type-specific techniques
            print(f"🔧 Applying {artifact_type}-specific restoration...")
            restoration_result = restore_artifact_image(image_path, "medium", artifact_type)
            
            if restoration_result.get("status") != "success":
                return {
                    "status": "error",
                    "message": restoration_result.get("error_message", "Restoration failed")
                }
            
            # Step 3: Generate vivid description AND show the reconstruction
            reconstruction_desc = restoration_result.get("reconstruction_description", "")
            generation_method = restoration_result.get("generation_method", "Enhancement")
            
            prompt = f"""You are an expert artifact conservator. You have this AI reconstruction description:

{reconstruction_desc}

Also, identification details:
{artifact_info}

Based on this information, provide a VIVID, COMPELLING description (150-200 words) formatted as:

**HOW IT LOOKED WHEN CREATED**

[Paint an extremely visual picture of the pristine, complete artifact - describe colors, missing parts reconstructed, surface finish, decorative details, overall magnificence]

**WHAT'S DAMAGED NOW**

[Quick bullet list of current damage]

**AI RECONSTRUCTION DETAILS**

[Specific reconstruction guidance from the AI - how missing parts should look based on symmetry, style, period]

Be EXTREMELY descriptive and visual - help people imagine the original beauty!"""
            
            # Use Gemini model for final analysis
            full_prompt = f"{self.system_prompt}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            analysis_text = response.text if response.text else "Analysis unavailable"
            
            # Add note about image generation
            if "AI Image Generation" in generation_method:
                analysis_text = f"**NOTE: Generated pristine image using AI**\n\n{analysis_text}"
            else:
                analysis_text = f"**NOTE: Enhanced image shown. Full AI image generation available with DALL-E 3**\n\n{analysis_text}"
            
            return {
                "status": "success",
                "restored_image_base64": restoration_result.get("restored_image_base64"),
                "restoration_level": restoration_result.get("restoration_level"),
                "artifact_type": artifact_type,
                "artifact_identification": artifact_info,
                "analysis": analysis_text,
                "image_path": image_path
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}"
            }


if __name__ == "__main__":
    agent = RestorationAgent()
    print("[OK] Restoration Agent ready for use")
