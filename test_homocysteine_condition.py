#!/usr/bin/env python3

"""
Test script for quick-homocysteine condition and its sub-conditions
Tests: quick-homocysteine, quick-Homo12, quick-Homo15
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_homocysteine_condition():
    """Test quick-homocysteine condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Homocysteine (quick-homocysteine) Condition ===\n")
    
    # Test Case 1: Optimal homocysteine <7.0 (should NOT trigger)
    print("Test Case 1: Optimal homocysteine <7.0 (should NOT trigger)")
    lab_results_1 = {
        'INFLAM_HOMOCYS': 6.5,  # Below optimal threshold of 7.0
        'VIT_B12': 800,
        'VIT_D25': 45.0  # Other lab data
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, {})
    
    # Check what conditions are triggered
    homo_main = processed_1.get('quick-homocysteine', False)
    homo_value = processed_1.get('homocysteine-value', None)
    homo_12 = processed_1.get('quick-Homo12', False)
    homo_15 = processed_1.get('quick-Homo15', False)
    b12_value = processed_1.get('quick-B12-value', None)
    
    print(f"Homocysteine value stored: {homo_value}")
    print(f"Main condition triggered: {homo_main}")
    print(f"Homo12 condition triggered: {homo_12}")
    print(f"Homo15 condition triggered: {homo_15}")
    print(f"B12 value stored: {b12_value}")
    
    if not homo_main and homo_value == 6.5:
        print("✅ Correctly NOT triggered for optimal levels - PASS")
    else:
        print("❌ Should not trigger for optimal levels - FAIL")
    
    print()
    
    # Test Case 2: Elevated homocysteine 8.5 (should trigger main only)
    print("Test Case 2: Elevated homocysteine 8.5 (should trigger main only)")
    lab_results_2 = {
        'INFLAM_HOMOCYS': 8.5,  # Above 7.0 but below 12.0
        'VIT_B12': 600,
        'VIT_FOLATE': 12.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, {})
    
    homo_main_2 = processed_2.get('quick-homocysteine', False)
    homo_value_2 = processed_2.get('homocysteine-value', None)
    homo_12_2 = processed_2.get('quick-Homo12', False)
    homo_15_2 = processed_2.get('quick-Homo15', False)
    folate_value_2 = processed_2.get('quick-folic-acid-value', None)
    
    print(f"Homocysteine value stored: {homo_value_2}")
    print(f"Main condition triggered: {homo_main_2}")
    print(f"Homo12 condition triggered: {homo_12_2}")
    print(f"Homo15 condition triggered: {homo_15_2}")
    print(f"Folate value stored: {folate_value_2}")
    
    if homo_main_2 and not homo_12_2 and not homo_15_2:
        print("✅ Correctly triggered main condition only - PASS")
    else:
        print("❌ Should trigger main condition only - FAIL")
    
    print()
    
    # Test Case 3: High homocysteine 13.2 (should trigger main + Homo12)
    print("Test Case 3: High homocysteine 13.2 (should trigger main + Homo12)")
    lab_results_3 = {
        'INFLAM_HOMOCYS': 13.2,  # Above 12.0 but below 15.0
        'VIT_B12': 450,
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, {})
    
    homo_main_3 = processed_3.get('quick-homocysteine', False)
    homo_value_3 = processed_3.get('homocysteine-value', None)
    homo_12_3 = processed_3.get('quick-Homo12', False)
    homo_15_3 = processed_3.get('quick-Homo15', False)
    
    print(f"Homocysteine value stored: {homo_value_3}")
    print(f"Main condition triggered: {homo_main_3}")
    print(f"Homo12 condition triggered: {homo_12_3}")
    print(f"Homo15 condition triggered: {homo_15_3}")
    
    if homo_main_3 and homo_12_3 and not homo_15_3:
        print("✅ Correctly triggered main + Homo12 conditions - PASS")
    else:
        print("❌ Should trigger main + Homo12 conditions - FAIL")
    
    print()
    
    # Test Case 4: Very high homocysteine 16.8 (should trigger all conditions)
    print("Test Case 4: Very high homocysteine 16.8 (should trigger ALL conditions)")
    lab_results_4 = {
        'INFLAM_HOMOCYS': 16.8,  # Above 15.0
        'VIT_B12': 350,
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, {})
    
    homo_main_4 = processed_4.get('quick-homocysteine', False)
    homo_value_4 = processed_4.get('homocysteine-value', None)
    homo_12_4 = processed_4.get('quick-Homo12', False)
    homo_15_4 = processed_4.get('quick-Homo15', False)
    
    print(f"Homocysteine value stored: {homo_value_4}")
    print(f"Main condition triggered: {homo_main_4}")
    print(f"Homo12 condition triggered: {homo_12_4}")
    print(f"Homo15 condition triggered: {homo_15_4}")
    
    if homo_main_4 and homo_12_4 and homo_15_4:
        print("✅ Correctly triggered ALL conditions - PASS")
        
        # Test template processing for highest level
        roadmap_4 = generator.generate_roadmap(client_data, lab_results_4, {})
        if '↑\'d Homocysteine Levels Can Impair Brain Function' in roadmap_4:
            print("✅ Template section header found - PASS")
            
            # Check for key content elements
            content_checks = [
                'Your HOMOCYSTEINE level was 16.8',
                'goal level < 7 umol/L',
                'TRIMETHYLGLYCINE 1000 mg/day',
                'HOMOCYSTEINE levels are > 12',
                'CREATINE MONOHYDRATE',
                'HOMOCYSTEINE levels are > 15',
                'Masterclass:'
            ]
            
            missing_content = []
            for check in content_checks:
                if check not in roadmap_4:
                    missing_content.append(check)
            
            if missing_content:
                print(f"❌ Missing content: {missing_content}")
            else:
                print("✅ All expected content found!")
        else:
            print("❌ Template section header missing - FAIL")
    else:
        print("❌ Should trigger ALL conditions - FAIL")
    
    print()
    
    # Test Case 5: No homocysteine data (should not trigger)
    print("Test Case 5: No homocysteine data (should NOT trigger)")
    lab_results_5 = {
        'VIT_D25': 45.0,  # Only other lab data
        'VIT_B12': 500
    }
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, {})
    
    homo_main_5 = processed_5.get('quick-homocysteine', False)
    homo_value_5 = processed_5.get('homocysteine-value', None)
    homo_12_5 = processed_5.get('quick-Homo12', False)
    homo_15_5 = processed_5.get('quick-Homo15', False)
    
    print(f"Homocysteine value stored: {homo_value_5}")
    print(f"Main condition triggered: {homo_main_5}")
    print(f"Homo12 condition triggered: {homo_12_5}")
    print(f"Homo15 condition triggered: {homo_15_5}")
    
    if not homo_main_5 and not homo_value_5 and not homo_12_5 and not homo_15_5:
        print("✅ Correctly NOT triggered when no data - PASS")
    else:
        print("❌ Should not trigger when no data - FAIL")
    
    print()
    
    # Test Case 6: Show generated content sample
    if homo_main_4 and homo_12_4 and homo_15_4:
        print("=== Sample Generated Content (High Homocysteine) ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results_4, {})
        
        # Extract homocysteine section
        lines = roadmap_sample.split('\n')
        in_section = False
        section_lines = []
        
        for line in lines:
            if '↑\'d Homocysteine Levels Can Impair Brain Function' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() == '---':
                break
            elif in_section:
                section_lines.append(line)
        
        if section_lines:
            for line in section_lines[:15]:  # Show first 15 lines
                print(line)
            if len(section_lines) > 15:
                print("... (truncated)")
    
    print("\n=== Test Summary ===")
    print("Homocysteine (quick-homocysteine) condition implementation complete!")
    print("- Triggers on: Homocysteine > 7.0 umol/L")
    print("- Displays: Homocysteine value, B12 value, folate value")
    print("- Sub-condition quick-Homo12: Levels > 12 → Trimethylglycine recommendation")
    print("- Sub-condition quick-Homo15: Levels > 15 → Creatine monohydrate recommendation")
    print("- Clinical focus: B vitamin optimization for homocysteine recycling")
    print("- Educational: Includes masterclass link for patient education")

if __name__ == "__main__":
    test_homocysteine_condition() 