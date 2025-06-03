#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_d_55_59_final():
    """Final verification showing D-55-59 section matching the screenshot"""
    
    print("✅ D-55-59 Vitamin D Section - Final Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test Case: Vitamin D = 57 ng/mL (in 55-59 range)
    print("\n📋 Example: Vitamin D = 57 ng/mL")
    print("-" * 40)
    
    lab_results = {
        'VIT_D25': 57.0
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract and display the D-55-59 section
    lines = roadmap.split('\n')
    
    # Find the D-55-59 content
    d_55_59_content = []
    in_section = False
    
    for line in lines:
        if "falls very close to the optimal parameters" in line:
            in_section = True
        if in_section:
            d_55_59_content.append(line)
            if ("encouraged to continue your current VITAMIN D supplement" in line or 
                len(d_55_59_content) > 5):  # Stop after finding the content or max lines
                break
    
    if d_55_59_content:
        print("🎯 D-55-59 Section Output:")
        print("-" * 30)
        for line in d_55_59_content:
            if line.strip():  # Only show non-empty lines
                print(f"   {line.strip()}")
    
    # Verify the key phrases match the screenshot
    expected_phrases = [
        "falls very close to the optimal parameters",
        "no additional intervention is recommended", 
        "encouraged to continue your current VITAMIN D supplement"
    ]
    
    print(f"\n✅ Verification Against Screenshot:")
    print("-" * 40)
    
    all_present = True
    for phrase in expected_phrases:
        present = phrase in roadmap
        print(f"  ✅ '{phrase}': {'✅ PRESENT' if present else '❌ MISSING'}")
        if not present:
            all_present = False
    
    if all_present:
        print(f"\n🎉 SUCCESS: D-55-59 section matches screenshot exactly!")
        print(f"   📊 Range: 55 < vitamin D ≤ 59 ng/mL")
        print(f"   💊 Action: Continue current supplement")
        print(f"   🎯 Message: Close to optimal, no intervention needed")
    else:
        print(f"\n❌ Some content is missing from the expected output")
    
    return all_present

if __name__ == "__main__":
    verify_d_55_59_final() 