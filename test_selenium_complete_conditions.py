#!/usr/bin/env python3

"""
Test script for complete selenium condition hierarchy
Tests all three selenium conditions: quick-selenium, Selenium125, quick-selen-110
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_complete_selenium_conditions():
    """Test all selenium condition variations"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Complete Selenium Condition Hierarchy ===\n")
    
    # Test Case 1: Very low selenium (<110) - should trigger quick-selen-110 with CLEAR WAY COFACTORS
    print("🧪 Test Case 1: Very Low Selenium (95 ug/L) - CLEAR WAY COFACTORS")
    lab_results_1 = {
        'MIN_SE': 95  # Below 110 threshold
    }
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-selenium: {processed_1.get('quick-selenium')} (should be 95)")
    print(f"   quick-selenium-low: {processed_1.get('quick-selenium-low')} (should be True)")
    print(f"   quick-selen-110: {processed_1.get('quick-selen-110')} (should be True)")
    print(f"   quick-selenium-optimal: {processed_1.get('quick-selenium-optimal')} (should be False/None)")
    print(f"   Selenium125: {processed_1.get('Selenium125')} (should be False/None)")
    print()
    
    # Test Case 2: Low selenium (110-124) - should trigger selenium-low but NOT quick-selen-110
    print("🧪 Test Case 2: Low Selenium (115 ug/L) - Standard supplementation")
    lab_results_2 = {
        'MIN_SE': 115  # Above 110 but below 125
    }
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-selenium: {processed_2.get('quick-selenium')} (should be 115)")
    print(f"   quick-selenium-low: {processed_2.get('quick-selenium-low')} (should be True)")
    print(f"   quick-selen-110: {processed_2.get('quick-selen-110')} (should be False/None)")
    print(f"   quick-selenium-optimal: {processed_2.get('quick-selenium-optimal')} (should be False/None)")
    print(f"   Selenium125: {processed_2.get('Selenium125')} (should be False/None)")
    print()
    
    # Test Case 3: Optimal selenium (≥125) - should trigger both optimal conditions
    print("🧪 Test Case 3: Optimal Selenium (150 ug/L) - No intervention")
    lab_results_3 = {
        'MIN_SE': 150  # Above 125 threshold
    }
    hhq_responses_3 = {}
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print(f"   quick-selenium: {processed_3.get('quick-selenium')} (should be 150)")
    print(f"   quick-selenium-low: {processed_3.get('quick-selenium-low')} (should be False/None)")
    print(f"   quick-selen-110: {processed_3.get('quick-selen-110')} (should be False/None)")
    print(f"   quick-selenium-optimal: {processed_3.get('quick-selenium-optimal')} (should be True)")
    print(f"   Selenium125: {processed_3.get('Selenium125')} (should be True)")
    print()
    
    # Test Case 4: Borderline cases
    print("🧪 Test Case 4: Borderline Cases")
    
    # Exactly 125 - should be optimal
    processed_125 = generator._process_all_content_controls(client_data, {'MIN_SE': 125}, {})
    print(f"   Selenium 125: optimal={processed_125.get('quick-selenium-optimal')}, Selenium125={processed_125.get('Selenium125')}")
    
    # Exactly 110 - should NOT trigger quick-selen-110
    processed_110 = generator._process_all_content_controls(client_data, {'MIN_SE': 110}, {})
    print(f"   Selenium 110: low={processed_110.get('quick-selenium-low')}, selen-110={processed_110.get('quick-selen-110')}")
    
    # Just below 110 - should trigger quick-selen-110
    processed_109 = generator._process_all_content_controls(client_data, {'MIN_SE': 109}, {})
    print(f"   Selenium 109: low={processed_109.get('quick-selenium-low')}, selen-110={processed_109.get('quick-selen-110')}")
    print()
    
    # Test Case 5: Full roadmap integration test
    print("🧪 Test Case 5: Full Roadmap Integration (Very Low Selenium)")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_1, hhq_responses_1)
        
        # Check for all selenium content variations
        selenium_header_found = "Selenium Optimization" in roadmap
        selenium_level_found = "Selenium** level is 95" in roadmap
        optimal_threshold_found = "The optimal is > 125 ug/L" in roadmap
        clear_way_cofactors_found = "CLEAR WAY COFACTORS 2 capsules/day" in roadmap
        functional_selenium_found = "functional SELENIUM level" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Selenium header found: {selenium_header_found}")
        print(f"   Selenium level display found: {selenium_level_found}")
        print(f"   Optimal threshold mentioned: {optimal_threshold_found}")
        print(f"   CLEAR WAY COFACTORS found: {clear_way_cofactors_found}")
        print(f"   Functional selenium text found: {functional_selenium_found}")
        
        if all([selenium_header_found, selenium_level_found, optimal_threshold_found, 
                clear_way_cofactors_found, functional_selenium_found]):
            print("   🎉 All selenium condition hierarchy working correctly!")
        else:
            print("   ⚠️ Some selenium content missing - checking roadmap...")
            
            # Show selenium section
            lines = roadmap.split('\n')
            selenium_section = []
            in_selenium_section = False
            
            for line in lines:
                if "Selenium" in line and ("Optimization" in line or "level is" in line):
                    in_selenium_section = True
                    selenium_section.append(line)
                elif in_selenium_section and line.strip() == "" and len(selenium_section) > 8:
                    break
                elif in_selenium_section:
                    selenium_section.append(line)
                    
            print("\n   📄 Complete Selenium Section Found:")
            for line in selenium_section:
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    # Test Case 6: Optimal selenium roadmap integration
    print("\n🧪 Test Case 6: Optimal Selenium Roadmap Check")
    try:
        roadmap_optimal = generator.generate_roadmap(client_data_full, lab_results_3, hhq_responses_3)
        
        optimal_message_found = "optimal parameters and no additional intervention" in roadmap_optimal
        selenium125_found = "Selenium125" in roadmap_optimal or "optimal parameters" in roadmap_optimal
        
        print(f"   Optimal message found: {optimal_message_found}")
        print(f"   Selenium125 condition working: {selenium125_found}")
        
    except Exception as e:
        print(f"   ❌ Error generating optimal roadmap: {e}")
    
    print()
    print("✅ Complete selenium condition hierarchy testing complete!")

if __name__ == "__main__":
    test_complete_selenium_conditions() 