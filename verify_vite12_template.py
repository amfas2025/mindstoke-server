#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def verify_vite12_template():
    """Verify that the VitE12 section appears correctly in template output"""
    
    print("📋 VitE12 Template Verification")
    print("=" * 50)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test with optimal vitamin E
    processed_content = {
        'VitE12': True,
        'quick-vitE': '15.0 mg/L'
    }
    
    # Load template
    template = generator._load_template()
    
    # Apply content controls
    result = generator._apply_content_controls_to_template(template, processed_content)
    
    # Check if VitE12 section appears
    vite12_text = "This level falls within the optimal parameters and no additional intervention is recommended."
    vite12_appears = vite12_text in result
    
    print(f"✅ VitE12 section appears in template: {vite12_appears}")
    
    # Check if general vitamin E section appears
    general_vite_appears = "Your combined **Vitamin E** level is 15.0 mg/L" in result
    print(f"✅ General vitamin E section appears: {general_vite_appears}")
    
    if vite12_appears and general_vite_appears:
        print("\n🎉 SUCCESS: Both VitE12 and general vitamin E sections are working!")
    else:
        print("\n❌ Issue: One or both sections are not appearing correctly")
        
        # Show context around vitamin E sections
        lines = result.split('\n')
        for i, line in enumerate(lines):
            if 'Vitamin E' in line or 'VitE12' in line:
                start = max(0, i-2)
                end = min(len(lines), i+3)
                print(f"\nContext around line {i+1}:")
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{lines[j]}")

if __name__ == "__main__":
    verify_vite12_template() 