#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data with MTHFR variants AND depression history
client_data = {
    'name': 'test_depression',
    'gender': 'female'
}

lab_results = {
    'APO1': 'E2/E4',
    'METAB_GLUT': 222.0,
    'MTHFR_1': 'Detected', 
    'MTHFR_2': 'Detected'
}

# HHQ responses that should trigger depression history
hhq_responses = {
    'hh_depression': True  # This should trigger quick-depression-mood-disorder
}

generator = RoadmapGenerator()

print("=== MTHFR + DEPRESSION HISTORY DEBUG ===")

# Check the processed content controls first
processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)

print(f"Depression control set: 'quick-depression-mood-disorder' = {processed_content.get('quick-depression-mood-disorder')}")
print(f"MTHFR variants control: 'has-MTHFR-variants' = {processed_content.get('has-MTHFR-variants')}")

# Generate full roadmap
roadmap_content = generator.generate_roadmap(client_data, lab_results, hhq_responses)

# Extract just the MTHFR section
lines = roadmap_content.split('\n')
mthfr_section_lines = []
in_mthfr_section = False

for line in lines:
    if '## **MTHFR Genetics & Methylation Support**' in line:
        in_mthfr_section = True
        mthfr_section_lines.append(line)
    elif in_mthfr_section:
        if line.strip().startswith('## **') and 'MTHFR' not in line:
            break  # Next section started
        mthfr_section_lines.append(line)

print(f"\n=== MTHFR SECTION WITH DEPRESSION HISTORY ===")
mthfr_text = '\n'.join(mthfr_section_lines)
print(mthfr_text)

# Check if the depression text is present
if "debilitating depression" in mthfr_text:
    print(f"\n✅ SUCCESS: Depression conditional text found!")
else:
    print(f"\n❌ MISSING: Depression conditional text NOT found")
    
# Also check for the key phrases
depression_phrases = [
    "debilitating depression",
    "elevated HOMOCYSTEINE",
    "recommendation extends beyond"
]

print(f"\n=== DEPRESSION PHRASE CHECK ===")
for phrase in depression_phrases:
    if phrase in mthfr_text:
        print(f"✅ Found: '{phrase}'")
    else:
        print(f"❌ Missing: '{phrase}'") 