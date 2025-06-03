#!/usr/bin/env python3

"""
Test script for selenium condition (quick-selenium)
Tests selenium level assessment and recommendations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_selenium_condition():
    """Test selenium condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Selenium (quick-selenium) Condition ===\n")
    
    # Test Case 1: Low selenium (<125 ug/L) - should trigger supplementation
    print("🧪 Test Case 1: Low Selenium Level (95 ug/L)")
    lab_results_1 = {
        'MIN_SE': 95  # Below optimal threshold of 125
    }
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-selenium: {processed_1.get('quick-selenium')} (should be 95)")
    print(f"   quick-selenium-low: {processed_1.get('quick-selenium-low')} (should be True)")
    print(f"   quick-selenium-optimal: {processed_1.get('quick-selenium-optimal')} (should be False/None)")
    print()
    
    # Test Case 2: Optimal selenium (≥125 ug/L) - should show optimal message
    print("🧪 Test Case 2: Optimal Selenium Level (150 ug/L)")
    lab_results_2 = {
        'MIN_SE': 150  # Above optimal threshold
    }
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-selenium: {processed_2.get('quick-selenium')} (should be 150)")
    print(f"   quick-selenium-low: {processed_2.get('quick-selenium-low')} (should be False/None)")
    print(f"   quick-selenium-optimal: {processed_2.get('quick-selenium-optimal')} (should be True)")
    print()
    
    # Test Case 3: Borderline selenium (exactly 125 ug/L) - should be optimal
    print("🧪 Test Case 3: Borderline Selenium Level (125 ug/L)")
    lab_results_3 = {
        'MIN_SE': 125  # Exactly at threshold
    }
    hhq_responses_3 = {}
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print(f"   quick-selenium: {processed_3.get('quick-selenium')} (should be 125)")
    print(f"   quick-selenium-low: {processed_3.get('quick-selenium-low')} (should be False/None)")
    print(f"   quick-selenium-optimal: {processed_3.get('quick-selenium-optimal')} (should be True)")
    print()
    
    # Test Case 4: Very low selenium (<70 ug/L) - should trigger supplementation
    print("🧪 Test Case 4: Very Low Selenium Level (55 ug/L)")
    lab_results_4 = {
        'MIN_SE': 55  # Very low
    }
    hhq_responses_4 = {}
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    
    print(f"   quick-selenium: {processed_4.get('quick-selenium')} (should be 55)")
    print(f"   quick-selenium-low: {processed_4.get('quick-selenium-low')} (should be True)")
    print(f"   quick-selenium-optimal: {processed_4.get('quick-selenium-optimal')} (should be False/None)")
    print()
    
    # Test Case 5: Missing selenium data - should not process
    print("🧪 Test Case 5: Missing Selenium Data")
    lab_results_5 = {
        'MIN_CU': 120  # Other data but no selenium
    }
    hhq_responses_5 = {}
    
    processed_5 = generator._process_all_content_controls(client_data, lab_results_5, hhq_responses_5)
    
    print(f"   quick-selenium: {processed_5.get('quick-selenium')} (should be None)")
    print(f"   quick-selenium-low: {processed_5.get('quick-selenium-low')} (should be False/None)")
    print(f"   quick-selenium-optimal: {processed_5.get('quick-selenium-optimal')} (should be False/None)")
    print()
    
    # Test Case 6: Full roadmap integration test with low selenium
    print("🧪 Test Case 6: Full Roadmap Integration Test (Low Selenium)")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_1, hhq_responses_1)
        
        # Check for selenium content
        selenium_header_found = "Selenium Optimization" in roadmap
        selenium_level_found = "Selenium** level is 95" in roadmap
        optimal_threshold_found = "The optimal is > 125 ug/L" in roadmap
        antioxidant_explanation_found = "helpful antioxidant and cofactor" in roadmap
        neurological_benefits_found = "reduce the risk of Alzheimer's disease and Parkinson's disease" in roadmap
        low_selenium_message_found = "too low for optimal neurological function" in roadmap
        supplementation_recommendation_found = "200 mcg daily of selenium" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Selenium header found: {selenium_header_found}")
        print(f"   Selenium level display found: {selenium_level_found}")
        print(f"   Optimal threshold mentioned: {optimal_threshold_found}")
        print(f"   Antioxidant explanation found: {antioxidant_explanation_found}")
        print(f"   Neurological benefits found: {neurological_benefits_found}")
        print(f"   Low selenium message found: {low_selenium_message_found}")
        print(f"   Supplementation recommendation found: {supplementation_recommendation_found}")
        
        if all([selenium_header_found, selenium_level_found, optimal_threshold_found, 
                antioxidant_explanation_found, neurological_benefits_found, 
                low_selenium_message_found, supplementation_recommendation_found]):
            print("   🎉 All selenium content controls working correctly!")
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
                elif in_selenium_section and line.strip() == "" and len(selenium_section) > 5:
                    break
                elif in_selenium_section:
                    selenium_section.append(line)
                    
            print("\n   📄 Selenium Section Found:")
            for line in selenium_section[:15]:  # Show first 15 lines
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    print()
    print("✅ Selenium condition testing complete!")

if __name__ == "__main__":
    test_selenium_condition() 