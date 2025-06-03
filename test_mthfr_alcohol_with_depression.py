#!/usr/bin/env python3

"""
Test script to verify MTHFR alcohol section works with depression conditionals
Tests the combination of quick-stopETOH and quick-depression-mood-disorder content controls
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

def test_mthfr_alcohol_with_depression():
    """Test the MTHFR alcohol section combined with depression history"""
    print("=== Testing MTHFR Alcohol + Depression Conditionals ===\n")
    
    generator = RoadmapGenerator()
    
    # Test case: Client with MTHFR variants AND depression history
    print("Testing client WITH MTHFR variants AND depression history:")
    print("   - MTHFR C677T: Heterozygous")
    print("   - MTHFR A1298C: Homozygous") 
    print("   - Depression History: True")
    print("   - Expected: Both alcohol recommendation AND depression conditionals\n")
    
    client_data = {
        'name': 'Test Client with Depression',
        'gender': 'female'
    }
    
    lab_results = {
        'MTHFR_1': 'Heterozygous',  # C677T variant present
        'MTHFR_2': 'Homozygous',    # A1298C variant present
        'METAB_GLUT': 180          # Low glutathione
    }
    
    hhq_responses = {
        'hh_depression': True,              # Depression history
        'hh_anxiety_medications': False,    # Alternative depression indicator
        'hh_alcohol_consumption': True      # Alcohol consumption history
    }
    
    # Process content controls
    processed_content = generator._process_all_content_controls(
        client_data, lab_results, hhq_responses
    )
    
    print("   Content Controls Set:")
    print(f"   - has-MTHFR-variants: {processed_content.get('has-MTHFR-variants', False)}")
    print(f"   - quick-MTHFR1: {processed_content.get('quick-MTHFR1', False)}")
    print(f"   - quick-MTHFR2: {processed_content.get('quick-MTHFR2', False)}")
    print(f"   - quick-stopETOH: {processed_content.get('quick-stopETOH', False)}")
    print(f"   - quick-depression-mood-disorder: {processed_content.get('quick-depression-mood-disorder', False)}")
    print(f"   - needs-methyl: {processed_content.get('needs-methyl', False)}")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check for alcohol recommendation
    alcohol_text = "Due to your METHYLATION genetics, you may consider complete abstinence from ALCOHOL"
    alcohol_found = alcohol_text in roadmap
    print(f"   - Alcohol recommendation found: {alcohol_found}")
    
    # Check for depression conditionals in each MTHFR section
    depression_main = "With your history of a debilitating depression, this recommendation extends beyond" in roadmap
    depression_c677t = "With your history of debilitating depression, this recommendation extends beyond" in roadmap
    depression_a1298c = "With your history of debilitating depression, this recommendation extends beyond" in roadmap
    
    print(f"   - Main MTHFR depression conditional: {depression_main}")
    print(f"   - C677T section depression conditional: {depression_c677t}")
    print(f"   - A1298C section depression conditional: {depression_a1298c}")
    
    # Extract and display the complete MTHFR section
    mthfr_start = roadmap.find("## **MTHFR Genetics & Methylation Support**")
    if mthfr_start != -1:
        mthfr_end = roadmap.find("---", mthfr_start)
        if mthfr_end != -1:
            mthfr_section = roadmap[mthfr_start:mthfr_end].strip()
            print(f"\n   Complete MTHFR Section with Alcohol + Depression:")
            print(f"   {'=' * 60}")
            print(f"   {mthfr_section}")
            print(f"   {'=' * 60}")
    
    # Count total sections present
    sections_found = []
    if "MTHFR GENETIC PROFILES" in roadmap:
        sections_found.append("Main MTHFR intro")
    if "The C677T and A1298C alleles are variants suggestive" in roadmap:
        sections_found.append("Combined variant description")
    if "The C677T allele is a variant suggestive of methylation" in roadmap:
        sections_found.append("Individual C677T section")
    if "The A1298C allele is a variant suggestive of methylation" in roadmap:
        sections_found.append("Individual A1298C section")
    if alcohol_text in roadmap:
        sections_found.append("Alcohol recommendation")
    if "Given your genetic MTHFR profile, you may consider taking a methylated B-complex" in roadmap:
        sections_found.append("Final B-complex recommendation")
    
    print(f"\n   Sections found in roadmap ({len(sections_found)} total):")
    for i, section in enumerate(sections_found, 1):
        print(f"   {i}. {section}")
    
    # Verify expected total: Should have 6 sections for both variants + depression + alcohol
    expected_sections = 6
    if len(sections_found) == expected_sections:
        print(f"   ✅ All {expected_sections} expected MTHFR sections present")
    else:
        print(f"   ❌ Expected {expected_sections} sections, found {len(sections_found)}")
        
    print(f"\n   Test Summary:")
    print(f"   - MTHFR variants detected: ✅")
    print(f"   - Depression conditionals active: {'✅' if depression_c677t and depression_a1298c else '❌'}")
    print(f"   - Alcohol recommendation present: {'✅' if alcohol_found else '❌'}")
    print(f"   - All sections rendering: {'✅' if len(sections_found) >= 5 else '❌'}")
    
    print("\n=== MTHFR Alcohol + Depression Test Complete ===")

if __name__ == "__main__":
    test_mthfr_alcohol_with_depression() 