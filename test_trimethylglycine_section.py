#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_trimethylglycine_section():
    """Test the TRIMETHYLGLYCINE supplement recommendation section"""
    
    print("🧪 Testing TRIMETHYLGLYCINE Supplement Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with homocysteine > 12 (should show TRIMETHYLGLYCINE)
    print("\n📋 Test Case 1: Homocysteine > 12 (should show TRIMETHYLGLYCINE)")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'INFLAM_HOMOCYS': 15.0,  # High homocysteine > 12
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses_1 = {}
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for TRIMETHYLGLYCINE content
    trimethyl_content = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_1
    methyl_b_complex_ref = "methylated B complex when HOMOCYSTEINE levels are > 12" in roadmap_1
    homocysteine_section = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_1
    
    print(f"✅ Homocysteine section appears: {homocysteine_section}")
    print(f"✅ TRIMETHYLGLYCINE recommendation appears: {trimethyl_content}")
    print(f"✅ Methylated B complex reference appears: {methyl_b_complex_ref}")
    
    # Test Case 2: Client with homocysteine = 12 exactly (should show TRIMETHYLGLYCINE)
    print("\n📋 Test Case 2: Homocysteine = 12 exactly (should NOT show)")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'INFLAM_HOMOCYS': 12.0,  # Exactly 12 (should NOT trigger > 12)
        'VIT_B12': 600,
        'VIT_FOLATE': 15
    }
    
    hhq_responses_2 = {}
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for TRIMETHYLGLYCINE content
    trimethyl_content_2 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_2
    homocysteine_section_2 = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_2
    
    print(f"✅ Homocysteine section appears: {homocysteine_section_2}")
    print(f"❌ TRIMETHYLGLYCINE should NOT appear (12 is not > 12): {not trimethyl_content_2}")
    
    # Test Case 3: Client with homocysteine = 12.1 (should show TRIMETHYLGLYCINE)
    print("\n📋 Test Case 3: Homocysteine = 12.1 (should show TRIMETHYLGLYCINE)")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'INFLAM_HOMOCYS': 12.1,  # Just above 12
        'VIT_B12': 700,
        'VIT_FOLATE': 18
    }
    
    hhq_responses_3 = {}
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check for TRIMETHYLGLYCINE content
    trimethyl_content_3 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_3
    homocysteine_section_3 = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_3
    
    print(f"✅ Homocysteine section appears: {homocysteine_section_3}")
    print(f"✅ TRIMETHYLGLYCINE recommendation appears: {trimethyl_content_3}")
    
    # Test Case 4: Client with low homocysteine (should NOT show TRIMETHYLGLYCINE)
    print("\n📋 Test Case 4: Low Homocysteine < 7 (should NOT show)")
    print("-" * 50)
    
    client_data_4 = {
        'full_name': 'Test Patient Four',
        'date_of_birth': '1985-01-01',
        'email': 'test4@example.com'
    }
    
    lab_results_4 = {
        'INFLAM_HOMOCYS': 6.0,  # Low homocysteine
        'VIT_B12': 800,
        'VIT_FOLATE': 20
    }
    
    hhq_responses_4 = {}
    
    # Generate roadmap
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    # Check that homocysteine section does NOT appear
    trimethyl_content_4 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_4
    homocysteine_section_4 = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_4
    
    print(f"❌ Homocysteine section should NOT appear: {not homocysteine_section_4}")
    print(f"❌ TRIMETHYLGLYCINE should NOT appear: {not trimethyl_content_4}")
    
    # Test Case 5: Homocysteine at 8 (shows section but no TRIMETHYLGLYCINE)
    print("\n📋 Test Case 5: Homocysteine = 8 (shows section, no TRIMETHYLGLYCINE)")
    print("-" * 50)
    
    client_data_5 = {
        'full_name': 'Test Patient Five',
        'date_of_birth': '1982-01-01',
        'email': 'test5@example.com'
    }
    
    lab_results_5 = {
        'INFLAM_HOMOCYS': 8.0,  # Elevated but not > 12
        'VIT_B12': 500,
        'VIT_FOLATE': 13
    }
    
    hhq_responses_5 = {}
    
    # Generate roadmap
    roadmap_5 = generator.generate_roadmap(client_data_5, lab_results_5, hhq_responses_5)
    
    # Check for sections
    trimethyl_content_5 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_5
    homocysteine_section_5 = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_5
    
    print(f"✅ Homocysteine section appears (8 > 7): {homocysteine_section_5}")
    print(f"❌ TRIMETHYLGLYCINE should NOT appear (8 not > 12): {not trimethyl_content_5}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        trimethyl_content and methyl_b_complex_ref and  # Test 1: > 12 shows
        not trimethyl_content_2 and homocysteine_section_2 and  # Test 2: = 12 doesn't show
        trimethyl_content_3 and  # Test 3: 12.1 shows  
        not trimethyl_content_4 and not homocysteine_section_4 and  # Test 4: < 7 doesn't show
        not trimethyl_content_5 and homocysteine_section_5  # Test 5: 8 shows section, no trimethyl
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! TRIMETHYLGLYCINE section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_trimethylglycine_section() 