#!/usr/bin/env python3
"""Test APO E4 content rendering"""

from roadmap_generator import RoadmapGenerator
import re

def test_apo_content():
    generator = RoadmapGenerator()
    client_data = {'name': 'Test Patient', 'gender': 'female'}
    lab_results = {'INFLAM_CRP': 2.5, 'APO1': 'E3/E4', 'OMEGA_CHECK': 4.0}
    hhq_responses = {'gender': 'female'}

    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)

    # Extract just the APO E4 section from template
    template_section = re.search(r'{{#quick-apo-e4-genetics}}.*?{{/quick-apo-e4-genetics}}', roadmap, re.DOTALL)
    if template_section:
        print('APO E4 section found in template')
    else:
        print('APO E4 section NOT found in template')

    # Check if the processed content is in the final roadmap
    if 'APO E4' in roadmap:
        print('APO E4 text found in final roadmap')
        apo_content = re.search(r'.*APO E4.*', roadmap)
        if apo_content:
            print(f'APO E4 line: {apo_content.group(0)}')
    else:
        print('APO E4 text NOT found in final roadmap')

    # Check for masterclass link
    if 'https://community.amindforallseasons.com' in roadmap:
        print('Masterclass link found')
    else:
        print('Masterclass link NOT found')
        
    # Check content controls
    processed = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    print(f"\nAPO E4 genetics control: {processed.get('quick-apo-e4-genetics', 'NOT FOUND')}")

if __name__ == "__main__":
    test_apo_content() 