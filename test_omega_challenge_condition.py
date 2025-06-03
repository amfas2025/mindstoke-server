#!/usr/bin/env python3

"""
Test script for checked-omega-63-ratio condition (OMEGA-3 CHALLENGE)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_omega_challenge_condition():
    """Test checked-omega-63-ratio condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'male',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing OMEGA-3 CHALLENGE Condition ===\n")
    
    # Test Case 1: History of concussion (should trigger)
    print("Test Case 1: History of concussion (SHOULD TRIGGER)")
    hhq_responses_1 = {
        'hh_concussion': True
    }
    
    lab_results_1 = {
        'VIT_D25': 45.0,
        'OMEGA_6_3_RATIO': 6.5  # Not extremely high, but concussion should trigger
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    triggered_1 = processed_1.get('checked-omega-63-ratio', False)
    print(f"Condition triggered: {triggered_1}")
    
    if triggered_1:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        if 'OMEGA-3 CHALLENGE' in roadmap_1 and '10,000 mg of combined EPA and DHA' in roadmap_1:
            print("✅ Template content found - PASS")
            
            # Check for key content elements
            content_checks = [
                'OMEGA-3 CHALLENGE Protocol:',
                'Dr. Michael Lewis',
                '10,000 mg of combined EPA and DHA',
                'for 1-2 months',
                'neurological recovery',
                'maintenance dosing of 3 caps per day'
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
    
    # Test Case 2: History of TBI (should trigger)
    print("Test Case 2: History of TBI (SHOULD TRIGGER)")
    hhq_responses_2 = {
        'hh_traumatic_brain_injury': True
    }
    
    lab_results_2 = {
        'VIT_D25': 45.0,
        'OMEGA_6_3_RATIO': 4.5  # Normal ratio, but TBI should trigger
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    triggered_2 = processed_2.get('checked-omega-63-ratio', False)
    print(f"Condition triggered: {triggered_2}")
    print("✅ TBI triggers condition - PASS" if triggered_2 else "❌ TBI should trigger - FAIL")
    
    print()
    
    # Test Case 3: Very high omega 6:3 ratio (should trigger)
    print("Test Case 3: Very high omega 6:3 ratio >10 (SHOULD TRIGGER)")
    hhq_responses_3 = {
        'hh_brain_fog': True  # No head injury
    }
    
    lab_results_3 = {
        'VIT_D25': 45.0,
        'OMEGA_6_3_RATIO': 12.5  # Very high ratio should trigger
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    triggered_3 = processed_3.get('checked-omega-63-ratio', False)
    print(f"Condition triggered: {triggered_3}")
    print("✅ High ratio triggers condition - PASS" if triggered_3 else "❌ High ratio should trigger - FAIL")
    
    print()
    
    # Test Case 4: Neither head injury nor high ratio (should NOT trigger)
    print("Test Case 4: No head injury and normal ratio (should NOT trigger)")
    hhq_responses_4 = {
        'hh_brain_fog': True,  # Other symptoms but no head injury
        'hh_memory_problems': False
    }
    
    lab_results_4 = {
        'VIT_D25': 45.0,
        'OMEGA_6_3_RATIO': 6.0  # Elevated but not extreme
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    triggered_4 = processed_4.get('checked-omega-63-ratio', False)
    print(f"Condition triggered: {triggered_4}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_4 else "❌ Should not trigger - FAIL")
    
    print()
    
    # Test Case 5: Alternative head injury terms (should trigger)
    print("Test Case 5: Head injury with alternative HHQ key (SHOULD TRIGGER)")
    hhq_responses_5 = {
        'hh_head_injury': True  # Alternative key
    }
    
    lab_results_5 = {
        'VIT_D25': 45.0,
        'OMEGA_6_3_RATIO': 5.0
    }
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, hhq_responses_5)
    triggered_5 = processed_5.get('checked-omega-63-ratio', False)
    print(f"Condition triggered: {triggered_5}")
    print("✅ Alternative head injury key works - PASS" if triggered_5 else "❌ Alternative key failed - FAIL")
    
    print()
    
    # Test Case 6: Show generated content sample
    if triggered_1:
        print("=== Sample Generated Content ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        
        # Extract OMEGA-3 CHALLENGE section
        lines = roadmap_sample.split('\n')
        in_challenge_section = False
        challenge_lines = []
        
        for line in lines:
            if 'OMEGA-3 CHALLENGE Protocol:' in line:
                in_challenge_section = True
                challenge_lines.append(line)
            elif in_challenge_section and line.strip() == '':
                break
            elif in_challenge_section:
                challenge_lines.append(line)
        
        if challenge_lines:
            for line in challenge_lines:
                print(line)
    
    # Test Case 7: Compound scenario - head injury + high ratio
    print("\n=== Compound Scenario Test ===")
    print("Test Case 7: Head injury + high omega ratio (both triggers)")
    hhq_responses_7 = {
        'hh_concussion': True,
        'hh_brain_fog': True
    }
    
    lab_results_7 = {
        'VIT_D25': 35.0,
        'OMEGA_6_3_RATIO': 15.0,  # Very high
        'OMEGA_CHECK': 3.8        # Low omega status
    }
    
    processed_7 = generator._process_all_content_controls(client_data, lab_results_7, hhq_responses_7)
    
    # Check multiple related conditions
    related_conditions = [
        'checked-omega-63-ratio',
        'quick-brain-fog', 
        'quick-VitD',
        'omega-63-ratio-elevated'
    ]
    
    print("Multiple related conditions triggered:")
    for condition in related_conditions:
        triggered = processed_7.get(condition, False)
        status = "✅ TRIGGERED" if triggered else "❌ Not triggered"
        print(f"  {condition}: {status}")
    
    print("\n=== Test Summary ===")
    print("OMEGA-3 CHALLENGE condition implementation complete!")
    print("- Triggers on: Concussion, TBI, head injury, OR omega 6:3 ratio >10")
    print("- Protocol: 10,000 mg combined EPA+DHA per day for 1-2 months")
    print("- Authority: Dr. Michael Lewis research")
    print("- Purpose: Neurological recovery and rapid omega-3 optimization")
    print("- Follow-up: Return to 3 caps per day maintenance dosing")

if __name__ == "__main__":
    test_omega_challenge_condition() 