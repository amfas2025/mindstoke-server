#!/usr/bin/env python3

import sys
import os
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vitamin_d_simple():
    """Test the simple vitamin D baseline section"""
    
    print("🧪 Testing Simple Vitamin D Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Client with vitamin D = 45 ng/mL
    print("\n📋 Test Case 1: Vitamin D = 45 ng/mL")
    print("-" * 50)
    
    client_data_1 = {
        'full_name': 'Test Patient One',
        'date_of_birth': '1980-01-01',
        'email': 'test1@example.com'
    }
    
    lab_results_1 = {
        'VIT_D25': 45.0
    }
    
    hhq_responses_1 = {}
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for simple vitamin D content
    baseline_text = "Your baseline Vitamin D level is" in roadmap_1
    value_display = "45.0 ng/mL" in roadmap_1
    optimal_range = "The optimal level is suggested to be 60-80 ng/mL" in roadmap_1
    
    print(f"✅ Baseline text appears: {baseline_text}")
    print(f"✅ Value displayed correctly: {value_display}")
    print(f"✅ Optimal range mentioned: {optimal_range}")
    
    # Test Case 2: Client with vitamin D = 72 ng/mL (in optimal range)
    print("\n📋 Test Case 2: Vitamin D = 72 ng/mL (optimal)")
    print("-" * 50)
    
    client_data_2 = {
        'full_name': 'Test Patient Two',
        'date_of_birth': '1975-01-01',
        'email': 'test2@example.com'
    }
    
    lab_results_2 = {
        'VIT_D25': 72.0
    }
    
    hhq_responses_2 = {}
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for simple vitamin D content
    baseline_text_2 = "Your baseline Vitamin D level is" in roadmap_2
    value_display_2 = "72.0 ng/mL" in roadmap_2
    optimal_range_2 = "The optimal level is suggested to be 60-80 ng/mL" in roadmap_2
    
    print(f"✅ Baseline text appears: {baseline_text_2}")
    print(f"✅ Value displayed correctly: {value_display_2}")
    print(f"✅ Optimal range mentioned: {optimal_range_2}")
    
    # Test Case 3: Client with vitamin D = 25 ng/mL (deficient)
    print("\n📋 Test Case 3: Vitamin D = 25 ng/mL (deficient)")
    print("-" * 50)
    
    client_data_3 = {
        'full_name': 'Test Patient Three',
        'date_of_birth': '1990-01-01',
        'email': 'test3@example.com'
    }
    
    lab_results_3 = {
        'VIT_D25': 25.0
    }
    
    hhq_responses_3 = {}
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data_3, lab_results_3, hhq_responses_3)
    
    # Check for simple vitamin D content
    baseline_text_3 = "Your baseline Vitamin D level is" in roadmap_3
    value_display_3 = "25.0 ng/mL" in roadmap_3
    optimal_range_3 = "The optimal level is suggested to be 60-80 ng/mL" in roadmap_3
    
    print(f"✅ Baseline text appears: {baseline_text_3}")
    print(f"✅ Value displayed correctly: {value_display_3}")
    print(f"✅ Optimal range mentioned: {optimal_range_3}")
    
    # Test Case 4: Client with NO vitamin D data (should NOT show simple section)
    print("\n📋 Test Case 4: No Vitamin D Data (should NOT show)")
    print("-" * 50)
    
    client_data_4 = {
        'full_name': 'Test Patient Four',
        'date_of_birth': '1985-01-01',
        'email': 'test4@example.com'
    }
    
    lab_results_4 = {}  # No vitamin D data
    
    hhq_responses_4 = {}
    
    # Generate roadmap
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    # Check that simple vitamin D content does NOT appear
    baseline_text_4 = "Your baseline Vitamin D level is" in roadmap_4
    
    print(f"❌ Simple Vitamin D section should NOT appear: {not baseline_text_4}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    all_tests_passed = (
        # Test 1: 45 ng/mL shows all elements
        baseline_text and value_display and optimal_range and
        # Test 2: 72 ng/mL shows all elements  
        baseline_text_2 and value_display_2 and optimal_range_2 and
        # Test 3: 25 ng/mL shows all elements
        baseline_text_3 and value_display_3 and optimal_range_3 and
        # Test 4: No data shows nothing
        not baseline_text_4
    )
    
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Simple Vitamin D section working correctly!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_vitamin_d_simple() 