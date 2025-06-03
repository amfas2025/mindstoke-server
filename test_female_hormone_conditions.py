#!/usr/bin/env python3
"""
Test suite for comprehensive female hormone function conditions
Validates all female hormone-related conditional blocks and logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_female_hormone_conditions():
    """Test comprehensive female hormone function scenarios."""
    
    print("=== Testing Comprehensive Female Hormone Function Conditions ===\n")
    
    generator = RoadmapGenerator()
    
    # Test 1: Premenopausal woman with optimal hormones
    print("Test 1: Premenopausal Optimal Hormones")
    print("-" * 40)
    
    client_data = {'firstname': 'Sarah', 'gender': 'female'}
    
    lab_results = {
        'FHt_FSH': 8.5,        # Optimal: <11 for premenopausal
        'FHt_E2': 120,         # Optimal: 50-500 for menstruating
        'FHt_PROG': 3.5,       # Optimal: 1-7
        'FHt_TT': 55,          # Optimal: 40-70
        'FHt_E1': 150,         # Optimal: <200
        'FHt_PROL': 13.0,      # Near optimal: ~13.75
        'FHt_LH': 20,          # Near optimal: ~22
        'FHt_SHBG': 65,        # Optimal: <75
        'FHt_DHT': 25          # Optimal: <30
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_natural_menopause': False,
        'hh_perimenopause': False
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"FSH: {lab_results.get('FHt_FSH')} (optimal: <11 for premenopausal)")
    print(f"Estradiol: {lab_results.get('FHt_E2')} (optimal: 50-500 for menstruating)")
    print(f"Progesterone: {lab_results.get('FHt_PROG')} (optimal: 1-7)")
    print(f"Testosterone: {lab_results.get('FHt_TT')} (optimal: 40-70)")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('quick-female-hormones-hrt') == False, "Should not recommend HRT for optimal levels"
    assert processed.get('quick-using-HRT') == False, "Should not be using HRT"
    
    print("✓ Test 1 passed: Optimal premenopausal hormones\n")
    
    # Test 2: Menopausal woman needing HRT
    print("Test 2: Menopausal Woman Needing HRT")
    print("-" * 40)
    
    lab_results = {
        'FHt_FSH': 35,         # Elevated: >20 for menopause
        'FHt_E2': 25,          # Low: <50 for menopause
        'FHt_PROG': 0.5,       # Low: <1
        'FHt_TT': 25,          # Low: <40
        'FHt_E1': 250,         # Elevated: >200
        'FHt_SHBG': 85         # Elevated: >75
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_natural_menopause': True,
        'hh_hot_flashes': True,
        'hh_brain_fog': True,
        'hh_low_libido': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"FSH: {lab_results.get('FHt_FSH')} (elevated: >20 for menopause)")
    print(f"Estradiol: {lab_results.get('FHt_E2')} (low: <50 for menopause)")
    print(f"Progesterone: {lab_results.get('FHt_PROG')} (low: <1)")
    print(f"Has menopausal symptoms: Hot flashes, brain fog, low libido")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('quick-female-hormones-hrt') == True, "Should recommend HRT"
    assert processed.get('quick-using-HRT') == False, "Should not be currently using HRT"
    
    print("✓ Test 2 passed: Menopausal woman needing HRT\n")
    
    # Test 3: Woman currently using HRT
    print("Test 3: Woman Currently Using HRT")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_takes_estrogen': True,
        'hh_takes_progesterone': True,
        'hh_natural_menopause': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Takes estrogen: True")
    print("Takes progesterone: True")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('quick-using-HRT') == True, "Should be using HRT"
    
    print("✓ Test 3 passed: Woman currently using HRT\n")
    
    # Test 4: Breast cancer history
    print("Test 4: Breast Cancer History")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_breast_cancer': True,
        'hh_brain_fog': True,
        'hh_memory_problems': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Breast cancer history: True")
    print("Has cognitive symptoms: brain fog, memory problems")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('Quick-Breast-CA') == True, "Should trigger breast cancer considerations"
    assert processed.get('quick-female-hormones-hrt') == True, "Should still recommend HRT discussion"
    
    print("✓ Test 4 passed: Breast cancer history\n")
    
    # Test 5: Breast cancer with sleep/anxiety issues
    print("Test 5: Breast Cancer with Sleep/Anxiety Issues")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_breast_cancer': True,
        'hh_insomnia': True,
        'hh_anxiety': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Breast cancer history: True")
    print("Sleep/anxiety issues: insomnia, anxiety")
    print()
    
    assert processed.get('Quick-Breast-CA') == True, "Should trigger breast cancer considerations"
    assert processed.get('BreastCA-Insomnia-Anxiety') == True, "Should trigger progesterone for sleep/anxiety"
    
    print("✓ Test 5 passed: Breast cancer with sleep/anxiety\n")
    
    # Test 6: Mood disorders
    print("Test 6: Mood Disorders")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_depression': True,
        'hh_anxiety': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Depression: True")
    print("Anxiety: True")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('Quick-Hormone-Mood-Disorder') == True, "Should trigger mood disorder considerations"
    assert processed.get('quick-female-hormones-hrt') == True, "Should recommend HRT for mood"
    
    print("✓ Test 6 passed: Mood disorders\n")
    
    # Test 7: Sleep issues with antidepressant use
    print("Test 7: Sleep Issues with Antidepressant Use")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_insomnia': True,
        'hh_takes_antidepressant': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Insomnia: True")
    print("Takes antidepressant: True")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('Prometrium-Sleep') == True, "Should recommend Prometrium for sleep"
    
    print("✓ Test 7 passed: Sleep issues with antidepressant\n")
    
    # Test 8: Frequent UTI issues
    print("Test 8: Frequent UTI Issues")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'female',
        'hh_frequent_uti': True,
        'hh_natural_menopause': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Frequent UTI: True")
    print("Natural menopause: True")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('Freq-UTI') == True, "Should trigger UTI considerations"
    assert processed.get('quick-female-hormones-hrt') == True, "Should recommend HRT for UTI prevention"
    
    print("✓ Test 8 passed: Frequent UTI issues\n")
    
    # Test 9: Surgical menopause (complex case)
    print("Test 9: Surgical Menopause Complex Case")
    print("-" * 40)
    
    lab_results = {
        'FHt_FSH': 45,         # Very elevated
        'FHt_E2': 15,          # Very low
        'FHt_PROG': 0.2,       # Very low
        'FHt_TT': 15           # Very low
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_t_hysterectomy_before40': True,
        'hh_hot_flashes': True,
        'hh_night_sweats': True,
        'hh_brain_fog': True,
        'hh_depression': True,
        'hh_low_libido': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"FSH: {lab_results.get('FHt_FSH')} (very elevated)")
    print(f"Estradiol: {lab_results.get('FHt_E2')} (very low)")
    print("Surgical menopause before 40")
    print("Multiple symptoms: hot flashes, night sweats, brain fog, depression, low libido")
    print()
    
    assert processed.get('quick-female-hormones') == True, "Should trigger female hormones section"
    assert processed.get('quick-female-hormones-hrt') == True, "Should strongly recommend HRT"
    assert processed.get('Quick-Hormone-Mood-Disorder') == True, "Should address mood disorders"
    
    print("✓ Test 9 passed: Surgical menopause complex case\n")
    
    # Test 10: Male client (should not trigger female hormones)
    print("Test 10: Male Client (Should Not Trigger)")
    print("-" * 40)
    
    hhq_responses = {
        'gender': 'male',
        'hh_depression': True,
        'hh_insomnia': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, {})
    
    print("Gender: male")
    print("Depression: True")
    print("Insomnia: True")
    print()
    
    assert processed.get('quick-female-hormones') == False, "Should not trigger female hormones for male"
    assert processed.get('Quick-Hormone-Mood-Disorder') == False, "Should not trigger female-specific mood protocols"
    
    print("✓ Test 10 passed: Male client correctly excluded\n")
    
    print("=== All Female Hormone Tests Passed! ===")
    print("✓ Comprehensive female hormone implementation working correctly")
    print("✓ Proper gender filtering")
    print("✓ Menopause status evaluation")
    print("✓ HRT recommendations based on levels and symptoms")
    print("✓ Breast cancer considerations")
    print("✓ Sleep and mood disorder protocols")
    print("✓ UTI prevention strategies")

if __name__ == "__main__":
    test_female_hormone_conditions() 