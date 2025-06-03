#!/usr/bin/env python3

"""
Test script to verify the autoimmune disease section appears correctly.
"""

from roadmap_generator import RoadmapGenerator

def test_autoimmune_section():
    """Test that autoimmune disease section appears when relevant conditions are present."""
    
    print("🧠 Testing Autoimmune Disease Section")
    print("=" * 60)
    
    generator = RoadmapGenerator()
    
    # Test case 1: NO autoimmune triggers
    print("\n🧪 Testing: No Autoimmune Triggers")
    print("-" * 40)
    
    client_data = {'name': 'Test', 'gender': 'female', 'dob': '1970-01-01'}
    lab_results = {'VIT_D25': 30}
    hhq_no_autoimmune = {'hh-diabetes': True, 'hh-high-blood-pressure': True}
    
    # Check what controls are generated
    risk_controls = generator._process_risk_profile_insights(hhq_no_autoimmune)
    print(f"Risk controls generated: {len(risk_controls)} controls")
    for k, v in risk_controls.items():
        print(f"  {k}: {v}")
    
    # Generate roadmap and check for autoimmune section
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_no_autoimmune)
    autoimmune_positions = []
    search_start = 0
    while True:
        pos = roadmap.find("Autoimmune Disease and Brain Health", search_start)
        if pos == -1:
            break
        autoimmune_positions.append(pos)
        search_start = pos + 1
    
    print(f"\nAutoimmune section found at positions: {autoimmune_positions}")
    
    # Check each occurrence
    for i, pos in enumerate(autoimmune_positions, 1):
        context_start = max(0, pos - 200)
        context_end = min(len(roadmap), pos + 200)
        context = roadmap[context_start:context_end]
        print(f"\nPosition {i} (character {pos}):")
        print(f"Context: ...{context}...")
        
        # Check if this is within content control tags
        before_section = roadmap[:pos]
        after_section = roadmap[pos:]
        
        # Look for content control tags
        last_open_tag = before_section.rfind("{{#autoimmune-disease-section}}")
        last_close_tag = before_section.rfind("{{/autoimmune-disease-section}}")
        next_close_tag = after_section.find("{{/autoimmune-disease-section}}")
        
        if last_open_tag > last_close_tag and next_close_tag != -1:
            print("  ✅ This is properly within content control tags")
        else:
            print("  ⚠️  This appears to be from another source!")
    
    # Test case 2: WITH autoimmune triggers
    print("\n" + "=" * 60)
    print("\n🧪 Testing: With Autoimmune Triggers")
    print("-" * 40)
    
    hhq_with_autoimmune = {
        'hh-autoimmune-disease': True,
        'hh-arthritis': True,
        'hh-chronic-allergies': True
    }
    
    # Check what controls are generated
    risk_controls = generator._process_risk_profile_insights(hhq_with_autoimmune)
    print(f"Risk controls generated: {len(risk_controls)} controls")
    for k, v in risk_controls.items():
        print(f"  {k}: {v}")
    
    # Generate roadmap and check for autoimmune section
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_with_autoimmune)
    autoimmune_positions = []
    search_start = 0
    while True:
        pos = roadmap.find("Autoimmune Disease and Brain Health", search_start)
        if pos == -1:
            break
        autoimmune_positions.append(pos)
        search_start = pos + 1
    
    print(f"\nAutoimmune section found at positions: {autoimmune_positions}")
    
    # Check if the section content appears (should be visible when triggered)
    if "As a result of your health history, we have summarized some principles" in roadmap:
        print("✅ Autoimmune section content is visible (correctly triggered)")
    else:
        print("❌ Autoimmune section content is not visible")

if __name__ == "__main__":
    test_autoimmune_section() 