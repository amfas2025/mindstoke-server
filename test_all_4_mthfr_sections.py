#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Test data with MTHFR variants AND depression history
client_data = {
    'name': 'test_4_mthfr',
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

print("=== ALL 4 MTHFR DEPRESSION SECTIONS TEST ===")

# Check the processed content controls first
processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)

print(f"Depression control: 'quick-depression-mood-disorder' = {processed_content.get('quick-depression-mood-disorder')}")
print(f"MTHFR variants: 'has-MTHFR-variants' = {processed_content.get('has-MTHFR-variants')}")
print(f"MTHFR1 control: 'quick-MTHFR1' = {processed_content.get('quick-MTHFR1')}")
print(f"MTHFR2 control: 'quick-MTHFR2' = {processed_content.get('quick-MTHFR2')}")
print(f"needs-methyl control: 'needs-methyl' = {processed_content.get('needs-methyl')}")

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
    "- The C677T allele is a variant",            # Individual C677T (first instance)
    "- The A1298C allele is a variant"            # Individual A1298C
]

print(f"\n=== SECTION VERIFICATION ===")
for section in expected_sections:
    if section in mthfr_text:
        print(f"✅ Found: '{section}'")
    else:
        print(f"❌ Missing: '{section}'")

# Count occurrences of C677T sections (should be 2 - one basic, one with needs-methyl)
c677t_count = mthfr_text.count("- The C677T allele is a variant")
print(f"\n=== C677T SECTIONS COUNT ===")
print(f"Number of '- The C677T allele is a variant' sections: {c677t_count}")

# Expected: 4 total depression mentions (1 main + 2 C677T + 1 A1298C)
if depression_count == 4:
    print(f"\n🎉 SUCCESS: Found all 4 depression conditionals!")
    print(f"   - 1 in main combined section")
    print(f"   - 2 in individual C677T sections")  
    print(f"   - 1 in individual A1298C section")
elif depression_count == 3:
    print(f"\n⚠️  PARTIAL: Found 3/4 depression conditionals")
    print(f"   - Missing the 4th section (likely the needs-methyl C677T section)")
else:
    print(f"\n❌ ISSUE: Only {depression_count}/4 depression conditionals found")

print(f"\n=== DETAILED SECTION BREAKDOWN ===")
# Split by lines and analyze each section
section_markers = []
for i, line in enumerate(mthfr_text.split('\n')):
    if "The C677T and A1298C alleles are variants" in line:
        section_markers.append(("Main section", i))
    elif "- The C677T allele is a variant" in line:
        section_markers.append(("C677T section", i))
    elif "- The A1298C allele is a variant" in line:
        section_markers.append(("A1298C section", i))

for section_name, line_num in section_markers:
    print(f"{section_name} found at line {line_num}") 