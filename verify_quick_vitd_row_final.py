#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_quick_vitd_row_final():
    """Final verification showing quick-VitD-row section matching the screenshot"""
    
    print("✅ Quick-VitD-row Vitamin D Section - Final Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test Case: Vitamin D = 45 ng/mL (40-49 range - should trigger quick-VitD-row)
    print("\n📋 Example: Vitamin D = 45 ng/mL (Suboptimal - requires supplementation)")
    print("-" * 70)
    
    lab_results = {
        'VIT_D25': 45.0
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract vitamin D section
    lines = roadmap.split('\n')
    vitamin_d_section = []
    
    for i, line in enumerate(lines):
        if "Your VITAMIN D level is suboptimal" in line:
            # Extract the quick-VitD-row section (next 8-10 lines)
            for j in range(i, min(i + 10, len(lines))):
                if lines[j].strip():
                    vitamin_d_section.append(lines[j])
                # Stop if we hit the next major section
                if j > i and ("**" in lines[j] and "VITAMIN" not in lines[j]):
                    break
            break
    
    print("\n📋 Generated Quick-VitD-row Section:")
    print("-" * 40)
    for line in vitamin_d_section:
        print(line.strip())
    
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION RESULTS:")
    print("=" * 60)
    
    # Check for exact phrases from screenshot
    roadmap_text = ' '.join(vitamin_d_section)
    
    checks = [
        ("Header text", "Your VITAMIN D level is suboptimal, and supplementation is recommended" in roadmap_text),
        ("Guidebook reference", "Please note the section in your Guidebook" in roadmap_text),
        ("D-less-30 dosing", "10,000 iu" in roadmap_text),
        ("D-30-39 dosing", "8,000 iu" in roadmap_text),
        ("D-40-49 dosing", "4,000 iu" in roadmap_text),
        ("D-50-59 dosing", "2,000 iu" in roadmap_text),
        ("Recheck instruction", "recheck your levels in 90 days" in roadmap_text)
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
        print("✅ Quick-VitD-row section matches screenshot exactly")
    else:
        print("❌ Some checks failed")
    print("=" * 60)

if __name__ == "__main__":
    verify_quick_vitd_row_final() 