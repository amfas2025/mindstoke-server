#!/usr/bin/env python3
"""
Test script to verify the extended chronic inflammation section with A/G ratio and uric acid conditions
"""

from roadmap_generator import RoadmapGenerator
import re

def test_extended_inflammation_conditions():
    """Test the A/G ratio and uric acid conditions."""
    
    print("=== Testing Extended Chronic Inflammation Conditions ===\n")
    
    generator = RoadmapGenerator()
    
    # Test data with inflammation markers, A/G ratio components, and uric acid
    client_data = {'name': 'Test Patient', 'gender': 'female'}
    
    lab_results = {
        'INFLAM_CRP': 2.5,      # Elevated CRP
        'APO1': 'E3/E4',        # APO E4 genetics  
        'OMEGA_CHECK': 4.0,     # Low omega-3
        'LFT_ALB': 3.8,         # Low albumin 
        'LFT_TP': 7.5,          # Total protein -> A/G ratio = 3.8/(7.5-3.8) = 1.03 (low)
        'INFLAM_URIC': 7.2      # Elevated uric acid
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_alcohol_consumption': True,  # Alcohol consumption for compound conditions
        'hh_gout': True                  # Gout history for UAAcid-Gout
    }
    
    # Generate the roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Test all content controls
    processed = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    print('=== Content Control Results ===')
    
    # A/G Ratio conditions
    print(f"A/G Ratio value: {processed.get('quick-AG-ratio', 'NOT FOUND')}")
    print(f"A/G Ratio optimal (≥1.5): {processed.get('quick-AG-15', 'NOT FOUND')}")
    print(f"A/G Ratio low: {processed.get('ag-ratio-low', 'NOT FOUND')}")
    print(f"A/G + Alcohol compound: {processed.get('quick-AG-ETOH', 'NOT FOUND')}")
    
    print()
    
    # Uric Acid conditions  
    print(f"Uric Acid value: {processed.get('quick-uric-acid', 'NOT FOUND')}")
    print(f"Uric Acid optimal (≤6.5): {processed.get('UricAcid65', 'NOT FOUND')}")
    print(f"Uric Acid elevated: {processed.get('uric-acid-elevated', 'NOT FOUND')}")
    print(f"Uric Acid + Gout: {processed.get('UAAcid-Gout', 'NOT FOUND')}")
    print(f"Uric Acid + Alcohol: {processed.get('quick-uric-acid-ETOH', 'NOT FOUND')}")
    
    print()
    
    # CRP conditions (from previous section)
    print(f"CRP value: {processed.get('quick-CRP', 'NOT FOUND')}")
    print(f"CRP elevated: {processed.get('quick-CRP-elevated', 'NOT FOUND')}")
    print(f"APO E4 genetics: {processed.get('quick-apo-e4-genetics', 'NOT FOUND')}")
    
    print("\n=== Template Content Checks ===")
    
    # Check for A/G ratio content
    if 'A/G RATIO' in roadmap:
        print("✓ A/G Ratio content found")
        ag_match = re.search(r'Your baseline \*\*A/G RATIO\*\* is ([\d.]+)', roadmap)
        if ag_match:
            print(f"  - A/G ratio value displayed: {ag_match.group(1)}")
    else:
        print("✗ A/G Ratio content NOT found")
    
    # Check for uric acid content
    if 'URIC ACID' in roadmap:
        print("✓ Uric Acid content found")
        uric_match = re.search(r'Your baseline \*\*URIC ACID\*\* level was ([\d.]+)', roadmap)
        if uric_match:
            print(f"  - Uric acid value displayed: {uric_match.group(1)}")
    else:
        print("✗ Uric Acid content NOT found")
    
    # Check for alcohol interaction content
    if 'A/G Ratio + Alcohol' in roadmap:
        print("✓ A/G + Alcohol interaction found")
    else:
        print("✗ A/G + Alcohol interaction NOT found")
    
    if 'URIC ACID + Alcohol' in roadmap:
        print("✓ Uric Acid + Alcohol interaction found")
    else:
        print("✗ Uric Acid + Alcohol interaction NOT found")
    
    # Check for gout condition
    if 'GOUT' in roadmap:
        print("✓ Gout condition content found")
    else:
        print("✗ Gout condition content NOT found")
    
    print(f"\n=== Chronic Inflammation Section Length ===")
    inflammation_section = re.search(r'## \*\*Chronic Inflammation.*?(?=---|$)', roadmap, re.DOTALL)
    if inflammation_section:
        section_content = inflammation_section.group(0)
        print(f"Total section length: {len(section_content)} characters")
        print(f"Number of condition blocks: {section_content.count('{{#')}")
    else:
        print("Chronic inflammation section not found")

if __name__ == "__main__":
    test_extended_inflammation_conditions() 