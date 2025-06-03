#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_d_50_55_output():
    """Debug the D-50-55 output for vitamin D = 55"""
    
    print("🔍 Debugging D-50-55 Output for Vitamin D = 55 ng/mL")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    lab_results = {
        'VIT_D25': 55.0
    }
    
    hhq_responses = {}
    
    # Get processed content controls
    processed_content = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    print(f"⚙️ Content Controls:")
    print("-" * 30)
    print(f"D-50-55: {processed_content.get('D-50-55', 'NOT SET')}")
    print(f"D-55-59: {processed_content.get('D-55-59', 'NOT SET')}")
    print(f"D-optimal: {processed_content.get('D-optimal', 'NOT SET')}")
    
    # Generate full roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    # Search for specific vitamin D content
    print(f"\n📋 Searching for Vitamin D Content:")
    print("-" * 40)
    
    # Look for specific phrases
    phrases_to_check = [
        "Since your VITAMIN D was 50-59",
        "supplement with 4,000 IU", 
        "falls very close to the optimal parameters",
        "no additional intervention is recommended",
        "encouraged to continue your current VITAMIN D supplement",
        "Vitamin D Optimization"
    ]
    
    for phrase in phrases_to_check:
        found = phrase in roadmap
        print(f"'{phrase}': {'✅ FOUND' if found else '❌ NOT FOUND'}")
    
    # Show a snippet around any vitamin D content
    print(f"\n📄 Vitamin D Section Snippet:")
    print("-" * 40)
    
    # Find and show vitamin D related content
    lines = roadmap.split('\n')
    vitamin_d_lines = []
    
    for i, line in enumerate(lines):
        if 'vitamin d' in line.lower() or 'VITAMIN D' in line:
            # Get context around this line
            start = max(0, i-2)
            end = min(len(lines), i+5)
            for j in range(start, end):
                if j not in [k for k, _ in vitamin_d_lines]:
                    vitamin_d_lines.append((j, lines[j]))
    
    if vitamin_d_lines:
        for line_num, line_content in vitamin_d_lines[:10]:  # Show first 10 relevant lines
            print(f"{line_num:3d}: {line_content}")
    else:
        print("No vitamin D content found!")

if __name__ == "__main__":
    debug_d_50_55_output() 