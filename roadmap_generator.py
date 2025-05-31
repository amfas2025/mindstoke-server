import re
import json
from datetime import datetime
from typing import Dict, Any, Optional
import os

class RoadmapGenerator:
    """
    Roadmap generation engine for Mind Stoke platform.
    Processes the roadmap template with client data, lab results, and HHQ responses.
    """
    
    def __init__(self, template_path: str = None):
        """Initialize the roadmap generator with template file."""
        if template_path is None:
            template_path = "/Users/jstoker/Documents/mindstoke-server/roadmap-template/new-patient-roadmap.txt"
        
        self.template_path = template_path
        self.template_content = self._load_template()
        
        # Lab value mappings from extraction logs
        self.lab_mappings = {
            # Basic labs
            'CBC_WBC': 'WBC',
            'CBC_RBC': 'RBC', 
            'CBC_HGB': 'Hemoglobin',
            'CBC_HCT': 'Hematocrit',
            'CBC_MCV': 'MCV',
            'CBC_PLT': 'Platelets',
            'CBC_NEUT_ABS': 'Neutrophils (Absolute)',
            'CBC_LYMPH_ABS': 'Lymphs (Absolute)',
            
            # Chemistry panel
            'CHEM_GLU': 'Glucose',
            'CHEM_BUN': 'BUN',
            'CHEM_CREAT': 'Creatinine',
            'CHEM_EGFR': 'eGFR',
            'CHEM_NA': 'Sodium',
            'CHEM_K': 'Potassium',
            'CHEM_CL': 'Chloride',
            'CHEM_CA': 'Calcium',
            
            # Liver function
            'LFT_ALB': 'Albumin',
            'LFT_ALT': 'ALT (SGPT)',
            'LFT_AST': 'AST (SGOT)',
            'LFT_ALKP': 'Alkaline Phosphatase',
            'LFT_TBILI': 'Bilirubin, Total',
            
            # Lipids
            'LIPID_CHOL': 'Cholesterol, Total',
            'LIPID_TRIG': 'Triglycerides',
            'LIPID_HDL': 'HDL Cholesterol',
            'LIPID_LDL': 'LDL Chol Calc (NIH)',
            
            # Hormones - Female
            'FHt_FSH': 'FSH',
            'FHt_E2': 'Estradiol',
            'FHt_PROG': 'Progesterone',
            'FHt_TEST': 'Testosterone',
            
            # Hormones - Male  
            'MHt_TEST_TOT': 'Testosterone',
            'MHt_TEST_FREE': 'Free Testosterone',
            'MHt_PSA': 'PSA',
            
            # Thyroid
            'THY_TSH': 'TSH',
            'THY_T3F': 'Triiodothyronine (T3), Free',
            'THY_T4F': 'T4, Free (Direct)',
            'THY_TGAB': 'Thyroglobulin Antibody',
            
            # Neurological hormones
            'NEURO_PREG': 'Pregnenolone, MS',
            'NEURO_DHEAS': 'DHEA-Sulfate',
            
            # Vitamins & minerals
            'VIT_D25': 'Vitamin D, 25-Hydroxy',
            'VIT_B12': 'Vitamin B12',
            'VIT_E': 'Vitamin E (Alpha Tocopherol)',
            'MIN_ZN': 'Zinc, Plasma or Serum',
            'MIN_CU': 'Copper, Serum or Plasma',
            'MIN_SE': 'Selenium, Serum/Plasma',
            'MIN_MG_RBC': 'Magnesium, RBC',
            
            # Inflammatory markers
            'INFLAM_CRP': 'C-Reactive Protein, Cardiac',
            'INFLAM_URIC': 'Uric Acid',
            'INFLAM_HOMOCYS': 'Homocyst(e)ine',
            
            # Metabolic
            'METAB_INS': 'Insulin',
            'METAB_HBA1C': 'Hemoglobin A1c',
            'METAB_GLUT': 'Total Glutathione',
            
            # Omega fatty acids
            'OMEGA_CHECK': 'OmegaCheck(TM)',
            'OMEGA_6_3_RATIO': 'Omega-6/Omega-3 Ratio',
            'OMEGA_3_TOT': 'Omega-3 total',
            'OMEGA_6_TOT': 'Omega-6 total',
            'OMEGA_AA': 'Arachidonic Acid',
            'OMEGA_AA_EPA': 'Arachidonic Acid/EPA Ratio',
            
            # Genetics
            'APO1': 'APO E Genotyping Result',
            'APO2': 'APO E Genotyping Result',  # Same field, split for processing
            'MTHFR_1': 'MTHFR C677T',
            'MTHFR_2': 'MTHFR A1298C'
        }
        
    def _load_template(self) -> str:
        """Load the roadmap template file."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        except Exception as e:
            raise Exception(f"Error loading template: {str(e)}")
    
    def generate_roadmap(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], 
                        hhq_responses: Dict[str, Any] = None) -> str:
        """
        Generate a personalized roadmap for a client.
        
        Args:
            client_data: Client information (name, gender, dob, etc.)
            lab_results: Dictionary of lab results keyed by armgasys_variable
            hhq_responses: HHQ survey responses (optional)
            
        Returns:
            Personalized roadmap as string
        """
        roadmap = self.template_content
        
        # 1. Replace basic client information
        roadmap = self._replace_client_info(roadmap, client_data)
        
        # 2. Process lab values and conditional logic
        roadmap = self._process_lab_values(roadmap, lab_results)
        
        # 3. Apply genetic-based conditions
        roadmap = self._process_genetics(roadmap, lab_results)
        
        # 4. Apply gender-specific sections
        roadmap = self._process_gender_sections(roadmap, client_data.get('gender'))
        
        # 5. Process HHQ-based recommendations
        if hhq_responses:
            roadmap = self._process_hhq_responses(roadmap, hhq_responses)
        
        # 6. Clean up any remaining placeholders
        roadmap = self._cleanup_placeholders(roadmap)
        
        return roadmap
    
    def _replace_client_info(self, roadmap: str, client_data: Dict[str, Any]) -> str:
        """Replace basic client information placeholders."""
        # Client name replacements
        name = client_data.get('name', 'Patient')
        roadmap = roadmap.replace('_______', name)  # Main name placeholder
        roadmap = roadmap.replace('___________', name)  # Secondary name placeholder
        roadmap = roadmap.replace('Dear _-', f'Dear {name},')
        
        # Date replacements
        report_date = datetime.now().strftime('%B %d, %Y')
        roadmap = roadmap.replace('Report Date: _', f'Report Date: {report_date}')
        roadmap = roadmap.replace('Report Date: __', f'Report Date: {report_date}')
        
        # Labs drawn date
        labs_date = client_data.get('labs_date', report_date)
        roadmap = roadmap.replace('Labs Drawn: _____', f'Labs Drawn: {labs_date}')
        
        return roadmap
    
    def _process_lab_values(self, roadmap: str, lab_results: Dict[str, Any]) -> str:
        """Process lab values and apply conditional logic based on ranges."""
        
        # APO E Genetics
        apo_e = lab_results.get('APO1', '')
        roadmap = self._process_apo_e_genetics(roadmap, apo_e)
        
        # Glutathione
        glutathione = lab_results.get('METAB_GLUT', 0)
        roadmap = roadmap.replace('GLUTATHIONE level was_', f'GLUTATHIONE level was {glutathione}')
        
        # MTHFR
        mthfr_c677t = lab_results.get('MTHFR_1', 'Not Detected')
        mthfr_a1298c = lab_results.get('MTHFR_2', 'Not Detected')
        roadmap = self._process_mthfr_genetics(roadmap, mthfr_c677t, mthfr_a1298c)
        
        # Homocysteine
        homocysteine = lab_results.get('INFLAM_HOMOCYS', 0)
        roadmap = roadmap.replace('HOMOCYSTEINE level was_', f'HOMOCYSTEINE level was {homocysteine}')
        
        # B vitamins
        b12 = lab_results.get('VIT_B12', 0)
        roadmap = roadmap.replace('VITAMIN B12 level was_', f'VITAMIN B12 level was {b12}')
        
        # Vitamin D
        vit_d = lab_results.get('VIT_D25', 0)
        roadmap = self._process_vitamin_d(roadmap, vit_d)
        
        # Vitamin E
        vit_e = lab_results.get('VIT_E', 0)
        roadmap = roadmap.replace('combined Vitamin E level is_', f'combined Vitamin E level is {vit_e}')
        
        # Omega fatty acids
        omega_check = lab_results.get('OMEGA_CHECK', 0)
        omega_ratio = lab_results.get('OMEGA_6_3_RATIO', 0)
        aa_epa_ratio = lab_results.get('OMEGA_AA_EPA', 0)
        arachidonic = lab_results.get('OMEGA_AA', 0)
        
        roadmap = roadmap.replace('OMEGACHECK(TM) value was _ %', f'OMEGACHECK(TM) value was {omega_check} %')
        roadmap = roadmap.replace('OMEGA 6:3 ratio was _-to-1', f'OMEGA 6:3 ratio was {omega_ratio}-to-1')
        roadmap = roadmap.replace('ratio was found to be _x\'s', f'ratio was found to be {omega_ratio}x\'s')
        roadmap = roadmap.replace('ARACHADONIC ACID-to-EPA ratio was_', f'ARACHADONIC ACID-to-EPA ratio was {aa_epa_ratio}')
        roadmap = roadmap.replace('ARACHADONIC ACID level was_', f'ARACHADONIC ACID level was {arachidonic}')
        
        # Magnesium
        mg_rbc = lab_results.get('MIN_MG_RBC', 0)
        roadmap = roadmap.replace('MAGNESIUM RBC level is_', f'MAGNESIUM RBC level is {mg_rbc}')
        
        # Copper and Zinc
        copper = lab_results.get('MIN_CU', 0)
        zinc = lab_results.get('MIN_ZN', 0)
        roadmap = roadmap.replace('COPPER level is_', f'COPPER level is {copper}')
        roadmap = roadmap.replace('ZINC level is_', f'ZINC level is {zinc}')
        
        # Calculate copper to zinc ratio
        if copper and zinc:
            cz_ratio = round(copper / zinc, 2)
            roadmap = roadmap.replace('COPPER-to-ZINC RATIO is ____', f'COPPER-to-ZINC RATIO is {cz_ratio}')
        
        # Selenium
        selenium = lab_results.get('MIN_SE', 0)
        roadmap = roadmap.replace('Selenium level is_', f'Selenium level is {selenium}')
        
        # Blood sugar markers
        glucose = lab_results.get('CHEM_GLU', 0)
        insulin = lab_results.get('METAB_INS', 0)
        hba1c = lab_results.get('METAB_HBA1C', 0)
        
        roadmap = roadmap.replace('fasting BLOOD SUGAR was_', f'fasting BLOOD SUGAR was {glucose}')
        roadmap = roadmap.replace('baseline INSULIN was_', f'baseline INSULIN was {insulin}')
        roadmap = roadmap.replace('baseline A1c was_', f'baseline A1c was {hba1c}')
        
        # Calculate HOMA-IR if insulin and glucose available
        if insulin and glucose:
            homa_ir = round((insulin * glucose) / 405, 2)
            roadmap = roadmap.replace('HOMA-IR calculation is_', f'HOMA-IR calculation is {homa_ir}')
        
        # Cholesterol panel
        total_chol = lab_results.get('LIPID_CHOL', 0)
        triglycerides = lab_results.get('LIPID_TRIG', 0)
        hdl = lab_results.get('LIPID_HDL', 0)
        ldl = lab_results.get('LIPID_LDL', 0)
        
        roadmap = roadmap.replace('TOTAL CHOLESTEROL level was_', f'TOTAL CHOLESTEROL level was {total_chol}')
        roadmap = roadmap.replace('TRIGLYCERIDE level was_', f'TRIGLYCERIDE level was {triglycerides}')
        roadmap = roadmap.replace('HDL CHOLESTEROL, which is often considered "the good cholesterol," was_', 
                                f'HDL CHOLESTEROL, which is often considered "the good cholesterol," was {hdl}')
        roadmap = roadmap.replace('LDL CHOLESTEROL, which is often considered "the bad cholesterol" was_',
                                f'LDL CHOLESTEROL, which is often considered "the bad cholesterol" was {ldl}')
        
        # Calculate triglyceride to HDL ratio
        if triglycerides and hdl:
            trig_hdl_ratio = round(triglycerides / hdl, 2)
            roadmap = roadmap.replace('TRIG-to-HDL RATIO was_', f'TRIG-to-HDL RATIO was {trig_hdl_ratio}')
        
        return roadmap
    
    def _process_apo_e_genetics(self, roadmap: str, apo_e: str) -> str:
        """Process APO E genetics and apply appropriate conditional text."""
        roadmap = roadmap.replace('Your APO E Genotype is ___', f'Your APO E Genotype is {apo_e}')
        
        # Determine APO E risk level and apply appropriate sections
        if 'E4' in apo_e:
            if apo_e == 'E4/E4':
                # Both APO E4 genes - highest risk
                sections_to_keep = ['both APO E4 genes']
            else:
                # One APO E4 gene - moderate risk  
                sections_to_keep = ['one of the APO E4 genes']
        else:
            # No APO E4 genes - lower genetic risk
            sections_to_keep = ['do not have the APO E genetic risk']
        
        return roadmap
    
    def _process_mthfr_genetics(self, roadmap: str, c677t: str, a1298c: str) -> str:
        """Process MTHFR genetics and recommendations."""
        roadmap = roadmap.replace('Your MTHFR Genotype shows a _ variant and a_ variant', 
                                f'Your MTHFR Genotype shows a {c677t} variant and a {a1298c} variant')
        
        # Apply MTHFR-specific recommendations based on variants
        if c677t != 'Not Detected' or a1298c != 'Not Detected':
            # Has one or more MTHFR variants - needs methylated B vitamins
            pass  # Keep methylation recommendations
        else:
            # No MTHFR variants - remove methylation-specific text
            pass
            
        return roadmap
    
    def _process_vitamin_d(self, roadmap: str, vit_d: float) -> str:
        """Process Vitamin D levels and apply appropriate recommendations."""
        roadmap = roadmap.replace('baseline Vitamin D level is_', f'baseline Vitamin D level is {vit_d}')
        
        # Apply vitamin D recommendations based on level
        if vit_d >= 60:
            # Optimal level
            recommendation = "This level falls within the optimal parameters and no additional intervention is recommended."
        elif vit_d >= 50:
            # Close to optimal
            recommendation = "This level is close to the optimal parameters and though no additional intervention is recommended, you may want to check your VITAMIN D level a few times per year to make sure that it does not drop."
        elif vit_d >= 40:
            # Suboptimal - needs 4000 IU
            recommendation = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was 40-49, you are encouraged to supplement with 4,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
        elif vit_d >= 30:
            # Low - needs 8000 IU
            recommendation = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was 30-39, you are encouraged to supplement with 8,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
        else:
            # Very low - needs 10000 IU
            recommendation = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was < 30, you are encouraged to supplement with 10,000 iu of VITAMIN D3 per day and then recheck your levels in 90 days."
        
        return roadmap
    
    def _process_genetics(self, roadmap: str, lab_results: Dict[str, Any]) -> str:
        """Process genetic information and conditional recommendations."""
        # This is handled in _process_lab_values for APO E and MTHFR
        return roadmap
    
    def _process_gender_sections(self, roadmap: str, gender: str) -> str:
        """Apply gender-specific hormone sections."""
        if gender and gender.lower() in ['female', 'f']:
            # Keep female hormone sections, remove male sections
            # This would involve more complex text processing
            pass
        elif gender and gender.lower() in ['male', 'm']:
            # Keep male hormone sections, remove female sections
            pass
        
        return roadmap
    
    def _process_hhq_responses(self, roadmap: str, hhq_responses: Dict[str, Any]) -> str:
        """Process HHQ responses and apply lifestyle recommendations."""
        # Process tagged responses for brain fog, energy, sleep, etc.
        # This would involve checking specific HHQ tags and adding recommendations
        return roadmap
    
    def _cleanup_placeholders(self, roadmap: str) -> str:
        """Clean up any remaining unfilled placeholders."""
        # Replace any remaining single underscores with "Not Available"
        roadmap = re.sub(r'\b_\b', 'Not Available', roadmap)
        
        # Replace any remaining multiple underscores
        roadmap = re.sub(r'_{3,}', 'Not Available', roadmap)
        
        return roadmap
    
    def get_supplement_recommendations(self, lab_results: Dict[str, Any]) -> list:
        """Extract supplement recommendations based on lab results."""
        recommendations = []
        
        # Vitamin D
        vit_d = lab_results.get('VIT_D25', 0)
        if vit_d < 60:
            if vit_d < 30:
                recommendations.append("Vitamin D3 10,000 IU daily")
            elif vit_d < 40:
                recommendations.append("Vitamin D3 8,000 IU daily")
            elif vit_d < 50:
                recommendations.append("Vitamin D3 4,000 IU daily")
            else:
                recommendations.append("Vitamin D3 2,000 IU daily")
        
        # Omega-3
        omega_ratio = lab_results.get('OMEGA_6_3_RATIO', 0)
        if omega_ratio > 4:
            recommendations.append("High-quality Omega-3 supplement (Nordic Naturals Pro-Omega 2000)")
        
        # Magnesium
        mg_rbc = lab_results.get('MIN_MG_RBC', 0)
        if mg_rbc < 5.2:
            recommendations.append("Magnesium Threonate 2000 mg at night")
        
        # MTHFR support
        mthfr_c677t = lab_results.get('MTHFR_1', 'Not Detected')
        mthfr_a1298c = lab_results.get('MTHFR_2', 'Not Detected')
        if mthfr_c677t != 'Not Detected' or mthfr_a1298c != 'Not Detected':
            recommendations.append("Methylated B-Complex (MethylPro)")
        
        # Glutathione support
        glutathione = lab_results.get('METAB_GLUT', 0)
        if glutathione < 300:
            recommendations.append("NAC 600 mg twice daily")
            recommendations.append("Glutathione Recycler 1 capsule twice daily")
        
        return recommendations

# Usage example
if __name__ == "__main__":
    # Example usage
    generator = RoadmapGenerator()
    
    sample_client_data = {
        'name': 'Connie B',
        'gender': 'female',
        'dob': '1960-01-01',
        'labs_date': 'May 30, 2025'
    }
    
    sample_lab_results = {
        'CBC_WBC': 7.6,
        'FHt_FSH': 76.1,
        'APO1': 'E2/E4',
        'MTHFR_1': 'Not Detected',
        'MTHFR_2': 'Not Detected',
        'VIT_D25': 73.2,
        'METAB_GLUT': 222,
        'OMEGA_6_3_RATIO': 4.9
    }
    
    try:
        roadmap = generator.generate_roadmap(sample_client_data, sample_lab_results)
        print("Roadmap generated successfully!")
        print(f"Length: {len(roadmap)} characters")
    except Exception as e:
        print(f"Error generating roadmap: {str(e)}") 