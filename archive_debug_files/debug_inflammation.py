#!/usr/bin/env python3
"""Debug script to check content control processing"""

from roadmap_generator import RoadmapGenerator

def debug_controls():
    generator = RoadmapGenerator()
    
    lab_results = {'INFLAM_CRP': 2.5, 'APO1': 'E3/E4', 'OMEGA_CHECK': 4.0}
    hhq_responses = {'gender': 'female'}
    client_data = {'name': 'Test Patient', 'gender': 'female'}
    
    processed = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    print('CRP-related controls:')
    for key, value in processed.items():
        if 'CRP' in key or 'crp' in key:
            print(f'  {key}: {value}')
    
    print('\nAPO E-related controls:')
    for key, value in processed.items():
        if 'apo' in key.lower() or 'e4' in key.lower():
            print(f'  {key}: {value}')
            
    print('\nOmega-related controls:')
    for key, value in processed.items():
        if 'omega' in key.lower():
            print(f'  {key}: {value}')

if __name__ == "__main__":
    debug_controls() 