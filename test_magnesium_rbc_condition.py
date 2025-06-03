#!/usr/bin/env python3

"""
Test script for quick-MagRBC condition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_magnesium_rbc_condition():
    """Test quick-MagRBC condition logic and template content"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Magnesium RBC (quick-MagRBC) Condition ===\n")
    
    # Test Case 1: Low Magnesium RBC <5.2 (should trigger low)
    print("Test Case 1: Low Magnesium RBC <5.2 (SHOULD TRIGGER)")
    lab_results_1 = {
        'MIN_MG_RBC': 4.8,  # Below optimal of 5.2
        'VIT_D25': 45.0
    }
    
    processed_1 = generator._process_all_content_controls(client_data, lab_results_1, {})
    
    # Check what conditions are triggered
    mag_value = processed_1.get('quick-MagRBC', None)
    mag_low = processed_1.get('quick-MagRBC-low', False)
    mag_optimal = processed_1.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mag_value}")
    print(f"Low condition triggered: {mag_low}")
    print(f"Optimal condition triggered: {mag_optimal}")
    
    if mag_value and mag_low:
        # Test template processing
        roadmap_1 = generator.generate_roadmap(client_data, lab_results_1, {})
        if 'Magnesium RBC Optimization:' in roadmap_1 and 'MAGNESIUM THREONATE 2000 mg' in roadmap_1:
            print("✅ Template content found - PASS")
            
            # Check for key content elements
            content_checks = [
                'Magnesium RBC Optimization:',
                'baseline MAGNESIUM RBC level is 4.8',
                'optimal level is suggested to be > 5.2 mg/dL',
                'falls below the optimal parameters',
                'MAGNESIUM THREONATE 2000 mg at night',
                'cross the blood-brain barrier',
                'MAGNESIUM GLYCINATE',
                'MAGNESIUM TAURATE'
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
        print("❌ Condition not triggered properly - FAIL")
    
    print()
    
    # Test Case 2: Optimal Magnesium RBC >=5.2 (should trigger optimal)
    print("Test Case 2: Optimal Magnesium RBC >=5.2 (SHOULD TRIGGER OPTIMAL)")
    lab_results_2 = {
        'MIN_MG_RBC': 5.8,  # Above optimal of 5.2
        'VIT_D25': 45.0
    }
    
    processed_2 = generator._process_all_content_controls(client_data, lab_results_2, {})
    
    # Check what conditions are triggered
    mag_value_2 = processed_2.get('quick-MagRBC', None)
    mag_low_2 = processed_2.get('quick-MagRBC-low', False)
    mag_optimal_2 = processed_2.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mag_value_2}")
    print(f"Low condition triggered: {mag_low_2}")
    print(f"Optimal condition triggered: {mag_optimal_2}")
    
    if mag_value_2 and mag_optimal_2 and not mag_low_2:
        print("✅ Optimal condition triggered correctly - PASS")
        
        # Test template processing
        roadmap_2 = generator.generate_roadmap(client_data, lab_results_2, {})
        if 'within the optimal parameters' in roadmap_2:
            print("✅ Optimal template content found - PASS")
        else:
            print("❌ Optimal template content missing - FAIL")
    else:
        print("❌ Optimal condition not triggered properly - FAIL")
    
    print()
    
    # Test Case 3: No Magnesium RBC data (should not trigger)
    print("Test Case 3: No Magnesium RBC data (should NOT trigger)")
    lab_results_3 = {
        'VIT_D25': 45.0  # Only other lab data
    }
    
    processed_3 = generator._process_all_content_controls(client_data, lab_results_3, {})
    
    mag_value_3 = processed_3.get('quick-MagRBC', None)
    mag_low_3 = processed_3.get('quick-MagRBC-low', False)
    mag_optimal_3 = processed_3.get('quick-MagRBC-optimal', False)
    
    print(f"Magnesium RBC value stored: {mag_value_3}")
    print(f"Low condition triggered: {mag_low_3}")
    print(f"Optimal condition triggered: {mag_optimal_3}")
    
    if not mag_value_3 and not mag_low_3 and not mag_optimal_3:
        print("✅ Correctly NOT triggered when no data - PASS")
    else:
        print("❌ Should not trigger when no data - FAIL")
    
    print()
    
    # Test Case 4: Show generated content sample
    if mag_value and mag_low:
        print("=== Sample Generated Content (Low Magnesium) ===")
        roadmap_sample = generator.generate_roadmap(client_data, lab_results_1, {})
        
        # Extract Magnesium RBC section
        lines = roadmap_sample.split('\n')
        in_section = False
        section_lines = []
        
        for line in lines:
            if 'Magnesium RBC Optimization:' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() == '' and len(section_lines) > 3:
                break
            elif in_section:
                section_lines.append(line)
        
        if section_lines:
            for line in section_lines:
                print(line)
    
    print("\n=== Test Summary ===")
    print("Magnesium RBC (quick-MagRBC) condition implementation complete!")
    print("- Triggers on: Any Magnesium RBC lab value present")
    print("- Displays: Actual lab value with optimal reference (>5.2 mg/dL)")
    print("- Low condition: <5.2 mg/dL → MAGNESIUM THREONATE 2000mg recommendation")
    print("- Optimal condition: ≥5.2 mg/dL → No intervention needed")
    print("- Forms recommended: Magnesium Threonate (brain), Glycinate, Taurate")
    print("- Clinical focus: Blood-brain barrier penetration for neurological support")

if __name__ == "__main__":
    test_magnesium_rbc_condition() 