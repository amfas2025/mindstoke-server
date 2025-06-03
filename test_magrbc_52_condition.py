#!/usr/bin/env python3

"""
Test script for quick-MagRBC-52 condition
Tests the specific borderline magnesium RBC condition around 5.2 mg/dL threshold
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_magrbc_52_condition():
    """Test quick-MagRBC-52 condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Magnesium RBC-52 (quick-MagRBC-52) Condition ===\n")
    
    # Test Case 1: Magnesium RBC = 5.0 (should trigger quick-MagRBC-52)
    print("Test Case 1: Magnesium RBC = 5.0 (should trigger quick-MagRBC-52)")
    lab_results_1 = {
        'MIN_MG_RBC': 5.0,  # Within 5.0-5.2 range
        'VIT_D25': 45.0     # Other lab data
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, {})
    
    # Check what conditions are triggered
    mg_rbc_main = processed_1.get('quick-MagRBC', None)
    mg_rbc_52 = processed_1.get('quick-MagRBC-52', False)
    mg_rbc_low = processed_1.get('quick-MagRBC-low', False)
    mg_rbc_optimal = processed_1.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mg_rbc_main}")
    print(f"quick-MagRBC-52 condition triggered: {mg_rbc_52}")
    print(f"quick-MagRBC-low condition triggered: {mg_rbc_low}")
    print(f"quick-MagRBC-optimal condition triggered: {mg_rbc_optimal}")
    
    if mg_rbc_main == 5.0 and mg_rbc_52 and mg_rbc_low:
        print("✅ Correctly triggered quick-MagRBC-52 for borderline level - PASS")
    else:
        print("❌ Should trigger quick-MagRBC-52 for borderline level - FAIL")
    
    print()
    
    # Test Case 2: Magnesium RBC = 5.2 (should trigger quick-MagRBC-52)
    print("Test Case 2: Magnesium RBC = 5.2 (should trigger quick-MagRBC-52)")
    lab_results_2 = {
        'MIN_MG_RBC': 5.2,  # Exactly at threshold
        'VIT_D25': 50.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, {})
    
    mg_rbc_main_2 = processed_2.get('quick-MagRBC', None)
    mg_rbc_52_2 = processed_2.get('quick-MagRBC-52', False)
    mg_rbc_low_2 = processed_2.get('quick-MagRBC-low', False)
    mg_rbc_optimal_2 = processed_2.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mg_rbc_main_2}")
    print(f"quick-MagRBC-52 condition triggered: {mg_rbc_52_2}")
    print(f"quick-MagRBC-low condition triggered: {mg_rbc_low_2}")
    print(f"quick-MagRBC-optimal condition triggered: {mg_rbc_optimal_2}")
    
    if mg_rbc_main_2 == 5.2 and mg_rbc_52_2 and mg_rbc_optimal_2:
        print("✅ Correctly triggered quick-MagRBC-52 at threshold - PASS")
    else:
        print("❌ Should trigger quick-MagRBC-52 at threshold - FAIL")
    
    print()
    
    # Test Case 3: Magnesium RBC = 5.1 (should trigger quick-MagRBC-52)
    print("Test Case 3: Magnesium RBC = 5.1 (should trigger quick-MagRBC-52)")
    lab_results_3 = {
        'MIN_MG_RBC': 5.1,  # Within borderline range
        'VIT_D25': 45.0
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, {})
    
    mg_rbc_main_3 = processed_3.get('quick-MagRBC', None)
    mg_rbc_52_3 = processed_3.get('quick-MagRBC-52', False)
    mg_rbc_low_3 = processed_3.get('quick-MagRBC-low', False)
    mg_rbc_optimal_3 = processed_3.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mg_rbc_main_3}")
    print(f"quick-MagRBC-52 condition triggered: {mg_rbc_52_3}")
    print(f"quick-MagRBC-low condition triggered: {mg_rbc_low_3}")
    print(f"quick-MagRBC-optimal condition triggered: {mg_rbc_optimal_3}")
    
    if mg_rbc_main_3 == 5.1 and mg_rbc_52_3 and mg_rbc_low_3:
        print("✅ Correctly triggered quick-MagRBC-52 for borderline level - PASS")
    else:
        print("❌ Should trigger quick-MagRBC-52 for borderline level - FAIL")
    
    print()
    
    # Test Case 4: Magnesium RBC = 4.8 (should NOT trigger quick-MagRBC-52)
    print("Test Case 4: Magnesium RBC = 4.8 (should NOT trigger quick-MagRBC-52)")
    lab_results_4 = {
        'MIN_MG_RBC': 4.8,  # Below 5.0 range
        'VIT_D25': 45.0
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, {})
    
    mg_rbc_main_4 = processed_4.get('quick-MagRBC', None)
    mg_rbc_52_4 = processed_4.get('quick-MagRBC-52', False)
    mg_rbc_low_4 = processed_4.get('quick-MagRBC-low', False)
    
    print(f"Magnesium RBC value stored: {mg_rbc_main_4}")
    print(f"quick-MagRBC-52 condition triggered: {mg_rbc_52_4}")
    print(f"quick-MagRBC-low condition triggered: {mg_rbc_low_4}")
    
    if mg_rbc_main_4 == 4.8 and not mg_rbc_52_4 and mg_rbc_low_4:
        print("✅ Correctly NOT triggered quick-MagRBC-52 for low level - PASS")
    else:
        print("❌ Should NOT trigger quick-MagRBC-52 for low level - FAIL")
    
    print()
    
    # Test Case 5: Magnesium RBC = 5.5 (should NOT trigger quick-MagRBC-52)
    print("Test Case 5: Magnesium RBC = 5.5 (should NOT trigger quick-MagRBC-52)")
    lab_results_5 = {
        'MIN_MG_RBC': 5.5,  # Above 5.2 range
        'VIT_D25': 45.0
    }
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, {})
    
    mg_rbc_main_5 = processed_5.get('quick-MagRBC', None)
    mg_rbc_52_5 = processed_5.get('quick-MagRBC-52', False)
    mg_rbc_optimal_5 = processed_5.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mg_rbc_main_5}")
    print(f"quick-MagRBC-52 condition triggered: {mg_rbc_52_5}")
    print(f"quick-MagRBC-optimal condition triggered: {mg_rbc_optimal_5}")
    
    if mg_rbc_main_5 == 5.5 and not mg_rbc_52_5 and mg_rbc_optimal_5:
        print("✅ Correctly NOT triggered quick-MagRBC-52 for optimal level - PASS")
    else:
        print("❌ Should NOT trigger quick-MagRBC-52 for optimal level - FAIL")
    
    print()
    
    # Test Case 6: Test template integration
    print("Test Case 6: Testing template integration")
    
    # Test with borderline magnesium RBC that should show the quick-MagRBC-52 content
    roadmap_52 = generator.generate_roadmap(client_data, lab_results_1, {})
    if 'Consider starting **MAGNESIUM THREONATE 2000 mg at night**' in roadmap_52:
        print("✅ Template correctly shows MAGNESIUM THREONATE recommendation")
        
        # Check for the specific quick-MagRBC-52 content (shorter text)
        content_lines = roadmap_52.split('\n')
        found_specific_52_content = False
        for line in content_lines:
            if ('Consider starting **MAGNESIUM THREONATE 2000 mg at night**' in line and 
                'This form of magnesium is specifically designed to cross the blood-brain barrier' in line and
                len(line) < 200):  # Shorter version from quick-MagRBC-52
                found_specific_52_content = True
                break
        
        if found_specific_52_content:
            print("✅ Template shows specific quick-MagRBC-52 content")
        else:
            print("❌ Template missing specific quick-MagRBC-52 content")
    else:
        print("❌ Template missing magnesium recommendation")
    
    print("\n=== Test Summary ===")
    print("Magnesium RBC-52 (quick-MagRBC-52) condition implementation complete!")
    print("- Triggers for: Magnesium RBC levels between 5.0-5.2 mg/dL (borderline range)")
    print("- Content: Specific MAGNESIUM THREONATE 2000 mg recommendation")
    print("- Clinical focus: Borderline magnesium status requiring targeted supplementation")
    print("- Threshold logic: Covers the critical 5.2 mg/dL transition point")

if __name__ == "__main__":
    test_magrbc_52_condition() 