#!/usr/bin/env python3
"""
Test suite for neurologically active hormone conditions
Validates PREGNENOLONE and DHEA-s conditional blocks and logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_neurologically_active_hormones():
    """Test comprehensive neurologically active hormone scenarios."""
    
    print("=== Testing Neurologically Active Hormone Conditions ===\n")
    
    generator = RoadmapGenerator()
    
    # Test 1: Optimal PREGNENOLONE levels (150-200 ng/dL)
    print("Test 1: Optimal PREGNENOLONE Levels")
    print("-" * 40)
    
    client_data = {'firstname': 'Sarah', 'gender': 'female'}
    
    lab_results = {
        'NEURO_PREG': 175,  # Optimal pregnenolone 150-200 ng/dL
        'NEURO_DHEAS': 180  # Optimal DHEA-s >150 ng/dL
    }
    
    hhq_responses = {
        'gender': 'female'
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"PREGNENOLONE: {lab_results.get('NEURO_PREG')} ng/dL (optimal: 150-200)")
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (optimal: >150)")
    print()
    
    assert processed.get('quick-pregnenolone-101') == True, "Should show optimal pregnenolone"
    assert processed.get('quick-DHEA-151') == True, "Should show optimal DHEA-s"
    assert processed.get('quick-PROG-50-100') == False, "Should not recommend pregnenolone supplementation"
    assert processed.get('quick-DHEA-150') == False, "Should not recommend DHEA supplementation"
    
    print("✓ Test 1 passed: Optimal neurologically active hormones\n")
    
    # Test 2: Low PREGNENOLONE needing supplementation (50-100 ng/dL)
    print("Test 2: Low PREGNENOLONE (50-100 ng/dL)")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 75,   # Low pregnenolone 50-100 ng/dL
        'NEURO_DHEAS': 200  # Normal DHEA-s
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"PREGNENOLONE: {lab_results.get('NEURO_PREG')} ng/dL (low: 50-100)")
    print(f"Recommendation: PREGNENOLONE 100 mg each night")
    print()
    
    assert processed.get('quick-pregnenolone-101') == False, "Should not show optimal pregnenolone"
    assert processed.get('quick-PROG-50-100') == True, "Should recommend pregnenolone supplementation"
    assert processed.get('quick-DHEA-151') == True, "Should show optimal DHEA-s"
    
    print("✓ Test 2 passed: Low pregnenolone supplementation\n")
    
    # Test 3: Very low PREGNENOLONE (<50 ng/dL)
    print("Test 3: Very Low PREGNENOLONE (<50 ng/dL)")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 35,   # Very low pregnenolone <50 ng/dL
        'NEURO_DHEAS': 120  # Low DHEA-s <150 ng/dL
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"PREGNENOLONE: {lab_results.get('NEURO_PREG')} ng/dL (very low: <50)")
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (low: <150)")
    print()
    
    assert processed.get('quick-PROG<50') == True, "Should show very low pregnenolone"
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA supplementation"
    
    print("✓ Test 3 passed: Very low pregnenolone and DHEA-s\n")
    
    # Test 4: Low DHEA-s needing supplementation (<150 ng/dL)
    print("Test 4: Low DHEA-s (<150 ng/dL)")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 180,  # Optimal pregnenolone
        'NEURO_DHEAS': 120  # Low DHEA-s <150 ng/dL
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (low: <150)")
    print(f"Recommendation: 7-KETO DHEA 100 mg at night")
    print()
    
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA supplementation"
    assert processed.get('quick-pregnenolone-101') == True, "Should show optimal pregnenolone"
    
    print("✓ Test 4 passed: Low DHEA-s supplementation\n")
    
    # Test 5: Borderline DHEA-s (200-249 ng/dL)
    print("Test 5: Borderline DHEA-s (200-249 ng/dL)")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 160,  # Optimal pregnenolone
        'NEURO_DHEAS': 225  # Borderline DHEA-s 200-249 ng/dL
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (borderline: 200-249)")
    print(f"Recommendation: 7-KETO DHEA 50 mg at night")
    print()
    
    assert processed.get('quick-DHEA-200-249') == True, "Should recommend lower dose DHEA"
    assert processed.get('quick-DHEA-151') == True, "Should also show above 150 condition"
    
    print("✓ Test 5 passed: Borderline DHEA-s dosing\n")
    
    # Test 6: DHEA and cardiovascular disease correlation
    print("Test 6: DHEA-s and Cardiovascular Disease")
    print("-" * 40)
    
    lab_results = {
        'NEURO_DHEAS': 80  # Very low DHEA-s
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_heart_disease': True,
        'hh_cardiovascular_disease': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (very low)")
    print(f"Cardiovascular disease history: True")
    print()
    
    assert processed.get('quick-DHEA-ASVD') == True, "Should show DHEA-cardiovascular correlation"
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA supplementation"
    
    print("✓ Test 6 passed: DHEA-cardiovascular disease correlation\n")
    
    # Test 7: Male with prostate cancer and LUPRON
    print("Test 7: Male with Prostate Cancer and LUPRON")
    print("-" * 40)
    
    lab_results = {
        'NEURO_DHEAS': 95   # Low DHEA-s from LUPRON suppression
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_prostate_cancer': True,
        'hh_takes_lupron': True,
        'hh_hormone_suppression': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"DHEA-s: {lab_results.get('NEURO_DHEAS')} ng/dL (suppressed by LUPRON)")
    print(f"Prostate cancer + LUPRON: True")
    print()
    
    assert processed.get('quick-DHEA-LUPRON') == True, "Should show LUPRON-DHEA connection"
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA support"
    
    print("✓ Test 7 passed: LUPRON-induced DHEA suppression\n")
    
    # Test 8: Cortisol support needed
    print("Test 8: Low Cortisol Support Needed")
    print("-" * 40)
    
    lab_results = {
        'NEURO_CORT': 12,   # Low cortisol <15
        'NEURO_DHEAS': 140  # Borderline low DHEA-s
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_chronic_fatigue': True,
        'hh_adrenal_fatigue': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} μg/dL (low: <15)")
    print(f"Chronic fatigue and adrenal issues")
    print()
    
    assert processed.get('quick-cortisol-15') == True, "Should recommend cortisol support"
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA support"
    
    print("✓ Test 8 passed: Cortisol support protocols\n")
    
    # Test 9: Female with no neurological hormone issues
    print("Test 9: Optimal Neurological Hormones")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 185,  # Optimal pregnenolone
        'NEURO_DHEAS': 220, # Optimal DHEA-s
        'NEURO_CORT': 18    # Optimal cortisol
    }
    
    hhq_responses = {
        'gender': 'female'
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"All neurological hormones optimal")
    print()
    
    assert processed.get('quick-pregnenolone-101') == True, "Should show optimal pregnenolone"
    assert processed.get('quick-DHEA-151') == True, "Should show optimal DHEA-s"
    assert processed.get('quick-PROG-50-100') == False, "Should not recommend supplements"
    assert processed.get('quick-DHEA-150') == False, "Should not recommend supplements"
    
    print("✓ Test 9 passed: Optimal neurological hormones\n")
    
    # Test 10: Male with multiple neurological hormone deficiencies
    print("Test 10: Multiple Neurological Hormone Deficiencies")
    print("-" * 40)
    
    lab_results = {
        'NEURO_PREG': 45,   # Very low pregnenolone
        'NEURO_DHEAS': 85,  # Very low DHEA-s
        'NEURO_CORT': 8     # Very low cortisol
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_chronic_fatigue': True,
        'hh_brain_fog': True,
        'hh_low_energy': True,
        'hh_depression': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Multiple deficiencies with fatigue/cognitive symptoms")
    print()
    
    assert processed.get('quick-PROG<50') == True, "Should show very low pregnenolone"
    assert processed.get('quick-DHEA-150') == True, "Should recommend DHEA"
    assert processed.get('quick-cortisol-15') == True, "Should recommend cortisol support"
    
    print("✓ Test 10 passed: Multiple neurological hormone deficiencies\n")
    
    print("=== All Neurologically Active Hormone Tests Passed! ===")
    print("✓ PREGNENOLONE threshold evaluation working correctly")
    print("✓ DHEA-s level assessment and supplementation")
    print("✓ Cortisol support protocols")
    print("✓ Cardiovascular disease correlations")
    print("✓ LUPRON-induced hormone suppression")
    print("✓ Gender-appropriate recommendations")

if __name__ == "__main__":
    test_neurologically_active_hormones() 