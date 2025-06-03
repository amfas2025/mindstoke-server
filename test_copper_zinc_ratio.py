#!/usr/bin/env python3

"""
Test script for copper to zinc ratio condition (quick-CZratio-14)
Tests: elevated ratio (>1.4) and optimal ratio (≤1.4)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_copper_zinc_ratio_condition():
    """Test copper to zinc ratio condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Copper to Zinc Ratio (quick-CZratio-14) Condition ===\n")
    
    # Test Case 1: Elevated ratio (>1.4) - should trigger intervention
    print("🧪 Test Case 1: Elevated C:Z Ratio (1.8)")
    lab_results_1 = {
        'MIN_CU': 144,  # Copper 144 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 144/80 = 1.8 (elevated)
    }
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-CZratio-14: {processed_1.get('quick-CZratio-14')} (should be 1.8)")
    print(f"   quick-CZratio-14-elevated: {processed_1.get('quick-CZratio-14-elevated')} (should be True)")
    print(f"   quick-CZratio-14-optimal: {processed_1.get('quick-CZratio-14-optimal')} (should be False/None)")
    print(f"   quick-copper: {processed_1.get('quick-copper')} (should be 144)")
    print(f"   quick-zinc: {processed_1.get('quick-zinc')} (should be 80)")
    print()
    
    # Test Case 2: Optimal ratio (≤1.4) - should show optimal message
    print("🧪 Test Case 2: Optimal C:Z Ratio (1.2)")
    lab_results_2 = {
        'MIN_CU': 96,   # Copper 96 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 96/80 = 1.2 (optimal)
    }
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-CZratio-14: {processed_2.get('quick-CZratio-14')} (should be 1.2)")
    print(f"   quick-CZratio-14-elevated: {processed_2.get('quick-CZratio-14-elevated')} (should be False/None)")
    print(f"   quick-CZratio-14-optimal: {processed_2.get('quick-CZratio-14-optimal')} (should be True)")
    print(f"   quick-copper: {processed_2.get('quick-copper')} (should be 96)")
    print(f"   quick-zinc: {processed_2.get('quick-zinc')} (should be 80)")
    print()
    
    # Test Case 3: Borderline elevated ratio (exactly 1.4) - should show optimal
    print("🧪 Test Case 3: Borderline C:Z Ratio (1.4)")
    lab_results_3 = {
        'MIN_CU': 112,  # Copper 112 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 112/80 = 1.4 (borderline)
    }
    hhq_responses_3 = {}
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print(f"   quick-CZratio-14: {processed_3.get('quick-CZratio-14')} (should be 1.4)")
    print(f"   quick-CZratio-14-elevated: {processed_3.get('quick-CZratio-14-elevated')} (should be False/None)")
    print(f"   quick-CZratio-14-optimal: {processed_3.get('quick-CZratio-14-optimal')} (should be True)")
    print()
    
    # Test Case 4: Missing zinc data - should not calculate ratio
    print("🧪 Test Case 4: Missing Zinc Data")
    lab_results_4 = {
        'MIN_CU': 120  # Copper only, no zinc
    }
    hhq_responses_4 = {}
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    
    print(f"   quick-CZratio-14: {processed_4.get('quick-CZratio-14')} (should be None)")
    print(f"   quick-CZratio-14-elevated: {processed_4.get('quick-CZratio-14-elevated')} (should be False/None)")
    print(f"   quick-CZratio-14-optimal: {processed_4.get('quick-CZratio-14-optimal')} (should be False/None)")
    print()
    
    # Test Case 5: Full roadmap integration test with elevated ratio
    print("🧪 Test Case 5: Full Roadmap Integration Test (Elevated Ratio)")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_1, hhq_responses_1)
        
        # Check for copper to zinc ratio content
        ratio_display_found = "Your **C:Z RATIO** is 1.8" in roadmap
        elevated_message_found = "is trending elevated" in roadmap
        zinc_recommendation_found = "ZINC PICCOLINATE 30-50 mg" in roadmap
        vitamin_c_recommendation_found = "VITAMIN C 500 mg/day" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Ratio display found: {ratio_display_found}")
        print(f"   Elevated message found: {elevated_message_found}")
        print(f"   Zinc recommendation found: {zinc_recommendation_found}")
        print(f"   Vitamin C recommendation found: {vitamin_c_recommendation_found}")
        
        if all([ratio_display_found, elevated_message_found, zinc_recommendation_found, vitamin_c_recommendation_found]):
            print("   🎉 All copper to zinc ratio content controls working correctly!")
        else:
            print("   ⚠️ Some copper to zinc ratio content missing - checking roadmap...")
            
            # Show copper to zinc section
            lines = roadmap.split('\n')
            cz_section = []
            in_cz_section = False
            
            for line in lines:
                if "C:Z RATIO" in line or "Copper to Zinc" in line:
                    in_cz_section = True
                    cz_section.append(line)
                elif in_cz_section and line.strip() == "":
                    break
                elif in_cz_section:
                    cz_section.append(line)
                    
            print("\n   📄 Copper to Zinc Section Found:")
            for line in cz_section[:10]:  # Show first 10 lines
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    print()
    print("✅ Copper to zinc ratio condition testing complete!")

if __name__ == "__main__":
    test_copper_zinc_ratio_condition() 