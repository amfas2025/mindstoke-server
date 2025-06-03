#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def show_betaine_section():
    """Show the actual generated BETAINE HCL section"""
    
    print("🔍 BETAINE HCL Section Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client with bariatric surgery history
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses = {
        'hh_bariatric_surgery': True
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the Medical History section
    history_start = roadmap.find("## **Medical History & Specialized Protocols**")
    if history_start == -1:
        print("❌ Medical History section not found!")
        return
    
    # Find the end of the medical history section (next ## section or ---)
    next_section = roadmap.find("---", history_start + 1)
    if next_section == -1:
        history_section = roadmap[history_start:]
    else:
        history_section = roadmap[history_start:next_section]
    
    print("\n📋 Generated Medical History Section:")
    print("-" * 50)
    print(history_section)
    
    # Extract just the bariatric surgery content
    print("\n🎯 Bariatric Surgery Specific Content:")
    print("-" * 50)
    
    lines = history_section.split('\n')
    bariatric_content = []
    
    capture_bariatric = False
    for line in lines:
        if "**Bariatric Surgery Support:**" in line:
            capture_bariatric = True
            bariatric_content.append(line)
        elif capture_bariatric and line.strip():
            if line.startswith("{{#") or line.startswith("{{/"):
                # Stop at next content control
                break
            elif line.startswith("**") and "Surgery" not in line:
                # Stop at next section
                break
            else:
                bariatric_content.append(line)
        elif capture_bariatric and not line.strip():
            # Include empty lines within the section
            bariatric_content.append(line)
    
    for line in bariatric_content:
        print(line)
    
    # Show content controls status
    print("\n⚙️ Content Controls Status:")
    print("-" * 30)
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    controls_to_check = ['BariSurg', 'quick-gallbladder']
    for control in controls_to_check:
        status = processed_content.get(control, False)
        print(f"✅ {control}: {status}")
    
    # Show comparison with screenshot text
    print("\n📸 Screenshot Comparison:")
    print("-" * 30)
    
    expected_text = "Consider taking a BETAINE HCL supplement with your meals, and particularly when you take a B-COMPLEX supplement. Your history of bariatric surgery may have reduced your ability to make HCL and can lead to acid reflux, poor digestion, bloating, etc. This can also negatively impact your ability to absorb essential B vitamins."
    
    text_match = expected_text in roadmap
    
    print(f"✅ BETAINE HCL text matches screenshot: {text_match}")
    
    if text_match:
        print("🎉 PERFECT! BETAINE HCL content matches screenshot word-for-word!")
    else:
        print("❌ Text doesn't match exactly - checking for key phrases...")
        
        key_phrases = [
            "BETAINE HCL supplement with your meals",
            "particularly when you take a B-COMPLEX supplement",
            "history of bariatric surgery may have reduced your ability to make HCL",
            "acid reflux, poor digestion, bloating",
            "negatively impact your ability to absorb essential B vitamins"
        ]
        
        for phrase in key_phrases:
            match = phrase in roadmap
            print(f"  - '{phrase}': {match}")

if __name__ == "__main__":
    show_betaine_section() 