#!/usr/bin/env python3
"""Debug APO E processing"""

from roadmap_generator import RoadmapGenerator

def debug_apo_e():
    generator = RoadmapGenerator()
    
    lab_results = {'APO1': 'E3/E4'}
    apo_e = generator._get_lab_value(lab_results, ['APO1', 'APO E Genotyping Result'])
    print(f'APO E value extracted: {apo_e}')
    print(f'APO E type: {type(apo_e)}')
    
    if apo_e:
        apo_str = str(apo_e)
        print(f'APO E string: "{apo_str}"')
        print(f'Contains E4: {"E4" in apo_str}')
    
    # Test the genetics processing directly
    processed = generator._process_genetics_comprehensive(lab_results)
    print(f'\nGenetics processing results:')
    for key, value in processed.items():
        print(f'  {key}: {value}')

if __name__ == "__main__":
    debug_apo_e() 