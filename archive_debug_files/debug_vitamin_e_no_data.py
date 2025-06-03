#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def debug_vitamin_e_no_data():
    """Debug why vitamin E section appears when there's no data"""
    
    print("🐛 Debugging Vitamin E Section - No Data Case")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Test Patient',
        'full_name': 'Test Patient',
        'date_of_birth': '1980-01-01',
        'email': 'test@example.com'
    }
    
    # Test: No vitamin E data
    lab_results = {}
    
    processed = generator._process_all_content_controls(client_data, lab_results)
    roadmap = generator.generate_roadmap(client_data, lab_results)
    
    print(f"Content Control quick-vitE: {processed.get('quick-vitE')}")
    print(f"Type of quick-vitE: {type(processed.get('quick-vitE'))}")
    
    # Check if vitamin E section text appears in roadmap
    vit_e_text = "Your combined **Vitamin E** level is"
    vit_e_appears = vit_e_text in roadmap
    
    print(f"Vitamin E section text appears: {vit_e_appears}")
    
    # Show a snippet around where vitamin E section would be
    if vit_e_appears:
        start_idx = roadmap.find(vit_e_text)
        snippet = roadmap[start_idx:start_idx+150]
        print(f"Vitamin E section snippet: {snippet}")
    else:
        print("✅ Vitamin E section correctly hidden when no data")

if __name__ == "__main__":
    debug_vitamin_e_no_data() 