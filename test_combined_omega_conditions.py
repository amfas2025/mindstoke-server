#!/usr/bin/env python3

"""
Test script for combined omega-3 related conditions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_combined_omega_conditions():
    """Test how multiple omega-3 conditions work together"""
    
    generator = RoadmapGenerator()
    
    # Test client with multiple omega-3 risk factors
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Combined OMEGA-3 Conditions ===\n")
    
    # Complex scenario: Concussion + taking krill oil + elevated CRP + low omega status
    print("Complex Scenario: Multiple omega-3 risk factors")
    hhq_responses = {
        'hh_concussion': True,           # Should trigger OMEGA-3 CHALLENGE
        'hh_taking_krill_oil': True,     # Should trigger krill oil advice
        'hh_brain_fog': True,
        'hh_memory_problems': True
    }
    
    lab_results = {
        'INFLAM_CRP': 1.5,              # Should trigger CRP-omega compound condition
        'OMEGA_CHECK': 4.2,             # Low omega status
        'OMEGA_6_3_RATIO': 8.5,         # Elevated ratio
        'VIT_D25': 32.0,                # Low vitamin D
        'VIT_B12': 420.0                # Suboptimal B12
    }
    
    print("Client Profile:")
    print("- History of concussion")
    print("- Currently taking krill oil")
    print("- CRP elevated (1.5)")
    print("- OmegaCheck low (4.2)")
    print("- Omega 6:3 ratio elevated (8.5)")
    print("- Vitamin D low (32.0)")
    print("- Brain fog and memory issues")
    
    # Process content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    # Check all omega-3 related conditions
    omega_conditions = [
        'checked-omega-63-ratio',        # OMEGA-3 CHALLENGE
        'Quick-krill',                   # Krill oil advice
        'quick-CRP-09-omega-<5',        # CRP + low omega compound
        'quick-brain-fog',               # Brain fog symptoms
        'quick-memory-issues',           # Memory problems
        'quick-VitD'                     # Vitamin D status
    ]
    
    print(f"\n=== Triggered Conditions ===")
    for condition in omega_conditions:
        triggered = processed_content.get(condition, False)
        status = "✅ TRIGGERED" if triggered else "❌ Not triggered"
        print(f"{condition}: {status}")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check for all omega-3 related content in the roadmap
    omega_content_checks = [
        'OMEGA-3 CHALLENGE Protocol:',
        '10,000 mg of combined EPA and DHA',
        'Dr. Michael Lewis',
        'Krill Oil Considerations:',
        'KRILL OIL is extremely low in DHA and EPA',
        'combination of elevated CRP and low Omega-3',
        'Triple Strength OMEGA-3 FISH OIL',
        'TRIGLYCERIDE-derived OMEGA-3'
    ]
    
    print(f"\n=== Content Verification ===")
    found_content = []
    missing_content = []
    
    for content in omega_content_checks:
        found = content in roadmap
        if found:
            found_content.append(content)
        else:
            missing_content.append(content)
        status = "✅ Found" if found else "❌ Missing"
        print(f"{content}: {status}")
    
    # Extract and show all omega-3 related sections
    print(f"\n=== Generated OMEGA-3 Related Content ===")
    
    # OMEGA-3 CHALLENGE section
    if 'OMEGA-3 CHALLENGE Protocol:' in roadmap:
        print("\n--- OMEGA-3 CHALLENGE Section ---")
        lines = roadmap.split('\n')
        in_section = False
        
        for line in lines:
            if 'OMEGA-3 CHALLENGE Protocol:' in line:
                in_section = True
                print(line)
            elif in_section and line.strip() == '':
                break
            elif in_section:
                print(line)
    
    # Krill Oil section
    if 'Krill Oil Considerations:' in roadmap:
        print("\n--- Krill Oil Considerations Section ---")
        lines = roadmap.split('\n')
        in_section = False
        
        for line in lines:
            if 'Krill Oil Considerations:' in line:
                in_section = True
                print(line)
            elif in_section and line.strip() == '':
                break
            elif in_section:
                print(line)
    
    # CRP-Omega compound section
    if 'Compound Inflammation Risk:' in roadmap:
        print("\n--- CRP-Omega Compound Section ---")
        lines = roadmap.split('\n')
        in_section = False
        
        for line in lines:
            if 'Compound Inflammation Risk:' in line:
                in_section = True
                print(line)
            elif in_section and line.strip() == '':
                break
            elif in_section:
                print(line)
    
    print(f"\n=== Analysis ===")
    print(f"Total omega-3 conditions triggered: {len([c for c in omega_conditions if processed_content.get(c, False)])}")
    print(f"Content sections found: {len(found_content)}")
    print(f"Content sections missing: {len(missing_content)}")
    
    if len(found_content) >= 6:
        print("✅ Excellent integration - multiple omega-3 conditions working together!")
    elif len(found_content) >= 4:
        print("✅ Good integration - most omega-3 conditions working")
    else:
        print("❌ Integration issues - some omega-3 conditions not working properly")
    
    print(f"\n=== Clinical Interpretation ===")
    print("This client would receive comprehensive omega-3 optimization:")
    print("1. OMEGA-3 CHALLENGE (10,000mg for 1-2 months) for neurological recovery")
    print("2. Advice to switch from krill oil to superior triglyceride-based fish oil")
    print("3. Recognition of compound inflammation risk (CRP + low omega-3)")
    print("4. Standard omega-3 maintenance protocol after challenge period")
    print("5. Integrated approach addressing both neurological and inflammatory aspects")

if __name__ == "__main__":
    test_combined_omega_conditions() 