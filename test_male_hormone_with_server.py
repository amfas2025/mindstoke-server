#!/usr/bin/env python3
"""
Server integration test for comprehensive male hormone conditions
Tests the full pipeline from client data to generated roadmap
"""

import requests
import json

def test_male_hormone_with_server():
    """Test male hormone conditions with actual server integration."""
    
    print("=== Testing Male Hormone Conditions with Server ===\n")
    
    # Test client ID
    client_id = "78659670-c75f-4c9e-b9d9-49a18db641b6"
    
    # Test data for male with low testosterone and symptoms
    test_data = {
        'client_data': {
            'firstname': 'Michael',
            'gender': 'male',
            'age': 45
        },
        'lab_results': {
            'HORM_TT': 380,      # Low total testosterone
            'HORM_FT': 9.5,      # Low free testosterone  
            'HORM_SHBG': 58,     # Elevated SHBG
            'HORM_PSA': 2.1,     # Normal PSA
            'HORM_LH': 8.2,      # Elevated LH (primary hypogonadism)
            'HORM_FSH': 12.1,    # Elevated FSH
            'HORM_PROL': 18.5,   # Slightly elevated prolactin
            'HORM_DHT': 45,      # Normal DHT
            'HORM_E2': 28,       # Slightly elevated estradiol
            'HORM_E1': 65,       # Elevated estrone
            'HORM_PROG': 0.6     # Low progesterone
        },
        'hhq_responses': {
            'hh_erectile_dysfunction': True,
            'hh_low_libido': True,
            'hh_fatigue': True,
            'hh_brain_fog': True,
            'hh_memory_problems': True,
            'hh_mood_changes': True,
            'hh_sleep_problems': True,
            'hh_muscle_weakness': True,
            'hh_weight_gain': True,
            'hh_takes_testosterone': False,
            'hh_prostate_cancer': False
        }
    }
    
    try:
        # Test the debug endpoint
        debug_url = f"http://localhost:5001/roadmap/debug/{client_id}"
        
        print("Testing debug endpoint...")
        debug_response = requests.post(debug_url, 
                                     json=test_data,
                                     headers={'Content-Type': 'application/json'})
        
        if debug_response.status_code == 200:
            debug_result = debug_response.json()
            processed = debug_result.get('processed_content', {})
            
            print("✓ Server connection successful")
            print(f"✓ Processed {len(processed)} conditions")
            
            # Check key male hormone conditions
            male_conditions = [
                'quick-male-hormones',
                'testosterone-low', 
                'quick-male-hormones-hrt',
                'zma-testosterone-support'
            ]
            
            print("\nMale Hormone Conditions:")
            print("-" * 30)
            for condition in male_conditions:
                status = "✓" if processed.get(condition) else "✗"
                print(f"{status} {condition}: {processed.get(condition)}")
            
            # Check hormone lab values are populated
            hormone_values = [
                'MHt_TT', 'MHt_FREE_T', 'MHt_SHBG', 'MHt_PSA',
                'MHt_LH', 'MHt_FSH', 'MHt_PROL', 'MHt_DHT',
                'MHt_E2', 'MHt_E1', 'MHt_PROG'
            ]
            
            print("\nHormone Lab Values:")
            print("-" * 20)
            for value in hormone_values:
                if value in processed:
                    print(f"✓ {value}: {processed[value]}")
                else:
                    print(f"✗ {value}: Missing")
            
            # Test roadmap generation
            print("\nTesting roadmap generation...")
            roadmap_url = f"http://localhost:5001/roadmap/generate/{client_id}"
            roadmap_response = requests.post(roadmap_url,
                                           json=test_data,
                                           headers={'Content-Type': 'application/json'})
            
            if roadmap_response.status_code == 200:
                roadmap_content = roadmap_response.text
                
                # Check for male hormone content in roadmap
                male_keywords = [
                    'Male Hormone Levels and Brain Health',
                    'TOTAL TESTOSTERONE',
                    'FREE TESTOSTERONE',
                    'TESTOSTERONE OPTIMIZATION',
                    'ZMA'
                ]
                
                print("\nRoadmap Content Check:")
                print("-" * 22)
                for keyword in male_keywords:
                    if keyword in roadmap_content:
                        print(f"✓ Found: {keyword}")
                    else:
                        print(f"✗ Missing: {keyword}")
                
                print(f"\n✓ Generated roadmap ({len(roadmap_content)} characters)")
                
            else:
                print(f"✗ Roadmap generation failed: {roadmap_response.status_code}")
                print(roadmap_response.text)
                
        else:
            print(f"✗ Debug endpoint failed: {debug_response.status_code}")
            print(debug_response.text)
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Make sure it's running on localhost:5001")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")

if __name__ == "__main__":
    test_male_hormone_with_server() 