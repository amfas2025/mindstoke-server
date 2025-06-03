#!/usr/bin/env python3

"""
Test script for Taking-an-OMEGA condition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_taking_omega_condition():
    """Test Taking-an-OMEGA condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'male',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing 'Taking an OMEGA' Condition ===\n")
    
    # Test Case 1: Taking omega-3 BUT ratio still >4:1 (should trigger)
    print("Test Case 1: Taking omega-3 but ratio still >4:1 (SHOULD TRIGGER)")
    hhq_responses_1 = {
        'hh_taking_fish_oil': True  # Currently taking omega-3
    }
    
    lab_results_1 = {
        'OMEGA_6_3_RATIO': 6.5,  # Still suboptimal despite supplementing
        'OMEGA_CHECK': 5.0,      # Low-normal
        'VIT_D25': 45.0
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    triggered_1 = processed_1.get('Taking-an-OMEGA', False)
    print(f"Condition triggered: {triggered_1}")
    
    if triggered_1:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        if 'Taking an OMEGA:' in roadmap_1 and 'evidence-based goal for the 4:1' in roadmap_1:
            print("✅ Template content found - PASS")
            
            # Check for key content elements
            content_checks = [
                'Taking an OMEGA:',
                'Though you are currently supplementing',
                'evidence-based goal for the 4:1',
                'OMEGA 6:3 RATIO',
                'look at the label of your OMEGA-3',
                'high-potency, triglyceride-based',
                'increase your maintenance dosing to 2 capsules, 2 x\'s/day',
                'Triple Strength OMEGA-3 FISH OIL',
                'Sports Research (Costco)',
                'PRO-OMEGA 2000',
                'ULTIMATE OMEGA 2X',
                'Nordic Naturals'
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
    
    # Test Case 2: Alternative HHQ omega-3 key (should trigger)
    print("Test Case 2: Alternative omega-3 HHQ key (SHOULD TRIGGER)")
    hhq_responses_2 = {
        'hh_taking_omega3': True  # Alternative key
    }
    
    lab_results_2 = {
        'OMEGA_6_3_RATIO': 5.2,  # Suboptimal
        'VIT_D25': 45.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    triggered_2 = processed_2.get('Taking-an-OMEGA', False)
    print(f"Condition triggered: {triggered_2}")
    print("✅ Alternative HHQ key works - PASS" if triggered_2 else "❌ Alternative key failed - FAIL")
    
    print()
    
    # Test Case 3: Taking omega-3 AND ratio is optimal (should NOT trigger)
    print("Test Case 3: Taking omega-3 AND ratio is optimal (should NOT trigger)")
    hhq_responses_3 = {
        'hh_taking_fish_oil': True  # Taking omega-3
    }
    
    lab_results_3 = {
        'OMEGA_6_3_RATIO': 3.2,  # Optimal ratio
        'OMEGA_CHECK': 7.8,      # Good omega status
        'VIT_D25': 45.0
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    triggered_3 = processed_3.get('Taking-an-OMEGA', False)
    print(f"Condition triggered: {triggered_3}")
    print("✅ Correctly NOT triggered when ratio is optimal - PASS" if not triggered_3 else "❌ Should not trigger when ratio is good - FAIL")
    
    print()
    
    # Test Case 4: NOT taking omega-3 but ratio is poor (should NOT trigger)
    print("Test Case 4: NOT taking omega-3 but ratio is poor (should NOT trigger)")
    hhq_responses_4 = {
        'hh_exercise': True  # No omega-3 supplementation
    }
    
    lab_results_4 = {
        'OMEGA_6_3_RATIO': 8.5,  # Poor ratio
        'OMEGA_CHECK': 3.2,      # Low omega status
        'VIT_D25': 45.0
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    triggered_4 = processed_4.get('Taking-an-OMEGA', False)
    print(f"Condition triggered: {triggered_4}")
    print("✅ Correctly NOT triggered when not taking omega-3 - PASS" if not triggered_4 else "❌ Should not trigger when not supplementing - FAIL")
    
    print()
    
    # Test Case 5: Show generated content sample
    if triggered_1:
        print("=== Sample Generated Content ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        
        # Extract Taking an OMEGA section
        lines = roadmap_sample.split('\n')
        in_section = False
        section_lines = []
        
        for line in lines:
            if 'Taking an OMEGA:' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() == '':
                break
            elif in_section:
                section_lines.append(line)
        
        if section_lines:
            for line in section_lines:
                print(line)
    
    # Test Case 6: Integration with other omega conditions
    print("\n=== Integration with Other Omega Conditions ===")
    print("Test Case 6: Taking omega-3 + suboptimal ratio + krill oil")
    hhq_responses_6 = {
        'hh_taking_fish_oil': True,    # Taking omega-3
        'hh_taking_krill_oil': True,   # But it's krill oil (low potency)
        'hh_brain_fog': True           # Has neurological symptoms
    }
    
    lab_results_6 = {
        'OMEGA_6_3_RATIO': 7.8,       # Poor ratio despite supplementing
        'OMEGA_CHECK': 4.2,           # Low omega status
        'INFLAM_CRP': 0.8,            # Normal CRP
        'VIT_D25': 35.0
    }
    
    processed_6 = generator._process_all_content_controls(client_data, lab_results_6, hhq_responses_6)
    
    # Check multiple related omega conditions
    omega_conditions = [
        'Taking-an-OMEGA',              # This condition
        'Quick-krill',                  # Krill oil advice
        'omega-neurological-suboptimal', # Neurological optimization
        'quick-brain-fog'               # Brain fog
    ]
    
    print("Multiple omega-3 related conditions triggered:")
    for condition in omega_conditions:
        triggered = processed_6.get(condition, False)
        status = "✅ TRIGGERED" if triggered else "❌ Not triggered"
        print(f"  {condition}: {status}")
    
    print("\n=== Test Summary ===")
    print("'Taking an OMEGA' condition implementation complete!")
    print("- Triggers on: IS taking omega-3 supplements AND omega 6:3 ratio >4:1")
    print("- Message: You're supplementing but not reaching optimal ratios - upgrade quality/dosing")
    print("- Recommends: High-potency triglyceride-based supplements, increase to 2 caps 2x/day")
    print("- Brands: Sports Research, Nordic Naturals Pro-Omega 2000, Ultimate Omega 2X")
    print("- Clinical insight: Addresses clients who think they're covered but need optimization")

if __name__ == "__main__":
    test_taking_omega_condition() 