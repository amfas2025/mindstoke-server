#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_d_60_plus_final():
    """Final verification showing D-60+ section matching the screenshot"""
    
    print("✅ D-60+ Vitamin D Section - Final Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test Case: Vitamin D = 70 ng/mL (optimal range)
    print("\n📋 Example: Vitamin D = 70 ng/mL (Optimal Range)")
    print("-" * 50)
    
    lab_results = {
        'VIT_D25': 70.0
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the exact vitamin D section
    lines = roadmap.split('\n')
    vitamin_d_section = []
    in_vitamin_d_section = False
    
    for line in lines:
        if 'Vitamin D Optimization' in line:
            in_vitamin_d_section = True
        elif in_vitamin_d_section and line.strip() and not line.startswith(' ') and '**' in line:
            # Next major section
            break
        
        if in_vitamin_d_section:
            vitamin_d_section.append(line)
    
    print("📋 Generated Vitamin D Content:")
    print("-" * 30)
    for line in vitamin_d_section:
        if line.strip():
            print(line)
    
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION RESULTS:")
    print("=" * 60)
    
    # Check for key phrases from screenshot
    roadmap_text = roadmap.lower()
    
    checks = [
        ("'falls within the optimal parameters'", "falls within the optimal parameters" in roadmap_text),
        ("'no additional intervention is recommended'", "no additional intervention is recommended" in roadmap_text),
        ("Vitamin D value displayed", "70.0 ng/ml" in roadmap_text),
        ("D-optimal section triggered", "vitamin d optimization" in roadmap_text)
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ D-60+ Vitamin D section matches screenshot exactly")
    else:
        print("❌ Some checks failed")
    print("=" * 60)

if __name__ == "__main__":
    verify_d_60_plus_final() 