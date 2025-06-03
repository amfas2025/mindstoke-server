#!/usr/bin/env python3
"""
Test suite for comprehensive male hormone function conditions
Validates all male hormone-related conditional blocks and logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_male_hormone_conditions():
    """Test comprehensive male hormone function scenarios."""
    
    print("=== Testing Comprehensive Male Hormone Function Conditions ===\n")
    
    generator = RoadmapGenerator()
    
    # Test 1: Male with optimal hormone levels
    print("Test 1: Male with Optimal Hormone Levels")
    print("-" * 40)
    
    client_data = {'firstname': 'John', 'gender': 'male'}
    
    lab_results = {
        'MHt_TT': 750,         # Optimal total testosterone: >600
        'MHt_FREE_T': 16,      # Optimal free testosterone: 12-15 pg/mL
        'MHt_SHBG': 35,        # Optimal SHBG: <45 pg/mL  
        'MHt_PSA': 1.8,        # Optimal PSA: <4.0
        'MHt_LH': 4.5,         # Optimal LH: closer to 5.1
        'MHt_FSH': 3.0,        # Optimal FSH: closer to 2.2
        'MHt_PROL': 10.5,      # Optimal prolactin: close to 11.25
        'MHt_DHT': 45,         # Optimal DHT: <52
        'MHt_E2': 22,          # Optimal estradiol: <25 pg/mL
        'MHt_E1': 55,          # Optimal estrone: <60 pg/mL
        'MHt_PROG': 0.6        # Optimal progesterone: close to 0.8
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_erectile_dysfunction': False,
        'hh_low_libido': False,
        'hh_fatigue': False
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Total testosterone: {lab_results.get('MHt_TT')} ng/dL (optimal: >600)")
    print(f"Free testosterone: {lab_results.get('MHt_FREE_T')} pg/mL (optimal: 12-15)")
    print(f"SHBG: {lab_results.get('MHt_SHBG')} (optimal: <45)")
    print(f"PSA: {lab_results.get('MHt_PSA')} (optimal: <4.0)")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('testosterone-low') == False, "Should not show low testosterone for optimal levels"
    assert processed.get('quick-male-hormones-hrt') == False, "Should not recommend HRT for optimal levels"
    
    print("✓ Test 1 passed: Optimal male hormones\n")
    
    # Test 2: Male with low testosterone needing optimization
    print("Test 2: Male with Low Testosterone")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 350,         # Low total testosterone: <400
        'MHt_FREE_T': 8,       # Low free testosterone: <12 pg/mL
        'MHt_SHBG': 55,        # Elevated SHBG: >45
        'MHt_PSA': 2.1         # Normal PSA
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_erectile_dysfunction': True,
        'hh_low_libido': True,
        'hh_fatigue': True,
        'hh_brain_fog': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Total testosterone: {lab_results.get('MHt_TT')} ng/dL (low: <400)")
    print(f"Free testosterone: {lab_results.get('MHt_FREE_T')} pg/mL (low: <12)")
    print(f"SHBG: {lab_results.get('MHt_SHBG')} (elevated: >45)")
    print(f"Symptoms: ED, low libido, fatigue, brain fog")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('testosterone-low') == True, "Should show low testosterone"
    assert processed.get('free-testosterone-low') == True, "Should show low free testosterone"
    assert processed.get('quick-male-hormones-shbg') == True, "Should show elevated SHBG"
    assert processed.get('quick-male-hormones-hrt') == True, "Should recommend HRT for low levels"
    
    print("✓ Test 2 passed: Low testosterone with symptoms\n")
    
    # Test 3: Male with prostate cancer history 
    print("Test 3: Male with Prostate Cancer History")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'male',
        'hh_prostate_cancer': True,
        'hh_takes_lupron': True,
        'hh_brain_fog': True,
        'hh_memory_problems': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Prostate cancer history: True")
    print("Takes LUPRON: True")
    print("Has cognitive symptoms: brain fog, memory problems")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('quick-LUPRON') == True, "Should trigger LUPRON considerations"
    assert processed.get('quick-male-hormones-hrt') == True, "Should still recommend HRT discussion"
    
    print("✓ Test 3 passed: Prostate cancer history\n")
    
    # Test 4: Male with elevated PSA
    print("Test 4: Male with Elevated PSA")
    print("-" * 40)
    
    lab_results = {
        'MHt_PSA': 6.5,        # Elevated PSA: >4.0
        'MHt_TT': 450          # Borderline testosterone
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_age_over_50': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"PSA: {lab_results.get('MHt_PSA')} (elevated: >4.0)")
    print(f"Age over 50: True")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('Quick-PSA') == True, "Should trigger PSA considerations"
    assert processed.get('quick-male-hormones-hrt') == False, "Should not recommend HRT with elevated PSA"
    
    print("✓ Test 4 passed: Elevated PSA screening\n")
    
    # Test 5: Male with sleep apnea and low hormones
    print("Test 5: Male with Sleep Apnea and Hormone Issues")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 380,         # Low testosterone
        'MHt_FREE_T': 9        # Low free testosterone
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_sleep_apnea': True,
        'hh_uses_cpap': True,
        'hh_snoring': True,
        'hh_fatigue': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("Sleep apnea: True")
    print("Uses CPAP: True")
    print("Low testosterone symptoms")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('quick-sleep-hormones') == True, "Should trigger sleep-hormone connection"
    assert processed.get('testosterone-low') == True, "Should show low testosterone"
    
    print("✓ Test 5 passed: Sleep apnea with hormone issues\n")
    
    # Test 6: Male with metabolic dysfunction affecting hormones
    print("Test 6: Male with Metabolic Dysfunction")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 420,         # Borderline low testosterone
        'METAB_INS': 15,       # Elevated insulin
        'CHEM_GLU': 110,       # Elevated glucose
        'LIPID_TRIG': 180      # Elevated triglycerides
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_diabetes': True,
        'hh_metabolic_syndrome': True,
        'hh_low_energy': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("Diabetes: True")
    print("Metabolic syndrome: True")
    print("Borderline testosterone with metabolic issues")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('testosterone-low') == True, "Should show testosterone concerns"
    assert processed.get('quick-diabetes') == True, "Should show diabetes condition"
    
    print("✓ Test 6 passed: Metabolic dysfunction affecting hormones\n")
    
    # Test 7: Male on testosterone replacement therapy
    print("Test 7: Male Currently on TRT")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 850,         # High testosterone (on TRT)
        'MHt_FREE_T': 25,      # High free testosterone
        'MHt_E2': 35,          # Elevated estradiol (aromatization)
        'MHt_PSA': 1.5         # Normal PSA
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_takes_testosterone': True,
        'hh_hormone_replacement': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("Takes testosterone: True")
    print("On hormone replacement: True")
    print("High testosterone levels (TRT)")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('quick-using-TRT') == True, "Should show current TRT use"
    assert processed.get('testosterone-low') == False, "Should not show low testosterone"
    
    print("✓ Test 7 passed: Current TRT use\n")
    
    # Test 8: Male with brain injury and hormone optimization
    print("Test 8: Male with TBI and Hormone Protocol")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 390,         # Low testosterone
        'MHt_FREE_T': 10       # Low free testosterone
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_traumatic_brain_injury': True,
        'hh_concussion': True,
        'hh_brain_fog': True,
        'hh_memory_problems': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("TBI history: True")
    print("Concussion history: True")
    print("Cognitive symptoms with low hormones")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('quick-tbi') == True, "Should trigger TBI condition"
    assert processed.get('Quick-Modafinil') == True, "Should trigger cognitive enhancement"
    assert processed.get('quick-male-hormones-hrt') == True, "Should recommend HRT for TBI"
    
    print("✓ Test 8 passed: TBI with hormone protocol\n")
    
    # Test 9: Older male with age-related decline
    print("Test 9: Older Male with Age-Related Decline")
    print("-" * 40)
    
    lab_results = {
        'MHt_TT': 480,         # Age-related decline
        'MHt_FREE_T': 11,      # Borderline free testosterone
        'MHt_SHBG': 48,        # Slightly elevated SHBG
        'MHt_PSA': 3.2,        # Elevated but normal PSA
        'MHt_LH': 8.5,         # Elevated LH (primary hypogonadism)
        'MHt_FSH': 6.0         # Elevated FSH
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_age_over_65': True,
        'hh_low_energy': True,
        'hh_muscle_weakness': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Age over 65: True")
    print(f"Total testosterone: {lab_results.get('MHt_TT')} (age-related decline)")
    print(f"Elevated LH/FSH suggesting primary hypogonadism")
    print()
    
    assert processed.get('quick-male-hormones') == True, "Should trigger male hormones section"
    assert processed.get('testosterone-low') == True, "Should show suboptimal testosterone"
    assert processed.get('quick-age-related-decline') == True, "Should trigger age-related protocols"
    
    print("✓ Test 9 passed: Age-related hormone decline\n")
    
    # Test 10: Female client (should not trigger male hormones)
    print("Test 10: Female Client (Should Not Trigger)")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_fatigue': True,
        'hh_low_libido': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Gender: female")
    print("Fatigue: True")
    print("Low libido: True")
    print()
    
    assert processed.get('quick-male-hormones') == False, "Should not trigger male hormones for female"
    assert processed.get('testosterone-low') == False, "Should not trigger male-specific protocols"
    
    print("✓ Test 10 passed: Female client correctly excluded\n")
    
    print("=== All Male Hormone Tests Passed! ===")
    print("✓ Comprehensive male hormone implementation working correctly")
    print("✓ Proper gender filtering")
    print("✓ Testosterone level evaluation")
    print("✓ HRT recommendations based on levels and symptoms")
    print("✓ Prostate cancer considerations")
    print("✓ Sleep and cognitive protocols")
    print("✓ Age-related hormone decline")
    print("✓ TRT monitoring and optimization")

if __name__ == "__main__":
    test_male_hormone_conditions() 