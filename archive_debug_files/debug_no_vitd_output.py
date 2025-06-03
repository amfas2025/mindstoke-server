#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_no_vitd_output():
    """Debug the exact output when there's no vitamin D data"""
    
    print("🔍 Debugging No Vitamin D Output")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {}  # No vitamin D data
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract just the Vitamin & Mineral Optimization section
    print("\n📋 Vitamin & Mineral Optimization Section:")
    print("-" * 50)
    
    # Find the section
    start_marker = "## **Vitamin & Mineral Optimization**"
    end_marker = "## **Metabolic & Blood Sugar Management**"
    
    start_idx = roadmap.find(start_marker)
    end_idx = roadmap.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        vitamin_section = roadmap[start_idx:end_idx].strip()
        print(vitamin_section)
    else:
        print("❌ Could not find Vitamin & Mineral section")
    
    # Also check if "Your baseline Vitamin D level is" appears anywhere
    baseline_count = roadmap.count("Your baseline Vitamin D level is")
    print(f"\n📊 'Your baseline Vitamin D level is' appears {baseline_count} times")
    
    if baseline_count > 0:
        print("\n🔍 All instances of this text:")
        lines = roadmap.split('\n')
        for i, line in enumerate(lines):
            if "Your baseline Vitamin D level is" in line:
                print(f"  Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    debug_no_vitd_output() 