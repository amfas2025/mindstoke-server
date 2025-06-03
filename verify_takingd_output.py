#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_takingd_output():
    """Verify and show the exact output of the quick-VitD-row-takingD section"""
    
    print("📋 Quick-VitD-row-takingD Section - Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test: Person taking vitamin D with level = 45 ng/mL (suboptimal)
    print("\n📋 Example: Taking Vitamin D, Level = 45 ng/mL")
    print("-" * 50)
    
    lab_results = {
        'VIT_D25': 45.0
    }
    
    hhq_responses = {
        'hh_taking_vitamin_d': True  # Person is taking vitamin D
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract vitamin D section
    lines = roadmap.split('\n')
    vitamin_d_section = []
    
    # Find the takingD section specifically
    capturing = False
    for i, line in enumerate(lines):
        if "In your health history, you indicated that you are taking a VITAMIN D supplement" in line:
            capturing = True
        
        if capturing:
            vitamin_d_section.append(line)
            # Stop when we hit the next major section or significant gap
            if len(vitamin_d_section) > 1 and (
                line.strip() == "" and i < len(lines) - 1 and 
                lines[i + 1].startswith("**") and "VITAMIN" not in lines[i + 1]
            ):
                break
            # Also stop if we encounter another major header
            if line.startswith("##") and "Vitamin" not in line:
                vitamin_d_section.pop()  # Remove the new header from our section
                break
    
    print("\n📋 Generated Quick-VitD-row-takingD Section:")
    print("-" * 50)
    for line in vitamin_d_section:
        if line.strip():  # Only show non-empty lines
            print(line)
    
    print("\n" + "=" * 60)
    print("🎯 CONTENT VERIFICATION:")
    print("=" * 60)
    
    # Verify exact content matches the screenshot
    roadmap_text = '\n'.join(vitamin_d_section)
    
    checks = [
        ("Header message", "In your health history, you indicated that you are taking a VITAMIN D supplement" in roadmap_text),
        ("Suboptimal levels", "However, your serum levels remain suboptimal" in roadmap_text),
        ("Guidebook reference", "Please note the section in your Guidebook" in roadmap_text),
        ("Additional dosing phrase", "add an additional" in roadmap_text),
        ("D < 30 dosing", "10,000 iu/day to your current dosing" in roadmap_text),
        ("D 30-39 dosing", "8,000 iu/day to your current dosing" in roadmap_text),
        ("D 40-49 dosing", "4,000 iu/day to your current dosing" in roadmap_text),
        ("D 50-59 dosing", "2,000 iu/day to your current dosing" in roadmap_text),
        ("Recheck instruction", "recheck in 90 days" in roadmap_text)
    ]
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CONTENT VERIFIED!")
        print("✅ Quick-VitD-row-takingD section matches expected format exactly")
    else:
        print("❌ Some content checks failed")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    verify_takingd_output() 