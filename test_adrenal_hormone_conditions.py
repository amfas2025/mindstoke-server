#!/usr/bin/env python3
"""
Test suite for adrenal hormone conditions (cortisol) that influence brain health
Validates cortisol threshold evaluation and supplement recommendations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_adrenal_hormone_conditions():
    """Test comprehensive adrenal hormone (cortisol) scenarios."""
    
    print("=== Testing Adrenal Hormone Conditions (Cortisol) ===\n")
    
    generator = RoadmapGenerator()
    
    # Test 1: Optimal cortisol levels (>15 ng/dL)
    print("Test 1: Optimal Cortisol Levels (>15 ng/dL)")
    print("-" * 45)
    
    client_data = {'firstname': 'Sarah', 'gender': 'female'}
    
    lab_results = {
        'NEURO_CORT': 18.5  # Optimal cortisol >15 ng/dL
    }
    
    hhq_responses = {
        'gender': 'female'
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (optimal: >15)")
    print("Expected: No intervention recommended")
    print()
    
    assert processed.get('quick-cortisol-15') == False, "Should not trigger low cortisol intervention"
    assert processed.get('Cort515') == False, "Should not trigger borderline cortisol condition"
    assert processed.get('quick-cortisol-lab-value') == "18.5", "Should display cortisol value"
    
    print("✓ Test 1 passed: Optimal cortisol levels\n")
    
    # Test 2: Borderline cortisol levels (5-15 ng/dL range - Cort515)
    print("Test 2: Borderline Cortisol (5-15 ng/dL - Cort515)")
    print("-" * 45)
    
    lab_results = {
        'NEURO_CORT': 12.0  # Borderline cortisol 5-15 ng/dL
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (borderline: 5-15)")
    print("Expected: Mild intervention - MITOCHONDRIAL OPTIMIZER or GOLD SUPER MEN N")
    print()
    
    assert processed.get('Cort515') == True, "Should trigger borderline cortisol condition"
    assert processed.get('quick-cortisol-15') == True, "Should trigger low cortisol support"
    assert processed.get('quick-cortisol-lab-value') == "12.0", "Should display cortisol value"
    
    print("✓ Test 2 passed: Borderline cortisol supplementation\n")
    
    # Test 3: Low cortisol levels (<5 ng/dL) 
    print("Test 3: Low Cortisol (<5 ng/dL)")
    print("-" * 30)
    
    lab_results = {
        'NEURO_CORT': 3.8  # Low cortisol <5 ng/dL
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (low: <5)")
    print("Expected: Comprehensive adrenal support needed")
    print()
    
    assert processed.get('quick-cortisol-15') == True, "Should trigger comprehensive cortisol support"
    assert processed.get('Cort515') == False, "Should not trigger borderline condition for very low levels"
    assert processed.get('quick-cortisol-lab-value') == "3.8", "Should display cortisol value"
    
    print("✓ Test 3 passed: Low cortisol comprehensive support\n")
    
    # Test 4: Very low cortisol with chronic fatigue symptoms
    print("Test 4: Very Low Cortisol + Chronic Fatigue")
    print("-" * 40)
    
    lab_results = {
        'NEURO_CORT': 2.1  # Very low cortisol
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_chronic_fatigue': True,
        'hh_adrenal_fatigue': True,
        'hh_morning_fatigue': True,
        'hh_low_energy': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (very low)")
    print("Symptoms: Chronic fatigue, adrenal fatigue, morning fatigue")
    print()
    
    assert processed.get('quick-cortisol-15') == True, "Should trigger comprehensive cortisol support"
    assert processed.get('cortisol-severe-support') == True, "Should trigger severe adrenal support"
    assert processed.get('Cort515') == False, "Should not trigger borderline condition"
    
    print("✓ Test 4 passed: Very low cortisol with severe symptoms\n")
    
    # Test 5: Cortisol right at 15 ng/dL threshold
    print("Test 5: Cortisol at 15 ng/dL Threshold")
    print("-" * 35)
    
    lab_results = {
        'NEURO_CORT': 15.0  # Right at threshold
    }
    
    hhq_responses = {
        'gender': 'female'
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (at threshold)")
    print("Expected: No intervention (≥15 is optimal)")
    print()
    
    assert processed.get('quick-cortisol-15') == False, "Should not trigger intervention at 15.0"
    assert processed.get('Cort515') == False, "Should not trigger borderline at 15.0"
    assert processed.get('quick-cortisol-lab-value') == "15.0", "Should display cortisol value"
    
    print("✓ Test 5 passed: Cortisol at exact threshold\n")
    
    # Test 6: Cortisol at 14.9 ng/dL (just below threshold)
    print("Test 6: Cortisol Just Below Threshold (14.9 ng/dL)")
    print("-" * 45)
    
    lab_results = {
        'NEURO_CORT': 14.9  # Just below 15 threshold
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (just below 15)")
    print("Expected: Trigger intervention (<15)")
    print()
    
    assert processed.get('quick-cortisol-15') == True, "Should trigger intervention below 15.0"
    assert processed.get('Cort515') == True, "Should trigger borderline condition"
    assert processed.get('quick-cortisol-lab-value') == "14.9", "Should display cortisol value"
    
    print("✓ Test 6 passed: Cortisol just below threshold\n")
    
    # Test 7: High cortisol levels (>25 ng/dL)
    print("Test 7: High Cortisol Levels (>25 ng/dL)")
    print("-" * 35)
    
    lab_results = {
        'NEURO_CORT': 28.5  # High cortisol
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_chronic_stress': True,
        'hh_anxiety': True,
        'hh_insomnia': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (high)")
    print("Symptoms: Chronic stress, anxiety, insomnia")
    print()
    
    assert processed.get('quick-cortisol-high') == True, "Should trigger high cortisol condition"
    assert processed.get('quick-cortisol-15') == False, "Should not trigger low cortisol"
    assert processed.get('Cort515') == False, "Should not trigger borderline condition"
    
    print("✓ Test 7 passed: High cortisol management\n")
    
    # Test 8: Female with cortisol and hormone interactions
    print("Test 8: Female with Cortisol + Hormone Interactions")
    print("-" * 50)
    
    lab_results = {
        'NEURO_CORT': 8.2,    # Low cortisol
        'NEURO_DHEAS': 110,   # Low DHEA-s  
        'NEURO_PREG': 45      # Low pregnenolone
    }
    
    hhq_responses = {
        'gender': 'female',
        'hh_chronic_fatigue': True,
        'hh_brain_fog': True,
        'hh_adrenal_fatigue': True,
        'hh_perimenopause': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Multiple hormone deficiencies with fatigue symptoms")
    print()
    
    assert processed.get('quick-cortisol-15') == True, "Should trigger cortisol support"
    assert processed.get('neurological-hormone-support') == True, "Should trigger comprehensive hormone support"
    assert processed.get('Cort515') == True, "Should trigger borderline cortisol condition"
    
    print("✓ Test 8 passed: Multi-hormone adrenal support\n")
    
    # Test 9: Male athlete with exercise-induced cortisol issues
    print("Test 9: Male Athlete with Exercise-Induced Cortisol Issues")
    print("-" * 55)
    
    lab_results = {
        'NEURO_CORT': 6.8  # Low cortisol from overtraining
    }
    
    hhq_responses = {
        'gender': 'male',
        'hh_exercise_intolerance': True,
        'hh_muscle_weakness': True,
        'hh_chronic_fatigue': True,
        'hh_athlete': True,
        'hh_overtraining': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print(f"Cortisol: {lab_results.get('NEURO_CORT')} ng/dL (exercise-induced low)")
    print("Athletic overtraining syndrome")
    print()
    
    assert processed.get('Cort515') == True, "Should trigger adrenal support for athlete"
    assert processed.get('exercise-cortisol-support') == True, "Should trigger exercise-specific support"
    
    print("✓ Test 9 passed: Exercise-induced adrenal issues\n")
    
    # Test 10: No cortisol data available
    print("Test 10: No Cortisol Data Available")
    print("-" * 35)
    
    lab_results = {}  # No cortisol data
    
    hhq_responses = {
        'gender': 'female',
        'hh_chronic_fatigue': True
    }
    
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("No cortisol lab data provided")
    print()
    
    assert processed.get('quick-cortisol-15') == False, "Should not trigger without data"
    assert processed.get('Cort515') == False, "Should not trigger without data"
    assert 'quick-cortisol-lab-value' not in processed, "Should not have lab value"
    
    print("✓ Test 10 passed: No cortisol data handling\n")
    
    print("=== All Adrenal Hormone (Cortisol) Tests Passed! ===")
    print("✓ Cortisol threshold evaluation working correctly")
    print("✓ Borderline cortisol support (Cort515)")
    print("✓ Comprehensive low cortisol management")
    print("✓ High cortisol recognition")
    print("✓ Multi-hormone interactions")
    print("✓ Exercise-induced adrenal issues")
    print("✓ Symptom-based severity assessment")

if __name__ == "__main__":
    test_adrenal_hormone_conditions() 