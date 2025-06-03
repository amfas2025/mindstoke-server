#!/usr/bin/env python3
"""
Debug ALL vitamin D conditions being set
"""

from roadmap_generator import RoadmapGenerator

def debug_all_vitamin_d_conditions():
    """Show all conditions being set that might affect vitamin D"""
    
    print("🔍 DEBUGGING ALL VITAMIN D CONDITIONS")
    print("=" * 50)
    
    client_data = {
        'firstname': 'Sarah',
        'today': 'December 2, 2025',
        'lab-date': 'October 15, 2024'
    }
    
    lab_results = {
        'genome-type': 'E3/E4',
        'VIT_D25': 32
    }
    
    hhq_responses = {}
    
    generator = RoadmapGenerator()
    all_conditions = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    print("🧪 ALL CONDITIONS CONTAINING 'D-' OR 'VIT':")
    vitamin_d_conditions = {}
    for key, value in all_conditions.items():
        if 'D-' in key or 'vit' in key.lower() or 'VIT' in key:
            vitamin_d_conditions[key] = value
    
    # Sort conditions for easier reading
    for condition in sorted(vitamin_d_conditions.keys()):
        value = vitamin_d_conditions[condition]
        status = "✅ TRUE" if value else "❌ FALSE"
        print(f"  {condition}: {status}")
    
    print("\n🔍 CONDITIONS CONTAINING '50' OR '59':")
    range_conditions = {k: v for k, v in all_conditions.items() if '50' in k or '59' in k}
    for condition in sorted(range_conditions.keys()):
        value = range_conditions[condition]
        status = "✅ TRUE" if value else "❌ FALSE"
        print(f"  {condition}: {status}")
    
    print(f"\n📊 TOTAL CONDITIONS SET: {len(all_conditions)}")
    print(f"📊 VITAMIN D RELATED: {len(vitamin_d_conditions)}")
    print(f"📊 RANGE CONDITIONS: {len(range_conditions)}")

if __name__ == "__main__":
    debug_all_vitamin_d_conditions() 