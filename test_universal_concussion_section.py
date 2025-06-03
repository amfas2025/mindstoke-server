#!/usr/bin/env python3
"""
Test script to verify the universal concussion section appears for all patients
"""

from roadmap_generator import RoadmapGenerator
import re

def test_universal_concussion_section():
    """Test that the universal concussion section appears for all patients."""
    
    print("=== Testing Universal Concussion Section ===\n")
    
    generator = RoadmapGenerator()
    
    # Test with different patient profiles to ensure universality
    test_cases = [
        {
            'name': 'Test Patient 1 - Male with minimal labs',
            'client_data': {'name': 'John Doe', 'gender': 'male'},
            'lab_results': {'INFLAM_CRP': 0.8},  # Low CRP
            'hhq_responses': {'gender': 'male'}
        },
        {
            'name': 'Test Patient 2 - Female with elevated markers',
            'client_data': {'name': 'Jane Smith', 'gender': 'female'},
            'lab_results': {'INFLAM_CRP': 3.5, 'APO1': 'E3/E4'},  # High CRP + APO E4
            'hhq_responses': {'gender': 'female', 'hh_brain_fog': True}
        },
        {
            'name': 'Test Patient 3 - No inflammation markers',
            'client_data': {'name': 'Alex Johnson', 'gender': 'female'},
            'lab_results': {'VIT_D25': 45},  # Only vitamin D
            'hhq_responses': {'gender': 'female'}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        
        # Generate roadmap
        roadmap = generator.generate_roadmap(
            test_case['client_data'], 
            test_case['lab_results'], 
            test_case['hhq_responses']
        )
        
        # Check for the concussion section
        concussion_section_found = "The Symptoms of a Historical Concussion May Be Chronic" in roadmap
        
        if concussion_section_found:
            print("  ✓ Universal concussion section found")
            
            # Check for key content elements
            key_elements = [
                "TSI Masterclass",
                "DYSAUTONOMIA", 
                "VOMS assessment",
                "ANTIOXIDANT CHALLENGE",
                "HYPERBARIC OXYGEN",
                "PROGESTERONE"
            ]
            
            elements_found = []
            for element in key_elements:
                if element in roadmap:
                    elements_found.append(element)
            
            print(f"  ✓ Key elements found: {len(elements_found)}/{len(key_elements)}")
            print(f"    - {', '.join(elements_found)}")
            
            # Check positioning after inflammation section
            inflammation_pos = roadmap.find("Chronic Inflammation Can Lead to Inflammation in Your Brain")
            concussion_pos = roadmap.find("The Symptoms of a Historical Concussion May Be Chronic")
            
            if inflammation_pos < concussion_pos:
                print("  ✓ Concussion section correctly positioned after inflammation section")
            else:
                print("  ⚠ Warning: Section positioning may be incorrect")
                
        else:
            print("  ✗ Universal concussion section NOT found")
            
        print()
    
    # Test specific content extraction
    print("=== Content Detail Check ===")
    
    # Use first test case for detailed content check
    roadmap = generator.generate_roadmap(
        test_cases[0]['client_data'], 
        test_cases[0]['lab_results'], 
        test_cases[0]['hhq_responses']
    )
    
    # Extract the concussion section
    concussion_match = re.search(
        r'## \*\*The Symptoms of a Historical Concussion May Be Chronic\*\*(.*?)(?=##|\Z)', 
        roadmap, 
        re.DOTALL
    )
    
    if concussion_match:
        concussion_content = concussion_match.group(1).strip()
        print(f"Concussion section length: {len(concussion_content)} characters")
        
        # Check for important subsections
        subsections = [
            "TSI Masterclass",
            "VOMS assessment", 
            "High-Tech Support Options",
            "ANTIOXIDANT CHALLENGE",
            "PROGESTERONE"
        ]
        
        print("\nSubsection content check:")
        for subsection in subsections:
            if subsection in concussion_content:
                print(f"  ✓ {subsection} content found")
            else:
                print(f"  ✗ {subsection} content missing")
        
        # Check for YouTube link
        if "youtube.com" in concussion_content:
            print("  ✓ YouTube link found")
        else:
            print("  ✗ YouTube link missing")
            
        # Check for masterclass links
        masterclass_links = concussion_content.count("community.amindforallseasons.com")
        print(f"  ✓ Found {masterclass_links} masterclass link(s)")
    else:
        print("Could not extract concussion section for detailed analysis")

if __name__ == "__main__":
    test_universal_concussion_section() 