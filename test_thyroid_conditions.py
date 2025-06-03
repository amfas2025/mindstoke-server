#!/usr/bin/env python3
"""
Test suite for comprehensive thyroid function conditions
Validates all thyroid-related conditional blocks and logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_thyroid_conditions():
    """Test comprehensive thyroid function scenarios."""
    
    print("=== Testing Comprehensive Thyroid Function Conditions ===\n")
    
    generator = RoadmapGenerator()
    
    # Test 1: Optimal thyroid function
    print("Test 1: Optimal Thyroid Function")
    print("-" * 40)
    
    client_data = {'firstname': 'Test', 'gender': 'male'}
    
    lab_results = {
        'THY_TSH': 1.5,        # Optimal: 0.4-2.5
        'THY_T3F': 3.8,        # Optimal: 3.2-4.2
        'THY_T4F': 1.5,        # Optimal: 1.3-1.8
        'RT3': 12,             # Optimal: <15
        'THY_TPOAB': 25,       # Optimal: <34
        'THY_TGAB': 0.5        # Optimal: <1
    }
    
    hhq_responses = {}
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (optimal: 0.4-2.5)")
    print(f"Free T3: {lab_results.get('THY_T3F')} (optimal: 3.2-4.2)")
    print(f"Free T4: {lab_results.get('THY_T4F')} (optimal: 1.3-1.8)")
    print(f"Reverse T3: {lab_results.get('RT3')} (optimal: <15)")
    print(f"TPO Ab: {lab_results.get('THY_TPOAB')} (optimal: <34)")
    print(f"TgAb: {lab_results.get('THY_TGAB')} (optimal: <1)")
    print()
    
    # Check that optimal thyroid function is detected
    assert processed.get('thyroid-optimal') == True, "Should trigger optimal thyroid"
    assert processed.get('quick-TSH>7') == False, "Should not trigger high TSH"
    assert processed.get('low-TSH') != True, "Should not trigger low TSH"
    assert processed.get('High-thyroid') != True, "Should not trigger high thyroid"
    
    print("✓ Optimal thyroid function detected correctly")
    print()
    
    # Test 2: High TSH (obvious hypothyroidism)
    print("Test 2: High TSH (Obvious Hypothyroidism)")
    print("-" * 40)
    
    lab_results = {
        'THY_TSH': 8.5,        # >7 = obvious hypothyroidism
        'THY_T3F': 2.8,        # <3.2 = low
        'THY_T4F': 1.0         # <1.3 = low
    }
    
    processed = generator._process_hhq_based_conditions({}, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (>7 = obvious hypothyroidism)")
    print(f"Free T3: {lab_results.get('THY_T3F')} (<3.2 = low)")
    print(f"Free T4: {lab_results.get('THY_T4F')} (<1.3 = low)")
    print()
    
    assert processed.get('quick-TSH>7') == True, "Should trigger high TSH"
    assert processed.get('thyroid-optimal') == False, "Should not be optimal"
    
    print("✓ High TSH condition detected correctly")
    print()
    
    # Test 3: Complex thyroid dysfunction
    print("Test 3: Complex Thyroid Dysfunction")
    print("-" * 40)
    
    lab_results = {
        'THY_TSH': 3.2,        # >2.5 = elevated
        'THY_T3F': 3.0,        # <3.6 = low for complex dysfunction
        'RT3': 18              # >15 = elevated
    }
    
    processed = generator._process_hhq_based_conditions({}, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (>2.5 = elevated)")
    print(f"Free T3: {lab_results.get('THY_T3F')} (<3.6 = low for complex dysfunction)")
    print(f"Reverse T3: {lab_results.get('RT3')} (>15 = elevated)")
    print()
    
    assert processed.get('TSH-T3-rT3') == True, "Should trigger complex dysfunction"
    assert processed.get('quick-reverseT3') == True, "Should trigger reverse T3"
    assert processed.get('thyroid-optimal') == False, "Should not be optimal"
    
    print("✓ Complex thyroid dysfunction detected correctly")
    print()
    
    # Test 4: Hashimoto's autoimmune thyroiditis
    print("Test 4: Hashimoto's Autoimmune Thyroiditis")
    print("-" * 40)
    
    lab_results = {
        'THY_TSH': 4.5,        # Elevated
        'THY_TPOAB': 85,       # >34 = autoimmune risk
        'THY_TGAB': 2.3        # >1 = autoimmune risk
    }
    
    hhq_responses = {
        'hh_hashimotos': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (elevated)")
    print(f"TPO Ab: {lab_results.get('THY_TPOAB')} (>34 = autoimmune risk)")
    print(f"TgAb: {lab_results.get('THY_TGAB')} (>1 = autoimmune risk)")
    print(f"HHQ Hashimoto's: {hhq_responses.get('hh_hashimotos')}")
    print()
    
    assert processed.get('quick-hashimotos') == True, "Should trigger Hashimoto's"
    assert processed.get('thyroid-row') == True, "Should trigger thyroid row"
    assert processed.get('thyroid-optimal') == False, "Should not be optimal"
    
    print("✓ Hashimoto's autoimmune condition detected correctly")
    print()
    
    # Test 5: Chronic fatigue + thyroid dysfunction
    print("Test 5: Chronic Fatigue + Thyroid Dysfunction")
    print("-" * 40)
    
    lab_results = {
        'THY_TSH': 3.8,        # Elevated
        'THY_T3F': 2.9,        # Low
        'RT3': 17              # Elevated
    }
    
    hhq_responses = {
        'hh_chronic_fatigue': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (elevated)")
    print(f"Free T3: {lab_results.get('THY_T3F')} (low)")
    print(f"Reverse T3: {lab_results.get('RT3')} (elevated)")
    print(f"Chronic Fatigue: {hhq_responses.get('hh_chronic_fatigue')}")
    print()
    
    assert processed.get('quick-fatigue') == True, "Should trigger fatigue condition"
    assert processed.get('thyroid-optimal') == False, "Should not be optimal"
    
    print("✓ Fatigue + thyroid dysfunction detected correctly")
    print()
    
    # Test 6: On thyroid medication but TSH still high
    print("Test 6: On Thyroid Medication but TSH Still High")
    print("-" * 40)
    
    lab_results = {
        'THY_TSH': 4.2         # Still elevated despite medication
    }
    
    hhq_responses = {
        'hh_takes_thyroid_medicine': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (still elevated)")
    print(f"Taking thyroid medication: {hhq_responses.get('hh_takes_thyroid_medicine')}")
    print()
    
    assert processed.get('High-thyroid') == True, "Should trigger high thyroid on medication"
    assert processed.get('low-TSH') == True, "Should trigger low TSH optimization"
    assert processed.get('thyroid-optimal') == False, "Should not be optimal"
    
    print("✓ High thyroid on medication detected correctly")
    print()
    
    # Test 7: Thyroid row display condition
    print("Test 7: Thyroid Row Display Condition")
    print("-" * 40)
    
    lab_results = {
        'RT3': 16,             # Has Reverse T3
        'THY_TPOAB': 45,       # Has TPO Ab
        'THY_TGAB': 1.5        # Has TgAb
    }
    
    processed = generator._process_hhq_based_conditions({}, lab_results)
    
    print(f"Has Reverse T3: {lab_results.get('RT3') is not None}")
    print(f"Has TPO Ab: {lab_results.get('THY_TPOAB') is not None}")
    print(f"Has TgAb: {lab_results.get('THY_TGAB') is not None}")
    print()
    
    assert processed.get('thyroid-row') == True, "Should trigger thyroid row display"
    
    print("✓ Thyroid row display condition working correctly")
    print()
    
    # Test 8: Comprehensive roadmap generation test
    print("Test 8: Full Roadmap Generation with Thyroid Content")
    print("-" * 40)
    
    client_data = {
        'firstname': 'Sarah',
        'gender': 'female',
        'email': 'sarah@test.com'
    }
    
    lab_results = {
        'THY_TSH': 3.5,        # Elevated
        'THY_T3F': 3.1,        # Low
        'THY_T4F': 1.2,        # Low
        'RT3': 16,             # Elevated
        'THY_TPOAB': 45,       # Elevated (Hashimoto's)
        'THY_TGAB': 1.5        # Elevated (Hashimoto's)
    }
    
    hhq_responses = {
        'hh_chronic_fatigue': True,
        'hh_hashimotos': True,
        'hh_takes_thyroid_medicine': False
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Check for presence of thyroid content
        thyroid_content_checks = [
            "Thyroid Function and Brain Health" in roadmap,
            "baseline **TSH** was 3.50" in roadmap,
            "baseline **FREE T3** was 3.10" in roadmap,
            "baseline **REVERSE T3** was 16.0" in roadmap,
            "**THYROID PEROXIDASE (TPO)**" in roadmap,
            "**HASHIMOTO'S THYROIDITIS**" in roadmap,
            "**CYTOMEL 5 mcg/day**" in roadmap,
            "**LOW DOSE NALTREXONE (LDN)**" in roadmap,
            "**AUTOIMMUNE PALEO DIET**" in roadmap
        ]
        
        print("Checking for thyroid content in generated roadmap:")
        for i, check in enumerate(thyroid_content_checks, 1):
            status = "✓" if check else "✗"
            print(f"  {status} Check {i}: {'PASS' if check else 'FAIL'}")
        
        all_checks_passed = all(thyroid_content_checks)
        assert all_checks_passed, "Some thyroid content checks failed"
        
        print("\n✓ Full roadmap generation with thyroid content working correctly")
        
    except Exception as e:
        print(f"✗ Error generating roadmap: {e}")
        raise
    
    print("\n" + "="*60)
    print("🎉 ALL THYROID CONDITION TESTS PASSED!")
    print("✓ Optimal thyroid function detection")
    print("✓ High TSH (hypothyroidism) detection")
    print("✓ Complex thyroid dysfunction (TSH + Reverse T3)")
    print("✓ Hashimoto's autoimmune condition")
    print("✓ Fatigue + thyroid dysfunction (Cytomel candidate)")
    print("✓ High thyroid on medication")
    print("✓ Thyroid row display logic")
    print("✓ Full roadmap generation with comprehensive thyroid content")
    print("="*60)

    # Test 9: Debug Scenario - TSH 4.2 with complex dysfunction
    print("Test 9: Debug Scenario (TSH 4.2 Complex Case)")
    print("-" * 40)
    
    client_data = {'firstname': 'Emma', 'gender': 'female'}
    
    lab_results = {
        'THY_TSH': 4.2,        # Elevated but not >7
        'THY_T3F': 3.0,        # Low  
        'THY_T4F': 1.2,        # Low
        'RT3': 18,             # Elevated
        'THY_TPOAB': 65,       # Elevated
        'THY_TGAB': 2.1        # Elevated
    }
    
    hhq_responses = {
        'hh_chronic_fatigue': True,
        'hh_hashimotos': True,
        'hh_takes_thyroid_medicine': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"TSH: {lab_results.get('THY_TSH')} (should NOT trigger TSH>7)")
    print(f"Expected: quick-TSH>7 should be False")
    print(f"Actual: quick-TSH>7 = {processed.get('quick-TSH>7', 'not set')}")
    
    # Generate actual roadmap content to see what appears
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check if hypothyroidism message appears
    if "obvious **HYPOTHYROIDISM**" in roadmap:
        print("❌ ERROR: Hypothyroidism message appears when it shouldn't!")
        print("This suggests the TSH>7 condition is not working properly.")
        
        # Find the exact context where this appears
        lines = roadmap.split('\n')
        for i, line in enumerate(lines):
            if "obvious **HYPOTHYROIDISM**" in line:
                print(f"Found at line {i}: {line.strip()}")
                # Show context
                start = max(0, i-2)
                end = min(len(lines), i+3)
                print("Context:")
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{lines[j]}")
                break
    else:
        print("✓ Hypothyroidism message correctly absent")
    
    print()

if __name__ == "__main__":
    test_thyroid_conditions() 