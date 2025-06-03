#!/usr/bin/env python3

import sys
import os
import re

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def show_methylpro_section():
    """Show the actual generated methylated B complex section"""
    
    print("🔍 Methylated B Complex Section Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client with MTHFR variants and depression
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'MTHFR_1': 'C677T Heterozygous',
        'MTHFR_2': 'A1298C Heterozygous',
        'INFLAM_HOMOCYS': 8.5,
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses = {
        'hh_depression': True
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the MTHFR section
    mthfr_start = roadmap.find("## **MTHFR Genetics & Methylation Support**")
    if mthfr_start == -1:
        print("❌ MTHFR section not found!")
        return
    
    # Find the end of the MTHFR section (next ## section or end)
    next_section = roadmap.find("## **", mthfr_start + 1)
    if next_section == -1:
        mthfr_section = roadmap[mthfr_start:]
    else:
        mthfr_section = roadmap[mthfr_start:next_section]
    
    print("\n📋 Generated MTHFR Section:")
    print("-" * 50)
    print(mthfr_section)
    
    # Highlight the specific methylpro content
    print("\n🎯 Specific Methylated B Complex Content:")
    print("-" * 50)
    
    lines = mthfr_section.split('\n')
    in_methylpro = False
    methylpro_content = []
    
    for line in lines:
        if "Consider starting methylated B complex supplement" in line:
            in_methylpro = True
            methylpro_content.append(line)
        elif in_methylpro and line.strip():
            if line.startswith('-') or "SUPER METHYL-SP" in line or "METHYLPRO" in line or "This recommendation is offered" in line or "in place of your current B-COMPLEX" in line:
                methylpro_content.append(line)
            elif line.startswith('##') or (line.startswith('-') and "Given your genetic MTHFR profile" in line):
                break
    
    for line in methylpro_content:
        print(line)
    
    # Show content controls status
    print("\n⚙️ Content Controls Status:")
    print("-" * 30)
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    controls_to_check = ['methylpro', 'MTHFR-depression', 'Quick-Takes-B', 'has-MTHFR-variants']
    for control in controls_to_check:
        status = processed_content.get(control, False)
        print(f"✅ {control}: {status}")

if __name__ == "__main__":
    show_methylpro_section() 