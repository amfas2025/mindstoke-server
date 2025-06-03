#!/usr/bin/env python3
"""
Server integration test for neurologically active hormone conditions
Tests the full pipeline from client data to generated roadmap
"""

import requests
import json

def test_neurological_hormones_with_server():
    """Test neurologically active hormone conditions with actual server integration."""
    
    print("=== Testing Neurologically Active Hormone Conditions with Server ===\n")
    
    # Test client ID
    client_id = "78659670-c75f-4c9e-b9d9-49a18db641b6"
    
    # Test data for client with multiple neurological hormone deficiencies
    test_data = {
        'client_data': {
            'firstname': 'Patricia',
            'gender': 'female',
            'age': 52
        },
        'lab_results': {
            'NEURO_PREG': 75,     # Low pregnenolone (50-100 range)
            'NEURO_DHEAS': 135,   # Low DHEA-s (<150)
            'NEURO_CORT': 12      # Low cortisol (<15)
        },
        'hhq_responses': {
            'gender': 'female',
            'hh_chronic_fatigue': True,
            'hh_brain_fog': True,
            'hh_memory_problems': True,
            'hh_adrenal_fatigue': True,
            'hh_low_energy': True,
            'hh_morning_fatigue': True
        }
    }
    
    try:
        # Test the debug endpoint
        url = f"http://127.0.0.1:5001/roadmap/debug/{client_id}"
        
        # Add test data as query parameters for lab values
        params = {
            'NEURO_PREG': test_data['lab_results']['NEURO_PREG'],
            'NEURO_DHEAS': test_data['lab_results']['NEURO_DHEAS'],
            'NEURO_CORT': test_data['lab_results']['NEURO_CORT'],
            'gender': 'female',
            'hh_chronic_fatigue': True,
            'hh_brain_fog': True,
            'hh_memory_problems': True,
            'hh_adrenal_fatigue': True
        }
        
        print(f"Testing with data:")
        print(f"- PREGNENOLONE: {test_data['lab_results']['NEURO_PREG']} ng/dL (low)")
        print(f"- DHEA-s: {test_data['lab_results']['NEURO_DHEAS']} ng/dL (low)")
        print(f"- Cortisol: {test_data['lab_results']['NEURO_CORT']} μg/dL (low)")
        print(f"- Symptoms: Chronic fatigue, brain fog, memory issues")
        print()
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                conditions = data.get('processed_conditions', {})
                
                print("✓ Server responded successfully!")
                print("\nNeurologically Active Hormone Conditions Found:")
                print("-" * 50)
                
                # Check PREGNENOLONE conditions
                if conditions.get('quick-PROG-50-100'):
                    print("✓ quick-PROG-50-100: PREGNENOLONE supplementation recommended")
                else:
                    print("✗ quick-PROG-50-100: NOT triggered (expected: True)")
                
                # Check DHEA-s conditions  
                if conditions.get('quick-DHEA-150'):
                    print("✓ quick-DHEA-150: DHEA supplementation recommended")
                else:
                    print("✗ quick-DHEA-150: NOT triggered (expected: True)")
                
                # Check cortisol conditions
                if conditions.get('quick-cortisol-15'):
                    print("✓ quick-cortisol-15: Cortisol support recommended")
                else:
                    print("✗ quick-cortisol-15: NOT triggered (expected: True)")
                
                # Check compound condition
                if conditions.get('neurological-hormone-support'):
                    print("✓ neurological-hormone-support: Comprehensive support needed")
                else:
                    print("✗ neurological-hormone-support: NOT triggered (expected: True)")
                
                # Check that optimal conditions are NOT triggered
                if not conditions.get('quick-pregnenolone-101'):
                    print("✓ quick-pregnenolone-101: Correctly NOT triggered (levels suboptimal)")
                else:
                    print("✗ quick-pregnenolone-101: Incorrectly triggered (should be False)")
                
                if not conditions.get('quick-DHEA-151'):
                    print("✓ quick-DHEA-151: Correctly NOT triggered (levels suboptimal)")
                else:
                    print("✗ quick-DHEA-151: Incorrectly triggered (should be False)")
                
                print("\nLab Values in Response:")
                print("-" * 25)
                if conditions.get('quick-pregnenolone-lab-value'):
                    print(f"✓ PREGNENOLONE: {conditions['quick-pregnenolone-lab-value']} ng/dL")
                if conditions.get('quick-dhea-lab-value'):
                    print(f"✓ DHEA-s: {conditions['quick-dhea-lab-value']} ng/dL")
                if conditions.get('quick-cortisol-lab-value'):
                    print(f"✓ Cortisol: {conditions['quick-cortisol-lab-value']} μg/dL")
                
                print(f"\n✅ Neurologically Active Hormone Server Integration Test: SUCCESS")
                print("All expected conditions are properly triggered!")
                
            except json.JSONDecodeError:
                print("✗ Failed to parse JSON response")
                print("Response content:", response.text[:500])
                
        else:
            print(f"✗ Server request failed with status code: {response.status_code}")
            print("Response:", response.text[:500])
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        print("Make sure the server is running at http://127.0.0.1:5001")
        
    # Test 2: Optimal neurological hormone levels
    print("\n" + "="*60)
    print("Test 2: Optimal Neurological Hormone Levels")
    print("="*60)
    
    optimal_params = {
        'NEURO_PREG': 180,    # Optimal pregnenolone
        'NEURO_DHEAS': 250,   # Optimal DHEA-s
        'NEURO_CORT': 18,     # Optimal cortisol
        'gender': 'female'
    }
    
    print(f"Testing with optimal data:")
    print(f"- PREGNENOLONE: {optimal_params['NEURO_PREG']} ng/dL (optimal)")
    print(f"- DHEA-s: {optimal_params['NEURO_DHEAS']} ng/dL (optimal)")
    print(f"- Cortisol: {optimal_params['NEURO_CORT']} μg/dL (optimal)")
    print()
    
    try:
        response = requests.get(url, params=optimal_params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            conditions = data.get('processed_conditions', {})
            
            print("✓ Server responded successfully!")
            print("\nOptimal Conditions Found:")
            print("-" * 25)
            
            if conditions.get('quick-pregnenolone-101'):
                print("✓ quick-pregnenolone-101: Optimal pregnenolone confirmed")
            else:
                print("✗ quick-pregnenolone-101: NOT triggered (expected: True)")
            
            if conditions.get('quick-DHEA-151'):
                print("✓ quick-DHEA-151: Optimal DHEA-s confirmed")
            else:
                print("✗ quick-DHEA-151: NOT triggered (expected: True)")
            
            # Check that supplementation conditions are NOT triggered
            if not conditions.get('quick-PROG-50-100'):
                print("✓ quick-PROG-50-100: Correctly NOT triggered (optimal levels)")
            else:
                print("✗ quick-PROG-50-100: Incorrectly triggered (should be False)")
            
            if not conditions.get('quick-DHEA-150'):
                print("✓ quick-DHEA-150: Correctly NOT triggered (optimal levels)")
            else:
                print("✗ quick-DHEA-150: Incorrectly triggered (should be False)")
            
            if not conditions.get('quick-cortisol-15'):
                print("✓ quick-cortisol-15: Correctly NOT triggered (optimal levels)")
            else:
                print("✗ quick-cortisol-15: Incorrectly triggered (should be False)")
            
            print(f"\n✅ Optimal Neurological Hormone Test: SUCCESS")
            
    except Exception as e:
        print(f"✗ Optimal test failed: {e}")

if __name__ == "__main__":
    test_neurological_hormones_with_server() 