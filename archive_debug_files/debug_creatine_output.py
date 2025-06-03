#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def show_creatine_section():
    """Show the actual generated CREATINE MONOHYDRATE section"""
    
    print("🔍 CREATINE MONOHYDRATE Section Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client with very high homocysteine > 15
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'INFLAM_HOMOCYS': 18.5,  # Very high > 15
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the homocysteine section
    homo_start = roadmap.find("## **↑'d Homocysteine Levels Can Impair Brain Function**")
    if homo_start == -1:
        print("❌ Homocysteine section not found!")
        return
    
    # Find the end of the homocysteine section (next ## section or ---)
    next_section = roadmap.find("---", homo_start + 1)
    if next_section == -1:
        homo_section = roadmap[homo_start:]
    else:
        homo_section = roadmap[homo_start:next_section]
    
    print("\n📋 Generated Homocysteine Section:")
    print("-" * 50)
    print(homo_section)
    
    # Highlight the specific supplement content
    print("\n🎯 Supplement Recommendations (Both Should Appear):")
    print("-" * 50)
    
    lines = homo_section.split('\n')
    supplement_content = []
    
    for line in lines:
        if ("TRIMETHYLGLYCINE" in line or 
            "CREATINE MONOHYDRATE" in line or 
            "methylated B complex when HOMOCYSTEINE levels are >" in line or
            "5 grams per day" in line or
            "chewable or a powder form" in line or
            "energy levels and help to support HOMOCYSTEINE recycling" in line):
            supplement_content.append(line)
    
    for line in supplement_content:
        print(line)
    
    # Show content controls status
    print("\n⚙️ Content Controls Status:")
    print("-" * 30)
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    controls_to_check = ['quick-homocysteine', 'quick-Homo12', 'quick-Homo15', 'homocysteine-value']
    for control in controls_to_check:
        status = processed_content.get(control, False)
        print(f"✅ {control}: {status}")
    
    # Show comparison with screenshot text
    print("\n📸 Screenshot Comparison:")
    print("-" * 30)
    
    trimethyl_expected = "Consider starting TRIMETHYLGLYCINE 1000 mg/day. We recommend adding this supplement to a methylated B complex when HOMOCYSTEINE levels are > 12."
    creatine_expected = "Consider starting a supplement called CREATINE MONOHYDRATE. The standard dose is 5 grams per day. We recommend adding this supplement to a methylated B complex and trimethylglycine when HOMOCYSTEINE levels are > 15. CREATINE comes in a chewable or a powder form that can be mixed in a drink. It can help improve energy levels and help to support HOMOCYSTEINE recycling."
    
    trimethyl_match = trimethyl_expected in roadmap
    creatine_match = creatine_expected in roadmap
    
    print(f"✅ TRIMETHYLGLYCINE text matches: {trimethyl_match}")
    print(f"✅ CREATINE text matches: {creatine_match}")
    
    if trimethyl_match and creatine_match:
        print("🎉 PERFECT! Both supplements match screenshot word-for-word!")
    else:
        print("❌ Some text doesn't match exactly")

if __name__ == "__main__":
    show_creatine_section() 