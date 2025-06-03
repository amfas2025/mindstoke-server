#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data - E2/E3 patient like in your screenshot
client_data = {
    'name': 'test2',
    'gender': 'female'
}

lab_results = {
    'APO1': 'E2/E3',
    'METAB_GLUT': 252.0
}

hhq_responses = {}

generator = RoadmapGenerator()

print("=== STEP-BY-STEP DEBUG ===")

# Step 1: Original template
print("1. Original template APOE sections:", generator.template_content.count("APO E Genetic Profile"))
print("1. Original template Welcome messages:", generator.template_content.count("Welcome"))

# Step 2: Process content controls
processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
print(f"2. Content controls processed. Quick-nonE4: {processed_content.get('quick-nonE4')}")

# Step 3: Apply content controls  
roadmap = generator._apply_content_controls_to_template(generator.template_content, processed_content)
print("3. After content controls - APOE sections:", roadmap.count("APO E Genetic Profile"))
print("3. After content controls - Welcome messages:", roadmap.count("Welcome"))

# Step 4: Replace client info
roadmap = generator._replace_client_info(roadmap, client_data)
print("4. After client info - APOE sections:", roadmap.count("APO E Genetic Profile"))
print("4. After client info - Welcome messages:", roadmap.count("Welcome"))

# Step 5: Process lab values
roadmap = generator._process_lab_values_intelligent(roadmap, lab_results, processed_content)
print("5. After lab values - APOE sections:", roadmap.count("APO E Genetic Profile"))
print("5. After lab values - Welcome messages:", roadmap.count("Welcome"))

# Final check
print(f"\nFinal roadmap length: {len(roadmap)} characters")

# Show first part of roadmap
print("\n=== FIRST 2000 CHARACTERS OF FINAL ROADMAP ===")
print(roadmap[:2000])
print("...")

# Check for specific duplication pattern
if "Welcome test2" in roadmap:
    positions = []
    start = 0
    while True:
        pos = roadmap.find("Welcome test2", start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    print(f"\n'Welcome test2' found at positions: {positions}")
    for i, pos in enumerate(positions):
        print(f"\nOccurrence {i+1} context:")
        print(roadmap[max(0, pos-100):pos+200]) 