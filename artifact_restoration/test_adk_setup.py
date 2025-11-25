"""
Test script to verify ADK setup and agents
"""
import os

print("="*60)
print("🧪 TESTING ADK SETUP")
print("="*60)

# Test 1: Import setup
print("\n1️⃣  Testing setup_adk.py...")
try:
    from setup_adk import GEMINI_API_KEY
    print("   ✅ Setup imported successfully")
    print(f"   ✅ API Key configured: {GEMINI_API_KEY[:10]}...")
except Exception as e:
    print(f"   ❌ Setup failed: {e}")
    exit(1)

# Test 2: Import tools
print("\n2️⃣  Testing restoration tools...")
try:
    from tools.restoration_tools import restore_artifact_image, predict_degradation
    print("   ✅ Tools imported successfully")
    
    # Test degradation prediction
    result = predict_degradation("canvas", 10)
    print(f"   ✅ Degradation test: {result['degradation_percentage']}% over 10 years")
except Exception as e:
    print(f"   ❌ Tools failed: {e}")
    exit(1)

# Test 3: Import agents
print("\n3️⃣  Testing ADK agents...")
try:
    from agents.adk_restoration_agent import RestorationAgent
    from agents.adk_data_agent import DataFetcherAgent
    from agents.adk_environmental_agent import EnvironmentalAgent
    print("   ✅ All agents imported successfully")
except Exception as e:
    print(f"   ❌ Agent import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Initialize agents
print("\n4️⃣  Initializing agents...")
try:
    restoration_agent = RestorationAgent()
    data_agent = DataFetcherAgent()
    environmental_agent = EnvironmentalAgent()
    print("   ✅ All agents initialized successfully")
except Exception as e:
    print(f"   ❌ Agent initialization failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Root agent
print("\n5️⃣  Testing Root Agent orchestrator...")
try:
    from agents.adk_root_agent import RootAgent
    root = RootAgent()
    print("   ✅ Root Agent initialized successfully")
except Exception as e:
    print(f"   ❌ Root Agent failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED - ADK SETUP COMPLETE")
print("="*60)
print("\n🚀 You can now run: python app.py")
print("\n")
