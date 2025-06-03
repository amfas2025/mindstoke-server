#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_d_55_59_controls():
    """Debug the D-55-59 content controls for different vitamin D values"""
    
    print("🔍 Debugging D-55-59 Content Controls")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    hhq_responses = {}
    
    # Test different vitamin D values
    test_values = [55, 56, 57, 58, 59, 60]
    
    for vit_d_value in test_values:
        print(f"\n📋 Test Case: Vitamin D = {vit_d_value} ng/mL")
        print("-" * 50)
        
        lab_results = {
            'VIT_D25': float(vit_d_value)
        }
        
        # Get processed content controls
        processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
        
        # Show vitamin D related controls
        print(f"⚙️ Vitamin D Content Controls for {vit_d_value} ng/mL:")
        print("-" * 30)
        
        vit_d_controls = [
            'D-optimal', 'D-deficient', 'D-insufficient', 
            'D-50-55', 'D-55-59', 'D-40-49', 'D-30-39', 'D-below-30',
            'quick-VitD-row', 'D-high'
        ]
        
        for control in vit_d_controls:
            status = processed_content.get(control, 'NOT SET')
            print(f"  {control}: {status}")

if __name__ == "__main__":
    debug_d_55_59_controls() 