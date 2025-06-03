#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_quick_vitd_row_takingd():
    """Test the quick-VitD-row-takingD vitamin D section for people already taking supplements"""
    
    print("🧪 Testing Quick-VitD-row-takingD Vitamin D Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test Case 1: Person taking vitamin D with level = 45 ng/mL (suboptimal)
    print("\n📋 Test Case 1: Taking Vitamin D, Level = 45 ng/mL (should show takingD section)")
    print("-" * 70)
    
    lab_results_1 = {
        'VIT_D25': 45.0
    }
    
    hhq_responses_1 = {
        'hh_taking_vitamin_d': True  # Person is taking vitamin D
    }
    
    # Get processed content controls
    processed_content_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print("⚙️ Content Controls:")
    print("-" * 20)
    print(f"quick-VitD-row: {processed_content_1.get('quick-VitD-row', 'NOT SET')}")
    print(f"quick-VitD-row-takingD: {processed_content_1.get('quick-VitD-row-takingD', 'NOT SET')}")
    print(f"D-40-49: {processed_content_1.get('D-40-49', 'NOT SET')}")
    
    # Generate roadmap
    roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
    
    # Check for takingD section content
    takingd_header = "In your health history, you indicated that you are taking a VITAMIN D supplement" in roadmap_1
    takingd_suboptimal = "However, your serum levels remain suboptimal" in roadmap_1
    takingd_guidebook = "Please note the section in your Guidebook" in roadmap_1
    takingd_additional = "add an additional" in roadmap_1
    takingd_4000_iu = "4,000 iu/day to your current dosing" in roadmap_1
    
    print(f"\n📋 Quick-VitD-row-takingD Content Check:")
    print("-" * 40)
    print(f"Header text found: {'✅ YES' if takingd_header else '❌ NO'}")
    print(f"Suboptimal text found: {'✅ YES' if takingd_suboptimal else '❌ NO'}")
    print(f"Guidebook reference found: {'✅ YES' if takingd_guidebook else '❌ NO'}")
    print(f"'Add additional' text found: {'✅ YES' if takingd_additional else '❌ NO'}")
    print(f"4,000 iu dosing found: {'✅ YES' if takingd_4000_iu else '❌ NO'}")
    
    # Test Case 2: Person NOT taking vitamin D with level = 45 ng/mL (should show regular section)
    print("\n📋 Test Case 2: NOT taking Vitamin D, Level = 45 ng/mL (should show regular section)")
    print("-" * 70)
    
    lab_results_2 = {
        'VIT_D25': 45.0
    }
    
    hhq_responses_2 = {
        'hh_taking_vitamin_d': False  # Person is NOT taking vitamin D
    }
    
    # Get processed content controls
    processed_content_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print("⚙️ Content Controls:")
    print("-" * 20)
    print(f"quick-VitD-row: {processed_content_2.get('quick-VitD-row', 'NOT SET')}")
    print(f"quick-VitD-row-takingD: {processed_content_2.get('quick-VitD-row-takingD', 'NOT SET')}")
    print(f"D-40-49: {processed_content_2.get('D-40-49', 'NOT SET')}")
    
    # Generate roadmap
    roadmap_2 = generator.generate_roadmap(client_data, lab_results_2, hhq_responses_2)
    
    # Check for regular section content
    regular_header = "Your VITAMIN D level is suboptimal, and supplementation is recommended" in roadmap_2
    regular_encouraged = "you are encouraged to supplement with" in roadmap_2
    regular_4000_iu = "4,000 iu of VITAMIN D3 per day" in roadmap_2
    
    print(f"\n📋 Regular Quick-VitD-row Content Check:")
    print("-" * 40)
    print(f"Regular header found: {'✅ YES' if regular_header else '❌ NO'}")
    print(f"'Encouraged to supplement' found: {'✅ YES' if regular_encouraged else '❌ NO'}")
    print(f"4,000 iu D3 dosing found: {'✅ YES' if regular_4000_iu else '❌ NO'}")
    
    # Test Case 3: Person taking vitamin D with level = 65 ng/mL (optimal - should show neither)
    print("\n📋 Test Case 3: Taking Vitamin D, Level = 65 ng/mL (optimal - should show D-optimal)")
    print("-" * 70)
    
    lab_results_3 = {
        'VIT_D25': 65.0
    }
    
    hhq_responses_3 = {
        'hh_taking_vitamin_d': True  # Person is taking vitamin D
    }
    
    # Get processed content controls
    processed_content_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print("⚙️ Content Controls:")
    print("-" * 20)
    print(f"quick-VitD-row: {processed_content_3.get('quick-VitD-row', 'NOT SET')}")
    print(f"quick-VitD-row-takingD: {processed_content_3.get('quick-VitD-row-takingD', 'NOT SET')}")
    print(f"D-optimal: {processed_content_3.get('D-optimal', 'NOT SET')}")
    
    # Generate roadmap
    roadmap_3 = generator.generate_roadmap(client_data, lab_results_3, hhq_responses_3)
    
    # Check for optimal section content
    optimal_header = "Your VITAMIN D level falls within the optimal parameters" in roadmap_3
    
    print(f"\n📋 D-optimal Content Check:")
    print("-" * 40)
    print(f"Optimal parameters text found: {'✅ YES' if optimal_header else '❌ NO'}")
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    test_1_passed = (
        processed_content_1.get('quick-VitD-row-takingD') == True and
        processed_content_1.get('quick-VitD-row') == False and
        takingd_header and takingd_suboptimal and takingd_4000_iu
    )
    
    test_2_passed = (
        processed_content_2.get('quick-VitD-row') == True and
        processed_content_2.get('quick-VitD-row-takingD') == False and
        regular_header and regular_encouraged and regular_4000_iu
    )
    
    test_3_passed = (
        processed_content_3.get('quick-VitD-row-takingD') == False and
        processed_content_3.get('quick-VitD-row') == False and
        processed_content_3.get('D-optimal') == True and
        optimal_header
    )
    
    print(f"Test 1 (Taking D, suboptimal): {'✅ PASS' if test_1_passed else '❌ FAIL'}")
    print(f"Test 2 (Not taking D, suboptimal): {'✅ PASS' if test_2_passed else '❌ FAIL'}")
    print(f"Test 3 (Taking D, optimal): {'✅ PASS' if test_3_passed else '❌ FAIL'}")
    
    all_tests_passed = test_1_passed and test_2_passed and test_3_passed
    
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED! Quick-VitD-row-takingD section working correctly!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_quick_vitd_row_takingd() 