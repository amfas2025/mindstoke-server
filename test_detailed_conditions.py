#!/usr/bin/env python3

"""
Test script to verify the detailed condition sections appear correctly in roadmaps.
"""

from roadmap_generator import RoadmapGenerator

def test_detailed_condition_sections():
    """Test that detailed condition sections appear when risk factors are high."""
    
    print("🧠 Testing Detailed Risk Condition Sections")
    print("=" * 60)
    
    generator = RoadmapGenerator()
    
    # Test client with high risk factors in multiple categories
    client_data = {
        'name': 'Test Patient',
        'gender': 'female',
        'dob': '1970-01-01'
    }
    
    # Minimal lab results 
    lab_results = {
        'VIT_D25': 25,
        'INFLAM_CRP': 3.5
    }
    
    # HHQ responses with high risk factors in each category
    hhq_responses = {
        # Traumatic
        'hh-head-injury': True,
        'hh-concussion': True,
        
        # Vascular  
        'hh-heart-attack': True,
        'hh-high-blood-pressure': True,
        
        # Toxic
        'hh-mold-exposure': True,
        'hh-chemical-exposure': True,
        
        # Glycotoxic
        'hh-diabetes': True,
        'hh-frequent-carb-sugar': True,
        
        # Atrophic
        'hh-menopause': True,
        'hh-thyroid-disease': True,
        
        # Inflammatory
        'hh-arthritis': True,
        'hh-chronic-pain': True
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Check for specific condition sections
    condition_markers = {
        'Traumatic': 'TRAUMATIC BRAIN INJURY (TBI) or repeat CONCUSSIONS can lead to impaired brain function',
        'Vascular': 'The intention is to improve cardiovascular health and the health of your blood vessels',
        'Toxic': 'RISK OF TOXICITY - Heavy Metals, Chemicals, Biotoxins may negatively impact brain health',
        'Glycotoxic': 'GLYCOTOXIC RISK - ↑\'d Blood Sugar, Insulin Resistance, or Diabetes may negatively impact brain health',
        'Atrophic': 'INSUFFICIENCY SYNDROMES such as suboptimal levels of nutrients, minerals, and hormones can impact brain health',
        'Inflammatory': 'Systemic INFLAMMATION can lead to neurological impairment and negatively impact brain health'
    }
    
    # Test each condition section
    for category, marker in condition_markers.items():
        if marker in roadmap:
            print(f"✅ {category} condition section found")
            
            # Extract the section content
            start_idx = roadmap.find(marker)
            if start_idx != -1:
                end_idx = roadmap.find('###', start_idx + 1)
                if end_idx == -1:
                    end_idx = roadmap.find('---', start_idx + 1)
                if end_idx == -1:
                    end_idx = start_idx + 500  # fallback
                
                section_content = roadmap[start_idx:end_idx]
                print(f"   📄 {category} section preview:")
                print(f"   {section_content[:200]}...")
                print()
        else:
            print(f"❌ {category} condition section NOT found")
    
    # Check for risk profile section
    if 'Risk Profile' in roadmap and 'risk factors for cognitive decline' in roadmap:
        print("✅ Risk Profile section found")
    else:
        print("❌ Risk Profile section NOT found")
    
    # Check for screening tests section
    if 'Additional Screening Tests Related to Brain Health' in roadmap:
        print("✅ Additional Screening Tests section found")
    else:
        print("❌ Additional Screening Tests section NOT found")
    
    print("\n" + "=" * 60)
    print("Detailed condition sections test completed!")

if __name__ == "__main__":
    test_detailed_condition_sections() 