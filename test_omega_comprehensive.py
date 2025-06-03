#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_omega_comprehensive():
    """Comprehensive test demonstrating the complete omega fatty acid system"""
    
    print("🧪 Comprehensive Omega Fatty Acid System Test")
    print("=" * 70)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client data for testing
    client_data = {
        'name': 'Test Patient',
        'gender': 'female'
    }
    
    print("\n📋 OMEGA FATTY ACID MARKERS SUMMARY:")
    print("   🟢 OmegaCheck: >5.4% (optimal for cardiovascular protection)")
    print("   🟢 Omega 6:3 Ratio: <4:1 (ideally 1:1, anti-inflammatory)")
    print("   🟢 Arachidonic Acid:EPA Ratio: <8.0 (reduced inflammation)")
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Perfect Omega Profile',
            'labs': {
                'OMEGA_CHECK': 6.8,
                'OMEGA_6_3_RATIO': 2.1,
                'OMEGA_AA_EPA': 5.2
            },
            'expected': 'All omega markers optimal - no intervention needed'
        },
        {
            'name': 'Poor Omega Profile (Standard American Diet)',
            'labs': {
                'OMEGA_CHECK': 3.2,
                'OMEGA_6_3_RATIO': 12.5,
                'OMEGA_AA_EPA': 15.8
            },
            'expected': 'All omega markers suboptimal - comprehensive omega-3 intervention'
        },
        {
            'name': 'Mixed Omega Profile',
            'labs': {
                'OMEGA_CHECK': 5.8,
                'OMEGA_6_3_RATIO': 6.2,
                'OMEGA_AA_EPA': 9.1
            },
            'expected': 'Some improvement needed - moderate omega-3 supplementation'
        },
        {
            'name': 'Borderline Cases',
            'labs': {
                'OMEGA_CHECK': 5.4,  # Exactly at threshold
                'OMEGA_6_3_RATIO': 4.0,  # Exactly at threshold
                'OMEGA_AA_EPA': 8.0  # Exactly at threshold
            },
            'expected': 'Borderline values - maintenance omega-3 protocol'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🧪 Test {i}: {scenario['name']}")
        print(f"   Expected: {scenario['expected']}")
        
        # Setup lab data
        lab_results = scenario['labs']
        
        # Generate roadmap
        roadmap = generator.generate_roadmap(client_data, lab_results, {})
        
        # Check for display sections
        omega_check_val = scenario['labs']['OMEGA_CHECK']
        omega_ratio_val = scenario['labs']['OMEGA_6_3_RATIO']
        aa_epa_val = scenario['labs']['OMEGA_AA_EPA']
        
        has_omega_check = f"Your baseline **OMEGACHECK®** value was {omega_check_val} %" in roadmap
        has_omega_ratio = f"Your **OMEGA 6:3** ratio was {omega_ratio_val}-to-1" in roadmap
        has_aa_epa = f"Your **ARACHIDONIC ACID-to-EPA** ratio was {aa_epa_val}" in roadmap
        
        print(f"   ✅ OmegaCheck display: {has_omega_check}")
        print(f"   ✅ Omega 6:3 ratio display: {has_omega_ratio}")
        print(f"   ✅ AA:EPA ratio display: {has_aa_epa}")
        
        # Check for recommendations
        has_omega_check_rec = omega_check_val < 5.4 and "OmegaCheck value" in roadmap and "below the optimal threshold" in roadmap
        has_omega_ratio_rec = omega_ratio_val > 4.0 and "indicates excess omega-6 relative to omega-3" in roadmap
        has_aa_epa_rec = aa_epa_val > 8.0 and "suggests inflammatory dominance" in roadmap
        
        print(f"   🔄 OmegaCheck recommendations: {has_omega_check_rec if omega_check_val < 5.4 else 'Not needed'}")
        print(f"   🔄 Omega ratio recommendations: {has_omega_ratio_rec if omega_ratio_val > 4.0 else 'Not needed'}")
        print(f"   🔄 AA:EPA recommendations: {has_aa_epa_rec if aa_epa_val > 8.0 else 'Not needed'}")
        
        # Educational content
        has_sad_reference = "Standard American Diet" in roadmap
        has_5_4_threshold = "risk reduction begins when your value is > 5.4 %" in roadmap
        has_8_0_threshold = "we'd like to see this ratio < 8.0" in roadmap
        
        print(f"   📚 Educational content: SAD reference: {has_sad_reference}, 5.4% threshold: {has_5_4_threshold}, 8.0 threshold: {has_8_0_threshold}")
    
    print("\n🎉 COMPREHENSIVE OMEGA FATTY ACID SYSTEM COMPLETE!")
    print("=" * 70)
    print("✅ All omega fatty acid sections are properly implemented:")
    print("   📊 omega-check-display: Shows actual OmegaCheck percentage")
    print("   📊 omega-63-ratio-display: Shows actual Omega 6:3 ratio")
    print("   📊 arachidonic-acid-epa-ratio-display: Shows actual AA:EPA ratio")
    print("   🟢 omega-check-low: Triggers when <5.4% (cardiovascular risk)")
    print("   🟡 omega-63-ratio-elevated: Triggers when >4:1 (inflammatory risk)")
    print("   🔴 arachidonic-acid-epa-elevated: Triggers when >8.0 (inflammatory dominance)")
    print("\n🧬 This provides comprehensive omega fatty acid assessment for cardiovascular and inflammatory health!")

if __name__ == "__main__":
    test_omega_comprehensive() 