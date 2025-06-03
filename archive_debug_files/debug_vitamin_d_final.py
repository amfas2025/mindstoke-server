#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def show_vitamin_d_section():
    """Show the actual generated simple vitamin D section"""
    
    print("🔍 Simple Vitamin D Section Output Verification")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Client with vitamin D = 45 ng/mL
    client_data = {
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'VIT_D25': 45.0
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Extract the simple vitamin D section
    print("\n📋 Simple Vitamin D Section:")
    print("-" * 40)
    
    # Find the section
    start_marker = "{{#quick-vitD-simple}}"
    end_marker = "{{/quick-vitD-simple}}"
    
    # Since the template is processed, look for the actual content
    lines = roadmap.split('\n')
    
    for i, line in enumerate(lines):
        if "Your baseline Vitamin D level is" in line and "60-80 ng/mL" in line:
            print(f"✅ Found: {line.strip()}")
            
    print("\n📋 Expected format from screenshot:")
    print("-" * 40)
    print("Your baseline Vitamin D level is 45.0 ng/mL. The optimal level is suggested to be 60-80 ng/mL.")
    
    print("\n📊 Content Controls Status:")
    print("-" * 30)
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    print(f"quick-vitD: {processed_content.get('quick-vitD', 'NOT SET')}")
    print(f"quick-vitD-simple: {processed_content.get('quick-vitD-simple', 'NOT SET')}")

if __name__ == "__main__":
    show_vitamin_d_section() 