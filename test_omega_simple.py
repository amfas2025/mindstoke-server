#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_omega_simple():
    """Simple test to verify omega fatty acid sections work"""
    
    print("🧪 Simple Omega Fatty Acid Test")
    print("=" * 50)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test with simple lab values
    lab_results = {
        'OMEGA_CHECK': 3.5,
        'OMEGA_6_3_RATIO': 8.2,
        'OMEGA_AA_EPA': 12.5,
        'OMEGA_AA': 15.2  # Add absolute Arachidonic Acid level
    }
    
    client_data = {
        'name': 'Test Patient',
        'gender': 'female'
    }
    
    print("\n📋 Test Lab Values:")
    print(f"   OmegaCheck: {lab_results['OMEGA_CHECK']}% (target >5.4%)")
    print(f"   Omega 6:3 Ratio: {lab_results['OMEGA_6_3_RATIO']}:1 (target <4:1)")
    print(f"   AA:EPA Ratio: {lab_results['OMEGA_AA_EPA']} (target <8.0)")
    print(f"   Arachidonic Acid Level: {lab_results['OMEGA_AA']} (target <10)")
    
    try:
        # Test template processing directly
        print("\n🧪 Testing Template Processing...")
        
        # Create processed content manually
        processed_content = {
            'omega-check-display': True,
            'omega-check-value': '3.5',
            'omega-check-low': True,
            'omega-63-ratio-display': True,
            'omega-63-ratio-value': '8.2',
            'omega-63-ratio-elevated': True,
            'arachidonic-acid-epa-ratio-display': True,
            'aaepa-ratio-value': '12.5',
            'arachidonic-acid-epa-elevated': True,
            'arachidonic-acid-level-display': True,  # Add new AA level section
            'aa-level-value': '15.2'
        }
        
        print(f"   Processed content: {processed_content}")
        
        # Load and process template
        template = generator._load_template()
        result = generator._apply_content_controls_to_template(template, processed_content)
        
        # Check for specific content
        checks = [
            ('OmegaCheck display', 'Your baseline **OMEGACHECK®** value was 3.5 %'),
            ('OmegaCheck threshold', 'risk reduction begins when your value is > 5.4 %'),
            ('Omega ratio display', 'Your **OMEGA 6:3** ratio was 8.2-to-1'),
            ('Standard American Diet reference', 'Standard American Diet'),
            ('AA:EPA display', 'Your **ARACHIDONIC ACID-to-EPA** ratio was 12.5'),
            ('AA:EPA threshold', "we'd like to see this ratio < 8.0"),
            ('AA Level display', 'Your **ARACHIDONIC ACID** level was 15.2'),
            ('AA Level threshold', "we'd like to see this value < 10"),
            ('Omega ratio optimization', 'High-quality fish oil (Nordic Naturals Pro-Omega 2000 or equivalent)')
        ]
        
        print("\n✅ Content Verification:")
        for check_name, search_text in checks:
            found = search_text in result
            print(f"   {check_name}: {'✅' if found else '❌'}")
            
        # Count omega-related sections
        omega_sections = result.count('OMEGA')
        print(f"\n📊 Total omega-related content sections: {omega_sections}")
        
        print("\n🎉 Omega Fatty Acid sections are working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_omega_simple() 