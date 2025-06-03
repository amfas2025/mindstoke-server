#!/usr/bin/env python3

"""
Test script for enhanced zinc-liposomalC condition 
Tests the advanced treatment protocol for significantly elevated C:Z ratios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_zinc_liposomal_condition():
    """Test zinc-liposomalC enhanced condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Enhanced Zinc-Liposomal C (zinc-liposomalC) Condition ===\n")
    
    # Test Case 1: Significantly elevated ratio (>1.8) - should trigger liposomal protocol
    print("🧪 Test Case 1: Significantly Elevated C:Z Ratio (2.1)")
    lab_results_1 = {
        'MIN_CU': 168,  # Copper 168 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 168/80 = 2.1 (significantly elevated)
    }
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-CZratio-14: {processed_1.get('quick-CZratio-14')} (should be 2.1)")
    print(f"   quick-CZratio-14-elevated: {processed_1.get('quick-CZratio-14-elevated')} (should be True)")
    print(f"   zinc-liposomalC: {processed_1.get('zinc-liposomalC')} (should be True)")
    print()
    
    # Test Case 2: Moderately elevated ratio (1.5-1.8) - should not trigger liposomal protocol
    print("🧪 Test Case 2: Moderately Elevated C:Z Ratio (1.6)")
    lab_results_2 = {
        'MIN_CU': 128,  # Copper 128 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 128/80 = 1.6 (moderately elevated)
    }
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-CZratio-14: {processed_2.get('quick-CZratio-14')} (should be 1.6)")
    print(f"   quick-CZratio-14-elevated: {processed_2.get('quick-CZratio-14-elevated')} (should be True)")
    print(f"   zinc-liposomalC: {processed_2.get('zinc-liposomalC')} (should be False/None)")
    print()
    
    # Test Case 3: Borderline for liposomal protocol (exactly 1.8)
    print("🧪 Test Case 3: Borderline for Enhanced Protocol (1.8)")
    lab_results_3 = {
        'MIN_CU': 144,  # Copper 144 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 144/80 = 1.8 (borderline)
    }
    hhq_responses_3 = {}
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, hhq_responses_3)
    
    print(f"   quick-CZratio-14: {processed_3.get('quick-CZratio-14')} (should be 1.8)")
    print(f"   quick-CZratio-14-elevated: {processed_3.get('quick-CZratio-14-elevated')} (should be True)")
    print(f"   zinc-liposomalC: {processed_3.get('zinc-liposomalC')} (should be False/None, threshold is >1.8)")
    print()
    
    # Test Case 4: Very high ratio (>2.0) - should definitely trigger liposomal protocol
    print("🧪 Test Case 4: Very High C:Z Ratio (2.5)")
    lab_results_4 = {
        'MIN_CU': 200,  # Copper 200 μg/dL
        'MIN_ZN': 80    # Zinc 80 μg/dL
        # Ratio = 200/80 = 2.5 (very high)
    }
    hhq_responses_4 = {}
    
    processed_4 = generator._process_all_content_controls(client_data, lab_results_4, hhq_responses_4)
    
    print(f"   quick-CZratio-14: {processed_4.get('quick-CZratio-14')} (should be 2.5)")
    print(f"   quick-CZratio-14-elevated: {processed_4.get('quick-CZratio-14-elevated')} (should be True)")
    print(f"   zinc-liposomalC: {processed_4.get('zinc-liposomalC')} (should be True)")
    print()
    
    # Test Case 5: Full roadmap integration test with liposomal protocol
    print("🧪 Test Case 5: Full Roadmap Integration Test (Liposomal Protocol)")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_1, hhq_responses_1)
        
        # Check for enhanced protocol content
        ratio_display_found = "Your **C:Z RATIO** is 2.1" in roadmap
        enhanced_protocol_found = "Enhanced Copper-Zinc Protocol" in roadmap
        liposomal_vitamin_c_found = "LIPOSOMAL VITAMIN C + R-LIPOIC ACID 4 pumps daily" in roadmap
        enhanced_explanation_found = "liposomal delivery system provides superior absorption" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Ratio display found: {ratio_display_found}")
        print(f"   Enhanced protocol header found: {enhanced_protocol_found}")
        print(f"   Liposomal vitamin C recommendation found: {liposomal_vitamin_c_found}")
        print(f"   Enhanced explanation found: {enhanced_explanation_found}")
        
        if all([ratio_display_found, enhanced_protocol_found, liposomal_vitamin_c_found, enhanced_explanation_found]):
            print("   🎉 All zinc-liposomalC content controls working correctly!")
        else:
            print("   ⚠️ Some zinc-liposomalC content missing - checking roadmap...")
            
            # Show copper to zinc section
            lines = roadmap.split('\n')
            cz_section = []
            in_cz_section = False
            
            for line in lines:
                if "C:Z RATIO" in line or "Copper to Zinc" in line or "Enhanced Copper-Zinc" in line:
                    in_cz_section = True
                    cz_section.append(line)
                elif in_cz_section and line.strip() == "" and len(cz_section) > 5:
                    break
                elif in_cz_section:
                    cz_section.append(line)
                    
            print("\n   📄 Enhanced Copper to Zinc Section Found:")
            for line in cz_section[:15]:  # Show first 15 lines
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    print()
    print("✅ Enhanced zinc-liposomalC condition testing complete!")

if __name__ == "__main__":
    test_zinc_liposomal_condition() 