#!/usr/bin/env python3

"""
Test script for complete blood sugar and metabolic condition hierarchy
Tests: quick-glucose, quick-fasting-insulin, quick-homa-IR, quick-a1c, lab-a1c-L2b, A1c thresholds
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_blood_sugar_metabolic_conditions():
    """Test all blood sugar and metabolic condition variations"""
    
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    print("=== Testing Complete Blood Sugar & Metabolic Conditions ===\n")
    
    # Test Case 1: Optimal metabolic profile
    print("🧪 Test Case 1: Optimal Metabolic Profile")
    lab_results_optimal = {
        'CHEM_GLU': 85,      # Optimal glucose
        'METAB_INS': 5,      # Optimal insulin
        'METAB_HBA1C': 5.2,  # Optimal A1c
        'APO1': 'E3/E3'      # No E4 variant
    }
    
    processed_optimal = generator._process_all_content_controls(client_data, lab_results_optimal, {})
    
    print(f"   quick-glucose: {processed_optimal.get('quick-glucose')} (should be 85)")
    print(f"   quick-fasting-insulin: {processed_optimal.get('quick-fasting-insulin')} (should be 5)")
    print(f"   quick-homa-IR: {processed_optimal.get('quick-homa-IR')} (should be ~1.0)")
    print(f"   quick-a1c: {processed_optimal.get('quick-a1c')} (should be 5.2)")
    print(f"   quick-A1c<56: {processed_optimal.get('quick-A1c<56')} (should be True)")
    print(f"   lab-a1c-L2b: {processed_optimal.get('lab-a1c-L2b')} (should be False/None)")
    print()
    
    # Test Case 2: Mildly elevated metabolic markers
    print("🧪 Test Case 2: Mildly Elevated Metabolic Markers")
    lab_results_mild = {
        'CHEM_GLU': 105,     # Slightly elevated glucose
        'METAB_INS': 8,      # Slightly elevated insulin
        'METAB_HBA1C': 5.8,  # Mildly elevated A1c
        'APO1': 'E3/E4'      # Has E4 variant
    }
    
    processed_mild = generator._process_all_content_controls(client_data, lab_results_mild, {})
    
    print(f"   quick-glucose: {processed_mild.get('quick-glucose')} (should be 105)")
    print(f"   quick-fasting-insulin: {processed_mild.get('quick-fasting-insulin')} (should be 8)")
    print(f"   quick-homa-IR: {processed_mild.get('quick-homa-IR')} (should be ~2.1)")
    print(f"   quick-a1c: {processed_mild.get('quick-a1c')} (should be 5.8)")
    print(f"   quick-A1c>56: {processed_mild.get('quick-A1c>56')} (should be True)")
    print(f"   lab-a1c-L2b: {processed_mild.get('lab-a1c-L2b')} (should be True)")
    print(f"   glucose-elevated: {processed_mild.get('glucose-elevated')} (should be True)")
    print(f"   insulin-elevated: {processed_mild.get('insulin-elevated')} (should be True)")
    print()
    
    # Test Case 3: High metabolic dysfunction
    print("🧪 Test Case 3: High Metabolic Dysfunction")
    lab_results_high = {
        'CHEM_GLU': 125,     # Elevated glucose
        'METAB_INS': 15,     # High insulin
        'METAB_HBA1C': 6.2,  # Diabetic range A1c
        'APO1': 'E4/E4'      # Double E4 variant
    }
    
    processed_high = generator._process_all_content_controls(client_data, lab_results_high, {})
    
    print(f"   quick-glucose: {processed_high.get('quick-glucose')} (should be 125)")
    print(f"   quick-fasting-insulin: {processed_high.get('quick-fasting-insulin')} (should be 15)")
    print(f"   quick-homa-IR: {processed_high.get('quick-homa-IR')} (should be ~4.6)")
    print(f"   quick-a1c: {processed_high.get('quick-a1c')} (should be 6.2)")
    print(f"   quick-A1c>6: {processed_high.get('quick-A1c>6')} (should be True)")
    print(f"   quick-diabetes-risk: {processed_high.get('quick-diabetes-risk')} (should be True)")
    print(f"   lab-a1c-L2b: {processed_high.get('lab-a1c-L2b')} (should be True)")
    print(f"   HOMA-IR-elevated: {processed_high.get('HOMA-IR-elevated')} (should be True)")
    print()
    
    # Test Case 4: APO E4 specific thresholds
    print("🧪 Test Case 4: APO E4 Specific A1c Thresholds")
    
    # E4/E4 with A1c 5.4 (above 5.3 threshold for double E4)
    lab_e4e4 = {
        'CHEM_GLU': 90,
        'METAB_INS': 6,
        'METAB_HBA1C': 5.4,
        'APO1': 'E4/E4'
    }
    processed_e4e4 = generator._process_all_content_controls(client_data, lab_e4e4, {})
    print(f"   E4/E4 A1c 5.4: quick-A1c-E4E4-elevated={processed_e4e4.get('quick-A1c-E4E4-elevated')} (should be True)")
    
    # E3/E4 with A1c 5.7 (above 5.6 threshold for single E4)
    lab_e3e4 = {
        'CHEM_GLU': 90,
        'METAB_INS': 6,
        'METAB_HBA1C': 5.7,
        'APO1': 'E3/E4'
    }
    processed_e3e4 = generator._process_all_content_controls(client_data, lab_e3e4, {})
    print(f"   E3/E4 A1c 5.7: quick-A1c-E4-elevated={processed_e3e4.get('quick-A1c-E4-elevated')} (should be True)")
    print()
    
    # Test Case 5: HOMA-IR calculation accuracy
    print("🧪 Test Case 5: HOMA-IR Calculation Verification")
    test_cases = [
        (90, 5, 1.11),   # (glucose * insulin) / 405
        (100, 10, 2.47),
        (110, 15, 4.07),
        (120, 20, 5.93)
    ]
    
    for glucose, insulin, expected in test_cases:
        lab_calc = {'CHEM_GLU': glucose, 'METAB_INS': insulin}
        processed_calc = generator._process_all_content_controls(client_data, lab_calc, {})
        calculated = processed_calc.get('quick-homa-IR')
        print(f"   Glucose {glucose}, Insulin {insulin}: HOMA-IR = {calculated} (expected ~{expected})")
    print()
    
    # Test Case 6: Full roadmap integration test
    print("🧪 Test Case 6: Full Roadmap Integration")
    client_data_full = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data_full, lab_results_high, {})
        
        # Check for all metabolic content
        glucose_found = "fasting **BLOOD SUGAR** was 125" in roadmap
        insulin_found = "baseline **INSULIN** was 15" in roadmap
        homa_ir_found = "baseline **HOMA-IR** calculation is" in roadmap
        a1c_found = "baseline **A1c** was 6.2" in roadmap
        glysen_found = "**GLYSEN** and **GLYCOBERINE-MX**" in roadmap
        keto_found = "**KETOGENIC DIET**" in roadmap
        continuous_glucose_found = "**CONTINUOUS GLUCOSE MONITOR**" in roadmap
        
        print(f"   Roadmap generated successfully: ✅")
        print(f"   Glucose display found: {glucose_found}")
        print(f"   Insulin display found: {insulin_found}")
        print(f"   HOMA-IR display found: {homa_ir_found}")
        print(f"   A1c display found: {a1c_found}")
        print(f"   GLYSEN supplement found: {glysen_found}")
        print(f"   KETO diet recommendation found: {keto_found}")
        print(f"   Continuous glucose monitor found: {continuous_glucose_found}")
        
        if all([glucose_found, insulin_found, homa_ir_found, a1c_found, glysen_found, keto_found]):
            print("   🎉 All metabolic conditions working correctly!")
        else:
            print("   ⚠️ Some metabolic content missing - checking roadmap...")
            
            # Show metabolic section
            lines = roadmap.split('\n')
            metabolic_section = []
            in_metabolic_section = False
            
            for line in lines:
                if "Metabolic & Blood Sugar" in line:
                    in_metabolic_section = True
                    metabolic_section.append(line)
                elif in_metabolic_section and "---" in line:
                    break
                elif in_metabolic_section:
                    metabolic_section.append(line)
                    
            print("\n   📄 Complete Metabolic Section Found:")
            for line in metabolic_section[:20]:  # Show first 20 lines
                print(f"   {line}")
                
    except Exception as e:
        print(f"   ❌ Error generating roadmap: {e}")
    
    print()
    print("✅ Complete blood sugar & metabolic condition testing complete!")

if __name__ == "__main__":
    test_blood_sugar_metabolic_conditions() 