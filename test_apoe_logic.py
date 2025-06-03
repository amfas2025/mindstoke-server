#!/usr/bin/env python3
"""
Test script to verify APOE genetics logic matches reference system
"""

from roadmap_generator import RoadmapGenerator

def test_apoe_genetics():
    """Test APOE genetics processing logic"""
    
    generator = RoadmapGenerator()
    
    # Test cases based on reference system
    test_cases = [
        {
            'name': 'E4/E4 Homozygous',
            'labs': {'APO1': 'E4/E4'},
            'expected': {
                'quick-E4E4': True,
                'quick-E4': False,
                'quick-E4E3': False,
                'quick-nonE4': False
            }
        },
        {
            'name': 'E3/E4 Heterozygous',
            'labs': {'APO1': 'E3/E4'},
            'expected': {
                'quick-E4E4': False,
                'quick-E4': False,
                'quick-E4E3': True,
                'quick-nonE4': False
            }
        },
        {
            'name': 'E4/E3 Heterozygous (reversed)',
            'labs': {'APO1': 'E4/E3'},
            'expected': {
                'quick-E4E4': False,
                'quick-E4': False,
                'quick-E4E3': True,
                'quick-nonE4': False
            }
        },
        {
            'name': 'E2/E4 Heterozygous',
            'labs': {'APO1': 'E2/E4'},
            'expected': {
                'quick-E4E4': False,
                'quick-E4': True,
                'quick-E4E3': False,
                'quick-nonE4': False
            }
        },
        {
            'name': 'E3/E3 No E4',
            'labs': {'APO1': 'E3/E3'},
            'expected': {
                'quick-E4E4': False,
                'quick-E4': False,
                'quick-E4E3': False,
                'quick-nonE4': True
            }
        },
        {
            'name': 'E2/E3 No E4',
            'labs': {'APO1': 'E2/E3'},
            'expected': {
                'quick-E4E4': False,
                'quick-E4': False,
                'quick-E4E3': False,
                'quick-nonE4': True
            }
        },
        {
            'name': 'With Glutathione Low',
            'labs': {'APO1': 'E3/E4', 'Glutathione': '150'},
            'expected': {
                'quick-E4E3': True,
                'GSH<200': True,
                'glutathione-level': '150'
            }
        },
        {
            'name': 'With Glutathione Normal',
            'labs': {'APO1': 'E3/E3', 'Glutathione': '250'},
            'expected': {
                'quick-nonE4': True,
                'GSH<200': False,
                'glutathione-level': '250'
            }
        }
    ]
    
    print("Testing APOE Genetics Logic")
    print("=" * 50)
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input labs: {test_case['labs']}")
        
        # Process genetics
        result = generator._process_genetic_markers(test_case['labs'], {})
        
        print(f"Processed result: {result}")
        
        # Check expected values
        passed = True
        for key, expected_value in test_case['expected'].items():
            actual_value = result.get(key)
            if actual_value != expected_value:
                print(f"  ❌ FAIL: {key} expected {expected_value}, got {actual_value}")
                passed = False
                all_passed = False
            else:
                print(f"  ✅ PASS: {key} = {actual_value}")
        
        if passed:
            print(f"  🎉 {test_case['name']} PASSED")
        else:
            print(f"  💥 {test_case['name']} FAILED")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! APOE logic matches reference system.")
    else:
        print("💥 SOME TESTS FAILED. Check the logic above.")
    
    return all_passed

if __name__ == "__main__":
    test_apoe_genetics() 