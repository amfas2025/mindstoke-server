#!/usr/bin/env python3
"""
Debug vitamin D template nesting issue
"""

from roadmap_generator import RoadmapGenerator

def debug_vitamin_d_nesting():
    """Test if nested conditions are being processed correctly"""
    
    print("🔍 DEBUGGING VITAMIN D TEMPLATE NESTING")
    print("=" * 50)
    
    # Create simple test template with nested conditions
    test_template = """
{{#quick-VitD-row}}
PARENT SECTION ACTIVE

{{#D-30-39}}
30-39 CONTENT: 8,000 IU
{{/D-30-39}}

{{#D-50-59}}
50-59 CONTENT: 2,000 IU
{{/D-50-59}}

END PARENT
{{/quick-VitD-row}}
"""
    
    # Test conditions that match our actual data
    test_conditions = {
        'quick-VitD-row': True,    # Parent should be active
        'D-30-39': True,          # This should show (8,000 IU)
        'D-50-59': False,         # This should NOT show (2,000 IU)
    }
    
    generator = RoadmapGenerator()
    
    # Apply content controls
    result = generator._apply_content_controls_to_template(test_template, test_conditions)
    
    print("🧪 TEST CONDITIONS:")
    for condition, value in test_conditions.items():
        print(f"  {condition}: {value}")
    
    print("\n📄 RESULT:")
    print(result)
    
    print("\n🔍 ANALYSIS:")
    if "30-39 CONTENT" in result and "50-59 CONTENT" not in result:
        print("✅ Template processing: CORRECT")
    elif "30-39 CONTENT" in result and "50-59 CONTENT" in result:
        print("❌ Template processing: BROKEN (both conditions showing)")
    elif "30-39 CONTENT" not in result:
        print("❌ Template processing: BROKEN (correct condition not showing)")
    else:
        print("❓ Template processing: UNEXPECTED result")

if __name__ == "__main__":
    debug_vitamin_d_nesting() 