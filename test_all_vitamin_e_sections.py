#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_all_vitamin_e_sections():
    """Comprehensive test for all vitamin E sections"""
    
    print("🧪 Testing All Vitamin E Sections")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    ranges = generator._get_comprehensive_lab_ranges()
    
    # Test Case 1: Optimal vitamin E (no supplementation needed)
    print("\n🧪 Test Case 1: Optimal Vitamin E Level (15 mg/L)")
    
    labs_1 = {'VIT_E': 15.0}
    hhq_1 = {}
    
    processed_1 = generator._process_nutrient_markers(labs_1, hhq_1, ranges)
    
    print(f"   quick-vitE: {processed_1.get('quick-vitE')}")
    print(f"   VitE12: {processed_1.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_1.get('quick-vitE-row')} (should be False)")
    print(f"   Quick-Thinner: {processed_1.get('Quick-Thinner')} (should be False)")
    
    # Test Case 2: Low vitamin E (supplementation needed)
    print("\n🧪 Test Case 2: Low Vitamin E Level (8 mg/L)")
    
    labs_2 = {'VIT_E': 8.0}
    hhq_2 = {}
    
    processed_2 = generator._process_nutrient_markers(labs_2, hhq_2, ranges)
    
    print(f"   quick-vitE: {processed_2.get('quick-vitE')}")
    print(f"   VitE12: {processed_2.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_2.get('quick-vitE-row')} (should be True)")
    print(f"   Quick-Thinner: {processed_2.get('Quick-Thinner')} (should be False)")
    
    # Test Case 3: Low vitamin E + Blood thinner (caution needed)
    print("\n🧪 Test Case 3: Low Vitamin E + Blood Thinner (8 mg/L)")
    
    labs_3 = {'VIT_E': 8.0}
    hhq_3 = {'hh_blood_thinner': True}
    
    processed_3 = generator._process_nutrient_markers(labs_3, hhq_3, ranges)
    
    print(f"   quick-vitE: {processed_3.get('quick-vitE')}")
    print(f"   VitE12: {processed_3.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_3.get('quick-vitE-row')} (should be True)")
    print(f"   Quick-Thinner: {processed_3.get('Quick-Thinner')} (should be True)")
    
    # Test Case 4: High vitamin E (supplementation needed)
    print("\n🧪 Test Case 4: High Vitamin E Level (25 mg/L)")
    
    labs_4 = {'VIT_E': 25.0}
    hhq_4 = {}
    
    processed_4 = generator._process_nutrient_markers(labs_4, hhq_4, ranges)
    
    print(f"   quick-vitE: {processed_4.get('quick-vitE')}")
    print(f"   VitE12: {processed_4.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_4.get('quick-vitE-row')} (should be True)")
    print(f"   Quick-Thinner: {processed_4.get('Quick-Thinner')} (should be False)")
    
    # Test Case 5: Optimal vitamin E + Blood thinner (no interaction)
    print("\n🧪 Test Case 5: Optimal Vitamin E + Blood Thinner (15 mg/L)")
    
    labs_5 = {'VIT_E': 15.0}
    hhq_5 = {'hh_blood_thinner': True}
    
    processed_5 = generator._process_nutrient_markers(labs_5, hhq_5, ranges)
    
    print(f"   quick-vitE: {processed_5.get('quick-vitE')}")
    print(f"   VitE12: {processed_5.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_5.get('quick-vitE-row')} (should be False)")
    print(f"   Quick-Thinner: {processed_5.get('Quick-Thinner')} (should be False)")
    
    # Test Case 6: No vitamin E data
    print("\n🧪 Test Case 6: No Vitamin E Data")
    
    labs_6 = {}
    hhq_6 = {}
    
    processed_6 = generator._process_nutrient_markers(labs_6, hhq_6, ranges)
    
    print(f"   quick-vitE: {processed_6.get('quick-vitE')}")
    print(f"   VitE12: {processed_6.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_6.get('quick-vitE-row')} (should be False)")
    print(f"   Quick-Thinner: {processed_6.get('Quick-Thinner')} (should be False)")
    
    print("\n✅ Logic Summary:")
    print("   - VitE12: True when vitamin E is optimal (12-20 mg/L)")
    print("   - quick-vitE-row: True when vitamin E is outside optimal range")
    print("   - Quick-Thinner: True when quick-vitE-row is True AND patient takes blood thinners")
    print("   - quick-vitE: Always shows actual value when available")

if __name__ == "__main__":
    test_all_vitamin_e_sections() 