#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_d_50_55_final():
    """Final verification showing D-50-55 section matching the screenshot"""
    
    print("✅ D-50-55 Vitamin D Section - Final Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test Case: Vitamin D = 52 ng/mL (50-55 range)
    print("\n📋 Example: Vitamin D = 52 ng/mL (50-55 Range)")
    print("-" * 50)
    
    lab_results = {
        'VIT_D25': 52.0
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the relevant vitamin D content
    lines = roadmap.split('\n')
    relevant_lines = []
    
    for line in lines:
        if any(phrase in line.lower() for phrase in ['vitamin d', 'close to the optimal', 'intervention', 'few times per year']):
            relevant_lines.append(line)
    
    print("📋 Generated Vitamin D Content:")
    print("-" * 30)
    for line in relevant_lines:
        if line.strip():
            print(line.strip())
    
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION RESULTS:")
    print("=" * 60)
    
    # Check for exact phrases from screenshot
    roadmap_text = roadmap
    
    checks = [
        ("'This level is close to the optimal parameters'", "This level is close to the optimal parameters" in roadmap_text),
        ("'no additional intervention is recommended'", "no additional intervention is recommended" in roadmap_text),
        ("'check your VITAMIN D level a few times per year'", "check your VITAMIN D level a few times per year" in roadmap_text),
        ("'to make sure that it does not drop'", "to make sure that it does not drop" in roadmap_text),
        ("Vitamin D value displayed", "52.0 ng/mL" in roadmap_text),
        ("D-50-55 section triggered", "D-50-55" in str(generator._process_all_content_controls(client_data, lab_results, hhq_responses)))
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
        print("✅ D-50-55 Vitamin D section matches screenshot exactly")
        print("✅ Content: 'This level is close to the optimal parameters and though no additional")
        print("    intervention is recommended, you may want to check your VITAMIN D level a few") 
        print("    times per year to make sure that it does not drop.'")
    else:
        print("❌ Some checks failed")
    print("=" * 60)

if __name__ == "__main__":
    verify_d_50_55_final() 