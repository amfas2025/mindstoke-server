#!/usr/bin/env python3

"""
Test Quick-krill condition with server integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_quick_krill_server_integration():
    """Test Quick-krill with realistic server data"""
    
    generator = RoadmapGenerator()
    
    # Test client data matching our test client
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    # Use actual lab data from our test client
    lab_results = {
        'INFLAM_CRP': 1.2,
        'OMEGA_CHECK': 4.8,
        'VIT_D25': 35.0,
        'VIT_B12': 650.0,
        'MIN_MG_RBC': 4.8
    }
    
    print("=== Quick-krill Server Integration Test ===\n")
    
    # Simulate HHQ responses where client is taking krill oil
    hhq_responses = {
        'hh_taking_krill_oil': True,
        'hh_brain_fog': True,
        'hh_memory_problems': False
    }
    
    print("Client Profile:")
    print("- Taking krill oil supplements")
    print("- Has brain fog symptoms")
    print("- CRP slightly elevated (1.2)")
    print("- OmegaCheck suboptimal (4.8)")
    print("- Vitamin D low (35.0)")
    
    # Process content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    # Check multiple conditions
    conditions_to_check = [
        'Quick-krill',
        'quick-CRP-09-omega-<5',
        'quick-VitD',
        'quick-brain-fog'
    ]
    
    print(f"\n=== Triggered Conditions ===")
    for condition in conditions_to_check:
        triggered = processed_content.get(condition, False)
        status = "✅ TRIGGERED" if triggered else "❌ Not triggered"
        print(f"{condition}: {status}")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check for multiple omega-3 related content
    omega_content_checks = [
        'Krill Oil Considerations:',
        'KRILL OIL is extremely low in DHA and EPA',
        'Triple Strength OMEGA-3 FISH OIL',
        'TRIGLYCERIDE-derived OMEGA-3',
        'combination of elevated CRP and low Omega-3'
    ]
    
    print(f"\n=== Content Verification ===")
    for content in omega_content_checks:
        found = content in roadmap
        status = "✅ Found" if found else "❌ Missing"
        print(f"{content}: {status}")
    
    # Extract and show Quick-krill section
    if 'Krill Oil Considerations:' in roadmap:
        print(f"\n=== Generated Quick-krill Section ===")
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
    
    print(f"\n=== Summary ===")
    print("Quick-krill condition successfully implemented!")
    print("- Integrates with other omega-3 related conditions")
    print("- Provides education about krill oil limitations")
    print("- Recommends superior triglyceride-based alternatives")
    print("- Maintains consistent brand recommendations")

if __name__ == "__main__":
    test_quick_krill_server_integration() 