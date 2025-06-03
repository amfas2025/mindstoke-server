#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_d_50_55_updated():
    """Test the updated D-50-55 vitamin D section"""
    
    print("🧪 Testing Updated D-50-55 Vitamin D Section")
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
    
    # Test vitamin D values in the 50-55 range
    test_values = [50, 52, 53, 55]
    
    for vit_d_value in test_values:
        print(f"\n📋 Test Case: Vitamin D = {vit_d_value} ng/mL")
        print("-" * 50)
        
        lab_results = {
            'VIT_D25': float(vit_d_value)
        }
        
        # Get processed content controls
        processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
        
        print(f"⚙️ Content Controls:")
        print("-" * 20)
        print(f"D-50-55: {processed_content.get('D-50-55', 'NOT SET')}")
        print(f"D-55-59: {processed_content.get('D-55-59', 'NOT SET')}")
        print(f"D-optimal: {processed_content.get('D-optimal', 'NOT SET')}")
        
        # Generate roadmap
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Search for vitamin D content
        print(f"\n📋 Vitamin D Content:")
        print("-" * 20)
        
        # Look for specific phrases from screenshot
        close_optimal = "close to the optimal parameters" in roadmap
        no_intervention = "no additional intervention is recommended" in roadmap
        check_few_times = "check your VITAMIN D level a few times per year" in roadmap
        not_drop = "make sure that it does not drop" in roadmap
        
        print(f"'close to the optimal parameters': {'✅ FOUND' if close_optimal else '❌ NOT FOUND'}")
        print(f"'no additional intervention is recommended': {'✅ FOUND' if no_intervention else '❌ NOT FOUND'}")
        print(f"'check your VITAMIN D level a few times per year': {'✅ FOUND' if check_few_times else '❌ NOT FOUND'}")
        print(f"'make sure that it does not drop': {'✅ FOUND' if not_drop else '❌ NOT FOUND'}")
        
        # Show vitamin D related lines
        lines = roadmap.split('\n')
        for i, line in enumerate(lines):
            if 'vitamin d' in line.lower() and any(phrase in line.lower() for phrase in ['close', 'optimal', 'intervention', 'drop']):
                print(f"Line {i}: {line.strip()}")

if __name__ == "__main__":
    test_d_50_55_updated() 