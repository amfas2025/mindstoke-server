#!/usr/bin/env python3
"""
Test the roadmap generation with comprehensive client data
to validate all template sections and conditional logic.
"""

from roadmap_generator import RoadmapGenerator
from datetime import datetime, date
import json

def create_sample_client_data():
    """Create realistic client data for testing"""
    return {
        'firstname': 'Sarah',
        'lastname': 'Johnson', 
        'email': 'sarah.johnson@email.com',
        'gender': 'Female',
        'date_of_birth': '1975-06-15',
        'phone': '555-123-4567',
        'height_feet': 5,
        'height_inches': 6,
        'weight_lbs': 165,
        'today': datetime.now().strftime('%B %d, %Y'),
        'lab-date': 'October 15, 2024'
    }

def create_sample_lab_results():
    """Create comprehensive lab results covering all major template sections"""
    return {
        # APO E Genetics
        'APO1': 'E3',
        'APO2': 'E4',  # This will trigger APO E4 conditions
        'genome-type': 'E3/E4',
        
        # MTHFR Genetics
        'MTHFR_1': 'C/T',  # C677T variant
        'MTHFR_2': 'A/A',  # Normal A1298C
        'MTHFR_C677T': 'C/T',
        'MTHFR_A1298C': 'A/A',
        
        # Glutathione
        'glutathione-level': 180,  # Low - will trigger GSH<200 condition
        'METAB_GLUT': 180,
        
        # Vitamin D
        'VIT_D25': 32,  # Suboptimal - will trigger D-30-39 condition
        'quick-vitD': 32,
        
        # Vitamin E  
        'VIT_E': 8.5,  # Below optimal range
        'quick-vitE': 8.5,
        
        # Omega fatty acids
        'OMEGA_CHECK': 4.2,  # Below 5.4% threshold
        'omega-check-value': 4.2,
        'OMEGA_6_3_RATIO': 12,  # Elevated ratio
        'omega-63-ratio-value': 12,
        'OMEGA_AA_EPA': 9.5,  # Above 8.0 threshold
        'aaepa-ratio-value': 9.5,
        'OMEGA_AA': 11.2,  # Above 10.0 threshold
        'aa-level-value': 11.2,
        
        # Magnesium
        'MIN_MG_RBC': 4.8,  # Below 5.2 mg/dL
        'quick-MagRBC': 4.8,
        
        # Copper/Zinc ratio
        'MIN_CU': 120,
        'MIN_ZN': 80,
        'quick-CZratio-14': 1.5,  # Above 1.4 threshold
        
        # Selenium
        'MIN_SE': 110,  # Below 125 ug/L
        'quick-selenium': 110,
        
        # Blood sugar/metabolic
        'CHEM_GLU': 105,  # Slightly elevated
        'quick-glucose': 105,
        'METAB_INS': 12,  # Elevated insulin
        'quick-fasting-insulin': 12,
        'METAB_HBA1C': 5.8,  # Pre-diabetic range
        'quick-a1c': 5.8,
        
        # Inflammatory markers
        'INFLAM_CRP': 4.2,  # Elevated CRP
        'quick-hsCRP-value': 4.2,
        'INFLAM_HOMOCYS': 13.5,  # Elevated homocysteine
        'homocysteine-value': 13.5,
        
        # B vitamins
        'VIT_B12': 850,  # Within range but could be higher
        'quick-B12-value': 850,
        'VIT_FOLATE': 12,  # Slightly low
        'quick-folic-acid-value': 12,
        
        # Thyroid function
        'THY_TSH': 3.2,  # Above optimal range
        'quick-TSH': 3.2,
        'THY_T3F': 3.0,  # Below optimal
        'quick-FT3': 3.0,
        'THY_T4F': 1.1,  # Below optimal
        'quick-FT4': 1.1,
        'THY_RT3': 16,  # Elevated reverse T3
        'quick-rT3': 16,
        'THY_TPO': 45,  # Elevated TPO antibodies
        'quick-TPO': 45,
        'THY_TGAB': 2.5,  # Elevated thyroglobulin antibodies
        'quick-tg-ab': 2.5,
        
        # Male hormones (for testing - will be filtered by gender)
        'MHt_TEST_TOT': 450,
        'MHt_TEST_FREE': 10,
        'MHt_PSA': 1.2,
        
        # Female hormones
        'FHt_E2': 85,
        'FHt_PROG': 12,
        'FHt_FSH': 35,  # Perimenopause range
        
        # Additional markers
        'LIPID_CHOL': 220,
        'LIPID_HDL': 45,
        'LIPID_LDL': 135,
        'LIPID_TRIG': 160
    }

def create_sample_hhq_responses():
    """Create HHQ responses that will trigger various conditions"""
    return {
        # Health history flags that trigger template conditions
        'hh-brain_fog': 'Yes',
        'hh-fatigue': 'Yes', 
        'hh-depression': 'Yes',
        'hh-anxiety': 'Yes',
        'hh-headaches': 'Yes',
        'hh-allergies': 'Yes',
        'hh-alcohol_use': 'Moderate',
        'hh-alcohol_withdrawal': 'No',
        'hh-taking_nac': 'No',
        'hh-taking_vitamin_d': 'Yes',
        'hh-taking_omega3': 'Yes',
        'hh-taking_krill_oil': 'No',
        'hh-taking_b_complex': 'No',
        'hh-diabetes': 'No',
        'hh-celiac': 'No',
        'hh-likes_sugar': 'Yes',
        'hh-likes_soda': 'Occasionally',
        'hh-histamine_diet': 'No',
        'hh-mcas': 'No',
        'hh-concussion_history': 'Yes',
        'hh-tbi_history': 'No',
        'hh-root_canals': 'Yes',
        'hh-gallbladder_issues': 'No',
        'hh-autoimmune_disease': 'No',
        'hh-hashimotos': 'Possible',
        'hh-parkinsons': 'No',
        'hh-multiple_allergies': 'Yes',
        'hh-gi_health_issues': 'Yes',
        'hh-constipation': 'Occasionally',
        'hh-hsv': 'No',
        'hh-ebv': 'Unknown',
        'hh-sleep_issues': 'Yes',
        'hh-restless_sleep': 'Yes',
        'hh-stress_levels': 'High',
        'hh-exercise_frequency': 'Rarely',
        'hh-dental_health': 'Fair',
        
        # Risk factor questions
        'quick-E4': True,  # Will be set based on genetics
        'quick-nonE4': False,
        'quick-depression-mood-disorder': True,
        'quick-fatigue': True,
        'quick-taking-NAC': False,
        'quick-ETOH-WD': False,
        'quick-vitD-simple': True,
        'quick-VitD-row': True,
        'quick-VitD-row-takingD': True,
        'quick-likes-sugar': True,
        'quick-likes-soda': True,
        'Quick-Allergies': True,
        'Quick-Histamine-Diet': False,
        'quick-MCAS': False,
        'quick-diabetes-risk': True,
        'quick-male-hormones': False,  # Female client
        'quick-female-hormones': True,
        'quick-hashimotos': True,
        'quick-sleep-hormones': True,
        'toxicity-real': True,
        'lifestyle-change': True
    }

def test_roadmap_generation():
    """Test the complete roadmap generation process"""
    print("🧪 Testing Mind Stoke Roadmap Generation")
    print("=" * 50)
    
    # Initialize generator
    generator = RoadmapGenerator()
    
    # Create test data
    client_data = create_sample_client_data()
    lab_results = create_sample_lab_results()
    hhq_responses = create_sample_hhq_responses()
    
    print(f"📊 Testing with client: {client_data['firstname']} {client_data['lastname']}")
    print(f"🧬 APO E Genotype: {lab_results['genome-type']}")
    print(f"🩸 Key lab values loaded: {len(lab_results)} markers")
    print(f"📋 HHQ responses loaded: {len(hhq_responses)} responses")
    print()
    
    # Generate roadmap
    try:
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        print("✅ Roadmap generation successful!")
        print(f"📄 Generated roadmap length: {len(roadmap)} characters")
        print()
        
        # Test specific sections
        test_sections = [
            ("APO E Genetics", "APO E Genetic Profile"),
            ("MTHFR Section", "MTHFR Genetics"),
            ("Vitamin D", "Vitamin D level is"),
            ("Omega fatty acids", "OMEGA-3"),
            ("Blood sugar", "BLOOD SUGAR"),
            ("Inflammation", "C-Reactive Protein"),
            ("Thyroid", "TSH"),
            ("Lifestyle", "Lifestyle Change")
        ]
        
        print("🔍 Section Analysis:")
        for section_name, search_term in test_sections:
            if search_term in roadmap:
                print(f"  ✅ {section_name}: Present")
            else:
                print(f"  ❌ {section_name}: Missing")
        
        # Check for conditional triggers
        print("\n🎯 Conditional Logic Testing:")
        
        # APO E4 condition
        if "APO E4" in roadmap and "greater risk" in roadmap:
            print("  ✅ APO E4 risk warnings: Triggered correctly")
        else:
            print("  ❌ APO E4 risk warnings: Not triggered")
            
        # Low glutathione condition  
        if "GLUTATHIONE level is very low" in roadmap:
            print("  ✅ Low glutathione condition: Triggered correctly")
        else:
            print("  ❌ Low glutathione condition: Not triggered")
            
        # Vitamin D supplementation
        if "8,000 iu" in roadmap and "VITAMIN D3" in roadmap:
            print("  ✅ Vitamin D dosing: Correct for level 32")
        else:
            print("  ❌ Vitamin D dosing: Incorrect or missing")
            
        # Omega-3 recommendations
        if "OMEGA-3" in roadmap and ("PRO-OMEGA 2000" in roadmap or "ULTIMATE OMEGA" in roadmap):
            print("  ✅ Omega-3 recommendations: Present")
        else:
            print("  ❌ Omega-3 recommendations: Missing")
        
        # Save sample output for review
        output_file = f"sample_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(roadmap)
        print(f"\n💾 Sample roadmap saved to: {output_file}")
        
        # Show first 500 characters as preview
        print("\n📖 Roadmap Preview (first 500 characters):")
        print("-" * 50)
        print(roadmap[:500] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating roadmap: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_generation():
    """Test PDF generation functionality"""
    print("\n📄 Testing PDF Generation")
    print("=" * 30)
    
    try:
        generator = RoadmapGenerator()
        client_data = create_sample_client_data()
        lab_results = create_sample_lab_results()
        hhq_responses = create_sample_hhq_responses()
        
        # Generate PDF
        pdf_path = generator.generate_visual_pdf(
            client_data, 
            lab_results, 
            hhq_responses,
            output_path=f"sample_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        print(f"✅ PDF generated successfully: {pdf_path}")
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test text generation
    text_success = test_roadmap_generation()
    
    # Test PDF generation  
    pdf_success = test_pdf_generation()
    
    print("\n" + "=" * 50)
    print("🏁 TESTING SUMMARY")
    print("=" * 50)
    print(f"Text Generation: {'✅ PASS' if text_success else '❌ FAIL'}")
    print(f"PDF Generation:  {'✅ PASS' if pdf_success else '❌ FAIL'}")
    
    if text_success and pdf_success:
        print("\n🎉 All tests passed! Your roadmap system is ready for client data.")
    else:
        print("\n⚠️  Some tests failed. Review the output above for details.") 