#!/usr/bin/env python3
"""
Test script to verify APOE section renders correctly with glutathione values
"""

from roadmap_generator import RoadmapGenerator

def test_apoe_section_rendering():
    """Test APOE section rendering with different glutathione levels"""
    
    generator = RoadmapGenerator()
    
    # Test case 1: E3/E4 with low glutathione (should trigger GSH<200)
    client_data = {'name': 'Test Patient', 'gender': 'female'}
    lab_results = {
        'APO1': 'E3/E4',
        'Glutathione': '150'  # Low glutathione
    }
    hhq_responses = {}
    
    print("Testing APOE Section with Low Glutathione")
    print("=" * 50)
    
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract just the APOE section
    apoe_start = roadmap.find("APO E Genetic Profile and Your Risk for Oxidative Stress")
    apoe_end = roadmap.find("## **MTHFR Genetics")
    apoe_section = roadmap[apoe_start:apoe_end]
    
    print("APOE Section Output:")
    print("-" * 30)
    print(apoe_section)
    print("-" * 30)
    
    # Check key elements
    checks = [
        ("Title present", "APO E Genetic Profile and Your Risk for Oxidative Stress" in apoe_section),
        ("Genotype shown", "E3/E4" in apoe_section),
        ("Glutathione level shown", "150" in apoe_section),
        ("GSH<200 message present", "Your GLUTATHIONE level is very low" in apoe_section),
        ("E4E3 content shown", "APO E E4/E3 genetic variant" in apoe_section),
        ("Consider following present", "Consider the following:" in apoe_section)
    ]
    
    print("\nValidation Results:")
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    # Test case 2: E3/E3 with normal glutathione (should NOT trigger GSH<200)
    print("\nTesting APOE Section with Normal Glutathione")
    print("=" * 50)
    
    lab_results_normal = {
        'APO1': 'E3/E3',
        'Glutathione': '300'  # Normal glutathione
    }
    
    roadmap2 = generator.generate_roadmap(client_data, lab_results_normal, hhq_responses)
    
    # Extract just the APOE section
    apoe_start2 = roadmap2.find("APO E Genetic Profile and Your Risk for Oxidative Stress")
    apoe_end2 = roadmap2.find("## **MTHFR Genetics")
    apoe_section2 = roadmap2[apoe_start2:apoe_end2]
    
    print("APOE Section Output:")
    print("-" * 30)
    print(apoe_section2)
    print("-" * 30)
    
    # Check key elements for normal glutathione
    checks2 = [
        ("Genotype shown", "E3/E3" in apoe_section2),
        ("Glutathione level shown", "300" in apoe_section2),
        ("GSH<200 message NOT present", "Your GLUTATHIONE level is very low" not in apoe_section2),
        ("nonE4 content shown", "You do not have the APO E genetic risk for Alzheimer's" in apoe_section2)
    ]
    
    print("\nValidation Results:")
    for check_name, result in checks2:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 APOE SECTION TEST PASSED! Word-for-word match with reference system.")
    else:
        print("💥 SOME CHECKS FAILED. Review the output above.")
    
    return all_passed

if __name__ == "__main__":
    test_apoe_section_rendering() 