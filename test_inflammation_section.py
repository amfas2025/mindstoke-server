#!/usr/bin/env python3
"""
Test script to verify the chronic inflammation section is working properly
"""

from roadmap_generator import RoadmapGenerator
import re

def test_inflammation_section():
    """Test the chronic inflammation section rendering."""
    
    print("=== Testing Chronic Inflammation Section ===\n")
    
    generator = RoadmapGenerator()
    
    # Test data that should trigger CRP conditions
    client_data = {'name': 'Test Patient', 'gender': 'female'}
    
    lab_results = {
        'INFLAM_CRP': 2.5,  # Elevated CRP > 1
        'APO1': 'E3/E4',    # APO E4 genetics  
        'OMEGA_CHECK': 4.0  # Low omega-3
    }
    
    hhq_responses = {
        'gender': 'female'
    }
    
    # Generate the roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Look for the chronic inflammation section
    inflammation_section = re.search(r'## \*\*Chronic Inflammation.*?(?=---|$)', roadmap, re.DOTALL)
    
    if inflammation_section:
        print('✓ Chronic Inflammation section found!')
        section_content = inflammation_section.group(0)
        print(f"Section length: {len(section_content)} characters")
        print("\nFirst 800 characters:")
        print(section_content[:800] + "...")
        print("\n" + "="*50)
        
        # Check for specific content
        checks = [
            ('CRP value display', 'baseline **hsCRP** is 2.5' in section_content),
            ('Triggers table', 'Triggers of Systemic Inflammation' in section_content),
            ('Table structure', '| **Low Grade Infections**' in section_content),
            ('CRP > 1 messaging', 'CRP > 1:' in section_content),
            ('APO E4 content', 'APO E4' in section_content),
            ('Masterclass link', 'https://community.amindforallseasons.com' in section_content)
        ]
        
        print("\nContent checks:")
        for check_name, result in checks:
            status = "✓" if result else "✗"
            print(f"{status} {check_name}: {result}")
            
    else:
        print('✗ Chronic Inflammation section NOT found')
        print("Available sections in roadmap:")
        sections = re.findall(r'## \*\*([^*]+)\*\*', roadmap)
        for section in sections[:10]:  # Show first 10 sections
            print(f"  - {section}")
    
    return inflammation_section is not None

if __name__ == "__main__":
    test_inflammation_section() 