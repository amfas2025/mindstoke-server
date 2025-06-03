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

print("=== MTHFR SECTION DEBUG ===")

# Generate full roadmap
roadmap_content = generator.generate_roadmap(client_data, lab_results, hhq_responses)

print(f"Total roadmap length: {len(roadmap_content)} characters")

# Search for MTHFR mentions
mthfr_keyword_searches = [
    "MTHFR",
    "Genetics",
    "Methylation", 
    "C677T",
    "A1298C",
    "folate",
    "methylated"
]

print("\n=== SEARCHING FOR MTHFR-RELATED CONTENT ===")
for keyword in mthfr_keyword_searches:
    count = roadmap_content.count(keyword)
    if count > 0:
        print(f"✅ Found '{keyword}': {count} times")
        # Show context around first occurrence
        first_occurrence = roadmap_content.find(keyword)
        if first_occurrence > -1:
            start = max(0, first_occurrence - 100)
            end = min(len(roadmap_content), first_occurrence + 200)
            context = roadmap_content[start:end]
            print(f"   Context: ...{context}...")
            print()
    else:
        print(f"❌ '{keyword}' not found")

# Look for section headers
print("\n=== ALL SECTION HEADERS ===")
lines = roadmap_content.split('\n')
for i, line in enumerate(lines):
    if '##' in line and ('Genetics' in line or 'MTHFR' in line or 'Methylation' in line):
        print(f"Line {i}: {line}")
        # Show next few lines for context
        for j in range(1, 6):
            if i+j < len(lines):
                print(f"  +{j}: {lines[i+j]}")
        print()

# Check if MTHFR section exists but is empty
print("\n=== LOOKING FOR MTHFR SECTION STRUCTURE ===")
sections = roadmap_content.split('##')
for i, section in enumerate(sections):
    if 'MTHFR' in section or 'Genetics' in section or 'Methylation' in section:
        print(f"Section {i} (first 500 chars):")
        print("=" * 50)
        print(section[:500])
        print("=" * 50)
        print(f"Section length: {len(section)} characters")
        print()

# Check what sections ARE present
print("\n=== ALL SECTIONS PRESENT ===")
for i, section in enumerate(sections):
    if section.strip():
        # Get section title (first line)
        first_line = section.split('\n')[0].strip()
        if first_line and len(first_line) < 100:  # Reasonable header length
            print(f"Section {i}: {first_line}")

print(f"\n=== TOTAL SECTIONS: {len([s for s in sections if s.strip()])} ===") 