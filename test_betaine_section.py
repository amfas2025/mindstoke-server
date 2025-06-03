#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_betaine_section():
    """Test the BETAINE HCL supplement recommendation section for bariatric surgery"""
    
    print("🧪 Testing BETAINE HCL Supplement Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with bariatric surgery history (should show BETAINE HCL)
    print("\n📋 Test Case 1: Bariatric Surgery History (should show BETAINE HCL)")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'VIT_B12': 450,
        'VIT_FOLATE': 12
    }
    
    hhq_responses_1 = {
        'hh_bariatric_surgery': True
    }
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for BETAINE HCL content
    betaine_content = "Consider taking a BETAINE HCL supplement with your meals" in roadmap_1
    b_complex_mention = "particularly when you take a B-COMPLEX supplement" in roadmap_1
    hcl_impact = "may have reduced your ability to make HCL" in roadmap_1
    digestive_symptoms = "can lead to acid reflux, poor digestion, bloating, etc." in roadmap_1
    b_vitamin_absorption = "negatively impact your ability to absorb essential B vitamins" in roadmap_1
    bariatric_section = "**Bariatric Surgery Support:**" in roadmap_1
    
    print(f"✅ BETAINE HCL recommendation appears: {betaine_content}")
    print(f"✅ B-COMPLEX mention appears: {b_complex_mention}")
    print(f"✅ HCL production impact mentioned: {hcl_impact}")
    print(f"✅ Digestive symptoms mentioned: {digestive_symptoms}")
    print(f"✅ B vitamin absorption mentioned: {b_vitamin_absorption}")
    print(f"✅ Bariatric Surgery section title appears: {bariatric_section}")
    
    # Test Case 2: Client WITHOUT bariatric surgery history (should NOT show BETAINE HCL)
    print("\n📋 Test Case 2: No Bariatric Surgery History (should NOT show BETAINE HCL)")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'VIT_B12': 600,
        'VIT_FOLATE': 15
    }
    
    hhq_responses_2 = {}  # No bariatric surgery
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check that BETAINE HCL content does NOT appear
    betaine_content_2 = "Consider taking a BETAINE HCL supplement with your meals" in roadmap_2
    bariatric_section_2 = "**Bariatric Surgery Support:**" in roadmap_2
    
    print(f"❌ BETAINE HCL should NOT appear: {not betaine_content_2}")
    print(f"❌ Bariatric Surgery section should NOT appear: {not bariatric_section_2}")
    
    # Test Case 3: Client with false bariatric surgery flag (should NOT show BETAINE HCL)
    print("\n📋 Test Case 3: Bariatric Surgery = False (should NOT show BETAINE HCL)")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'VIT_B12': 700,
        'VIT_FOLATE': 18
    }
    
    hhq_responses_3 = {
        'hh_bariatric_surgery': False  # Explicitly false
    }
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check that BETAINE HCL content does NOT appear
    betaine_content_3 = "Consider taking a BETAINE HCL supplement with your meals" in roadmap_3
    bariatric_section_3 = "**Bariatric Surgery Support:**" in roadmap_3
    
    print(f"❌ BETAINE HCL should NOT appear (false): {not betaine_content_3}")
    print(f"❌ Bariatric Surgery section should NOT appear (false): {not bariatric_section_3}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        # Test 1: Bariatric surgery shows BETAINE HCL
        betaine_content and b_complex_mention and hcl_impact and 
        digestive_symptoms and b_vitamin_absorption and bariatric_section and
        # Test 2: No bariatric surgery shows nothing
        not betaine_content_2 and not bariatric_section_2 and
        # Test 3: False bariatric surgery shows nothing
        not betaine_content_3 and not bariatric_section_3
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! BETAINE HCL section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_betaine_section() 