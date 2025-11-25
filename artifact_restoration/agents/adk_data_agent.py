"""  
Data Fetcher Agent using Google Gemini API
"""
import google.generativeai as genai
import os
from typing import Dict, Any


class DataFetcherAgent:
    """Gemini-based agent for artifact historical data"""
    
    def __init__(self):
        # Configure API
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        # Use Gemini model directly
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.system_prompt = """You are an expert art historian and archaeologist with comprehensive knowledge of global artifacts and access to extensive museum databases.Your expertise includes:
1. Historical periods and cultural contexts across all civilizations
2. Material science and conservation techniques  
3. Artifact provenance and authentication
4. Major museum collections worldwide (Louvre, British Museum, Metropolitan Museum, Smithsonian, etc.)
5. Cultural and historical significance
6. Current locations and environmental conditions of famous artifacts

When analyzing artifacts:
- Identify similar artifacts in major museum collections with specific names and locations
- Provide the current city and country where similar artifacts are housed
- Describe the environmental conditions and climate of those locations
- Include specific museum names, collection details, and acquisition dates when applicable

Provide scholarly, detailed information with specific examples and real museum locations."""
        
        print("[OK] Data Fetcher Agent initialized")
    
    def fetch_context(self, analysis: str, artifact_identification: str = "") -> Dict[str, Any]:
        """
        Fetch historical context based on restoration analysis and vision identification
        
        Args:
            analysis: Text from restoration agent analysis
            artifact_identification: Vision API identification of the artifact
            
        Returns:
            Dictionary with historical context
        """
        try:
            prompt = f"""You have detailed artifact identification from vision analysis:

{artifact_identification}

Additional restoration analysis:
{analysis}

Provide CONCISE historical context (maximum 150 words) in this format:

**ARTIFACT IDENTITY**
Name: [exact name if famous]
Creator: [artist/culture]
Date: [specific year or period]

**CURRENT LOCATION**
Museum: [institution name]
City/Country: [location]
Climate: [temperature/humidity]

**HISTORICAL SIGNIFICANCE**
[2-3 sentences about importance]

**SIMILAR ARTIFACTS**
1. [Name - Museum, City]
2. [Name - Museum, City]

**CONSERVATION STATUS**
[Current preservation approach in 1-2 sentences]

Be specific and factual. If this is a famous artifact, state its exact name and real location."""
            
            # Use Gemini model
            full_prompt = f"{self.system_prompt}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            context_text = response.text if response.text else "Historical context unavailable"
            
            return {
                "status": "success",
                "historical_context": context_text
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Data fetching failed: {str(e)}"
            }


if __name__ == "__main__":
    agent = DataFetcherAgent()
    print("[OK] Data Fetcher Agent ready for use")
