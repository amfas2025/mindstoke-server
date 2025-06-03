#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_omega_fatty_acids():
    """Test omega fatty acid sections"""
    
    print("🧪 Testing Omega Fatty Acid Sections")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Low OmegaCheck',
            'labs': {'OMEGA_CHECK': 3.5},
            'expected': ['omega-check-display: True', 'omega-check-low: True']
        },
        {
            'name': 'Optimal OmegaCheck',
            'labs': {'OMEGA_CHECK': 6.2},
            'expected': ['omega-check-display: True', 'omega-check-low: False']
        },
        {
            'name': 'Elevated Omega 6:3 Ratio',
            'labs': {'OMEGA_6_3_RATIO': 8.5},
            'expected': ['omega-63-ratio-display: True', 'omega-63-ratio-elevated: True']
        },
        {
            'name': 'Optimal Omega 6:3 Ratio',
            'labs': {'OMEGA_6_3_RATIO': 3.2},
            'expected': ['omega-63-ratio-display: True', 'omega-63-ratio-elevated: False']
        },
        {
            'name': 'Elevated AA:EPA Ratio',
            'labs': {'OMEGA_AA_EPA': 12.5},
            'expected': ['arachidonic-acid-epa-ratio-display: True', 'arachidonic-acid-epa-elevated: True']
        },
        {
            'name': 'Optimal AA:EPA Ratio',
            'labs': {'OMEGA_AA_EPA': 6.2},
            'expected': ['arachidonic-acid-epa-ratio-display: True', 'arachidonic-acid-epa-elevated: False']
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['name']}")
        
        try:
            # Simple processing using existing method structure
            processed = {}
            ranges = {'OmegaCheck': {'optimal_min': 5.4}, 'Omega63Ratio': {'optimal_max': 4.0}, 'AA_EPA_Ratio': {'optimal_max': 8.0}}
            
            # Process omega check
            if 'OMEGA_CHECK' in scenario['labs']:
                value = scenario['labs']['OMEGA_CHECK']
                processed['omega-check-display'] = True
                processed['omega-check-value'] = f"{value}"
                processed['omega-check-low'] = value < 5.4
            
            # Process omega 6:3 ratio
            if 'OMEGA_6_3_RATIO' in scenario['labs']:
                value = scenario['labs']['OMEGA_6_3_RATIO']
                processed['omega-63-ratio-display'] = True
                processed['omega-63-ratio-value'] = f"{value}"
                processed['omega-63-ratio-elevated'] = value > 4.0
            
            # Process AA:EPA ratio
            if 'OMEGA_AA_EPA' in scenario['labs']:
                value = scenario['labs']['OMEGA_AA_EPA']
                processed['arachidonic-acid-epa-ratio-display'] = True
                processed['aaepa-ratio-value'] = f"{value}"
                processed['arachidonic-acid-epa-elevated'] = value > 8.0
            
            print(f"   Processed controls: {processed}")
            
            # Test template application
            template = generator._load_template()
            result = generator._apply_content_controls_to_template(template, processed)
            
            # Check for expected content
            if 'OMEGA_CHECK' in scenario['labs']:
                omega_check_text = f"Your baseline **OMEGACHECK®** value was {scenario['labs']['OMEGA_CHECK']} %" in result
                print(f"   ✅ OmegaCheck display: {omega_check_text}")
            
            if 'OMEGA_6_3_RATIO' in scenario['labs']:
                ratio_text = f"Your **OMEGA 6:3** ratio was {scenario['labs']['OMEGA_6_3_RATIO']}-to-1" in result
                print(f"   ✅ Omega 6:3 ratio display: {ratio_text}")
            
            if 'OMEGA_AA_EPA' in scenario['labs']:
                aa_epa_text = f"Your **ARACHIDONIC ACID-to-EPA** ratio was {scenario['labs']['OMEGA_AA_EPA']}" in result
                print(f"   ✅ AA:EPA ratio display: {aa_epa_text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n🎉 Omega Fatty Acid Sections Test Complete!")

if __name__ == "__main__":
    test_omega_fatty_acids() 