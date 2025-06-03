#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data with MTHFR variants AND depression history
client_data = {
    'name': 'test_all_mthfr',
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

print("=== ALL MTHFR DEPRESSION CONDITIONALS TEST ===")

# Check the processed content controls first
processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)

print(f"Depression control: 'quick-depression-mood-disorder' = {processed_content.get('quick-depression-mood-disorder')}")
print(f"MTHFR variants: 'has-MTHFR-variants' = {processed_content.get('has-MTHFR-variants')}")
print(f"MTHFR1 control: 'quick-MTHFR1' = {processed_content.get('quick-MTHFR1')}")
print(f"MTHFR2 control: 'quick-MTHFR2' = {processed_content.get('quick-MTHFR2')}")

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

print(f"\n=== COMPLETE MTHFR SECTION ===")
mthfr_text = '\n'.join(mthfr_section_lines)
print(mthfr_text)

# Count depression conditionals 
depression_count = mthfr_text.count("debilitating depression")
print(f"\n=== DEPRESSION CONDITIONAL CHECK ===")
print(f"Number of 'debilitating depression' mentions: {depression_count}")

# Check for all expected sections
expected_sections = [
    "The C677T and A1298C alleles are variants",  # Main section
    "- The C677T allele is a variant",            # Individual C677T
    "- The A1298C allele is a variant"            # Individual A1298C
]

print(f"\n=== SECTION VERIFICATION ===")
for section in expected_sections:
    if section in mthfr_text:
        print(f"✅ Found: '{section}'")
    else:
        print(f"❌ Missing: '{section}'")

# Verify each section has depression conditional
sections_with_depression = []
if "The C677T and A1298C alleles are variants" in mthfr_text and "debilitating depression" in mthfr_text:
    main_section_start = mthfr_text.find("The C677T and A1298C alleles are variants")
    main_section_end = mthfr_text.find("- The C677T allele", main_section_start)
    if main_section_end == -1:
        main_section_end = len(mthfr_text)
    main_section = mthfr_text[main_section_start:main_section_end]
    if "debilitating depression" in main_section:
        sections_with_depression.append("Main combined section")

if "- The C677T allele is a variant" in mthfr_text:
    c677t_start = mthfr_text.find("- The C677T allele is a variant")
    c677t_end = mthfr_text.find("- The A1298C allele", c677t_start)
    if c677t_end == -1:
        c677t_end = len(mthfr_text)
    c677t_section = mthfr_text[c677t_start:c677t_end]
    if "debilitating depression" in c677t_section:
        sections_with_depression.append("Individual C677T section")

if "- The A1298C allele is a variant" in mthfr_text:
    a1298c_start = mthfr_text.find("- The A1298C allele is a variant")
    a1298c_section = mthfr_text[a1298c_start:]
    if "debilitating depression" in a1298c_section:
        sections_with_depression.append("Individual A1298C section")

print(f"\n=== SECTIONS WITH DEPRESSION CONDITIONALS ===")
for section in sections_with_depression:
    print(f"✅ {section}")

if len(sections_with_depression) == 3:
    print(f"\n🎉 SUCCESS: All 3 MTHFR sections have depression conditionals!")
else:
    print(f"\n❌ ISSUE: Only {len(sections_with_depression)}/3 sections have depression conditionals") 