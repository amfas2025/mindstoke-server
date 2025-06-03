#!/usr/bin/env python3

"""
Debug script to check homocysteine value content controls
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

def debug_homocysteine_values():
    """Debug the homocysteine section value controls"""
    print("=== Debugging Homocysteine Value Controls ===\n")
    
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
    
    # Get the processed content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, {})
    
    print("Relevant content controls for homocysteine section:")
    print(f"quick-homocysteine: {processed_content.get('quick-homocysteine', 'NOT SET')}")
    print(f"homocysteine-value: {processed_content.get('homocysteine-value', 'NOT SET')}")
    print(f"quick-B12-value: {processed_content.get('quick-B12-value', 'NOT SET')}")
    print(f"quick-folic-acid-value: {processed_content.get('quick-folic-acid-value', 'NOT SET')}")
    
    print("\nAll controls containing 'B12':")
    for key, value in processed_content.items():
        if 'B12' in key or 'b12' in key.lower():
            print(f"{key}: {value}")
    
    print("\nAll controls containing 'folate' or 'folic':")
    for key, value in processed_content.items():
        if 'folate' in key.lower() or 'folic' in key.lower():
            print(f"{key}: {value}")
            
    print("\nAll controls containing 'homocysteine':")
    for key, value in processed_content.items():
        if 'homocysteine' in key.lower():
            print(f"{key}: {value}")

if __name__ == "__main__":
    debug_homocysteine_values() 