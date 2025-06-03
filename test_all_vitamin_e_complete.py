#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_all_vitamin_e_complete():
    """Comprehensive test for ALL vitamin E sections including elevated levels"""
    
    print("🧪 Testing Complete Vitamin E System")
    print("=" * 70)
    
    # Initialize generator
    generator = RoadmapGenerator()
    ranges = generator._get_comprehensive_lab_ranges()
    
    print(f"📋 Vitamin E Optimal Range: {ranges['VitE']['optimal_min']}-{ranges['VitE']['optimal_max']} mg/L")
    print(f"📋 Elevated Threshold: >30 mg/L")
    
    # Test Case 1: Very low vitamin E (supplementation needed)
    print("\n🧪 Test Case 1: Very Low Vitamin E Level (5 mg/L)")
    
    labs_1 = {'VIT_E': 5.0}
    hhq_1 = {}
    
    processed_1 = generator._process_nutrient_markers(labs_1, hhq_1, ranges)
    
    print(f"   quick-vitE: {processed_1.get('quick-vitE')}")
    print(f"   VitE12: {processed_1.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_1.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_1.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_1.get('Quick-Thinner')} (should be False)")
    
    # Test Case 2: Optimal vitamin E (no intervention)
    print("\n🧪 Test Case 2: Optimal Vitamin E Level (15 mg/L)")
    
    labs_2 = {'VIT_E': 15.0}
    hhq_2 = {}
    
    processed_2 = generator._process_nutrient_markers(labs_2, hhq_2, ranges)
    
    print(f"   quick-vitE: {processed_2.get('quick-vitE')}")
    print(f"   VitE12: {processed_2.get('VitE12')} (should be True)")
    print(f"   quick-vitE-row: {processed_2.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_2.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_2.get('Quick-Thinner')} (should be False)")
    
    # Test Case 3: Moderately high vitamin E (still needs adjustment)
    print("\n🧪 Test Case 3: Moderately High Vitamin E Level (25 mg/L)")
    
    labs_3 = {'VIT_E': 25.0}
    hhq_3 = {}
    
    processed_3 = generator._process_nutrient_markers(labs_3, hhq_3, ranges)
    
    print(f"   quick-vitE: {processed_3.get('quick-vitE')}")
    print(f"   VitE12: {processed_3.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_3.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_3.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_3.get('Quick-Thinner')} (should be False)")
    
    # Test Case 4: Dangerously elevated vitamin E (safety warning)
    print("\n🧪 Test Case 4: Dangerously Elevated Vitamin E Level (35 mg/L)")
    
    labs_4 = {'VIT_E': 35.0}
    hhq_4 = {}
    
    processed_4 = generator._process_nutrient_markers(labs_4, hhq_4, ranges)
    
    print(f"   quick-vitE: {processed_4.get('quick-vitE')}")
    print(f"   VitE12: {processed_4.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_4.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_4.get('quick-vitE-row-elevated')} (should be True)")
    print(f"   Quick-Thinner: {processed_4.get('Quick-Thinner')} (should be False)")
    
    # Test Case 5: Low vitamin E + Blood thinner (caution needed)
    print("\n🧪 Test Case 5: Low Vitamin E + Blood Thinner (8 mg/L)")
    
    labs_5 = {'VIT_E': 8.0}
    hhq_5 = {'hh_blood_thinner': True}
    
    processed_5 = generator._process_nutrient_markers(labs_5, hhq_5, ranges)
    
    print(f"   quick-vitE: {processed_5.get('quick-vitE')}")
    print(f"   VitE12: {processed_5.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_5.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_5.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_5.get('Quick-Thinner')} (should be True)")
    
    # Test Case 6: Elevated vitamin E + Blood thinner (no interaction warning)
    print("\n🧪 Test Case 6: Elevated Vitamin E + Blood Thinner (35 mg/L)")
    
    labs_6 = {'VIT_E': 35.0}
    hhq_6 = {'hh_blood_thinner': True}
    
    processed_6 = generator._process_nutrient_markers(labs_6, hhq_6, ranges)
    
    print(f"   quick-vitE: {processed_6.get('quick-vitE')}")
    print(f"   VitE12: {processed_6.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_6.get('quick-vitE-row')} (should be False)")
    print(f"   quick-vitE-row-elevated: {processed_6.get('quick-vitE-row-elevated')} (should be True)")
    print(f"   Quick-Thinner: {processed_6.get('Quick-Thinner')} (should be False - no supplement recommended)")
    
    # Test Case 7: Boundary test (exactly 30 mg/L)
    print("\n🧪 Test Case 7: Boundary Level (30 mg/L)")
    
    labs_7 = {'VIT_E': 30.0}
    hhq_7 = {}
    
    processed_7 = generator._process_nutrient_markers(labs_7, hhq_7, ranges)
    
    print(f"   quick-vitE: {processed_7.get('quick-vitE')}")
    print(f"   VitE12: {processed_7.get('VitE12')} (should be False)")
    print(f"   quick-vitE-row: {processed_7.get('quick-vitE-row')} (should be True)")
    print(f"   quick-vitE-row-elevated: {processed_7.get('quick-vitE-row-elevated')} (should be False)")
    print(f"   Quick-Thinner: {processed_7.get('Quick-Thinner')} (should be False)")
    
    print("\n✅ Complete Vitamin E Logic Summary:")
    print("   🟢 VitE12: True when 12-20 mg/L (optimal range)")
    print("   🟡 quick-vitE-row: True when <12, 20-30 mg/L (needs adjustment/supplementation)")
    print("   🔴 quick-vitE-row-elevated: True when >30 mg/L (dangerously high)")
    print("   ⚠️  Quick-Thinner: True when quick-vitE-row is True AND patient on blood thinners")
    print("   📊 quick-vitE: Always shows actual value when available")

if __name__ == "__main__":
    test_all_vitamin_e_complete() 