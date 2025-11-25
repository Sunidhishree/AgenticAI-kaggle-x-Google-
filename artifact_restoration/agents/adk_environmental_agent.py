"""  
Environmental Analysis Agent using Google Gemini API
"""
import google.generativeai as genai
import os
from typing import Dict, Any
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.restoration_tools import predict_degradation


class EnvironmentalAgent:
    """Gemini-based agent for environmental degradation prediction"""
    
    def __init__(self):
        # Configure API
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        # Use Gemini model directly
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.system_prompt = """You are an expert in materials science, conservation science, and environmental degradation with knowledge of global climate patterns.Your expertise covers:
1. Environmental factors affecting artifacts (temperature, humidity, light, pollution, climate zones)
2. Material degradation patterns and timelines for different climates (tropical, temperate, arid, etc.)
3. Location-specific environmental risks based on typical climate zones
4. Preservation strategies and optimal storage conditions
5. Cost estimation for conservation measures
6. Risk assessment and mitigation

When analyzing environmental impact:
- If the artifact type suggests a probable location (e.g., Egyptian artifacts likely in Cairo, European art in European museums)
- Consider the typical climate conditions of major museum cities
- Provide specific temperature, humidity, and pollution levels for those locations
- Base degradation predictions on real environmental conditions

Provide scientifically accurate predictions with specific recommendations based on likely environmental conditions."""
        
        print("[OK] Environmental Agent initialized")
    
    def predict_degradation_timeline(self, historical_context: str, years: int, material: str = "canvas") -> Dict[str, Any]:
        """
        Predict environmental degradation over time
        
        Args:
            historical_context: Text from data fetcher agent
            years: Number of years to predict
            material: Primary material of artifact
            
        Returns:
            Dictionary with degradation predictions
        """
        try:
            # Get quantitative prediction
            degradation_data = predict_degradation(material, years)
            
            prompt = f"""Based on this artifact context, provide detailed environmental degradation predictions:

CONTEXT:
{historical_context}

QUANTITATIVE DATA:
- Material: {degradation_data['material']}
- Time span: {degradation_data['years']} years
- Predicted degradation: {degradation_data['degradation_percentage']}%
- Condition: {degradation_data['condition']}

Provide comprehensive analysis:

1. CURRENT BASELINE
   - Assessment of current state
   - Existing vulnerabilities

2. DEGRADATION TIMELINE
   - Predictions at {years//4}, {years//2}, and {years} years
   - Physical, chemical, and structural changes
   - Visual/aesthetic deterioration

3. ENVIRONMENTAL THREATS
   - Temperature effects
   - Humidity damage
   - Light degradation (UV and visible)
   - Air quality and pollution
   - Biological threats (mold, pests)

4. RECOMMENDED CONDITIONS
   - Temperature range (°C)
   - Humidity range (%)
   - Light levels (lux)
   - Air quality standards

5. PRESERVATION INTERVENTIONS
   - Immediate actions
   - Maintenance schedule
   - Long-term strategies

6. COST ESTIMATES
   - Environmental controls
   - Conservation treatments
   - Ongoing maintenance
   - Total over {years} years
"""
            
            # Use Gemini model
            full_prompt = f"{self.system_prompt}\n\n{prompt}\n\nIMPORTANT: Based on the historical context provided, determine the likely current location of this type of artifact (museum city and country), then analyze the environmental conditions typical of that location."
            response = self.model.generate_content(full_prompt)
            predictions_text = response.text if response.text else "Environmental predictions unavailable"
            
            return {
                "status": "success",
                "time_span_years": years,
                "degradation_data": degradation_data,
                "environmental_predictions": predictions_text
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Environmental analysis failed: {str(e)}"
            }


if __name__ == "__main__":
    agent = EnvironmentalAgent()
    print("[OK] Environmental Agent ready for use")
