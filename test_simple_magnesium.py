#!/usr/bin/env python3

"""
Simple test for Magnesium RBC logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_simple_magnesium():
    generator = RoadmapGenerator()
    
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    # Test with low magnesium
    lab_results = {'MIN_MG_RBC': 4.8}
    
    processed = generator._process_all_content_controls(client_data, lab_results, {})
    
    print("=== Low Magnesium Test (4.8) ===")
    print(f"quick-MagRBC value: {processed.get('quick-MagRBC')}")
    print(f"quick-MagRBC-low: {processed.get('quick-MagRBC-low')}")
    print(f"quick-MagRBC-optimal: {processed.get('quick-MagRBC-optimal')}")
    
    # Generate actual roadmap content
    roadmap = generator.generate_roadmap(client_data, lab_results, {})
    
    # Look for magnesium section
    lines = roadmap.split('\n')
    mag_lines = []
    in_mag_section = False
    
    for line in lines:
        if 'Magnesium RBC Optimization:' in line:
            in_mag_section = True
            mag_lines.append(line)
        elif in_mag_section and line.strip() == '':
            if len(mag_lines) > 1:  # Don't break on first empty line
                break
        elif in_mag_section:
            mag_lines.append(line)
    
    print("\n=== Generated Magnesium Section ===")
    for line in mag_lines:
        print(line)

if __name__ == "__main__":
    test_simple_magnesium() 