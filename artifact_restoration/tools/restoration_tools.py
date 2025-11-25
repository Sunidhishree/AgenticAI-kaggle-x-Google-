"""
Restoration Tools for ADK Agents
"""
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import google.generativeai as genai
import os
import base64
from io import BytesIO
from typing import Dict
import requests

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[WARNING] OpenAI library not available. Image generation will use fallback method.")


def identify_artifact_with_vision(image_path: str) -> dict:
    """Use Google Gemini Vision to identify artifact details.
    
    Args:
        image_path: Path to the artifact image
        
    Returns:
        Dictionary with artifact identification details
    """
    try:
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        # Use Gemini Vision model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Open image
        img = Image.open(image_path)
        
        prompt = """Analyze this artifact image carefully and provide PRECISE identification:

CRITICAL: Look at the actual content of the image and be accurate about what type of artifact this is.

Provide these details in this EXACT format:

ARTIFACT NAME: [If recognizable, provide the specific name like "Mona Lisa", "David by Michelangelo", "Terracotta Warrior". If not famous, say "Unknown [type]"]

TYPE: [Choose ONE from: painting, sculpture, statue, monument, pottery, ceramic, textile, manuscript, photograph, architecture, relief carving, bronze, metalwork, jewelry, furniture, or other - BE SPECIFIC]

MATERIAL: [What is it actually made from? Canvas and oil paint? Marble? Bronze? Terracotta? Wood? Be specific]

PERIOD: [Historical period like "Renaissance 1500s", "Ancient Greek 400 BCE", "Ming Dynasty 1400s", etc.]

ORIGIN: [Culture/civilization that created it]

LOCATION: [If this is a famous artifact, name the SPECIFIC museum and city. Example: "Louvre Museum, Paris" or "British Museum, London". If unknown, say "Unknown"]

CONDITION: [Describe any visible damage: cracks, fading, missing pieces, erosion, discoloration]

DESCRIPTION: [Brief physical description - what does it depict? Portrait? Landscape? Human figure? Animal? Abstract?]

CONFIDENCE: [High/Medium/Low - how confident are you this identification is correct?]

BE ACCURATE: If this is a sculpture or statue, do NOT call it a painting. If it's pottery, do NOT call it a sculpture. Look at the actual form and material."""
        
        response = model.generate_content([prompt, img])
        
        return {
            "status": "success",
            "identification": response.text,
            "has_vision_data": True
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Vision identification failed: {str(e)}",
            "has_vision_data": False
        }


def restore_artifact_image(image_path: str, restoration_level: str = "medium", artifact_type: str = "unknown") -> dict:
    """Generates an image showing how the artifact looked when originally created using AI.
    
    Args:
        image_path: The file path to the artifact image
        restoration_level: "light", "medium", or "heavy"
        artifact_type: Type of artifact ("painting", "sculpture", "monument", "pottery", etc.)
    
    Returns:
        Dictionary with AI-generated image of original pristine state
    """
    try:
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "error_message": f"Image not found: {image_path}"
            }
        
        img = Image.open(image_path).convert('RGB')
        artifact_type_lower = artifact_type.lower()
        
        # Get API keys
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        # Step 1: Use Gemini to analyze what needs to be reconstructed
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        analysis_prompt = f"""Analyze this damaged {artifact_type} image in extreme detail:

1. What parts are MISSING or BROKEN? (arms, nose, fingers, legs, decorative elements, etc.)
2. What is the material? (marble, bronze, terracotta, canvas, wood, etc.)
3. What period/style? (Ancient Greek, Renaissance, etc.)
4. How would the COMPLETE, PRISTINE artifact look when first created?

Describe the PERFECT, UNDAMAGED version with ALL missing parts reconstructed in vivid visual detail."""

        analysis_response = model.generate_content([analysis_prompt, img])
        reconstruction_description = analysis_response.text
        
        # Step 2: Try to generate pristine image using OpenAI DALL-E
        if OPENAI_AVAILABLE and openai_key:
            try:
                print("[INFO] Attempting to generate pristine image using OpenAI DALL-E...")
                
                client = OpenAI(api_key=openai_key)
                
                # Create detailed generation prompt
                dalle_prompt = f"""A perfect, pristine, museum-quality photograph of a complete {artifact_type} in its original condition when first created. 

Based on this analysis: {reconstruction_description[:500]}

The artifact should be:
- COMPLETE with ALL parts intact (no missing arms, noses, fingers, or decorative elements)
- PRISTINE condition (no cracks, erosion, weathering, or damage)
- Original surface finish (polished marble, vibrant paint, gilded details, etc.)
- Professional museum photography lighting
- High resolution, photorealistic

Show the magnificent artifact exactly as it appeared when first completed."""

                # Generate image using DALL-E 3
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=dalle_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                # Download generated image
                image_url = response.data[0].url
                img_response = requests.get(image_url)
                
                if img_response.status_code == 200:
                    generated_image_base64 = base64.b64encode(img_response.content).decode('utf-8')
                    
                    return {
                        "status": "success",
                        "message": f"AI-generated pristine {artifact_type} using DALL-E 3",
                        "restored_image_base64": generated_image_base64,
                        "restoration_level": restoration_level,
                        "artifact_type": artifact_type,
                        "reconstruction_description": reconstruction_description,
                        "generation_method": "OpenAI DALL-E 3 - Full Reconstruction",
                        "note": "This is an AI-generated image showing how the artifact looked when originally created with all parts intact"
                    }
                else:
                    raise Exception(f"Failed to download generated image: {img_response.status_code}")
                    
            except Exception as e:
                print(f"[WARNING] DALL-E generation failed: {e}. Using enhanced fallback.")
        
        # Fallback: Enhanced existing image with detailed description
        print("[INFO] Using enhanced image with AI reconstruction description...")
        
        # Apply strong enhancement to show what we can
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.4)
        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.15)
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=95)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {
            "status": "success",
            "message": f"Enhanced {artifact_type} with AI reconstruction guidance",
            "restored_image_base64": img_base64,
            "restoration_level": restoration_level,
            "artifact_type": artifact_type,
            "reconstruction_description": reconstruction_description,
            "generation_method": "Enhanced Image + AI Description (Set OPENAI_API_KEY for full generation)",
            "note": "Enhanced image shown. For full AI reconstruction of missing parts, add OPENAI_API_KEY to .env file"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error_message": f"Restoration failed: {str(e)}"
        }


def predict_degradation(material: str, years: int) -> dict:
    """Predicts how an artifact will degrade over time based on its material.
    
    Args:
        material: The primary material of the artifact (e.g., "canvas", "paper", 
                 "stone", "wood", "metal", "textile").
        years: Number of years into the future to predict degradation (1-100).
    
    Returns:
        Dictionary with degradation prediction.
        Success: {
            "status": "success",
            "material": "canvas",
            "years": 10,
            "degradation_percentage": 35,
            "condition": "Fair - Noticeable degradation, some detail loss"
        }
    """
    # Degradation rates by material (percentage per year)
    degradation_rates = {
        "paper": 4.5,
        "canvas": 3.5,
        "wood": 2.8,
        "textile": 4.0,
        "stone": 0.8,
        "metal": 1.5,
        "ceramic": 1.0,
        "glass": 0.5
    }
    
    material_lower = material.lower()
    rate = degradation_rates.get(material_lower, 3.0)
    degradation = min(rate * years, 100)
    
    # Determine condition
    if degradation < 10:
        condition = "Excellent - Minimal changes"
    elif degradation < 25:
        condition = "Good - Minor surface wear"
    elif degradation < 50:
        condition = "Fair - Noticeable degradation, some detail loss"
    elif degradation < 75:
        condition = "Poor - Significant deterioration"
    else:
        condition = "Critical - Severe damage, major restoration required"
    
    return {
        "status": "success",
        "material": material,
        "years": years,
        "degradation_percentage": round(degradation, 1),
        "condition": condition
    }


# Test the functions
if __name__ == "__main__":
    print("✅ Restoration tools created")
    print(f"📊 Test degradation: {predict_degradation('canvas', 10)}")
