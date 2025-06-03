#!/usr/bin/env python3

"""
Test script for magnesium optimal condition (quick-MagRBC-optimal)
Verifies that optimal magnesium levels display the correct message.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_magnesium_optimal_condition():
    """Test optimal magnesium condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Magnesium Optimal (quick-MagRBC-optimal) Condition ===\n")
    
    # Test Case 1: Optimal magnesium (5.2 mg/dL - exactly at threshold)
    print("🧪 Test Case 1: Optimal Magnesium (5.2 mg/dL)")
    lab_results_1 = {'MIN_MG_RBC': 5.2}
    hhq_responses_1 = {}
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, hhq_responses_1)
    
    print(f"   quick-MagRBC: {processed_1.get('quick-MagRBC')} (should be 5.2)")
    print(f"   quick-MagRBC-optimal: {processed_1.get('quick-MagRBC-optimal')} (should be True)")
    print(f"   quick-MagRBC-low: {processed_1.get('quick-MagRBC-low')} (should be False/None)")
    print()
    
    # Test Case 2: High optimal magnesium (6.0 mg/dL)
    print("🧪 Test Case 2: High Optimal Magnesium (6.0 mg/dL)")
    lab_results_2 = {'MIN_MG_RBC': 6.0}
    hhq_responses_2 = {}
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, hhq_responses_2)
    
    print(f"   quick-MagRBC: {processed_2.get('quick-MagRBC')} (should be 6.0)")
    print(f"   quick-MagRBC-optimal: {processed_2.get('quick-MagRBC-optimal')} (should be True)")
    print(f"   quick-MagRBC-low: {processed_2.get('quick-MagRBC-low')} (should be False/None)")
    print()
    
    # Test Case 3: Integration test with full roadmap
    print("🧪 Test Case 3: Full Roadmap Integration Test")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_2, hhq_responses_2)
        
        # Check for optimal magnesium content
        optimal_content_found = "This level falls within the optimal parameters and no additional intervention is recommended" in roadmap
        mag_value_found = "6.0" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Optimal magnesium content found: {optimal_content_found}")
        print(f"   Magnesium value displayed: {mag_value_found}")
        
        if optimal_content_found:
            print("   🎉 Optimal magnesium condition working correctly!")
        else:
            print("   ⚠️ Optimal magnesium content not found - checking roadmap...")
            
            # Show magnesium section
            lines = roadmap.split('\n')
            mag_section = []
            in_mag_section = False
            
            for line in lines:
                if "magnesium" in line.lower() or "MAGNESIUM" in line:
                    in_mag_section = True
                    mag_section.append(line)
                elif in_mag_section and line.strip() == "":
                    break
                elif in_mag_section:
                    mag_section.append(line)
                    
            print("\n   📄 Magnesium Section Found:")
            for line in mag_section[:5]:  # Show first 5 lines
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    print()
    print("✅ Magnesium optimal condition testing complete!")

if __name__ == "__main__":
    test_magnesium_optimal_condition() 