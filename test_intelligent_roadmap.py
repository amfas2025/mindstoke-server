#!/usr/bin/env python3

"""
Test script for the new intelligent roadmap processing system.
Tests all lab thresholds, compound conditionals, and HHQ integration.
"""

import sys
import os
sys.path.append('/Users/jstoker/Documents/mindstoke-server')

from roadmap_generator import RoadmapGenerator
from datetime import datetime
import json

def test_intelligent_processing():
    """Test the intelligent roadmap processing with comprehensive data."""
    
    print("🧠 Testing Intelligent Roadmap Processing System")
    print("=" * 60)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Test client data
    client_data = {
        'name': 'John Smith',
        'gender': 'male',
        'dob': '1975-05-15',
        'labs_date': 'May 31, 2025'
    }
    
    # Comprehensive lab results with values that trigger various conditions
    lab_results = {
        # Inflammatory markers - some elevated
        'INFLAM_CRP': 1.2,  # > 0.9 optimal, should trigger CRP conditions
        'INFLAM_HOMOCYS': 8.5,  # > 7 optimal, elevated homocysteine
        
        # Cardiovascular 
        'LIPID_CHOL': 140,  # < 150 optimal, should trigger cholesterol-row
        'LIPID_TRIG': 150,  
        'LIPID_HDL': 35,    # Will create elevated T-HDL ratio (150/35 = 4.3 > 3.5)
        
        # Metabolic - diabetes risk
        'CHEM_GLU': 98,     # > 95 optimal, elevated glucose
        'METAB_INS': 6.2,   # > 4.5 optimal, elevated insulin 
        'METAB_HBA1C': 5.8, # > 5.6 optimal, elevated A1c
        
        # Thyroid dysfunction
        'THY_TSH': 2.5,     # > 2.0 optimal, elevated TSH
        'THY_T3F': 3.0,     # < 3.2 optimal, low FT3
        'RT3': 18,          # > 15 optimal, elevated reverse T3
        
        # Male hormones - suboptimal
        'MHt_TEST_TOT': 650, # < 690 optimal, low testosterone
        'MHt_TEST_FREE': 10, # < 12 optimal, low free testosterone
        'NEURO_DHEAS': 120,  # < 150 optimal, low DHEA-s
        
        # Nutrients - deficiencies
        'VIT_D25': 45,      # < 50 optimal, insufficient vitamin D
        'VIT_E': 8,         # < 12 optimal, low vitamin E
        'OMEGA_CHECK': 4.8, # < 5.4 optimal, low omega index
        'OMEGA_6_3_RATIO': 6.5, # > 4.0 optimal, poor omega ratio
        'VIT_B12': 400,     # < 500 optimal, low B12
        
        # Minerals
        'MIN_ZN': 85,       # < 90 optimal, low zinc
        'MIN_CU': 120,      # For C:Z ratio calculation
        'MIN_MG_RBC': 4.8,  # < 5.2 optimal, low magnesium
        
        # Genetics
        'APO1': 'E3',
        'APO2': 'E4',       # E3/E4 - should trigger quick-E4E3
        'MTHFR_1': 'heterozygous', # Should trigger MTHFR1
        'MTHFR_2': 'normal'
    }
    
    # HHQ responses that trigger compound conditions
    hhq_responses = {
        # Medical history
        'hh_root_canal': True,           # + elevated CRP = compound condition
        'hh_current_smoker': True,       # Should trigger smoking conditions
        'hh_chronic_fatigue_syndrome': True, # + thyroid issues = compound
        'hh_breast_cancer': False,       # Male, so irrelevant
        'hh_snores': True,              
        'hh_partner_report_apnea': True,  # Snoring + apnea = compound
        
        # Substance use
        'hh_alcohol_4days': True,        # + homocysteine + B12 = compound
        
        # Medications
        'taking_antidepressant': True,
        'hh_takes_thyroid_medicine': True,
        
        # Sleep issues
        'hh_cant_stay_asleep': True,
        'hh_awaken_unrested': True,
        
        # Other conditions
        'hh_head_injury': True,
        'hh_depression_treatment': True
    }
    
    print("📊 Test Lab Values:")
    print(f"  CRP: {lab_results['INFLAM_CRP']} (>0.9 = elevated)")
    print(f"  Vitamin D: {lab_results['VIT_D25']} (<50 = insufficient)")  
    print(f"  Testosterone: {lab_results['MHt_TEST_TOT']} (<690 = low)")
    print(f"  TSH: {lab_results['THY_TSH']} (>2.0 = elevated)")
    print(f"  Glucose: {lab_results['CHEM_GLU']} (>95 = elevated)")
    print()
    
    # Test intelligent processing
    print("🔬 Running Intelligent Processing...")
    processed_content = generator._process_all_content_controls(
        client_data, lab_results, hhq_responses
    )
    
    print("✅ Content Controls Generated:")
    print(f"  Total controls processed: {len(processed_content)}")
    print()
    
    # Show key compound conditions
    compound_conditions = [
        'quick-CRP-09-omega-<5',    # CRP >0.9 + Omega <5.4
        'TSH-T3-rT3',               # Any thyroid dysfunction
        'quick-DHEA-AS-VD',         # DHEA <150 + VitD <50
        'HOMA_IR',                  # Calculated insulin resistance
        'T_HDL_Ratio',              # Calculated cardiovascular risk
        'root-canal-inflammation',   # Root canal + elevated CRP
        'alcohol-homocys-B12-compound', # Alcohol + homocysteine + B12
        'fatigue-thyroid-compound'   # Chronic fatigue + thyroid issues
    ]
    
    print("🧮 Key Compound Conditions:")
    for condition in compound_conditions:
        if condition in processed_content:
            value = processed_content[condition]
            status = "✅ TRIGGERED" if value else "❌ Not triggered"
            print(f"  {condition}: {status}")
        else:
            print(f"  {condition}: ❓ Not found")
    
    print()
    
    # Show calculated values
    calculated_values = ['HOMA_IR', 'T_HDL_Ratio', 'CZ_Ratio']
    print("📈 Calculated Lab Values:")
    for calc in calculated_values:
        if calc in processed_content:
            print(f"  {calc}: {processed_content[calc]}")
    
    print()
    
    # Test full roadmap generation
    print("📄 Generating Full Roadmap...")
    try:
        roadmap_content = generator.generate_roadmap(
            client_data=client_data,
            lab_results=lab_results,
            hhq_responses=hhq_responses
        )
        
        print(f"✅ Roadmap generated successfully!")
        print(f"📏 Content length: {len(roadmap_content)} characters")
        
        # Count how many content controls were applied
        remaining_placeholders = roadmap_content.count('{{')
        print(f"🔧 Remaining placeholders: {remaining_placeholders}")
        
        # Show a sample of the generated content
        sample = roadmap_content[:500] + "..." if len(roadmap_content) > 500 else roadmap_content
        print("\n📋 Sample Content:")
        print(sample)
        
    except Exception as e:
        print(f"❌ Error generating roadmap: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Intelligent Processing Test Complete!")

if __name__ == "__main__":
    test_intelligent_processing() 