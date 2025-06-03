#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data matching the patient showing issues
client_data = {
    'name': 'test2',
    'gender': 'female'
}

lab_results = {
    'APO1': 'E2/E3',
    'METAB_GLUT': 252.0,
    'MTHFR_1': 'Detected', 
    'MTHFR_2': 'Detected'
}

hhq_responses = {}

generator = RoadmapGenerator()

print("=== CONTENT CONTROL DEBUG ===")

# Generate full roadmap
final_roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)

# Check for unprocessed content controls
unprocessed_controls = []
import re

# Find all {{#...}} and {{/...}} patterns
control_patterns = re.findall(r'\{\{[#/][^}]+\}\}', final_roadmap)
if control_patterns:
    print(f"\n🚨 UNPROCESSED CONTENT CONTROLS FOUND:")
    for control in set(control_patterns):
        print(f"  - {control}")
        unprocessed_controls.append(control)

# Check for simple placeholders like {{control-name}}
placeholder_patterns = re.findall(r'\{\{[^#/][^}]+\}\}', final_roadmap)
if placeholder_patterns:
    print(f"\n🚨 UNPROCESSED PLACEHOLDERS FOUND:")
    for placeholder in set(placeholder_patterns):
        print(f"  - {placeholder}")

# Check specifically for MTHFR content
mthfr_section_start = final_roadmap.find("MTHFR Genetics")
if mthfr_section_start > -1:
    mthfr_section_end = final_roadmap.find("---", mthfr_section_start + 100)
    if mthfr_section_end == -1:
        mthfr_section_end = mthfr_section_start + 1000
    
    mthfr_section = final_roadmap[mthfr_section_start:mthfr_section_end]
    print(f"\n=== MTHFR SECTION CONTENT ===")
    print(mthfr_section)
    
    # Check for specific MTHFR controls
    mthfr_controls = ['quick-MTHFR1', 'quick-MTHFR2', 'has-MTHFR-variants']
    for control in mthfr_controls:
        if control in mthfr_section:
            print(f"\n🚨 Found unprocessed control '{control}' in MTHFR section")

if unprocessed_controls or placeholder_patterns:
    print(f"\n❌ CONTENT CONTROLS NOT PROCESSED PROPERLY")
else:
    print(f"\n✅ ALL CONTENT CONTROLS PROCESSED CORRECTLY")

def test_content_control_processing():
    """Debug content control processing."""
    
    # Simple template with content control
    test_template = """
Start of template

{{#autoimmune-disease-section}}
This autoimmune section should only appear when triggered.
{{/autoimmune-disease-section}}

End of template
"""
    
    from roadmap_generator import RoadmapGenerator
    generator = RoadmapGenerator()
    
    # Test with control = True
    print("=== Test 1: Control = True ===")
    processed_content = {'autoimmune-disease-section': True}
    result1 = generator._apply_content_controls_to_template(test_template, processed_content)
    print("Result:", repr(result1))
    print("Contains autoimmune text:", "autoimmune section should only appear" in result1)
    
    # Test with control = False  
    print("\n=== Test 2: Control = False ===")
    processed_content = {'autoimmune-disease-section': False}
    result2 = generator._apply_content_controls_to_template(test_template, processed_content)
    print("Result:", repr(result2))
    print("Contains autoimmune text:", "autoimmune section should only appear" in result2)
    
    # Test with control missing
    print("\n=== Test 3: Control Missing ===")
    processed_content = {}
    result3 = generator._apply_content_controls_to_template(test_template, processed_content)
    print("Result:", repr(result3))
    print("Contains autoimmune text:", "autoimmune section should only appear" in result3)

if __name__ == "__main__":
    test_content_control_processing() 