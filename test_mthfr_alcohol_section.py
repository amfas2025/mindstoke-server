#!/usr/bin/env python3

"""
Test script to verify MTHFR alcohol recommendation section
Tests the quick-stopETOH content control functionality
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

def test_mthfr_alcohol_section():
    """Test the MTHFR alcohol recommendation section"""
    print("=== Testing MTHFR Alcohol Recommendation Section ===\n")
    
    generator = RoadmapGenerator()
    
    # Test case 1: Client with MTHFR variants (should show alcohol recommendation)
    print("1. Testing client WITH MTHFR variants:")
    print("   - MTHFR C677T: Heterozygous")
    print("   - MTHFR A1298C: Not Detected")
    print("   - Expected: quick-stopETOH should be True\n")
    
    client_data = {
        'name': 'Test Client',
        'gender': 'male'
    }
    
    lab_results_with_mthfr = {
        'MTHFR_1': 'Heterozygous',  # C677T variant present
        'MTHFR_2': 'Not Detected',  # A1298C not present
        'METAB_GLUT': 250
    }
    
    hhq_responses = {
        'hh_depression': False,
        'hh_alcohol_consumption': True  # Has alcohol history
    }
    
    # Process content controls
    processed_content = generator._process_all_content_controls(
        client_data, lab_results_with_mthfr, hhq_responses
    )
    
    print("   Content Controls Set:")
    print(f"   - has-MTHFR-variants: {processed_content.get('has-MTHFR-variants', False)}")
    print(f"   - quick-MTHFR1: {processed_content.get('quick-MTHFR1', False)}")
    print(f"   - quick-MTHFR2: {processed_content.get('quick-MTHFR2', False)}")
    print(f"   - quick-stopETOH: {processed_content.get('quick-stopETOH', False)}")
    print(f"   - needs-methyl: {processed_content.get('needs-methyl', False)}")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results_with_mthfr, hhq_responses)
    
    # Check if alcohol recommendation appears
    alcohol_text = "Due to your METHYLATION genetics, you may consider complete abstinence from ALCOHOL"
    if alcohol_text in roadmap:
        print(f"   ✅ MTHFR alcohol recommendation text found in roadmap")
    else:
        print(f"   ❌ MTHFR alcohol recommendation text NOT found in roadmap")
    
    # Extract and show MTHFR section
    mthfr_start = roadmap.find("## **MTHFR Genetics & Methylation Support**")
    if mthfr_start != -1:
        mthfr_end = roadmap.find("---", mthfr_start)
        if mthfr_end != -1:
            mthfr_section = roadmap[mthfr_start:mthfr_end].strip()
            print(f"\n   Generated MTHFR Section:")
            print(f"   {'-' * 50}")
            print(f"   {mthfr_section}")
            print(f"   {'-' * 50}")
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Client without MTHFR variants (should NOT show alcohol recommendation)
    print("2. Testing client WITHOUT MTHFR variants:")
    print("   - MTHFR C677T: Not Detected")
    print("   - MTHFR A1298C: Not Detected")
    print("   - Expected: quick-stopETOH should be False\n")
    
    lab_results_no_mthfr = {
        'MTHFR_1': 'Not Detected',
        'MTHFR_2': 'Not Detected',
        'METAB_GLUT': 250
    }
    
    # Process content controls
    processed_content_no_mthfr = generator._process_all_content_controls(
        client_data, lab_results_no_mthfr, hhq_responses
    )
    
    print("   Content Controls Set:")
    print(f"   - has-MTHFR-variants: {processed_content_no_mthfr.get('has-MTHFR-variants', False)}")
    print(f"   - quick-MTHFR1: {processed_content_no_mthfr.get('quick-MTHFR1', False)}")
    print(f"   - quick-MTHFR2: {processed_content_no_mthfr.get('quick-MTHFR2', False)}")
    print(f"   - quick-stopETOH: {processed_content_no_mthfr.get('quick-stopETOH', False)}")
    print(f"   - needs-methyl: {processed_content_no_mthfr.get('needs-methyl', False)}")
    
    # Generate roadmap for no MTHFR variants
    roadmap_no_mthfr = generator.generate_roadmap(client_data, lab_results_no_mthfr, hhq_responses)
    
    # Check that alcohol recommendation does NOT appear
    if alcohol_text in roadmap_no_mthfr:
        print(f"   ❌ MTHFR alcohol recommendation text found (should not be present)")
    else:
        print(f"   ✅ MTHFR alcohol recommendation text correctly absent")
    
    # Extract and show MTHFR section for no variants case
    mthfr_start_no = roadmap_no_mthfr.find("## **MTHFR Genetics & Methylation Support**")
    if mthfr_start_no != -1:
        mthfr_end_no = roadmap_no_mthfr.find("---", mthfr_start_no)
        if mthfr_end_no != -1:
            mthfr_section_no = roadmap_no_mthfr[mthfr_start_no:mthfr_end_no].strip()
            print(f"\n   Generated MTHFR Section (No Variants):")
            print(f"   {'-' * 50}")
            print(f"   {mthfr_section_no}")
            print(f"   {'-' * 50}")
    
    print("\n" + "="*60 + "\n")
    
    # Test case 3: Both MTHFR variants present
    print("3. Testing client WITH BOTH MTHFR variants:")
    print("   - MTHFR C677T: Heterozygous")
    print("   - MTHFR A1298C: Homozygous")
    print("   - Expected: All MTHFR sections including alcohol recommendation\n")
    
    lab_results_both_mthfr = {
        'MTHFR_1': 'Heterozygous',
        'MTHFR_2': 'Homozygous',
        'METAB_GLUT': 250
    }
    
    # Process content controls
    processed_content_both = generator._process_all_content_controls(
        client_data, lab_results_both_mthfr, hhq_responses
    )
    
    print("   Content Controls Set:")
    print(f"   - has-MTHFR-variants: {processed_content_both.get('has-MTHFR-variants', False)}")
    print(f"   - quick-MTHFR1: {processed_content_both.get('quick-MTHFR1', False)}")
    print(f"   - quick-MTHFR2: {processed_content_both.get('quick-MTHFR2', False)}")
    print(f"   - quick-stopETOH: {processed_content_both.get('quick-stopETOH', False)}")
    print(f"   - needs-methyl: {processed_content_both.get('needs-methyl', False)}")
    
    # Generate roadmap for both variants
    roadmap_both = generator.generate_roadmap(client_data, lab_results_both_mthfr, hhq_responses)
    
    # Check for alcohol recommendation
    if alcohol_text in roadmap_both:
        print(f"   ✅ MTHFR alcohol recommendation text found")
    else:
        print(f"   ❌ MTHFR alcohol recommendation text NOT found")
    
    # Count how many individual MTHFR sections appear
    c677t_individual = "The C677T allele is a variant suggestive of methylation challenges" in roadmap_both
    a1298c_individual = "The A1298C allele is a variant suggestive of methylation challenges" in roadmap_both
    
    print(f"   - Individual C677T section present: {c677t_individual}")
    print(f"   - Individual A1298C section present: {a1298c_individual}")
    
    print("\n=== MTHFR Alcohol Section Test Complete ===")

if __name__ == "__main__":
    test_mthfr_alcohol_section() 