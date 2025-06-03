#!/usr/bin/env python3

"""
Test script to verify homocysteine section functionality
Tests the updated homocysteine section with B12 and folate values
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator

def test_homocysteine_section():
    """Test the homocysteine section with elevated values"""
    print("=== Testing Homocysteine Section ===\n")
    
    generator = RoadmapGenerator()
    
    # Test case: Client with elevated homocysteine and related B-vitamin issues
    print("Testing client WITH elevated homocysteine:")
    print("   - Homocysteine: 12.5 μmol/L (> 7 optimal)")
    print("   - B12: 450 pg/mL (< 1000 optimal)")
    print("   - Folate: 8.2 ng/mL (< 15 optimal)")
    print("   - Expected: Detailed homocysteine section should appear\n")
    
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
    
    # Check for homocysteine section presence
    if "↑'d Homocysteine Levels Can Impair Brain Function" in roadmap:
        print("✓ PASS: Homocysteine section title found")
        
        # Check for specific values
        if "12.5 μmol/L" in roadmap:
            print("✓ PASS: Homocysteine value (12.5 μmol/L) found")
        else:
            print("✗ FAIL: Homocysteine value not found")
            
        if "450.0 pg/mL" in roadmap:
            print("✓ PASS: B12 value (450.0 pg/mL) found")
        else:
            print("✗ FAIL: B12 value not found")
            
        if "8.2 ng/mL" in roadmap:
            print("✓ PASS: Folate value (8.2 ng/mL) found")
        else:
            print("✗ FAIL: Folate value not found")
            
        # Check for explanatory text
        if "goal level < 7 umol/L" in roadmap:
            print("✓ PASS: Homocysteine goal found")
        else:
            print("✗ FAIL: Homocysteine goal not found")
            
        if "> 1000 pg/mL to best support brain health" in roadmap:
            print("✓ PASS: B12 goal found")
        else:
            print("✗ FAIL: B12 goal not found")
            
        if "> 15 ng/mL to best support brain health" in roadmap:
            print("✓ PASS: Folate goal found")
        else:
            print("✗ FAIL: Folate goal not found")
            
        if "masterclass" in roadmap.lower():
            print("✓ PASS: Masterclass link found")
        else:
            print("✗ FAIL: Masterclass link not found")
            
    else:
        print("✗ FAIL: Homocysteine section not found in roadmap")
        print("\nFirst 1000 characters of roadmap:")
        print(roadmap[:1000])
    
    print("\n" + "="*50)
    
    # Test case 2: Normal homocysteine (should not show section)
    print("\nTesting client with NORMAL homocysteine:")
    print("   - Homocysteine: 5.2 μmol/L (< 7 optimal)")
    print("   - Expected: Homocysteine section should NOT appear\n")
    
    lab_results_normal = {
        'INFLAM_HOMOCYS': 5.2,  # Normal (< 7)
        'VIT_B12': 850,
        'VIT_FOLATE': 18.5,
    }
    
    roadmap_normal = generator.generate_roadmap(client_data, lab_results_normal)
    
    if "↑'d Homocysteine Levels Can Impair Brain Function" not in roadmap_normal:
        print("✓ PASS: Homocysteine section correctly hidden for normal values")
    else:
        print("✗ FAIL: Homocysteine section should not appear for normal values")

if __name__ == "__main__":
    test_homocysteine_section() 