#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_d_60_plus():
    """Test vitamin D content for 60+ ng/mL values"""
    
    print("🧪 Testing D-60+ Vitamin D Section")
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
    
    # Test different vitamin D values in the optimal range
    test_values = [60, 65, 70, 75, 80]
    
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
        print(f"D-optimal: {processed_content.get('D-optimal', 'NOT SET')}")
        print(f"D-55-59: {processed_content.get('D-55-59', 'NOT SET')}")
        print(f"D-high: {processed_content.get('D-high', 'NOT SET')}")
        
        # Generate roadmap
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Search for vitamin D content
        print(f"\n📋 Vitamin D Content:")
        print("-" * 20)
        
        # Look for specific phrases from screenshot
        optimal_params = "falls within the optimal parameters" in roadmap
        no_intervention = "no additional intervention is recommended" in roadmap
        
        print(f"'falls within the optimal parameters': {'✅ FOUND' if optimal_params else '❌ NOT FOUND'}")
        print(f"'no additional intervention is recommended': {'✅ FOUND' if no_intervention else '❌ NOT FOUND'}")
        
        # Show vitamin D related lines
        lines = roadmap.split('\n')
        for i, line in enumerate(lines):
            if ('vitamin d' in line.lower() and 
                ('level' in line.lower() or 'optimal' in line.lower())):
                print(f"Line {i}: {line.strip()}")

if __name__ == "__main__":
    test_d_60_plus() 