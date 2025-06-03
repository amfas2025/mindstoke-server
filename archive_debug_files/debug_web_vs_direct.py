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

print("=== COMPARING WEB ROUTE vs DIRECT CALL ===\n")

# This mimics the web route behavior
print("1. PROCESSED CONTENT (what _process_all_content_controls returns):")
processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
print(f"Type: {type(processed_content)}")
print(f"Keys (first 10): {list(processed_content.keys())[:10] if processed_content else 'None'}")

# Check MTHFR specific values
mthfr_keys = ['quick-MTHFR1', 'quick-MTHFR2', 'has-MTHFR-variants', 'MTHFR_C677T', 'MTHFR_A1298C']
print("\nMTHFR-related processed content:")
for key in mthfr_keys:
    if processed_content and key in processed_content:
        print(f"  {key}: {processed_content[key]}")

print("\n" + "="*60)

# This is what the web route passes to the template
print("2. ROADMAP CONTENT (what generate_roadmap returns):")
roadmap_content = generator.generate_roadmap(client_data, lab_results, hhq_responses)
print(f"Type: {type(roadmap_content)}")
print(f"Length: {len(roadmap_content) if roadmap_content else 0} characters")

# Check if it contains unprocessed controls
import re
unprocessed_controls = re.findall(r'\{\{[#/][^}]+\}\}', roadmap_content)
if unprocessed_controls:
    print(f"\n❌ UNPROCESSED CONTROLS FOUND: {len(set(unprocessed_controls))}")
    for control in set(unprocessed_controls)[:5]:  # Show first 5
        print(f"  - {control}")
else:
    print("\n✅ NO UNPROCESSED CONTROLS")

# Check specifically for MTHFR content in roadmap_content
mthfr_section_start = roadmap_content.find("MTHFR Genetics") if roadmap_content else -1
if mthfr_section_start > -1:
    mthfr_section_end = roadmap_content.find("---", mthfr_section_start + 100)
    if mthfr_section_end == -1:
        mthfr_section_end = mthfr_section_start + 500
    
    mthfr_section = roadmap_content[mthfr_section_start:mthfr_section_end]
    print(f"\n3. MTHFR SECTION IN ROADMAP_CONTENT:")
    print("=" * 40)
    print(mthfr_section)
    print("=" * 40)
    
    # Check for unprocessed MTHFR controls
    mthfr_controls = ['{{#quick-MTHFR1}}', '{{/quick-MTHFR1}}', '{{#quick-MTHFR2}}', '{{/quick-MTHFR2}}', '{{#has-MTHFR-variants}}']
    found_unprocessed = []
    for control in mthfr_controls:
        if control in mthfr_section:
            found_unprocessed.append(control)
    
    if found_unprocessed:
        print(f"\n❌ UNPROCESSED MTHFR CONTROLS: {found_unprocessed}")
    else:
        print(f"\n✅ MTHFR CONTROLS PROCESSED")

print("\n" + "="*60)
print("CONCLUSION:")
print("The web route should use processed_content instead of roadmap_content!")
print("Or roadmap_content should already be processed, but it's not.") 