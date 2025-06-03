#!/usr/bin/env python3

"""
Test script for CRP-Omega compound condition processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_crp_omega_compound():
    """Test CRP-omega compound condition logic"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing CRP-Omega Compound Condition ===\n")
    
    # Test Case 1: CRP >0.9 and OmegaCheck <5.4 (should trigger)
    print("Test Case 1: CRP = 1.2, OmegaCheck = 4.8 (SHOULD TRIGGER)")
    lab_results_1 = {
        'INFLAM_CRP': 1.2,
        'OMEGA_CHECK': 4.8
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, {})
    triggered_1 = processed_1.get('quick-CRP-09-omega-<5', False)
    print(f"Condition triggered: {triggered_1}")
    
    if triggered_1:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, {})
        if 'Triple Strength OMEGA-3 FISH OIL' in roadmap_1:
            print("✅ Template content found - PASS")
        else:
            print("❌ Template content missing - FAIL")
    else:
        print("❌ Condition not triggered - FAIL")
    
    print()
    
    # Test Case 2: CRP <0.9 (should NOT trigger)
    print("Test Case 2: CRP = 0.5, OmegaCheck = 4.8 (should NOT trigger)")
    lab_results_2 = {
        'INFLAM_CRP': 0.5,
        'OMEGA_CHECK': 4.8
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, {})
    triggered_2 = processed_2.get('quick-CRP-09-omega-<5', False)
    print(f"Condition triggered: {triggered_2}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_2 else "❌ Should not trigger - FAIL")
    
    print()
    
    # Test Case 3: OmegaCheck >5.4 (should NOT trigger)
    print("Test Case 3: CRP = 1.2, OmegaCheck = 6.0 (should NOT trigger)")
    lab_results_3 = {
        'INFLAM_CRP': 1.2,
        'OMEGA_CHECK': 6.0
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, {})
    triggered_3 = processed_3.get('quick-CRP-09-omega-<5', False)
    print(f"Condition triggered: {triggered_3}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_3 else "❌ Should not trigger - FAIL")
    
    print()
    
    # Test Case 4: Edge case - exactly at thresholds
    print("Test Case 4: CRP = 0.9, OmegaCheck = 5.4 (edge case - should NOT trigger)")
    lab_results_4 = {
        'INFLAM_CRP': 0.9,
        'OMEGA_CHECK': 5.4
    }
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, {})
    triggered_4 = processed_4.get('quick-CRP-09-omega-<5', False)
    print(f"Condition triggered: {triggered_4}")
    print("✅ Correctly NOT triggered - PASS" if not triggered_4 else "❌ Should not trigger - FAIL")
    
    print("\n=== Test Summary ===")
    print("CRP-Omega compound condition implementation complete!")
    print("- Logic: CRP >0.9 AND OmegaCheck <5.4")
    print("- Content: Comprehensive omega-3 supplementation recommendations")
    print("- Brands: Triple Strength OMEGA-3 FISH OIL, PRO-OMEGA 2000, ULTIMATE OMEGA 2X")
    print("- Dosing: 3 caps per day maintenance dose")

if __name__ == "__main__":
    test_crp_omega_compound() 