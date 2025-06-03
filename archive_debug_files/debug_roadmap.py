#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

# Create generator
generator = RoadmapGenerator()

print("=== TEMPLATE CONTENT ANALYSIS ===")
template = generator.template_content

# Check for multiple APOE sections
apoe_count = template.count("APO E Genetic Profile")
print(f"Number of APOE sections in template: {apoe_count}")

# Check for multiple welcome messages  
welcome_count = template.count("Welcome")
print(f"Number of Welcome messages in template: {welcome_count}")

# Show the first 1000 characters
print("\n=== FIRST 1000 CHARACTERS ===")
print(template[:1000])

# Show where duplicates occur if any
if apoe_count > 1:
    print("\n=== APOE SECTION LOCATIONS ===")
    start = 0
    for i in range(apoe_count):
        pos = template.find("APO E Genetic Profile", start)
        print(f"APOE section {i+1} at position: {pos}")
        print(f"Context: ...{template[max(0, pos-50):pos+100]}...")
        start = pos + 1

if welcome_count > 1:
    print("\n=== WELCOME MESSAGE LOCATIONS ===")
    start = 0
    for i in range(welcome_count):
        pos = template.find("Welcome", start)
        print(f"Welcome message {i+1} at position: {pos}")
        print(f"Context: ...{template[max(0, pos-50):pos+100]}...")
        start = pos + 1 