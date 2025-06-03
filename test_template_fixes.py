#!/usr/bin/env python3
"""
Test the fixed template processing
"""

import re
from roadmap_generator import RoadmapGenerator

def test_fixed_processing():
    """Test that the fixes resolve the template issues"""
    
    # Test data
    client_data = {
        'firstname': 'Sarah',
        'today': 'December 2, 2025', 
        'lab-date': 'October 15, 2024'
    }
    
    lab_results = {
        'genome-type': 'E3/E4',  # Should trigger ONLY E4 conditions
        'VIT_D25': 32,           # Should trigger ONLY D-30-39 condition
        'glutathione-level': 180
    }
    
    generator = RoadmapGenerator()
    roadmap = generator.generate_roadmap(client_data, lab_results, {})
    
    # Test 1: Client info replacement
    print("🧪 Testing Client Info Replacement")
    if '{{firstname}}' not in roadmap and 'Sarah' in roadmap:
        print("✅ Firstname replacement: FIXED")
    else:
        print("❌ Firstname replacement: STILL BROKEN")
    
    if '{{today}}' not in roadmap and 'December 2, 2025' in roadmap:
        print("✅ Today replacement: FIXED")
    else:
        print("❌ Today replacement: STILL BROKEN")
    
    # Test 2: APO E exclusive logic
    print("\n🧪 Testing APO E Exclusive Logic")
    apo_section = roadmap.split('## **MTHFR Genetics')[0]
    
    has_e4_risk = "greater risk of Alzheimer's" in apo_section
    has_non_e4 = "do not have the APO E genetic risk" in apo_section
    
    if has_e4_risk and not has_non_e4:
        print("✅ APO E logic: FIXED (only E4 messages)")
    elif not has_e4_risk and has_non_e4:
        print("✅ APO E logic: FIXED (only non-E4 messages)")
    else:
        print("❌ APO E logic: STILL BROKEN (conflicting messages)")
    
    # Test 3: Vitamin D exclusive dosing
    print("\n🧪 Testing Vitamin D Exclusive Dosing")
    
    # Debug: Show what vitamin D conditions are being set
    print("Debug - Vitamin D conditions set:")
    all_conditions = generator._process_all_content_controls(client_data, lab_results, {})
    vit_d_conditions = {k: v for k, v in all_conditions.items() 
                       if 'D-' in k or 'VitD' in k or 'vitD' in k}
    for condition, value in vit_d_conditions.items():
        print(f"  {condition}: {value}")
    
    # Also show parent conditions that might be affecting vitamin D
    parent_conditions = {k: v for k, v in all_conditions.items() 
                        if k in ['quick-vitD-simple', 'D-optimal', 'quick-VitD-row-takingD']}
    print("Debug - Parent vitamin D conditions:")
    for condition, value in parent_conditions.items():
        print(f"  {condition}: {value}")
    
    vit_d_doses = re.findall(r'(\d+,?\d*)\s*iu.*?VITAMIN D3', roadmap, re.IGNORECASE)
    unique_doses = set(vit_d_doses)
    
    if len(unique_doses) == 1:
        print(f"✅ Vitamin D dosing: FIXED (single recommendation: {unique_doses})")
    else:
        print(f"❌ Vitamin D dosing: STILL BROKEN (multiple: {unique_doses})")
    
    return roadmap

if __name__ == "__main__":
    test_fixed_processing()
    