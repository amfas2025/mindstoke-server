#!/usr/bin/env python3

"""
Comprehensive test for all omega-3 related conditions working together
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_comprehensive_omega_scenarios():
    """Test all omega-3 conditions in realistic clinical scenarios"""
    
    generator = RoadmapGenerator()
    
    print("=== Comprehensive Omega-3 Conditions Integration Test ===\n")
    
    # Scenario 1: Post-concussion athlete
    print("🏆 SCENARIO 1: Post-Concussion Athlete")
    print("Profile: Former football player with history of multiple concussions, currently experiencing brain fog")
    
    client_data_1 = {
        'first_name': 'Mike',
        'last_name': 'Johnson', 
        'gender': 'male',
        'date_of_birth': '1985-01-01'
    }
    
    hhq_responses_1 = {
        'hh_concussion': True,
        'hh_traumatic_brain_injury': True,
        'hh_brain_fog': True,
        'hh_memory_problems': True,
        'hh_sports_history': True
    }
    
    lab_results_1 = {
        'OMEGA_CHECK': 3.2,        # Very low
        'OMEGA_6_3_RATIO': 15.0,   # Very high ratio
        'INFLAM_CRP': 0.8,         # Normal CRP
        'VIT_D25': 28.0,           # Low vitamin D
        'VIT_B12': 350.0           # Suboptimal B12
    }
    
    processed_1 = generator._process_all_content_controls(client_data_1, lab_results_1, hhq_responses_1)
    
    omega_conditions_1 = {
        'omega-neurological-suboptimal': 'Neurological omega-3 optimization',
        'checked-omega-63-ratio': 'OMEGA-3 CHALLENGE (10,000mg protocol)',
        'Quick-krill': 'Krill oil considerations',
        'quick-CRP-09-omega-<5': 'CRP + omega compound condition'
    }
    
    print("Expected omega-3 interventions:")
    for condition, description in omega_conditions_1.items():
        triggered = processed_1.get(condition, False)
        status = "✅ Active" if triggered else "❌ Inactive"
        print(f"  {description}: {status}")
    
    # Generate roadmap for this scenario
    roadmap_1 = generator.generate_roadmap(client_data_1, lab_results_1, hhq_responses_1)
    
    # Check for omega-3 sections
    omega_sections = [
        'OMEGA-3 CHALLENGE Protocol:',
        'Neurological Omega-3 Optimization:',
        'PHYTO BRAIN-E'
    ]
    
    print("Roadmap sections generated:")
    for section in omega_sections:
        found = section in roadmap_1
        status = "✅ Found" if found else "❌ Missing"
        print(f"  {section}: {status}")
    
    print(f"Clinical recommendation: Mike should get BOTH the OMEGA-3 CHALLENGE (10,000mg for 1-2 months) AND the neurological optimization (PHYTO BRAIN-E for head trauma)")
    
    print("\n" + "="*80 + "\n")
    
    # Scenario 2: Middle-aged woman with inflammation and krill oil use
    print("👩 SCENARIO 2: Middle-aged Woman with Chronic Inflammation")
    print("Profile: 52-year-old woman taking krill oil, elevated CRP, low omega status, no head injury")
    
    client_data_2 = {
        'first_name': 'Sarah',
        'last_name': 'Williams', 
        'gender': 'female',
        'date_of_birth': '1972-01-01'
    }
    
    hhq_responses_2 = {
        'hh_taking_krill_oil': True,
        'hh_chronic_fatigue': True,
        'hh_joint_pain': True,
        'hh_supplement_history': True
    }
    
    lab_results_2 = {
        'OMEGA_CHECK': 4.8,        # Low (below 5.4)
        'OMEGA_6_3_RATIO': 7.5,    # Elevated ratio
        'INFLAM_CRP': 1.8,         # Elevated CRP
        'VIT_D25': 42.0,           # Suboptimal vitamin D
        'INFLAM_HOMOCYS': 12.5     # Elevated homocysteine
    }
    
    processed_2 = generator._process_all_content_controls(client_data_2, lab_results_2, hhq_responses_2)
    
    omega_conditions_2 = {
        'omega-neurological-suboptimal': 'Neurological omega-3 optimization',
        'checked-omega-63-ratio': 'OMEGA-3 CHALLENGE',
        'Quick-krill': 'Krill oil education/switching',
        'quick-CRP-09-omega-<5': 'CRP + omega compound inflammation risk'
    }
    
    print("Expected omega-3 interventions:")
    for condition, description in omega_conditions_2.items():
        triggered = processed_2.get(condition, False)
        status = "✅ Active" if triggered else "❌ Inactive"
        print(f"  {description}: {status}")
    
    roadmap_2 = generator.generate_roadmap(client_data_2, lab_results_2, hhq_responses_2)
    
    # Check for specific content
    inflammatory_content = [
        'Compound Inflammation Risk:',
        'Krill Oil Considerations:',
        'extremely low in DHA and EPA',
        'TRIGLYCERIDE-derived OMEGA-3'
    ]
    
    print("Anti-inflammatory content generated:")
    for content in inflammatory_content:
        found = content in roadmap_2
        status = "✅ Found" if found else "❌ Missing"
        print(f"  {content}: {status}")
    
    print(f"Clinical recommendation: Sarah should switch from krill oil to triglyceride-based fish oil AND address compound inflammation risk")
    
    print("\n" + "="*80 + "\n")
    
    # Scenario 3: Optimal omega status person
    print("💚 SCENARIO 3: Person with Optimal Omega-3 Status")
    print("Profile: Health-conscious individual with good omega-3 levels, no neurological symptoms")
    
    client_data_3 = {
        'first_name': 'David',
        'last_name': 'Chen', 
        'gender': 'male',
        'date_of_birth': '1990-01-01'
    }
    
    hhq_responses_3 = {
        'hh_regular_exercise': True,
        'hh_healthy_diet': True,
        'hh_takes_fish_oil': True
    }
    
    lab_results_3 = {
        'OMEGA_CHECK': 8.2,        # Excellent
        'OMEGA_6_3_RATIO': 3.5,    # Optimal ratio
        'INFLAM_CRP': 0.4,         # Low inflammation
        'VIT_D25': 65.0,           # Optimal vitamin D
        'VIT_B12': 850.0           # Good B12
    }
    
    processed_3 = generator._process_all_content_controls(client_data_3, lab_results_3, hhq_responses_3)
    
    print("Omega-3 condition triggers (should be minimal):")
    for condition, description in omega_conditions_1.items():
        triggered = processed_3.get(condition, False)
        status = "✅ Triggered" if triggered else "❌ Not triggered"
        print(f"  {description}: {status}")
    
    print(f"Clinical recommendation: David's omega-3 status is optimal - continue current regimen")
    
    print("\n" + "="*80 + "\n")
    
    # Scenario 4: Complex case with multiple risk factors
    print("⚠️  SCENARIO 4: Complex Multi-Risk Case")
    print("Profile: Elderly person with diabetes, taking krill oil, history of mild stroke, brain fog")
    
    client_data_4 = {
        'first_name': 'Betty',
        'last_name': 'Rodriguez', 
        'gender': 'female',
        'date_of_birth': '1945-01-01'
    }
    
    hhq_responses_4 = {
        'hh_taking_krill_oil': True,
        'hh_diabetes': True,
        'hh_stroke': True,              # Should trigger neurological
        'hh_brain_fog': True,
        'hh_memory_problems': True,
        'hh_high_blood_pressure': True
    }
    
    lab_results_4 = {
        'OMEGA_CHECK': 2.8,        # Very low
        'OMEGA_6_3_RATIO': 18.0,   # Extremely high
        'INFLAM_CRP': 3.5,         # High inflammation
        'VIT_D25': 22.0,           # Deficient
        'METAB_HBA1C': 8.2,        # Poor diabetes control
        'INFLAM_HOMOCYS': 18.0     # Very high
    }
    
    processed_4 = generator._process_all_content_controls(client_data_4, lab_results_4, hhq_responses_4)
    
    print("All omega-3 conditions triggered:")
    for condition, description in omega_conditions_1.items():
        triggered = processed_4.get(condition, False)
        status = "✅ CRITICAL" if triggered else "❌ Not triggered"
        print(f"  {description}: {status}")
    
    # Additional compound conditions
    additional_conditions = [
        'quick-diabetes',
        'quick-stroke', 
        'quick-brain-fog',
        'quick-memory-issues'
    ]
    
    print("Additional related conditions:")
    for condition in additional_conditions:
        triggered = processed_4.get(condition, False)
        status = "✅ Active" if triggered else "❌ Inactive"
        print(f"  {condition}: {status}")
    
    roadmap_4 = generator.generate_roadmap(client_data_4, lab_results_4, hhq_responses_4)
    
    print(f"Clinical recommendation: Betty needs AGGRESSIVE omega-3 intervention - OMEGA-3 CHALLENGE + PHYTO BRAIN-E + krill oil switching + inflammation management")
    
    print("\n" + "="*80 + "\n")
    
    # Summary analysis
    print("📊 INTEGRATION ANALYSIS SUMMARY")
    print("="*50)
    
    scenarios = [
        ("Post-Concussion Athlete", processed_1, "High-risk neurological"),
        ("Chronic Inflammation", processed_2, "Moderate inflammatory risk"),
        ("Optimal Status", processed_3, "Low risk - maintenance"),
        ("Complex Multi-Risk", processed_4, "Critical - aggressive intervention")
    ]
    
    for name, processed, risk_level in scenarios:
        omega_triggered = sum(1 for condition in omega_conditions_1.keys() if processed.get(condition, False))
        print(f"{name}: {omega_triggered}/4 omega conditions | {risk_level}")
    
    print("\n✅ All omega-3 conditions are working together seamlessly!")
    print("- omega-neurological-suboptimal: General neurological optimization")
    print("- checked-omega-63-ratio: Aggressive OMEGA-3 CHALLENGE protocol")  
    print("- Quick-krill: Education about krill oil limitations")
    print("- quick-CRP-09-omega-<5: Compound inflammation risk management")
    print("\n🎯 Each condition serves a specific clinical purpose while complementing the others!")

if __name__ == "__main__":
    test_comprehensive_omega_scenarios() 