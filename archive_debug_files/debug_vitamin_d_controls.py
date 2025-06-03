#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_vitamin_d_controls():
    """Debug the vitamin D content controls"""
    
    print("🔍 Debugging Vitamin D Content Controls")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test Case: No vitamin D data
    print("\n📋 Test Case: No Vitamin D Data")
    print("-" * 50)
    
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {}  # No vitamin D data
    
    hhq_responses = {}
    
    # Get processed content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    # Show vitamin D related controls
    print("\n⚙️ Vitamin D Content Controls:")
    print("-" * 30)
    
    vit_d_controls = [
        'quick-vitD', 'quick-vitD-simple', 'D-optimal', 'D-deficient', 
        'D-insufficient', 'D-50-55', 'D-40-49', 'D-30-39', 'D-below-30',
        'quick-VitD-row', 'D-high'
    ]
    
    for control in vit_d_controls:
        status = processed_content.get(control, 'NOT SET')
        print(f"  {control}: {status}")
    
    # Test Case: With vitamin D = 45
    print("\n📋 Test Case: Vitamin D = 45 ng/mL")
    print("-" * 50)
    
    lab_results_with_d = {
        'VIT_D25': 45.0
    }
    
    # Get processed content controls
    processed_content_with_d = generator._process_all_content_controls(client_data, lab_results_with_d, hhq_responses)
    
    print("\n⚙️ Vitamin D Content Controls (with data):")
    print("-" * 30)
    
    for control in vit_d_controls:
        status = processed_content_with_d.get(control, 'NOT SET')
        print(f"  {control}: {status}")

if __name__ == "__main__":
    debug_vitamin_d_controls() 