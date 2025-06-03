#!/usr/bin/env python3
"""
Debug script to show actual female hormone content generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_female_hormone_content():
    """Debug female hormone content generation."""
    
    print("=== Debugging Female Hormone Content Generation ===\n")
    
    generator = RoadmapGenerator()
    
    # Test case: Premenopausal with optimal hormones
    client_data = {
        'firstname': 'Sarah',
        'gender': 'female',
        'email': 'sarah@test.com'
    }
    
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
    
    print("Input Data:")
    print(f"  Gender: {hhq_responses.get('gender')}")
    print(f"  Natural menopause: {hhq_responses.get('hh_natural_menopause')}")
    print(f"  Perimenopause: {hhq_responses.get('hh_perimenopause')}")
    print()
    
    print("Lab Values:")
    for key, value in lab_results.items():
        print(f"  {key}: {value}")
    print()
    
    # Test the processing
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("Processed Conditions:")
    relevant_conditions = [k for k in processed.keys() if 'female' in k.lower() or 'hormone' in k.lower() or 'hrt' in k.lower()]
    for condition in sorted(relevant_conditions):
        print(f"  {condition}: {processed.get(condition)}")
    print()
    
    # Analyze the decision logic
    print("Decision Analysis:")
    menopause_status = generator._determine_menopause_status(hhq_responses)
    print(f"  Menopause status: {menopause_status}")
    
    # Check hormone dysfunction
    hormone_dysfunction = False
    fsh = lab_results.get('FHt_FSH')
    estradiol = lab_results.get('FHt_E2')
    progesterone = lab_results.get('FHt_PROG')
    testosterone_female = lab_results.get('FHt_TT')
    
    print(f"  FSH analysis: {fsh}")
    if fsh is not None:
        if menopause_status in ['premenopausal', 'perimenopause'] and fsh > 11:
            hormone_dysfunction = True
            print(f"    FSH dysfunction: True (>{11} for premenopausal)")
        elif menopause_status in ['natural_menopause', 'surgical_menopause'] and fsh > 20:
            hormone_dysfunction = True
            print(f"    FSH dysfunction: True (>{20} for menopausal)")
        else:
            print(f"    FSH dysfunction: False")
    
    print(f"  Estradiol analysis: {estradiol}")
    if estradiol is not None:
        if menopause_status in ['premenopausal', 'perimenopause'] and (estradiol < 50 or estradiol > 500):
            hormone_dysfunction = True
            print(f"    Estradiol dysfunction: True (outside 50-500 for premenopausal)")
        elif menopause_status in ['natural_menopause', 'surgical_menopause'] and (estradiol < 50 or estradiol > 150):
            hormone_dysfunction = True
            print(f"    Estradiol dysfunction: True (outside 50-150 for menopausal)")
        else:
            print(f"    Estradiol dysfunction: False")
    
    print(f"  Progesterone analysis: {progesterone}")
    if progesterone is not None and (progesterone < 1 or progesterone > 7):
        hormone_dysfunction = True
        print(f"    Progesterone dysfunction: True (outside 1-7)")
    else:
        print(f"    Progesterone dysfunction: False")
    
    print(f"  Testosterone analysis: {testosterone_female}")
    if testosterone_female is not None and (testosterone_female < 40 or testosterone_female > 70):
        hormone_dysfunction = True
        print(f"    Testosterone dysfunction: True (outside 40-70)")
    else:
        print(f"    Testosterone dysfunction: False")
    
    print(f"  Overall hormone dysfunction: {hormone_dysfunction}")
    
    # Check symptom-based triggers
    has_menopausal_symptoms = (
        hhq_responses.get('hh_hot_flashes', False) or
        hhq_responses.get('hh_night_sweats', False) or
        hhq_responses.get('hh_mood_swings', False) or
        hhq_responses.get('hh_low_libido', False) or
        hhq_responses.get('hh_vaginal_dryness', False) or
        hhq_responses.get('hh_brain_fog', False) or
        hhq_responses.get('hh_memory_problems', False)
    )
    
    has_cognitive_symptoms = (
        hhq_responses.get('hh_brain_fog', False) or
        hhq_responses.get('hh_memory_problems', False) or
        hhq_responses.get('hh_attention_problems', False) or
        hhq_responses.get('hh_cognitive_decline', False)
    )
    
    print(f"  Has menopausal symptoms: {has_menopausal_symptoms}")
    print(f"  Has cognitive symptoms: {has_cognitive_symptoms}")
    print(f"  Is menopausal: {menopause_status in ['natural_menopause', 'surgical_menopause']}")
    
    # HRT recommendation logic
    should_recommend_hrt = (hormone_dysfunction or has_menopausal_symptoms or has_cognitive_symptoms or 
                           menopause_status in ['natural_menopause', 'surgical_menopause'])
    print(f"  Should recommend HRT: {should_recommend_hrt}")
    print(f"  Actual HRT recommendation: {processed.get('quick-female-hormones-hrt')}")

if __name__ == "__main__":
    debug_female_hormone_content() 