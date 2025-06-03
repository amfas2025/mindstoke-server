#!/usr/bin/env python3

"""
Test script for quick-vitE condition and its sub-conditions
Tests: quick-vitE, VitE12, quick-vitE-row, quick-vitE-row-elevated, Quick-Thinner
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vitamin_e_condition():
    """Test quick-vitE condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Vitamin E (quick-vitE) Condition ===\n")
    
    # Test Case 1: Low vitamin E (< 12) - should trigger quick-vitE-row
    print("🧪 Test Case 1: Low Vitamin E (8.5 mg/L)")
    lab_results_1 = {'VIT_E': 8.5}
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-vitE: {processed_1.get('quick-vitE')} (should be '8.5 mg/L')")
    print(f"   VitE12: {processed_1.get('VitE12')} (should be False)")  
    print(f"   quick-vitE-row: {processed_1.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_1.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_1.get('Quick-Thinner')} (should be False)")
    print()
    
    # Test Case 2: Optimal vitamin E (12-20) - should trigger VitE12  
    print("🧪 Test Case 2: Optimal Vitamin E (15.2 mg/L)")
    lab_results_2 = {'VIT_E': 15.2}
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-vitE: {processed_2.get('quick-vitE')} (should be '15.2 mg/L')")
    print(f"   VitE12: {processed_2.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_2.get('quick-vitE-row')} (should be False)")  
    print(f"   quick-vitE-row-elevated: {processed_2.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_2.get('Quick-Thinner')} (should be False)")
    print()
    
    # Test Case 3: Elevated vitamin E (> 20) - should trigger both VitE12 and quick-vitE-row-elevated
    print("🧪 Test Case 3: Elevated Vitamin E (25.8 mg/L)")
    lab_results_3 = {'VIT_E': 25.8}
    hhq_responses_3 = {}
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print(f"   quick-vitE: {processed_3.get('quick-vitE')} (should be '25.8 mg/L')")
    print(f"   VitE12: {processed_3.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_3.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_3.get('quick-vitE-row-elevated')} (should be True)")
    print(f"   Quick-Thinner: {processed_3.get('Quick-Thinner')} (should be False)")
    print()
    
    # Test Case 4: Borderline vitamin E (exactly 12) - should trigger VitE12
    print("🧪 Test Case 4: Borderline Vitamin E (12.0 mg/L)")
    lab_results_4 = {'VIT_E': 12.0}
    hhq_responses_4 = {}
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    
    print(f"   quick-vitE: {processed_4.get('quick-vitE')} (should be '12.0 mg/L')")
    print(f"   VitE12: {processed_4.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_4.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_4.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_4.get('Quick-Thinner')} (should be False)")
    print()
    
    # Test Case 5: Low vitamin E + Blood thinner interaction
    print("🧪 Test Case 5: Low Vitamin E (9.1 mg/L) + Blood Thinner")
    lab_results_5 = {'VIT_E': 9.1}
    hhq_responses_5 = {'hh_blood_thinner': True}
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, hhq_responses_5)
    
    print(f"   quick-vitE: {processed_5.get('quick-vitE')} (should be '9.1 mg/L')")
    print(f"   VitE12: {processed_5.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_5.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_5.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_5.get('Quick-Thinner')} (should be True)")
    print()
    
    # Test Case 6: No vitamin E data  
    print("🧪 Test Case 6: No Vitamin E Data")
    lab_results_6 = {}
    hhq_responses_6 = {}
    
    processed_6 = generator._process_all_content_controls(client_data, lab_results_6, hhq_responses_6)
    
    print(f"   quick-vitE: {processed_6.get('quick-vitE')} (should be None)")
    print(f"   VitE12: {processed_6.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_6.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_6.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_6.get('Quick-Thinner')} (should be False)")
    print()
    
    # Test Case 7: Borderline high vitamin E (exactly 20) - should not trigger elevated  
    print("🧪 Test Case 7: Borderline High Vitamin E (20.0 mg/L)")
    lab_results_7 = {'VIT_E': 20.0}
    hhq_responses_7 = {}
    
    processed_7 = generator._process_all_content_controls(client_data, lab_results_7, hhq_responses_7)
    
    print(f"   quick-vitE: {processed_7.get('quick-vitE')} (should be '20.0 mg/L')")
    print(f"   VitE12: {processed_7.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_7.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_7.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_7.get('Quick-Thinner')} (should be False)")
    print()
    
    print("✅ Vitamin E condition testing complete!")

if __name__ == "__main__":
    test_vitamin_e_condition() 