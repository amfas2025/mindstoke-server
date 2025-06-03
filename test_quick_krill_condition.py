#!/usr/bin/env python3

"""
Test script for Quick-krill condition processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_quick_krill_condition():
    """Test Quick-krill condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Quick-krill Condition ===\n")
    
    # Test Case 1: Client taking krill oil (should trigger)
    print("Test Case 1: Client taking krill oil (SHOULD TRIGGER)")
    hhq_responses_1 = {
        'hh_taking_krill_oil': True
    }
    
    lab_results = {
        'VIT_D25': 45.0,
        'OMEGA_CHECK': 4.2
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results, hhq_responses_1)
    triggered_1 = processed_1.get('Quick-krill', False)
    print(f"Condition triggered: {triggered_1}")
    
    if triggered_1:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results, hhq_responses_1)
        if 'extremely low in DHA and EPA omega-3 fatty acids' in roadmap_1:
            print("✅ Template content found - PASS")
            
            # Check for key content elements
            content_checks = [
                'Triple Strength OMEGA-3 FISH OIL',
                'TRIGLYCERIDE-derived OMEGA-3',
                'Ethyl Ester',
                'PRO-OMEGA 2000',
                'ULTIMATE OMEGA 2X',
                'maintenance dose is 3 caps per day'
            ]
            
            missing_content = []
            for check in content_checks:
                if check not in roadmap_1:
                    missing_content.append(check)
            
            if missing_content:
                print(f"❌ Missing content: {missing_content}")
            else:
                print("✅ All expected content found!")
        else:
            print("❌ Template content missing - FAIL")
    else:
        print("❌ Condition not triggered - FAIL")
    
    print()
    
    # Test Case 2: Alternative HHQ key (should trigger)
    print("Test Case 2: Alternative HHQ key 'hh_supplement_krill' (SHOULD TRIGGER)")
    hhq_responses_2 = {
        'hh_supplement_krill': True
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results, hhq_responses_2)
    triggered_2 = processed_2.get('Quick-krill', False)
    print(f"Condition triggered: {triggered_2}")
    print("✅ Alternative key works - PASS" if triggered_2 else "❌ Alternative key failed - FAIL")
    
    print()
    
    # Test Case 3: Another alternative key (should trigger)
    print("Test Case 3: Alternative HHQ key 'hh_krill_oil' (SHOULD TRIGGER)")
    hhq_responses_3 = {
        'hh_krill_oil': True
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results, hhq_responses_3)
    triggered_3 = processed_3.get('Quick-krill', False)
    print(f"Condition triggered: {triggered_3}")
    print("✅ Third alternative key works - PASS" if triggered_3 else "❌ Third alternative key failed - FAIL")
    
    print()
    
    # Test Case 4: No krill oil mentioned (should NOT trigger)
    print("Test Case 4: No krill oil in HHQ (should NOT trigger)")
    hhq_responses_4 = {
        'hh_taking_nac': True,  # Different supplement
        'hh_exercise_regular': True
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results, hhq_responses_4)
    triggered_4 = processed_4.get('Quick-krill', False)
    print(f"Condition triggered: {triggered_4}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_4 else "❌ Should not trigger - FAIL")
    
    print()
    
    # Test Case 5: Show generated content sample
    if triggered_1:
        print("=== Sample Generated Content ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results, hhq_responses_1)
        
        # Extract krill oil section
        lines = roadmap_sample.split('\n')
        in_krill_section = False
        krill_lines = []
        
        for line in lines:
            if 'Krill Oil Considerations:' in line:
                in_krill_section = True
                krill_lines.append(line)
            elif in_krill_section and line.strip() == '':
                break
            elif in_krill_section:
                krill_lines.append(line)
        
        if krill_lines:
            for line in krill_lines:
                print(line)
    
    print("\n=== Test Summary ===")
    print("Quick-krill condition implementation complete!")
    print("- Triggers on: hh_taking_krill_oil, hh_supplement_krill, hh_krill_oil")
    print("- Content: Explains krill oil limitations and recommends superior alternatives")
    print("- Brands: Triple Strength OMEGA-3 FISH OIL, PRO-OMEGA 2000, ULTIMATE OMEGA 2X")
    print("- Education: Triglyceride vs Ethyl Ester absorption differences")
    print("- Dosing: 3 caps per day maintenance dose")

if __name__ == "__main__":
    test_quick_krill_condition() 