#!/usr/bin/env python3

"""
Check test client's CRP and OmegaCheck values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator
import requests
import json

def check_test_client_crp_omega():
    """Check test client's actual CRP and Omega values"""
    
    # Test client ID
    client_id = "78659670-c75f-4c9e-b9d9-49a18db641b6"
    
    try:
        # Get debug data from the endpoint
        response = requests.get(f"http://localhost:5001/roadmap/debug/{client_id}")
        
        if response.status_code == 200:
            debug_data = response.json()
            
            # Extract lab results
            lab_data = debug_data.get('lab_data', {})
            processed_content = debug_data.get('processed_content', {})
            
            print("=== Test Client CRP-Omega Analysis ===\n")
            
            # Check CRP values
            crp_value = lab_data.get('INFLAM_CRP') or lab_data.get('C-Reactive Protein, Cardiac')
            print(f"CRP Value: {crp_value}")
            
            # Check OmegaCheck values  
            omega_value = lab_data.get('OMEGA_CHECK') or lab_data.get('OmegaCheck(TM)')
            print(f"OmegaCheck Value: {omega_value}")
            
            # Check if condition is triggered
            condition_triggered = processed_content.get('quick-CRP-09-omega-<5', False)
            print(f"Condition Triggered: {condition_triggered}")
            
            # Analysis
            print("\n=== Analysis ===")
            if crp_value and omega_value:
                crp_val = float(crp_value)
                omega_val = float(omega_value)
                
                print(f"CRP > 0.9? {crp_val} > 0.9 = {crp_val > 0.9}")
                print(f"OmegaCheck < 5.4? {omega_val} < 5.4 = {omega_val < 5.4}")
                
                should_trigger = crp_val > 0.9 and omega_val < 5.4
                print(f"Should trigger: {should_trigger}")
                print(f"Actually triggered: {condition_triggered}")
                
                if should_trigger == condition_triggered:
                    print("✅ Logic is working correctly!")
                else:
                    print("❌ Logic issue detected")
            else:
                print("Missing lab values - cannot evaluate condition")
                print(f"Available CRP keys: {[k for k in lab_data.keys() if 'CRP' in k or 'crp' in k.lower()]}")
                print(f"Available Omega keys: {[k for k in lab_data.keys() if 'OMEGA' in k or 'omega' in k.lower()]}")
        
        else:
            print(f"Failed to get debug data: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_test_client_crp_omega() 