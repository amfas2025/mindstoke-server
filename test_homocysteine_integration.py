#!/usr/bin/env python3

"""
Integration test for homocysteine condition in full roadmap generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_homocysteine_integration():
    """Test homocysteine condition in full roadmap generation"""
    
    generator = RoadmapGenerator()
    
    # Test client data with elevated homocysteine
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    # Lab results with high homocysteine that should trigger all conditions
    lab_results = {
        'INFLAM_HOMOCYS': 16.2,  # High level >15 (should trigger all)
        'VIT_B12': 420,          # Low B12
        'VIT_D25': 35.0,         # Some other labs
        'OMEGA_CHECK': 4.8       # Low omega-3
    }
    
    print("=== Testing Homocysteine Integration ===")
    print(f"Homocysteine level: {lab_results['INFLAM_HOMOCYS']} umol/L")
    print(f"B12 level: {lab_results['VIT_B12']} pg/mL")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, {})
    
    # Check if homocysteine section is present
    if '↑\'d Homocysteine Levels Can Impair Brain Function' in roadmap:
        print("✅ Homocysteine section found in roadmap")
        
        # Check for specific content
        content_checks = [
            'Your HOMOCYSTEINE level was 16.2',
            'goal level < 7 umol/L',
            'TRIMETHYLGLYCINE 1000 mg/day',
            'CREATINE MONOHYDRATE',
            'Your VITAMIN B12 level was 420.0'
        ]
        
        found_content = []
        missing_content = []
        
        for check in content_checks:
            if check in roadmap:
                found_content.append(check)
            else:
                missing_content.append(check)
        
        print(f"✅ Found {len(found_content)}/{len(content_checks)} expected content elements")
        
        if missing_content:
            print(f"❌ Missing content: {missing_content}")
        else:
            print("✅ All expected content found!")
            
        # Extract and show the homocysteine section
        print("\n=== Homocysteine Section Extract ===")
        lines = roadmap.split('\n')
        in_section = False
        section_lines = []
        
        for line in lines:
            if '↑\'d Homocysteine Levels Can Impair Brain Function' in line:
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() == '---':
                break
            elif in_section:
                section_lines.append(line)
        
        for line in section_lines[:10]:  # Show first 10 lines
            print(line)
        
        if len(section_lines) > 10:
            print("... (truncated)")
            
    else:
        print("❌ Homocysteine section NOT found in roadmap")
        
        # Debug: Show what sections ARE present
        print("\nDebug: Sections found in roadmap:")
        lines = roadmap.split('\n')
        for line in lines:
            if line.startswith('##'):
                print(f"  {line}")

if __name__ == "__main__":
    test_homocysteine_integration() 