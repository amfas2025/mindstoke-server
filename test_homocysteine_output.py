#!/usr/bin/env python3

"""
Test to show actual homocysteine section output
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

def test_homocysteine_output():
    """Show the actual homocysteine section output"""
    print("=== Homocysteine Section Output ===\n")
    
    generator = RoadmapGenerator()
    
    # Lab results with elevated homocysteine
    lab_results = {
        'INFLAM_HOMOCYS': 12.5,  # Elevated (> 7)
        'VIT_B12': 450,          # Suboptimal (< 1000)
        'VIT_FOLATE': 8.2,       # Low (< 15)
    }
    
    client_data = {
        'name': 'Test Patient',
        'gender': 'male'
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results)
    
    # Extract just the homocysteine section
    start_marker = "↑'d Homocysteine Levels Can Impair Brain Function"
    end_marker = "---"
    
    start_pos = roadmap.find(start_marker)
    if start_pos != -1:
        # Find the end of this section
        end_pos = roadmap.find(end_marker, start_pos)
        if end_pos == -1:
            end_pos = start_pos + 1000  # Show first 1000 chars if no end marker
        
        homocysteine_section = roadmap[start_pos:end_pos]
        print("HOMOCYSTEINE SECTION OUTPUT:")
        print("=" * 60)
        print(homocysteine_section)
        print("=" * 60)
    else:
        print("Homocysteine section not found in roadmap")

if __name__ == "__main__":
    test_homocysteine_output() 