#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vitamin_d_55_59():
    """Test the D-55-59 vitamin D section"""
    
    print("🧪 Testing D-55-59 Vitamin D Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with vitamin D = 57 ng/mL (in 55-59 range)
    print("\n📋 Test Case 1: Vitamin D = 57 ng/mL (55-59 range)")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'VIT_D25': 57.0
    }
    
    hhq_responses_1 = {}
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for D-55-59 content
    close_to_optimal = "falls very close to the optimal parameters" in roadmap_1
    no_intervention = "no additional intervention is recommended" in roadmap_1
    continue_supplement = "encouraged to continue your current VITAMIN D supplement" in roadmap_1
    
    print(f"✅ 'Close to optimal' text appears: {close_to_optimal}")
    print(f"✅ 'No intervention' text appears: {no_intervention}")
    print(f"✅ 'Continue supplement' text appears: {continue_supplement}")
    
    # Test Case 2: Client with vitamin D = 56 ng/mL (boundary test)
    print("\n📋 Test Case 2: Vitamin D = 56 ng/mL (boundary)")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'VIT_D25': 56.0
    }
    
    hhq_responses_2 = {}
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for D-55-59 content
    close_to_optimal_2 = "falls very close to the optimal parameters" in roadmap_2
    no_intervention_2 = "no additional intervention is recommended" in roadmap_2
    continue_supplement_2 = "encouraged to continue your current VITAMIN D supplement" in roadmap_2
    
    print(f"✅ 'Close to optimal' text appears: {close_to_optimal_2}")
    print(f"✅ 'No intervention' text appears: {no_intervention_2}")
    print(f"✅ 'Continue supplement' text appears: {continue_supplement_2}")
    
    # Test Case 3: Client with vitamin D = 59 ng/mL (upper boundary)
    print("\n📋 Test Case 3: Vitamin D = 59 ng/mL (upper boundary)")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'VIT_D25': 59.0
    }
    
    hhq_responses_3 = {}
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check for D-55-59 content
    close_to_optimal_3 = "falls very close to the optimal parameters" in roadmap_3
    no_intervention_3 = "no additional intervention is recommended" in roadmap_3
    continue_supplement_3 = "encouraged to continue your current VITAMIN D supplement" in roadmap_3
    
    print(f"✅ 'Close to optimal' text appears: {close_to_optimal_3}")
    print(f"✅ 'No intervention' text appears: {no_intervention_3}")
    print(f"✅ 'Continue supplement' text appears: {continue_supplement_3}")
    
    # Test Case 4: Client with vitamin D = 55 ng/mL (should NOT show D-55-59, should show D-50-55)
    print("\n📋 Test Case 4: Vitamin D = 55 ng/mL (should show D-50-55, NOT D-55-59)")
    print("-" * 50)
    
    client_data_4 = {
        'full_name': 'Test Patient Four',
        'date_of_birth': '1985-01-01',
        'email': 'test4@example.com'
    }
    
    lab_results_4 = {
        'VIT_D25': 55.0
    }
    
    hhq_responses_4 = {}
    
    # Generate roadmap
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    # Check that D-55-59 content does NOT appear but D-50-55 does
    close_to_optimal_4 = "falls very close to the optimal parameters" in roadmap_4
    d_50_55_text = "This level is close to the optimal parameters" in roadmap_4
    
    print(f"❌ D-55-59 section should NOT appear: {not close_to_optimal_4}")
    print(f"✅ D-50-55 section should appear: {d_50_55_text}")
    
    # Test Case 5: Client with vitamin D = 60 ng/mL (should show D-optimal, NOT D-55-59)
    print("\n📋 Test Case 5: Vitamin D = 60 ng/mL (should show D-optimal, NOT D-55-59)")
    print("-" * 50)
    
    client_data_5 = {
        'full_name': 'Test Patient Five',
        'date_of_birth': '1985-01-01',
        'email': 'test5@example.com'
    }
    
    lab_results_5 = {
        'VIT_D25': 60.0
    }
    
    hhq_responses_5 = {}
    
    # Generate roadmap
    roadmap_5 = generator.generate_roadmap(client_data_5, lab_results_5, hhq_responses_5)
    
    # Check that D-55-59 content does NOT appear 
    close_to_optimal_5 = "falls very close to the optimal parameters" in roadmap_5
    
    print(f"❌ D-55-59 section should NOT appear: {not close_to_optimal_5}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        # Test 1: 57 ng/mL shows D-55-59 section
        close_to_optimal and no_intervention and continue_supplement and
        # Test 2: 56 ng/mL shows D-55-59 section  
        close_to_optimal_2 and no_intervention_2 and continue_supplement_2 and
        # Test 3: 59 ng/mL shows D-55-59 section
        close_to_optimal_3 and no_intervention_3 and continue_supplement_3 and
        # Test 4: 55 ng/mL shows D-50-55, not D-55-59
        not close_to_optimal_4 and d_50_55_text and
        # Test 5: 60 ng/mL does not show D-55-59
        not close_to_optimal_5
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! D-55-59 section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_vitamin_d_55_59() 