#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_all_vitamin_d_ranges():
    """Test all vitamin D ranges to ensure they're working correctly"""
    
    print("🧪 Comprehensive Vitamin D Range Test")
    print("=" * 50)
    
    # Test all vitamin D ranges
    test_cases = [
        (25, 'D-less-30 (deficient)'),
        (35, 'D-30-39 (insufficient)'),
        (45, 'D-40-49 (insufficient)'),
        (52, 'D-50-55 (close to optimal)'),
        (57, 'D-55-59 (very close to optimal)'),
        (65, 'D-optimal (optimal)')
    ]

    generator = RoadmapGenerator()
    all_passed = True

    for vit_d, expected_range in test_cases:
        client_data = {
            'full_name': 'Test Patient', 
            'date_of_birth': '1980-01-01', 
            'email': 'test@example.com'
        }
        lab_results = {'VIT_D25': float(vit_d)}
        
        processed = generator._process_all_content_controls(client_data, lab_results, {})
        roadmap = generator.generate_roadmap(client_data, lab_results, {})
        
        # Check which sections are active
        active_sections = []
        if processed.get('D-less-30'): active_sections.append('D-less-30')
        if processed.get('D-30-39'): active_sections.append('D-30-39')
        if processed.get('D-40-49'): active_sections.append('D-40-49')
        if processed.get('D-50-55'): active_sections.append('D-50-55')
        if processed.get('D-55-59'): active_sections.append('D-55-59')
        if processed.get('D-optimal'): active_sections.append('D-optimal')
        
        print(f"Vitamin D {vit_d} ng/mL ({expected_range}):")
        print(f"  Active sections: {active_sections}")
        print(f"  quick-VitD-row: {processed.get('quick-VitD-row', False)}")
        
        # Verify expected sections
        expected_active = []
        if vit_d < 30:
            expected_active = ['D-less-30']
        elif vit_d < 40:
            expected_active = ['D-30-39']
        elif vit_d < 50:
            expected_active = ['D-40-49']
        elif vit_d <= 55:
            expected_active = ['D-50-55']
        elif vit_d < 60:
            expected_active = ['D-55-59']
        else:
            expected_active = ['D-optimal']
        
        if set(active_sections) == set(expected_active):
            print(f"  ✅ PASS - Expected sections active")
        else:
            print(f"  ❌ FAIL - Expected {expected_active}, got {active_sections}")
            all_passed = False
        
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL VITAMIN D RANGES WORKING CORRECTLY!")
    else:
        print("❌ Some vitamin D ranges have issues")
    
    return all_passed

if __name__ == "__main__":
    test_all_vitamin_d_ranges() 