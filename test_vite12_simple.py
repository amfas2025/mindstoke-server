#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vite12_simple():
    """Simple test for VitE12 logic in _process_nutrient_markers"""
    
    print("🧪 Testing VitE12 Logic (Simple)")
    print("=" * 50)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Get the ranges
    ranges = generator._get_comprehensive_lab_ranges()
    
    # Test Case 1: Optimal vitamin E level (15 mg/L - within 12-20 range)
    print("\n🧪 Test Case 1: Optimal Vitamin E Level (15 mg/L)")
    
    labs_1 = {'VIT_E': 15.0}
    hhq_1 = {}
    
    processed_1 = generator._process_nutrient_markers(labs_1, hhq_1, ranges)
    
    print(f"   Content Control VitE12: {processed_1.get('VitE12')}")
    print(f"   Content Control quick-vitE: {processed_1.get('quick-vitE')}")
    print(f"   Expected VitE12: True (15 is within 12-20 range)")
    
    # Test Case 2: Low vitamin E level (8 mg/L - below optimal range)
    print("\n🧪 Test Case 2: Low Vitamin E Level (8 mg/L)")
    
    labs_2 = {'VIT_E': 8.0}
    hhq_2 = {}
    
    processed_2 = generator._process_nutrient_markers(labs_2, hhq_2, ranges)
    
    print(f"   Content Control VitE12: {processed_2.get('VitE12')}")
    print(f"   Content Control quick-vitE: {processed_2.get('quick-vitE')}")
    print(f"   Expected VitE12: False (8 is below 12)")
    
    # Test Case 3: High vitamin E level (25 mg/L - above optimal range)
    print("\n🧪 Test Case 3: High Vitamin E Level (25 mg/L)")
    
    labs_3 = {'VIT_E': 25.0}
    hhq_3 = {}
    
    processed_3 = generator._process_nutrient_markers(labs_3, hhq_3, ranges)
    
    print(f"   Content Control VitE12: {processed_3.get('VitE12')}")
    print(f"   Content Control quick-vitE: {processed_3.get('quick-vitE')}")
    print(f"   Expected VitE12: False (25 is above 20)")
    
    # Test Case 4: Borderline cases
    print("\n🧪 Test Case 4: Borderline Cases")
    
    for vit_e_val in [12.0, 20.0]:
        labs = {'VIT_E': vit_e_val}
        processed = generator._process_nutrient_markers(labs, {}, ranges)
        print(f"   VitE={vit_e_val}: VitE12={processed.get('VitE12')} (should be True)")
    
    # Test Case 5: Check the ranges being used
    print("\n📋 Range Information:")
    vit_e_range = ranges.get('VitE', {})
    print(f"   Vitamin E optimal_min: {vit_e_range.get('optimal_min')}")
    print(f"   Vitamin E optimal_max: {vit_e_range.get('optimal_max')}")
    
    # Summary
    print("\n✅ Logic Test Summary:")
    print("   - VitE12 should be True when vitamin E is between 12-20 mg/L")
    print("   - VitE12 should be False when vitamin E is outside 12-20 mg/L")
    print("   - quick-vitE should show the actual value with units when available")

if __name__ == "__main__":
    test_vite12_simple() 