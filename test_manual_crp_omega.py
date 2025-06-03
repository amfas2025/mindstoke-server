#!/usr/bin/env python3

"""
Manual test for CRP-Omega compound condition with realistic values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_manual_crp_omega():
    """Test with manually set CRP and Omega values"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Manual CRP-Omega Test with Realistic Values ===\n")
    
    # Realistic scenario: Elevated inflammation with poor omega status
    lab_results = {
        'INFLAM_CRP': 2.1,  # Elevated CRP (>0.9)
        'OMEGA_CHECK': 4.2,  # Low omega status (<5.4)
        'VIT_D25': 35.0,     # Add some other labs for context
        'VIT_B12': 650.0
    }
    
    print("Lab Values:")
    print(f"  CRP: {lab_results['INFLAM_CRP']} mg/L")
    print(f"  OmegaCheck: {lab_results['OMEGA_CHECK']}")
    print(f"  Vitamin D: {lab_results['VIT_D25']} ng/mL")
    print(f"  Vitamin B12: {lab_results['VIT_B12']} pg/mL")
    
    # Process content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, {})
    
    # Check if condition is triggered
    triggered = processed_content.get('quick-CRP-09-omega-<5', False)
    print(f"\nCondition 'quick-CRP-09-omega-<5' triggered: {triggered}")
    
    if triggered:
        print("✅ Condition correctly triggered!")
        
        # Generate full roadmap to check content
        roadmap = generator.generate_roadmap(client_data, lab_results, {})
        
        # Look for the specific content
        if 'Triple Strength OMEGA-3 FISH OIL' in roadmap:
            print("✅ Complete omega-3 content found in roadmap!")
            
            # Extract and display the relevant section
            lines = roadmap.split('\n')
            in_section = False
            section_lines = []
            
            for line in lines:
                if 'combination of elevated CRP and low Omega-3' in line:
                    in_section = True
                    section_lines.append(line)
                elif in_section and line.strip() == '':
                    break
                elif in_section:
                    section_lines.append(line)
            
            if section_lines:
                print("\n=== Generated Content ===")
                for line in section_lines:
                    print(line)
        else:
            print("❌ Omega-3 content not found in roadmap")
    else:
        print("❌ Condition should have been triggered")
        print(f"CRP ({lab_results['INFLAM_CRP']}) > 0.9? {lab_results['INFLAM_CRP'] > 0.9}")
        print(f"OmegaCheck ({lab_results['OMEGA_CHECK']}) < 5.4? {lab_results['OMEGA_CHECK'] < 5.4}")

if __name__ == "__main__":
    test_manual_crp_omega() 