#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_quick_vitd_row():
    """Test the quick-VitD-row vitamin D insufficiency section"""
    
    print("🧪 Testing Quick-VitD-row Vitamin D Section")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    hhq_responses = {}
    
    # Test different vitamin D values that should trigger quick-VitD-row
    test_cases = [
        (25, "D-less-30", "10,000 iu"),
        (35, "D-30-39", "8,000 iu"),
        (45, "D-40-49", "4,000 iu"),
        (55, "D-50-59", "2,000 iu"),
        (58, "D-50-59", "2,000 iu"),
        (65, None, None),  # Should NOT trigger quick-VitD-row
    ]
    
    for vit_d_value, expected_range, expected_dose in test_cases:
        print(f"\n📋 Test Case: Vitamin D = {vit_d_value} ng/mL")
        print("-" * 50)
        
        lab_results = {
            'VIT_D25': float(vit_d_value)
        }
        
        # Get processed content controls
        processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
        
        print(f"⚙️ Content Controls:")
        print("-" * 20)
        print(f"quick-VitD-row: {processed_content.get('quick-VitD-row', 'NOT SET')}")
        if expected_range:
            print(f"{expected_range}: {processed_content.get(expected_range, 'NOT SET')}")
        
        # Generate roadmap
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Search for quick-VitD-row content
        print(f"\n📋 Quick-VitD-row Content Check:")
        print("-" * 30)
        
        # Look for header phrase
        header_found = "Your VITAMIN D level is suboptimal, and supplementation is recommended" in roadmap
        guidebook_found = "Please note the section in your Guidebook" in roadmap
        
        print(f"Header text found: {'✅ YES' if header_found else '❌ NO'}")
        print(f"Guidebook reference found: {'✅ YES' if guidebook_found else '❌ NO'}")
        
        # Look for specific dosing recommendation
        if expected_dose:
            dose_found = expected_dose in roadmap
            print(f"Expected dose ({expected_dose}) found: {'✅ YES' if dose_found else '❌ NO'}")
        
        # Show relevant lines
        if header_found or guidebook_found:
            lines = roadmap.split('\n')
            for i, line in enumerate(lines):
                if any(phrase in line.lower() for phrase in ['suboptimal', 'supplementation', 'guidebook', 'encouraged to supplement']):
                    print(f"Line {i}: {line.strip()}")
        
        print(f"\n🎯 Expected to trigger quick-VitD-row: {'YES' if vit_d_value < 60 else 'NO'}")

if __name__ == "__main__":
    test_quick_vitd_row() 