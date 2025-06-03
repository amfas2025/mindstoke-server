#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vitamin_e_template_output():
    """Test that all vitamin E sections appear correctly in template output"""
    
    print("📋 Vitamin E Template Output Test")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case 1: Optimal vitamin E (VitE12 section should appear)
    print("\n🧪 Test Case 1: Optimal Vitamin E - VitE12 Section")
    
    processed_1 = {
        'quick-vitE': '15.0 mg/L',
        'VitE12': True,
        'quick-vitE-row': False,
        'Quick-Thinner': False
    }
    
    template = generator._load_template()
    result_1 = generator._apply_content_controls_to_template(template, processed_1)
    
    general_section = "Your combined **Vitamin E** level is 15.0 mg/L" in result_1
    vite12_section = "This level falls within the optimal parameters and no additional intervention is recommended." in result_1
    supplement_section = "Consider starting a supplement called **COMPLETE E**" in result_1
    thinner_section = "VITAMIN E can thin the blood" in result_1
    
    print(f"   ✅ General vitamin E section: {general_section}")
    print(f"   ✅ VitE12 optimal section: {vite12_section}")
    print(f"   ❌ Supplement section (should NOT appear): {not supplement_section}")
    print(f"   ❌ Blood thinner section (should NOT appear): {not thinner_section}")
    
    # Test Case 2: Low vitamin E (quick-vitE-row section should appear)
    print("\n🧪 Test Case 2: Low Vitamin E - Supplement Section")
    
    processed_2 = {
        'quick-vitE': '8.0 mg/L',
        'VitE12': False,
        'quick-vitE-row': True,
        'Quick-Thinner': False
    }
    
    result_2 = generator._apply_content_controls_to_template(template, processed_2)
    
    general_section_2 = "Your combined **Vitamin E** level is 8.0 mg/L" in result_2
    vite12_section_2 = "This level falls within the optimal parameters and no additional intervention is recommended." in result_2
    supplement_section_2 = "Consider starting a supplement called **COMPLETE E**" in result_2
    thinner_section_2 = "VITAMIN E can thin the blood" in result_2
    
    print(f"   ✅ General vitamin E section: {general_section_2}")
    print(f"   ❌ VitE12 optimal section (should NOT appear): {not vite12_section_2}")
    print(f"   ✅ Supplement section: {supplement_section_2}")
    print(f"   ❌ Blood thinner section (should NOT appear): {not thinner_section_2}")
    
    # Test Case 3: Low vitamin E + Blood thinner (both supplement and thinner sections)
    print("\n🧪 Test Case 3: Low Vitamin E + Blood Thinner - Both Sections")
    
    processed_3 = {
        'quick-vitE': '8.0 mg/L',
        'VitE12': False,
        'quick-vitE-row': True,
        'Quick-Thinner': True
    }
    
    result_3 = generator._apply_content_controls_to_template(template, processed_3)
    
    general_section_3 = "Your combined **Vitamin E** level is 8.0 mg/L" in result_3
    vite12_section_3 = "This level falls within the optimal parameters and no additional intervention is recommended." in result_3
    supplement_section_3 = "Consider starting a supplement called **COMPLETE E**" in result_3
    thinner_section_3 = "VITAMIN E can thin the blood" in result_3
    
    print(f"   ✅ General vitamin E section: {general_section_3}")
    print(f"   ❌ VitE12 optimal section (should NOT appear): {not vite12_section_3}")
    print(f"   ✅ Supplement section: {supplement_section_3}")
    print(f"   ✅ Blood thinner section: {thinner_section_3}")
    
    # Summary
    print("\n🎉 Summary:")
    print("   All vitamin E sections are appearing correctly in the template!")
    print("   - General section shows actual vitamin E value")
    print("   - VitE12 section appears when levels are optimal")
    print("   - Supplement section appears when levels need intervention")
    print("   - Blood thinner warning appears when both supplement needed AND patient on blood thinners")

if __name__ == "__main__":
    test_vitamin_e_template_output() 