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
    
    # Test Case 1: Low vitamin E <12.0 (should trigger supplementation)
    print("Test Case 1: Low vitamin E <12.0 (should trigger supplementation)")
    lab_results_1 = {
        'VIT_E': 8.5,  # Below optimal threshold of 12.0
        'VIT_D25': 45.0  # Other lab data
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, {})
    
    # Check what conditions are triggered
    vit_e_main = processed_1.get('quick-vitE', None)
    vit_e_12 = processed_1.get('VitE12', False)
    vit_e_row = processed_1.get('quick-vitE-row', False)
    vit_e_elevated = processed_1.get('quick-vitE-row-elevated', False)
    
    print(f"Vitamin E value stored: {vit_e_main}")
    print(f"VitE12 condition triggered: {vit_e_12}")
    print(f"quick-vitE-row condition triggered: {vit_e_row}")
    print(f"quick-vitE-row-elevated condition triggered: {vit_e_elevated}")
    
    if vit_e_main == 8.5 and vit_e_row and not vit_e_12 and not vit_e_elevated:
        print("✅ Correctly triggered supplementation for low levels - PASS")
    else:
        print("❌ Should trigger supplementation for low levels - FAIL")
    
    print()
    
    # Test Case 2: Optimal vitamin E 15.0 (should trigger VitE12)
    print("Test Case 2: Optimal vitamin E 15.0 (should trigger VitE12)")
    lab_results_2 = {
        'VIT_E': 15.0,  # In optimal range (12-20)
        'VIT_D25': 50.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, {})
    
    vit_e_main_2 = processed_2.get('quick-vitE', None)
    vit_e_12_2 = processed_2.get('VitE12', False)
    vit_e_row_2 = processed_2.get('quick-vitE-row', False)
    vit_e_elevated_2 = processed_2.get('quick-vitE-row-elevated', False)
    
    print(f"Vitamin E value stored: {vit_e_main_2}")
    print(f"VitE12 condition triggered: {vit_e_12_2}")
    print(f"quick-vitE-row condition triggered: {vit_e_row_2}")
    print(f"quick-vitE-row-elevated condition triggered: {vit_e_elevated_2}")
    
    if vit_e_main_2 == 15.0 and vit_e_12_2 and not vit_e_row_2 and not vit_e_elevated_2:
        print("✅ Correctly triggered optimal condition - PASS")
    else:
        print("❌ Should trigger optimal condition - FAIL")
    
    print()
    
    # Test Case 3: Elevated vitamin E 28.0 (should trigger toxicity warning)
    print("Test Case 3: Elevated vitamin E 28.0 (should trigger toxicity warning)")
    lab_results_3 = {
        'VIT_E': 28.0,  # Very elevated (>25)
        'VIT_D25': 45.0
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, {})
    
    vit_e_main_3 = processed_3.get('quick-vitE', None)
    vit_e_12_3 = processed_3.get('VitE12', False)
    vit_e_row_3 = processed_3.get('quick-vitE-row', False)
    vit_e_elevated_3 = processed_3.get('quick-vitE-row-elevated', False)
    
    print(f"Vitamin E value stored: {vit_e_main_3}")
    print(f"VitE12 condition triggered: {vit_e_12_3}")
    print(f"quick-vitE-row condition triggered: {vit_e_row_3}")
    print(f"quick-vitE-row-elevated condition triggered: {vit_e_elevated_3}")
    
    if vit_e_main_3 == 28.0 and vit_e_elevated_3 and not vit_e_12_3 and not vit_e_row_3:
        print("✅ Correctly triggered toxicity warning - PASS")
    else:
        print("❌ Should trigger toxicity warning - FAIL")
    
    print()
    
    # Test Case 4: Low vitamin E + Blood thinner (should trigger both conditions)
    print("Test Case 4: Low vitamin E + Blood thinner (should trigger both conditions)")
    lab_results_4 = {
        'VIT_E': 7.2,  # Below optimal
    }
    
    hhq_responses_4 = {
        'hh_blood_thinner': True,  # On blood thinner
        'hh_warfarin': True
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    
    vit_e_main_4 = processed_4.get('quick-vitE', None)
    vit_e_row_4 = processed_4.get('quick-vitE-row', False)
    quick_thinner_4 = processed_4.get('Quick-Thinner', False)
    
    print(f"Vitamin E value stored: {vit_e_main_4}")
    print(f"quick-vitE-row condition triggered: {vit_e_row_4}")
    print(f"Quick-Thinner condition triggered: {quick_thinner_4}")
    
    if vit_e_main_4 == 7.2 and vit_e_row_4 and quick_thinner_4:
        print("✅ Correctly triggered both supplement and blood thinner warnings - PASS")
    else:
        print("❌ Should trigger both supplement and blood thinner warnings - FAIL")
    
    print()
    
    # Test Case 5: No vitamin E data (should not trigger any conditions)
    print("Test Case 5: No vitamin E data (should NOT trigger)")
    lab_results_5 = {
        'VIT_D25': 45.0,  # Only other lab data
        'VIT_B12': 500
    }
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, {})
    
    vit_e_main_5 = processed_5.get('quick-vitE', None)
    vit_e_12_5 = processed_5.get('VitE12', False)
    vit_e_row_5 = processed_5.get('quick-vitE-row', False)
    vit_e_elevated_5 = processed_5.get('quick-vitE-row-elevated', False)
    
    print(f"Vitamin E value stored: {vit_e_main_5}")
    print(f"VitE12 condition triggered: {vit_e_12_5}")
    print(f"quick-vitE-row condition triggered: {vit_e_row_5}")
    print(f"quick-vitE-row-elevated condition triggered: {vit_e_elevated_5}")
    
    if not vit_e_main_5 and not vit_e_12_5 and not vit_e_row_5 and not vit_e_elevated_5:
        print("✅ Correctly NOT triggered when no data - PASS")
    else:
        print("❌ Should not trigger when no data - FAIL")
    
    print()
    
    # Test Case 6: Test template processing for each condition
    print("Test Case 6: Testing template integration")
    
    # Test with low vitamin E needing supplementation
    roadmap_low = generator.generate_roadmap(client_data, lab_results_1, {})
    if 'Your combined **Vitamin E** level is 8.5' in roadmap_low:
        print("✅ Template correctly displays vitamin E value")
        
        if '**COMPLETE E** from the company Metabolic Response Modifier' in roadmap_low:
            print("✅ Template correctly shows supplementation recommendation")
        else:
            print("❌ Missing supplementation recommendation")
    else:
        print("❌ Template missing vitamin E value")
    
    # Test with optimal vitamin E
    roadmap_optimal = generator.generate_roadmap(client_data, lab_results_2, {})
    if 'This level falls within the optimal parameters and no additional intervention is recommended' in roadmap_optimal:
        print("✅ Template correctly shows optimal message")
    else:
        print("❌ Missing optimal message")
    
    # Test with elevated vitamin E
    roadmap_elevated = generator.generate_roadmap(client_data, lab_results_3, {})
    if 'starting to trend quite elevated' in roadmap_elevated:
        print("✅ Template correctly shows toxicity warning")
    else:
        print("❌ Missing toxicity warning")
    
    # Test with blood thinner
    roadmap_thinner = generator.generate_roadmap(client_data, lab_results_4, hhq_responses_4)
    if 'VITAMIN E can thin the blood' in roadmap_thinner:
        print("✅ Template correctly shows blood thinner warning")
    else:
        print("❌ Missing blood thinner warning")
    
    print("\n=== Test Summary ===")
    print("Vitamin E (quick-vitE) condition implementation complete!")
    print("- Displays: Vitamin E value and optimal range (12-20 mg/L)")
    print("- VitE12: Optimal levels ≥12 mg/L (no intervention)")
    print("- quick-vitE-row: Suboptimal levels <12 mg/L (COMPLETE E supplement)")
    print("- quick-vitE-row-elevated: Elevated levels ≥25 mg/L (toxicity warning)")
    print("- Quick-Thinner: Blood thinner interaction warning")
    print("- Clinical focus: Comprehensive vitamin E status with safety considerations")

if __name__ == "__main__":
    test_vitamin_e_condition() 