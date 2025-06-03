#!/usr/bin/env python3
"""
Comprehensive roadmap testing and comparison script.
Use this to test roadmap generation against ARMGASYS standards.
"""

import json
from datetime import datetime
from roadmap_generator import RoadmapGenerator

class RoadmapTester:
    """Test harness for roadmap generation and comparison."""
    
    def __init__(self):
        self.generator = RoadmapGenerator()
        
    def create_sample_client_data(self, name="John Doe", gender="male", age=45):
        """Create sample client data for testing."""
        birth_year = datetime.now().year - age
        return {
            'name': name,
            'fullname': name,
            'firstname': name.split()[0],
            'gender': gender,
            'dob': f'{birth_year}-01-01',
            'age': age,
            'height': 180,  # cm
            'weight': 80    # kg
        }
    
    def create_comprehensive_lab_data(self):
        """Create comprehensive lab data covering all major systems."""
        return {
            # Inflammatory markers
            'INFLAM_CRP': 2.5,
            'INFLAM_HOMOCYS': 12.5,  # Elevated - should trigger recommendations
            'INFLAM_URIC': 7.2,
            
            # Vitamin D - test different ranges
            'VIT_D25': 32,  # Low - should trigger 8,000 IU recommendation
            
            # APO E genetics
            'APO1': 'E3/E4',  # Should trigger E4 recommendations
            'genome-type': 'E3/E4',
            
            # MTHFR genetics
            'MTHFR_1': 'Detected',
            'MTHFR_2': 'Not Detected',
            
            # Complete Blood Count
            'CBC_WBC': 6.5,
            'CBC_RBC': 4.5,
            'CBC_HGB': 14.2,
            'CBC_PLT': 300,
            
            # Basic Metabolic Panel
            'CHEM_GLU': 105,  # Slightly elevated
            'CHEM_BUN': 18,
            'CHEM_CREAT': 1.0,
            'CHEM_EGFR': 85,
            
            # Lipid Panel
            'LIPID_CHOL': 220,  # Elevated
            'LIPID_TRIG': 180,  # Elevated
            'LIPID_HDL': 42,    # Low
            'LIPID_LDL': 145,   # Elevated
            
            # Liver Function
            'LFT_ALT': 35,
            'LFT_AST': 28,
            'LFT_ALB': 4.2,
            
            # Thyroid Function
            'THY_TSH': 3.2,
            'THY_T3F': 3.1,
            'THY_T4F': 1.2,
            
            # Vitamins & Minerals
            'VIT_B12': 450,  # Suboptimal
            'MIN_ZN': 75,    # Low
            'MIN_MG_RBC': 4.8,  # Low
            'MIN_SE': 120,   # Low
            
            # Omega Fatty Acids
            'OMEGA_6_3_RATIO': 6.5,  # Elevated
            'OMEGA_CHECK': 4.2,      # Low
            
            # Metabolic markers
            'METAB_INS': 12,    # Elevated
            'METAB_HBA1C': 5.8, # Slightly elevated
            'METAB_GLUT': 280,  # Suboptimal
            
            # Hormones (male example)
            'MHt_TEST_TOT': 380,  # Low
            'MHt_TEST_FREE': 12,  # Low
        }
    
    def create_comprehensive_hhq_data(self):
        """Create comprehensive HHQ data with various conditions."""
        return {
            # Medical History
            'hh_brain_fog': True,
            'hh_chronic_fatigue': True,
            'hh_depression': True,
            'hh_chronic_allergies': True,
            'hh_sleep_problems': True,
            
            # Diet and Lifestyle
            'hh_likes_sugar': True,
            'hh_alcohol_consumption': True,
            'hh_current_smoker': False,
            
            # Supplements
            'hh_taking_omega3': False,
            'hh_taking_vitamin_d': False,
            'hh_taking_magnesium': False,
            
            # Digestive Health
            'hh_chronic_constipation': True,
            'hh_digestive_issues': True,
            'hh_food_sensitivities': True,
            
            # Autoimmune/Inflammatory
            'hh_autoimmune_disease': False,
            'hh_rheumatoid_arthritis': False,
            'hh_hashimotos': False,
            
            # Cardiovascular
            'hh_high_blood_pressure': True,
            'hh_heart_disease': False,
            
            # Neurological
            'hh_head_injury': False,
            'hh_memory_problems': True,
            'hh_headaches': True,
        }
    
    def generate_test_roadmap(self, client_name="Test Client", include_pdf=True):
        """Generate a comprehensive test roadmap."""
        print(f"\n🧪 Generating roadmap for {client_name}...")
        
        # Create test data
        client_data = self.create_sample_client_data(name=client_name)
        lab_results = self.create_comprehensive_lab_data()
        hhq_responses = self.create_comprehensive_hhq_data()
        
        # Generate text roadmap
        print("📄 Generating text roadmap...")
        roadmap_text = self.generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Save text roadmap
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        text_filename = f"test_roadmap_{client_name.replace(' ', '_')}_{timestamp}.txt"
        with open(text_filename, 'w') as f:
            f.write(roadmap_text)
        print(f"✅ Text roadmap saved: {text_filename}")
        
        # Generate PDF roadmap
        if include_pdf:
            print("📊 Generating PDF roadmap...")
            try:
                pdf_filename = self.generator.generate_visual_pdf(client_data, lab_results, hhq_responses)
                print(f"✅ PDF roadmap saved: {pdf_filename}")
            except Exception as e:
                print(f"❌ PDF generation failed: {str(e)}")
                pdf_filename = None
        else:
            pdf_filename = None
        
        return {
            'text_file': text_filename,
            'pdf_file': pdf_filename,
            'client_data': client_data,
            'lab_results': lab_results,
            'hhq_responses': hhq_responses,
            'roadmap_text': roadmap_text
        }
    
    def analyze_roadmap_content(self, roadmap_text):
        """Analyze roadmap content for key sections and recommendations."""
        analysis = {
            'sections_found': [],
            'supplement_recommendations': [],
            'vitamin_d_dosage': None,
            'apo_e_mentions': 0,
            'lab_values_mentioned': 0,
            'total_length': len(roadmap_text),
            'word_count': len(roadmap_text.split())
        }
        
        # Check for key sections
        sections_to_check = [
            'Vitamin D',
            'Omega-3',
            'Magnesium',
            'APO E',
            'MTHFR',
            'Homocysteine',
            'Brain Health',
            'Inflammation',
            'Cardiovascular',
            'Thyroid'
        ]
        
        for section in sections_to_check:
            if section.lower() in roadmap_text.lower():
                analysis['sections_found'].append(section)
        
        # Look for supplement dosages
        import re
        
        # Vitamin D dosage
        vit_d_pattern = r'(\d{1,2},?\d{3})\s*iu.*vitamin\s*d'
        vit_d_matches = re.findall(vit_d_pattern, roadmap_text.lower())
        if vit_d_matches:
            analysis['vitamin_d_dosage'] = vit_d_matches[0].replace(',', '')
        
        # Count APO E mentions
        analysis['apo_e_mentions'] = len(re.findall(r'apo\s*e', roadmap_text.lower()))
        
        # Count lab value mentions (numbers followed by units)
        lab_pattern = r'\d+\.?\d*\s*(ng/ml|pg/ml|mg/dl|μmol/l|iu/ml|ratio)'
        analysis['lab_values_mentioned'] = len(re.findall(lab_pattern, roadmap_text.lower()))
        
        return analysis
    
    def create_comparison_report(self, test_results, armgasys_reference=None):
        """Create a detailed comparison report."""
        analysis = self.analyze_roadmap_content(test_results['roadmap_text'])
        
        print(f"\n📊 ROADMAP ANALYSIS REPORT")
        print(f"="*50)
        print(f"📄 Text file: {test_results['text_file']}")
        print(f"📊 PDF file: {test_results['pdf_file'] or 'Not generated'}")
        print(f"📏 Length: {analysis['total_length']:,} characters")
        print(f"📝 Words: {analysis['word_count']:,} words")
        
        print(f"\n🔍 SECTIONS FOUND ({len(analysis['sections_found'])}):")
        for section in analysis['sections_found']:
            print(f"  ✅ {section}")
        
        print(f"\n💊 KEY RECOMMENDATIONS:")
        print(f"  🔸 Vitamin D dosage: {analysis['vitamin_d_dosage'] or 'Not found'} IU")
        print(f"  🔸 APO E mentions: {analysis['apo_e_mentions']}")
        print(f"  🔸 Lab values mentioned: {analysis['lab_values_mentioned']}")
        
        # Lab data summary
        print(f"\n🧪 TEST LAB DATA USED:")
        key_labs = {
            'Vitamin D': test_results['lab_results'].get('VIT_D25'),
            'CRP': test_results['lab_results'].get('INFLAM_CRP'),
            'Homocysteine': test_results['lab_results'].get('INFLAM_HOMOCYS'),
            'APO E': test_results['lab_results'].get('APO1'),
            'Total Cholesterol': test_results['lab_results'].get('LIPID_CHOL'),
        }
        
        for lab, value in key_labs.items():
            if value:
                print(f"  🔸 {lab}: {value}")
        
        print(f"\n🏥 HHQ CONDITIONS TESTED:")
        active_conditions = [k for k, v in test_results['hhq_responses'].items() if v]
        for condition in active_conditions[:10]:  # Show first 10
            print(f"  🔸 {condition.replace('hh_', '').replace('_', ' ').title()}")
        
        if armgasys_reference:
            print(f"\n🔄 COMPARISON WITH ARMGASYS:")
            print(f"  📊 This will be filled in when you provide ARMGASYS reference")
        
        return analysis


def run_comprehensive_test():
    """Run a comprehensive test of the roadmap generation system."""
    tester = RoadmapTester()
    
    print("🚀 COMPREHENSIVE ROADMAP TESTING")
    print("="*60)
    
    # Test case 1: Male with multiple conditions
    print("\n📋 TEST CASE 1: Male, 45, Multiple Health Issues")
    male_results = tester.generate_test_roadmap("John_Smith_Male_45", include_pdf=True)
    male_analysis = tester.create_comparison_report(male_results)
    
    # Test case 2: Female with different profile
    print("\n📋 TEST CASE 2: Female, 38, Different Profile")
    female_client = tester.create_sample_client_data("Jane_Doe", "female", 38)
    female_labs = tester.create_comprehensive_lab_data()
    # Modify for female-specific labs
    female_labs.update({
        'FHt_E2': 45,    # Low estradiol
        'FHt_PROG': 8,   # Low progesterone
        'FHt_TEST': 30,  # Female testosterone
    })
    female_hhq = tester.create_comprehensive_hhq_data()
    female_hhq.update({
        'hh_menopause': True,
        'hh_hormone_replacement_therapy': False,
    })
    
    female_roadmap = tester.generator.generate_roadmap(female_client, female_labs, female_hhq)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    female_filename = f"test_roadmap_Jane_Doe_Female_38_{timestamp}.txt"
    with open(female_filename, 'w') as f:
        f.write(female_roadmap)
    
    female_results = {
        'text_file': female_filename,
        'pdf_file': None,
        'roadmap_text': female_roadmap,
        'client_data': female_client,
        'lab_results': female_labs,
        'hhq_responses': female_hhq
    }
    
    print(f"✅ Female roadmap saved: {female_filename}")
    female_analysis = tester.create_comparison_report(female_results)
    
    print(f"\n🎯 NEXT STEPS FOR ARMGASYS COMPARISON:")
    print(f"1. 📋 Share your ARMGASYS roadmap examples")
    print(f"2. 🔍 We'll compare section by section")
    print(f"3. 🎯 Identify gaps and improvements needed")
    print(f"4. ⚡ Fine-tune the generation logic")
    print(f"5. ✅ Achieve ARMGASYS-level quality")
    
    return {
        'male_results': male_results,
        'female_results': female_results,
        'male_analysis': male_analysis,
        'female_analysis': female_analysis
    }


if __name__ == "__main__":
    # Run the comprehensive test
    results = run_comprehensive_test()
    
    print(f"\n🎉 Testing complete! Ready for ARMGASYS comparison.") 