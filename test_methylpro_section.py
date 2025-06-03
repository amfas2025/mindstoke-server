#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_methylpro_section():
    """Test the methylated B complex supplement recommendation section"""
    
    print("🧪 Testing Methylated B Complex Supplement Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with MTHFR variants and depression
    print("\n📋 Test Case 1: MTHFR variants + Depression History")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'MTHFR_1': 'C677T Heterozygous',  # Has MTHFR variant
        'MTHFR_2': 'A1298C Heterozygous',  # Has MTHFR variant
        'INFLAM_HOMOCYS': 8.5,
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses_1 = {
        'hh_depression': True  # Has depression history
    }
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for methylpro content
    methylpro_content = "Consider starting methylated B complex supplement" in roadmap_1
    super_methyl_content = "SUPER METHYL-SP from Apex Energetics" in roadmap_1
    methylpro_option = "METHYLPRO; B-COMPLEX + 5 mg L-METHYLFOLATE" in roadmap_1
    depression_content = "This recommendation is offered considering your history of depression" in roadmap_1
    replacement_content = "in place of your current B-COMPLEX supplement" in roadmap_1
    
    print(f"✅ Methylpro section appears: {methylpro_content}")
    print(f"✅ SUPER METHYL-SP mentioned: {super_methyl_content}")
    print(f"✅ METHYLPRO option mentioned: {methylpro_option}")
    print(f"✅ Depression-specific text appears: {depression_content}")
    print(f"✅ B-complex replacement text appears: {replacement_content}")
    
    # Test Case 2: Client with MTHFR variants but no depression
    print("\n📋 Test Case 2: MTHFR variants without Depression")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'MTHFR_1': 'C677T Heterozygous',  # Has MTHFR variant
        'MTHFR_2': 'Not Detected',  # No A1298C variant
        'INFLAM_HOMOCYS': 6.5,
        'VIT_B12': 800,
        'VIT_FOLATE': 18
    }
    
    hhq_responses_2 = {
        'hh_depression': False  # No depression history
    }
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for methylpro content
    methylpro_content_2 = "Consider starting methylated B complex supplement" in roadmap_2
    depression_content_2 = "This recommendation is offered considering your history of depression" in roadmap_2
    replacement_content_2 = "in place of your current B-COMPLEX supplement" in roadmap_2
    
    print(f"✅ Methylpro section appears: {methylpro_content_2}")
    print(f"❌ Depression-specific text should NOT appear: {not depression_content_2}")
    print(f"✅ B-complex replacement text appears: {replacement_content_2}")
    
    # Test Case 3: Client with no MTHFR variants
    print("\n📋 Test Case 3: No MTHFR variants")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'MTHFR_1': 'Not Detected',  # No MTHFR variant
        'MTHFR_2': 'Not Detected',  # No MTHFR variant
        'INFLAM_HOMOCYS': 6.0,
        'VIT_B12': 900,
        'VIT_FOLATE': 20
    }
    
    hhq_responses_3 = {
        'hh_depression': False
    }
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check that methylpro content does NOT appear
    methylpro_content_3 = "Consider starting methylated B complex supplement" in roadmap_3
    super_methyl_content_3 = "SUPER METHYL-SP from Apex Energetics" in roadmap_3
    replacement_content_3 = "in place of your current B-COMPLEX supplement" in roadmap_3
    
    print(f"❌ Methylpro section should NOT appear: {not methylpro_content_3}")
    print(f"❌ SUPER METHYL-SP should NOT appear: {not super_methyl_content_3}")
    print(f"❌ B-complex replacement should NOT appear: {not replacement_content_3}")
    
    # Test Case 4: Depression history but no MTHFR variants
    print("\n📋 Test Case 4: Depression without MTHFR variants")
    print("-" * 50)
    
    client_data_4 = {
        'full_name': 'Test Patient Four',
        'date_of_birth': '1985-01-01',
        'email': 'test4@example.com'
    }
    
    lab_results_4 = {
        'MTHFR_1': 'Not Detected',  # No MTHFR variant
        'MTHFR_2': 'Not Detected',  # No MTHFR variant
        'INFLAM_HOMOCYS': 9.0,
        'VIT_B12': 350,
        'VIT_FOLATE': 10
    }
    
    hhq_responses_4 = {
        'hh_depression': True  # Has depression but no MTHFR
    }
    
    # Generate roadmap
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    # Check that methylpro content does NOT appear (should only trigger with MTHFR)
    # But depression-specific content should appear
    methylpro_content_4 = "Consider starting methylated B complex supplement" in roadmap_4
    depression_content_4 = "This recommendation is offered considering your history of depression" in roadmap_4
    
    print(f"❌ Methylpro section should NOT appear without MTHFR: {not methylpro_content_4}")
    print(f"❌ Depression-specific text should NOT appear without MTHFR: {not depression_content_4}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        methylpro_content and super_methyl_content and depression_content and  # Test 1
        methylpro_content_2 and not depression_content_2 and  # Test 2
        not methylpro_content_3 and not super_methyl_content_3 and  # Test 3
        not methylpro_content_4 and not depression_content_4  # Test 4
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Methylated B complex section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_methylpro_section() 