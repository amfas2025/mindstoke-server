#!/usr/bin/env python3
"""
Debug script to show actual thyroid content generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator
import re

def debug_thyroid_content():
    """Debug thyroid content generation."""
    
    print("=== Debugging Thyroid Content Generation ===\n")
    
    generator = RoadmapGenerator()
    
    # Test case: Complex thyroid dysfunction with Hashimoto's
    client_data = {
        'firstname': 'Emma',
        'gender': 'female',
        'email': 'emma@test.com'
    }
    
    lab_results = {
        'THY_TSH': 4.2,        # Elevated
        'THY_T3F': 3.0,        # Low  
        'THY_T4F': 1.2,        # Low
        'RT3': 18,             # Elevated
        'THY_TPOAB': 65,       # Elevated (Hashimoto's)
        'THY_TGAB': 2.1        # Elevated (Hashimoto's)
    }
    
    hhq_responses = {
        'hh_chronic_fatigue': True,
        'hh_hashimotos': True,
        'hh_takes_thyroid_medicine': True
    }
    
    print("Input Lab Results:")
    print(f"  TSH: {lab_results['THY_TSH']} (optimal: 0.4-2.5)")
    print(f"  Free T3: {lab_results['THY_T3F']} (optimal: 3.2-4.2)")
    print(f"  Free T4: {lab_results['THY_T4F']} (optimal: 1.3-1.8)")
    print(f"  Reverse T3: {lab_results['RT3']} (optimal: <15)")
    print(f"  TPO Ab: {lab_results['THY_TPOAB']} (optimal: <34)")
    print(f"  TgAb: {lab_results['THY_TGAB']} (optimal: <1)")
    print()
    
    print("HHQ Responses:")
    print(f"  Chronic Fatigue: {hhq_responses['hh_chronic_fatigue']}")
    print(f"  Hashimoto's: {hhq_responses['hh_hashimotos']}")
    print(f"  Takes Thyroid Medicine: {hhq_responses['hh_takes_thyroid_medicine']}")
    print()
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract and display just the thyroid section
    thyroid_start = roadmap.find("## **Thyroid Function and Brain Health**")
    thyroid_end = roadmap.find("## **Hormone Optimization Protocols**")
    
    if thyroid_start != -1 and thyroid_end != -1:
        thyroid_section = roadmap[thyroid_start:thyroid_end]
        print("Generated Thyroid Section:")
        print("=" * 60)
        print(thyroid_section)
        print("=" * 60)
    else:
        print("Could not extract thyroid section from roadmap")
    
    # Show which conditions were triggered
    processed = generator._process_hhq_based_conditions(hhq_responses, lab_results)
    
    print("\nTriggered Thyroid Conditions:")
    thyroid_conditions = [
        'thyroid-optimal', 'thyroid-row', 'quick-TSH>7', 'low-TSH', 
        'High-thyroid', 'TSH-T3-rT3', 'quick-reverseT3', 'quick-fatigue', 
        'quick-hashimotos'
    ]
    
    for condition in thyroid_conditions:
        if condition in processed:
            print(f"  ✓ {condition}: {processed[condition]}")
        else:
            print(f"  - {condition}: not triggered")
    
    print(f"\nLab value displays:")
    display_vars = ['quick-TSH', 'quick-FT3', 'quick-FT4', 'quick-rT3', 'quick-TPO', 'quick-tg-ab']
    for var in display_vars:
        if var in processed:
            print(f"  {var}: {processed[var]}")
    
    print("\nDetailed Condition Analysis:")
    print(f"  TSH = {lab_results.get('THY_TSH')}")
    print(f"  TSH > 7? {lab_results.get('THY_TSH', 0) > 7}")
    print(f"  TSH > 2.5? {lab_results.get('THY_TSH', 0) > 2.5}")
    print(f"  TSH > 2.5 and <= 7? {2.5 < lab_results.get('THY_TSH', 0) <= 7}")
    print(f"  Takes thyroid medicine? {hhq_responses.get('hh_takes_thyroid_medicine', False)}")
    
    thyroid_dysfunction_present = (
        (lab_results.get('THY_TSH') and lab_results.get('THY_TSH') > 2.5) or
        (lab_results.get('THY_T3F') and lab_results.get('THY_T3F') < 3.2) or
        (lab_results.get('RT3') and lab_results.get('RT3') > 15)
    )
    print(f"  Thyroid dysfunction present? {thyroid_dysfunction_present}")
    
    has_chronic_fatigue = (hhq_responses.get('hh_chronic_fatigue', False) or 
                          hhq_responses.get('hh_chronic_fatigue_syndrome', False) or
                          hhq_responses.get('hh_fatigue', False))
    print(f"  Has chronic fatigue? {has_chronic_fatigue}")
    print(f"  Should trigger fatigue condition? {has_chronic_fatigue and thyroid_dysfunction_present}")
    print()

    # Test regex escaping specifically
    print("\nTesting Regex Escaping:")
    test_content = """
{{#quick-TSH>7}}
- HYPOTHYROIDISM MESSAGE
{{/quick-TSH>7}}
"""
    
    control_name = "quick-TSH>7"
    escaped_control_name = re.escape(control_name)
    print(f"  Original control name: {control_name}")
    print(f"  Escaped control name: {escaped_control_name}")
    
    # Test pattern matching
    block_pattern = f"{{{{#{escaped_control_name}}}}}(.*?){{{{/{escaped_control_name}}}}}"
    print(f"  Block pattern: {block_pattern}")
    
    matches = re.findall(block_pattern, test_content, flags=re.DOTALL)
    print(f"  Found matches: {matches}")
    
    # Test removal (when condition is False)
    result = re.sub(block_pattern, "", test_content, flags=re.DOTALL)
    print(f"  After removal: {repr(result)}")
    print()

if __name__ == "__main__":
    debug_thyroid_content() 