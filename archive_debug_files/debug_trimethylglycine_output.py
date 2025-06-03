#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def show_trimethylglycine_section():
    """Show the actual generated TRIMETHYLGLYCINE section"""
    
    print("🔍 TRIMETHYLGLYCINE Section Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client with elevated homocysteine > 12
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'INFLAM_HOMOCYS': 15.5,  # Elevated > 12
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
    
    # Highlight the specific TRIMETHYLGLYCINE content
    print("\n🎯 Specific TRIMETHYLGLYCINE Content:")
    print("-" * 50)
    
    lines = homo_section.split('\n')
    trimethyl_content = []
    
    for line in lines:
        if "TRIMETHYLGLYCINE" in line or "methylated B complex when HOMOCYSTEINE levels are > 12" in line:
            trimethyl_content.append(line)
    
    for line in trimethyl_content:
        print(line)
    
    # Show content controls status
    print("\n⚙️ Content Controls Status:")
    print("-" * 30)
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    controls_to_check = ['quick-homocysteine', 'quick-Homo12', 'homocysteine-value']
    for control in controls_to_check:
        status = processed_content.get(control, False)
        print(f"✅ {control}: {status}")
    
    # Show comparison with screenshot text
    print("\n📸 Screenshot Comparison:")
    print("-" * 30)
    expected_text = "Consider starting TRIMETHYLGLYCINE 1000 mg/day. We recommend adding this supplement to a methylated B complex when HOMOCYSTEINE levels are > 12."
    
    if expected_text in roadmap:
        print("✅ EXACT MATCH: Content matches screenshot word-for-word!")
    else:
        print("❌ NO MATCH: Content differs from screenshot")
        # Show what we actually have
        if trimethyl_content:
            print(f"Actual content: {trimethyl_content[0]}")

if __name__ == "__main__":
    show_trimethylglycine_section() 