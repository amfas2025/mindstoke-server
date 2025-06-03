#!/usr/bin/env python3

"""
Test script for omega-neurological-suboptimal condition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_neurological_omega_condition():
    """Test omega-neurological-suboptimal condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Neurological Omega-3 Optimization Condition ===\n")
    
    # Test Case 1: Low OmegaCheck (should trigger)
    print("Test Case 1: Low OmegaCheck <6.0 (SHOULD TRIGGER)")
    hhq_responses_1 = {
        'hh_stress': True  # No neurological symptoms
    }
    
    lab_results_1 = {
        'OMEGA_CHECK': 4.5,  # Low omega status
        'VIT_D25': 45.0
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    triggered_1 = processed_1.get('omega-neurological-suboptimal', False)
    print(f"Condition triggered: {triggered_1}")
    
    if triggered_1:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        if 'Neurological Omega-3 Optimization:' in roadmap_1 and 'PHYTO BRAIN-E' in roadmap_1:
            print("✅ Template content found - PASS")
            
            # Check for key content elements
            content_checks = [
                'Neurological Omega-3 Optimization:',
                'quite suboptimal for neurological functioning',
                'Triple Strength OMEGA-3 FISH OIL',
                'Sports Research (Costco)',
                'PRO-OMEGA 2000',
                'ULTIMATE OMEGA 2X',
                'Nordic Naturals',
                'maintenance dose is 3 capsules daily',
                'PHYTO BRAIN-E',
                '1-2 tsp, 2x\'s/day',
                'concentrated amount of DHA',
                'head trauma or neurodegenerative disease'
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
    
    # Test Case 2: Brain fog symptoms (should trigger)
    print("Test Case 2: Brain fog symptoms (SHOULD TRIGGER)")
    hhq_responses_2 = {
        'hh_brain_fog': True
    }
    
    lab_results_2 = {
        'OMEGA_CHECK': 7.0,  # Normal omega status but symptoms should trigger
        'VIT_D25': 45.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    triggered_2 = processed_2.get('omega-neurological-suboptimal', False)
    print(f"Condition triggered: {triggered_2}")
    print("✅ Brain fog triggers condition - PASS" if triggered_2 else "❌ Brain fog should trigger - FAIL")
    
    print()
    
    # Test Case 3: Memory problems (should trigger)
    print("Test Case 3: Memory problems (SHOULD TRIGGER)")
    hhq_responses_3 = {
        'hh_memory_problems': True
    }
    
    lab_results_3 = {
        'OMEGA_CHECK': 8.0,  # High omega but symptoms should trigger
        'VIT_D25': 45.0
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    triggered_3 = processed_3.get('omega-neurological-suboptimal', False)
    print(f"Condition triggered: {triggered_3}")
    print("✅ Memory problems trigger condition - PASS" if triggered_3 else "❌ Memory problems should trigger - FAIL")
    
    print()
    
    # Test Case 4: Head injury (should trigger)
    print("Test Case 4: Head injury (SHOULD TRIGGER)")
    hhq_responses_4 = {
        'hh_concussion': True
    }
    
    lab_results_4 = {
        'OMEGA_CHECK': 9.0,  # High omega but head injury should trigger
        'VIT_D25': 45.0
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    triggered_4 = processed_4.get('omega-neurological-suboptimal', False)
    print(f"Condition triggered: {triggered_4}")
    print("✅ Head injury triggers condition - PASS" if triggered_4 else "❌ Head injury should trigger - FAIL")
    
    print()
    
    # Test Case 5: Neither low omega nor neurological symptoms (should NOT trigger)
    print("Test Case 5: Good omega status and no neurological symptoms (should NOT trigger)")
    hhq_responses_5 = {
        'hh_stress': True,  # Non-neurological symptom
        'hh_fatigue': True
    }
    
    lab_results_5 = {
        'OMEGA_CHECK': 7.5,  # Good omega status
        'VIT_D25': 45.0
    }
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, hhq_responses_5)
    triggered_5 = processed_5.get('omega-neurological-suboptimal', False)
    print(f"Condition triggered: {triggered_5}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_5 else "❌ Should not trigger - FAIL")
    
    print()
    
    # Test Case 6: Show generated content sample
    if triggered_1:
        print("=== Sample Generated Content ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results_1, hhq_responses_1)
        
        # Extract neurological omega section
        lines = roadmap_sample.split('\n')
        in_section = False
        section_lines = []
        
        for line in lines:
            if 'Neurological Omega-3 Optimization:' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() == '':
                break
            elif in_section:
                section_lines.append(line)
        
        if section_lines:
            for line in section_lines:
                print(line)
    
    # Test Case 7: Multiple omega-3 conditions together
    print("\n=== Multiple Omega-3 Conditions Test ===")
    print("Test Case 7: Low omega + brain fog + concussion (multiple triggers)")
    hhq_responses_7 = {
        'hh_brain_fog': True,
        'hh_concussion': True,
        'hh_taking_krill_oil': True
    }
    
    lab_results_7 = {
        'OMEGA_CHECK': 3.8,       # Very low
        'OMEGA_6_3_RATIO': 12.0,  # Very high ratio
        'INFLAM_CRP': 1.2,        # Elevated
        'VIT_D25': 35.0
    }
    
    processed_7 = generator._process_all_content_controls(client_data, lab_results_7, hhq_responses_7)
    
    # Check multiple related omega conditions
    omega_conditions = [
        'omega-neurological-suboptimal',  # This condition
        'checked-omega-63-ratio',         # OMEGA-3 CHALLENGE
        'Quick-krill',                    # Krill oil advice
        'quick-CRP-09-omega-<5',         # CRP + omega compound
        'quick-brain-fog'                 # Brain fog
    ]
    
    print("Multiple omega-3 related conditions triggered:")
    for condition in omega_conditions:
        triggered = processed_7.get(condition, False)
        status = "✅ TRIGGERED" if triggered else "❌ Not triggered"
        print(f"  {condition}: {status}")
    
    print("\n=== Test Summary ===")
    print("Neurological Omega-3 Optimization condition implementation complete!")
    print("- Triggers on: OmegaCheck <6.0 OR neurological symptoms (brain fog, memory, head injury)")
    print("- Recommends: High-potency fish oil (3 caps daily) OR PHYTO BRAIN-E liquid (1-2 tsp, 2x/day)")
    print("- Special focus: DHA-concentrated liquid for head trauma/neurodegenerative disease")
    print("- Brands: Sports Research, Nordic Naturals Pro-Omega 2000, Ultimate Omega 2X")
    print("- Complements: Works alongside OMEGA-3 CHALLENGE and other omega conditions")

if __name__ == "__main__":
    test_neurological_omega_condition() 