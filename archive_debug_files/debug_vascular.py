#!/usr/bin/env python3

from roadmap_generator import RoadmapGenerator

def debug_vascular_section():
    """Debug why the vascular section isn't appearing."""
    
    generator = RoadmapGenerator()
    
    # Simple test case with just vascular risk
    client_data = {'name': 'Test', 'gender': 'male', 'dob': '1970-01-01'}
    lab_results = {'VIT_D25': 30}
    hhq_responses = {
        'hh-heart-attack': True,
        'hh-high-blood-pressure': True,
        'hh-stroke': True
    }
    
    # Check risk profile processing
    risk_controls = generator._process_risk_profile_insights(hhq_responses)
    print("Risk controls generated:")
    for k, v in risk_controls.items():
        if 'vascular' in k.lower():
            print(f"  {k}: {v}")
    
    # Generate roadmap 
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check for vascular section
    vascular_markers = [
        'VASCULAR RISK',
        'risk-vascular-high',
        'Unhealthy blood flow to the brain'
    ]
    
    print("\nVascular section checks:")
    for marker in vascular_markers:
        if marker in roadmap:
            print(f"  ✅ Found: {marker}")
        else:
            print(f"  ❌ Missing: {marker}")
    
    # Show a snippet around where vascular section should be
    if 'RISK OF TOXICITY' in roadmap:
        toxic_idx = roadmap.find('RISK OF TOXICITY')
        snippet = roadmap[max(0, toxic_idx-500):toxic_idx+500]
        print(f"\nSnippet around toxic section (vascular should be nearby):")
        print(snippet)

if __name__ == "__main__":
    debug_vascular_section() 