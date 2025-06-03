#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_creatine_section():
    """Test the CREATINE MONOHYDRATE supplement recommendation section"""
    
    print("🧪 Testing CREATINE MONOHYDRATE Supplement Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with homocysteine > 15 (should show BOTH TRIMETHYLGLYCINE and CREATINE)
    print("\n📋 Test Case 1: Homocysteine > 15 (should show BOTH supplements)")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'INFLAM_HOMOCYS': 18.0,  # High homocysteine > 15
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses_1 = {}
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for both supplements
    trimethyl_content = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_1
    creatine_content = "Consider starting a supplement called CREATINE MONOHYDRATE" in roadmap_1
    creatine_dose = "The standard dose is 5 grams per day" in roadmap_1
    creatine_trigger = "when HOMOCYSTEINE levels are > 15" in roadmap_1
    energy_support = "help improve energy levels and help to support HOMOCYSTEINE recycling" in roadmap_1
    
    print(f"✅ TRIMETHYLGLYCINE appears (>12): {trimethyl_content}")
    print(f"✅ CREATINE MONOHYDRATE appears (>15): {creatine_content}")
    print(f"✅ Creatine dose mentioned: {creatine_dose}")
    print(f"✅ Creatine trigger mentioned: {creatine_trigger}")
    print(f"✅ Energy/recycling benefits mentioned: {energy_support}")
    
    # Test Case 2: Client with homocysteine = 13 (should show TRIMETHYLGLYCINE only)
    print("\n📋 Test Case 2: Homocysteine = 13 (TRIMETHYLGLYCINE only)")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'INFLAM_HOMOCYS': 13.0,  # > 12 but not > 15
        'VIT_B12': 600,
        'VIT_FOLATE': 15
    }
    
    hhq_responses_2 = {}
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for supplements
    trimethyl_content_2 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_2
    creatine_content_2 = "Consider starting a supplement called CREATINE MONOHYDRATE" in roadmap_2
    
    print(f"✅ TRIMETHYLGLYCINE appears (13 > 12): {trimethyl_content_2}")
    print(f"❌ CREATINE should NOT appear (13 not > 15): {not creatine_content_2}")
    
    # Test Case 3: Client with homocysteine = 15 exactly (should show TRIMETHYLGLYCINE only)
    print("\n📋 Test Case 3: Homocysteine = 15 exactly (TRIMETHYLGLYCINE only)")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'INFLAM_HOMOCYS': 15.0,  # Exactly 15 (not > 15)
        'VIT_B12': 700,
        'VIT_FOLATE': 18
    }
    
    hhq_responses_3 = {}
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check for supplements
    trimethyl_content_3 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_3
    creatine_content_3 = "Consider starting a supplement called CREATINE MONOHYDRATE" in roadmap_3
    
    print(f"✅ TRIMETHYLGLYCINE appears (15 > 12): {trimethyl_content_3}")
    print(f"❌ CREATINE should NOT appear (15 is not > 15): {not creatine_content_3}")
    
    # Test Case 4: Client with homocysteine = 15.1 (should show BOTH)
    print("\n📋 Test Case 4: Homocysteine = 15.1 (should show BOTH)")
    print("-" * 50)
    
    client_data_4 = {
        'full_name': 'Test Patient Four',
        'date_of_birth': '1985-01-01',
        'email': 'test4@example.com'
    }
    
    lab_results_4 = {
        'INFLAM_HOMOCYS': 15.1,  # Just above 15
        'VIT_B12': 800,
        'VIT_FOLATE': 20
    }
    
    hhq_responses_4 = {}
    
    # Generate roadmap
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    # Check for both supplements
    trimethyl_content_4 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_4
    creatine_content_4 = "Consider starting a supplement called CREATINE MONOHYDRATE" in roadmap_4
    
    print(f"✅ TRIMETHYLGLYCINE appears (15.1 > 12): {trimethyl_content_4}")
    print(f"✅ CREATINE appears (15.1 > 15): {creatine_content_4}")
    
    # Test Case 5: Low homocysteine (should show neither)
    print("\n📋 Test Case 5: Homocysteine = 6 (should show neither)")
    print("-" * 50)
    
    client_data_5 = {
        'full_name': 'Test Patient Five',
        'date_of_birth': '1982-01-01',
        'email': 'test5@example.com'
    }
    
    lab_results_5 = {
        'INFLAM_HOMOCYS': 6.0,  # Low homocysteine
        'VIT_B12': 500,
        'VIT_FOLATE': 13
    }
    
    hhq_responses_5 = {}
    
    # Generate roadmap
    roadmap_5 = generator.generate_roadmap(client_data_5, lab_results_5, hhq_responses_5)
    
    # Check that neither appears
    trimethyl_content_5 = "Consider starting TRIMETHYLGLYCINE 1000 mg/day" in roadmap_5
    creatine_content_5 = "Consider starting a supplement called CREATINE MONOHYDRATE" in roadmap_5
    homocysteine_section_5 = "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap_5
    
    print(f"❌ Homocysteine section should NOT appear: {not homocysteine_section_5}")
    print(f"❌ TRIMETHYLGLYCINE should NOT appear: {not trimethyl_content_5}")
    print(f"❌ CREATINE should NOT appear: {not creatine_content_5}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        # Test 1: > 15 shows both
        trimethyl_content and creatine_content and creatine_dose and
        # Test 2: 13 shows trimethyl only  
        trimethyl_content_2 and not creatine_content_2 and
        # Test 3: 15 shows trimethyl only
        trimethyl_content_3 and not creatine_content_3 and
        # Test 4: 15.1 shows both
        trimethyl_content_4 and creatine_content_4 and
        # Test 5: 6 shows neither
        not trimethyl_content_5 and not creatine_content_5 and not homocysteine_section_5
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! CREATINE section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_creatine_section() 