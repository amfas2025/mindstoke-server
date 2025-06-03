#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data matching the E2/E3 client
client_data = {
    'name': 'test1',
    'gender': 'female'
}

lab_results = {
    'APO1': 'E2/E3',
    'METAB_GLUT': 222.0,
    'MTHFR_1': 'Not Detected', 
    'MTHFR_2': 'Not Detected'
}

hhq_responses = {
    'hh_taking_nac': True  # Use the correct key format for NAC
}

generator = RoadmapGenerator()

print("=== APOE E2/E3 SECTION DEBUG ===")

# Generate full roadmap
roadmap_content = generator.generate_roadmap(client_data, lab_results, hhq_responses)

# Extract just the APOE section
lines = roadmap_content.split('\n')
apoe_section_lines = []
in_apoe_section = False

for line in lines:
    if '## **APO E Genetic Profile' in line:
        in_apoe_section = True
        apoe_section_lines.append(line)
    elif in_apoe_section and line.startswith('## **') and 'APO E' not in line:
        # We've hit the next section
        break
    elif in_apoe_section:
        apoe_section_lines.append(line)

print("\n=== CURRENT APOE SECTION OUTPUT ===")
for line in apoe_section_lines:
    print(line)

print("\n=== APOE SECTION LENGTH ===")
print(f"Total lines: {len(apoe_section_lines)}")

# Check for specific reference elements
print("\n=== CHECKING REFERENCE ELEMENTS ===")
apoe_text = '\n'.join(apoe_section_lines)

checks = [
    ("E2/E3 genotype", "E2/E3" in apoe_text),
    ("Glutathione value", "222" in apoe_text),
    ("No E4 risk message", "You do not have the APO E genetic risk" in apoe_text),
    ("Additional testing recommendation", "ADDITIONAL IMMUNE SYSTEM TESTING" in apoe_text),
    ("NAC reference", "NAC" in apoe_text),
    ("Dosing reference", "dosing" in apoe_text)
]

for check_name, result in checks:
    status = "✅" if result else "❌"
    print(f"{status} {check_name}: {result}") 