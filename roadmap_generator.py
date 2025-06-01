import re
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

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
        
        # Visual assets configuration
        self.assets_base_path = "/Users/jstoker/Documents/mindstoke-server/app/static/images/roadmap"
        self.visual_assets = {
            'logos': {
                'main_logo': os.path.join(self.assets_base_path, 'logos', 'main_logo.png'),
                'amfas_logo': os.path.join(self.assets_base_path, 'logos', 'amfas_logo.png'),
            },
            'supplements': {
                'vitamin_d': os.path.join(self.assets_base_path, 'supplements', 'vitamin_d.png'),
                'omega3': os.path.join(self.assets_base_path, 'supplements', 'omega3.png'),
                'magnesium': os.path.join(self.assets_base_path, 'supplements', 'magnesium.png'),
                'b_complex': os.path.join(self.assets_base_path, 'supplements', 'b_complex.png'),
            },
            'icons': {
                'brain': os.path.join(self.assets_base_path, 'icons', 'brain.png'),
                'heart': os.path.join(self.assets_base_path, 'icons', 'heart.png'),
                'supplement': os.path.join(self.assets_base_path, 'icons', 'supplement.png'),
                'lab': os.path.join(self.assets_base_path, 'icons', 'lab.png'),
            },
            'branding': {
                'header_bg': os.path.join(self.assets_base_path, 'branding', 'header_bg.png'),
                'footer_bg': os.path.join(self.assets_base_path, 'branding', 'footer_bg.png'),
            }
        }
        
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
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings_to_try:
            try:
                with open(self.template_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    # Clean up any problematic characters
                    content = content.replace('\u2018', "'")  # Left single quotation mark
                    content = content.replace('\u2019', "'")  # Right single quotation mark
                    content = content.replace('\u201c', '"')  # Left double quotation mark
                    content = content.replace('\u201d', '"')  # Right double quotation mark
                    content = content.replace('\u2013', '-')  # En dash
                    content = content.replace('\u2014', '—')  # Em dash
                    content = content.replace('\u2026', '...')  # Horizontal ellipsis
                    return content
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                raise FileNotFoundError(f"Template file not found: {self.template_path}")
            except Exception as e:
                continue
        
        # If all encodings fail, try with error handling
        try:
            with open(self.template_path, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()
                return content
        except Exception as e:
            raise Exception(f"Error loading template: {str(e)}")
    
    def generate_roadmap(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], 
                        hhq_responses: Dict[str, Any] = None) -> str:
        """
        Generate a personalized roadmap for a client using intelligent conditional logic.
        
        Args:
            client_data: Client information (name, gender, dob, etc.)
            lab_results: Dictionary of lab results keyed by armgasys_variable
            hhq_responses: HHQ survey responses (optional)
            
        Returns:
            Personalized roadmap as string
        """
        roadmap = self.template_content
        
        # 1. Process all content controls using intelligent evaluation
        processed_content = self._process_all_content_controls(client_data, lab_results, hhq_responses)
        
        # 2. Apply all processed content controls to the template
        roadmap = self._apply_content_controls_to_template(roadmap, processed_content)
        
        # 3. Replace basic client information
        roadmap = self._replace_client_info(roadmap, client_data)
        
        # 4. Process lab values with intelligent thresholds
        roadmap = self._process_lab_values_intelligent(roadmap, lab_results, processed_content)
        
        # 5. Apply gender-specific sections
        roadmap = self._process_gender_sections(roadmap, client_data.get('gender'))
        
        # 6. Clean up any remaining placeholders
        roadmap = self._cleanup_placeholders(roadmap)
        
        return roadmap
    
    def _apply_content_controls_to_template(self, roadmap: str, processed_content: Dict[str, Any]) -> str:
        """
        Apply all processed content controls to the roadmap template.
        This replaces content control placeholders with appropriate content or removes them.
        """
        # Apply each content control from our intelligent processing
        for control_name, control_value in processed_content.items():
            # Handle conditional blocks: {{#control_name}}content{{/control_name}}
            block_pattern = f"{{{{#{control_name}}}}}(.*?){{{{/{control_name}}}}}"
            
            if isinstance(control_value, bool):
                if control_value:
                    # Show the content by removing the conditional markers, keeping the content
                    def replace_block(match):
                        return match.group(1)  # Return just the content without the markers
                    roadmap = re.sub(block_pattern, replace_block, roadmap, flags=re.DOTALL)
                else:
                    # Hide the content by removing the entire block
                    roadmap = re.sub(block_pattern, "", roadmap, flags=re.DOTALL)
            
            # Handle simple placeholders: {{control_name}}
            placeholder = f"{{{{{control_name}}}}}"
            if isinstance(control_value, (str, int, float)):
                # Replace with the actual value
                roadmap = roadmap.replace(placeholder, str(control_value))
            else:
                # For complex values, convert to string or remove if empty
                roadmap = roadmap.replace(placeholder, str(control_value) if control_value else "")
        
        # Special handling for MTHFR variants (template has specific placeholder pattern)
        if 'MTHFR_C677T' in processed_content and 'MTHFR_A1298C' in processed_content:
            mthfr_c677t = processed_content['MTHFR_C677T']
            mthfr_a1298c = processed_content['MTHFR_A1298C']
            
            # Enhanced MTHFR variant processing to handle all combinations
            variant_text = "Your MTHFR Genotype shows "
            variants_found = []
            
            # Process C677T variant - fix the detection logic
            if mthfr_c677t and str(mthfr_c677t).strip() not in ['Not Detected', 'not detected', '', 'normal']:
                if 'homozygous' in str(mthfr_c677t).lower():
                    variants_found.append("C677T homozygous")
                elif 'heterozygous' in str(mthfr_c677t).lower():
                    variants_found.append("C677T heterozygous") 
                else:
                    variants_found.append("C677T")
            
            # Process A1298C variant - fix the detection logic
            if mthfr_a1298c and str(mthfr_a1298c).strip() not in ['Not Detected', 'not detected', '', 'normal']:
                if 'homozygous' in str(mthfr_a1298c).lower():
                    variants_found.append("A1298C homozygous")
                elif 'heterozygous' in str(mthfr_a1298c).lower():
                    variants_found.append("A1298C heterozygous")
                else:
                    variants_found.append("A1298C")
            
            # Construct the appropriate text based on findings
            if len(variants_found) == 2:
                # Both variants detected
                variant_text += f"a {variants_found[0]} and an {variants_found[1]} variant"
            elif len(variants_found) == 1:
                # Single variant detected
                variant_name = variants_found[0]
                article = "an" if variant_name.startswith('A') else "a"
                variant_text += f"{article} {variant_name} variant"
            else:
                # No variants detected
                variant_text = "Your MTHFR Genotype shows no detected variants"
            
            # Replace the MTHFR template patterns (handle multiple possible patterns)
            old_patterns = [
                "Your MTHFR Genotype shows a _ variant and a_ variant",
                "Your MTHFR Genotype shows a Detected variant and aDetected variant",
                "Your MTHFR Genotype shows a _ variant and an _ variant",
                "Your MTHFR Genotype shows _ variant and _ variant"
            ]
            
            for old_pattern in old_patterns:
                roadmap = roadmap.replace(old_pattern, variant_text)
            
            print(f"DEBUG: Enhanced MTHFR processing. C677T: {mthfr_c677t}, A1298C: {mthfr_a1298c}, Variants found: {variants_found}, Final text: {variant_text}")
        
        return roadmap
    
    def _remove_content_control_section(self, roadmap: str, control_name: str) -> str:
        """
        Remove content control sections that should not be displayed.
        This handles both simple placeholders and content blocks.
        """
        # Pattern for content control blocks: {control_name}...content...{/control_name}
        block_pattern = f"{{{{#{control_name}}}}}.*?{{{{{control_name}}}}}.*?{{{{/{control_name}}}}}"
        roadmap = re.sub(block_pattern, "", roadmap, flags=re.DOTALL | re.IGNORECASE)
        
        # Pattern for simple conditional content: {control_name}content{/control_name}
        simple_pattern = f"{{{{{control_name}}}}}.*?{{{{/{control_name}}}}}"
        roadmap = re.sub(simple_pattern, "", roadmap, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove simple placeholder
        roadmap = roadmap.replace(f"{{{{{control_name}}}}}", "")
        
        return roadmap
    
    def _process_lab_values_intelligent(self, roadmap: str, lab_results: Dict[str, Any], 
                                       processed_content: Dict[str, Any]) -> str:
        """
        Process lab values using intelligent thresholds and compound logic.
        """
        # Use our intelligent processing results instead of simple replacement
        for lab_key, lab_value in lab_results.items():
            if lab_value is not None:
                # Replace lab value placeholders
                placeholder = f"{{{{{lab_key}}}}}"
                roadmap = roadmap.replace(placeholder, str(lab_value))
                
                # Also try common lab name variations
                for mapping_key, display_name in self.lab_mappings.items():
                    if mapping_key == lab_key:
                        display_placeholder = f"{{{{{display_name}}}}}"
                        roadmap = roadmap.replace(display_placeholder, str(lab_value))
        
        # Apply calculated lab values
        if 'HOMA_IR' in processed_content:
            roadmap = roadmap.replace("{{HOMA-IR}}", str(processed_content['HOMA_IR']))
        if 'T_HDL_Ratio' in processed_content:
            roadmap = roadmap.replace("{{T-HDL-Ratio}}", str(processed_content['T_HDL_Ratio']))
        if 'AG_Ratio' in processed_content:
            roadmap = roadmap.replace("{{A/G-Ratio}}", str(processed_content['AG_Ratio']))
        if 'CZ_Ratio' in processed_content:
            roadmap = roadmap.replace("{{Copper/Zinc-Ratio}}", str(processed_content['CZ_Ratio']))
        if 'EP_Ratio' in processed_content:
            roadmap = roadmap.replace("{{E:P-Ratio}}", str(processed_content['EP_Ratio']))
        
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
        
        # Determine APO E risk category based on genotype
        apo_e_upper = apo_e.upper()
        
        if 'E4/E4' in apo_e_upper:
            # E4/E4 genotype - highest risk
            apo_e_recommendation = """You have the APO E E4 / E4 genetic variant, which DOES increase your risk for Alzheimer's 
Dementia, cardiovascular disease, and potentially other neurodegenerative diseases. This finding is significant. 
Details about each of these interventions will follow."""
        elif 'E4' in apo_e_upper and ('E3' in apo_e_upper or 'E2' in apo_e_upper):
            # E4/E3 or E4/E2 genotype - moderate risk
            apo_e_recommendation = """You have the APO E E4 / E3 genetic variant, which DOES increase your risk for Alzheimer's 
Dementia, cardiovascular disease, and potentially other neurodegenerative diseases. This finding is significant. 
Details about each of these interventions will follow."""
        else:
            # No E4 variant (E3/E3, E3/E2, E2/E2) - lower risk
            apo_e_recommendation = """You do not have the APO E genetic risk for Alzheimer's Dementia. You should consider ADDITIONAL 
IMMUNE SYSTEM TESTING and/or TOXICITY TESTING to clarify your risk for TOXIC CONTRIBUTORS of neurodegenerative 
disease."""
        
        # Replace the APO E recommendation placeholder
        roadmap = roadmap.replace('APOE_RECOMMENDATION_PLACEHOLDER', apo_e_recommendation)
        
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

    def generate_visual_pdf(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], 
                           hhq_responses: Dict[str, Any] = None, output_path: str = None) -> str:
        """
        Generate a professionally formatted roadmap PDF matching the A MIND template design.
        """
        if output_path is None:
            output_path = f"/tmp/roadmap_{client_data.get('name', 'client')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Process all content controls first
        processed_content = self._process_all_content_controls(client_data, lab_results, hhq_responses)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=50, leftMargin=50,
                               topMargin=50, bottomMargin=50)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Define custom styles matching the A MIND design
        title_style = ParagraphStyle(
            'AMindTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.white,
            backColor=HexColor('#4A90A4'),  # Blue header color
            alignment=1,  # Center
            borderPadding=10
        )
        
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.white,
            backColor=colors.black,
            alignment=1,
            borderPadding=8
        )
        
        body_style = ParagraphStyle(
            'AMindBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leading=12,
            leftIndent=10,
            rightIndent=10
        )
        
        supplement_style = ParagraphStyle(
            'SupplementHighlight',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            backColor=HexColor('#90EE90'),  # Light green
            borderPadding=5,
            spaceAfter=8
        )
        
        # Add A MIND header/logo section
        if self._image_exists('logos', 'main_logo'):
            try:
                logo = RLImage(self.visual_assets['logos']['main_logo'], width=1.5*inch, height=0.75*inch)
                logo.hAlign = 'LEFT'
                story.append(logo)
            except:
                pass
        
        story.append(Spacer(1, 20))
        
        # Main title section
        client_name = processed_content.get('fullname', client_data.get('name', 'Patient'))
        title = Paragraph(f"Roadmap Summary for {client_name}<br/>The Enhance Protocol®", title_style)
        story.append(title)
        story.append(Spacer(1, 15))
        
        # Report info section
        today_date = processed_content.get('today', datetime.now().strftime('%B %d, %Y'))
        lab_date = processed_content.get('lab-date', today_date)
        
        info_table_data = [
            [f"Report Date: {today_date}", f"Labs Drawn: {lab_date}"]
        ]
        info_table = Table(info_table_data, colWidths=[3*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Your Test Results Section
        story.append(Paragraph("Your Test Results", section_header_style))
        
        test_results_text = """The next few pages include the results of your cognitive and blood tests. They include a short explanation of the 
importance of the test, along with your results. The test results are in RED on a gray background. To help you understand 
your next steps, follow the colored clues below."""
        story.append(Paragraph(test_results_text, body_style))
        story.append(Spacer(1, 10))
        
        # Supplement recommendations highlight
        supplement_text = "Supplement or Medication Recommendations are highlighted in Green"
        story.append(Paragraph(supplement_text, supplement_style))
        story.append(Spacer(1, 10))
        
        # AMFAS coaching note
        amfas_text = """Recommended homework, additional research, and opportunities to ask questions during office hours from the AMFAS 
Coaches or medical staff during Office Hours are highlighted in Yellow."""
        story.append(Paragraph(amfas_text, body_style))
        story.append(Spacer(1, 20))
        
        # Cognitive Test Results Section
        story.append(Paragraph("Your Baseline Cognitive Test Results", section_header_style))
        
        cognitive_text = """Each participant in The Enhance Protocol® completes a baseline cognitive test. Depending on your age and your 
current cognitive health, you have been asked to complete a MoCA test or a computer-based CNS VITAL SIGNS test. 
Your test results and summarized below, and if you would like a copy of your complete results, please email 
info@amindforallseasons.com and we will send you the full report."""
        story.append(Paragraph(cognitive_text, body_style))
        story.append(Spacer(1, 10))
        
        # Add cognitive test results or message
        cognitive_results_text = """The Enhance Protocol® is designed to help you improve brain functioning starting from your baseline. We look forward to helping 
you complete a retest once you have applied the recommendations in your Roadmap Report for at least a few months. Please 
attend one of our online Office Hours sessions and ask for guidance regarding how to understand your specific test results."""
        story.append(Paragraph(cognitive_results_text, body_style))
        story.append(Spacer(1, 15))
        
        # Conditional cognitive test message
        no_results_text = """<font color='red'><b>These are the results from your recent cognitive test.</b><br/>
<b>or</b><br/>
<b>We did not have any results from cognitive testing when we prepared this roadmap. You are encouraged to do a 
baseline cognitive test so we can measure your progress.</b></font>"""
        story.append(Paragraph(no_results_text, body_style))
        story.append(Spacer(1, 20))
        
        # Supplements section
        supplements_title = "A Targeted Supplements Approach Can Improve Your Brain Health"
        story.append(Paragraph(supplements_title, 
                             ParagraphStyle('SupplementTitle', parent=styles['Heading1'], 
                                          fontSize=16, spaceAfter=15, spaceBefore=20)))
        
        supplements_intro = """Many individuals are using supplements on a regular basis. You may be using supplements because your 
healthcare provider recommended it. You may be using supplements because you saw a commercial or read an 
article about the benefits of one supplement over another."""
        story.append(Paragraph(supplements_intro, body_style))
        story.append(Spacer(1, 10))
        
        # APO E Genetics Section
        story.append(Paragraph("APO E Genetic Profile and Your Risk for Oxidative Stress", section_header_style))
        
        # Use processed genome type
        genome_type = processed_content.get('genome-type', '[genome-type]')
        glut_value = processed_content.get('GLUT_VALUE', '[GLUT_VALUE]')
        
        apo_e_text = f"""Your APO E Genotype is {genome_type}. Your APO E genetics has some predictive value for increased risk of 
cardiovascular and neurodegenerative disease. Your GLUTATHIONE level was {glut_value} and many neurologists 
suggest the optimal range may exceed 300 μg/mL. GLUTATHIONE reflects your ability to calm oxidative stress."""
        story.append(Paragraph(apo_e_text, body_style))
        story.append(Spacer(1, 10))
        
        # Process APO E conditional sections using processed content
        # APO E genetics recommendations based on processed content
        if processed_content.get('quick-E4'):  # E4/E4 genotype
            apo_e_recommendation = """You have the APO E E4 / E4 genetic variant, which DOES increase your risk for Alzheimer's 
Dementia, cardiovascular disease, and potentially other neurodegenerative diseases. This finding is significant. 
Details about each of these interventions will follow."""
        elif processed_content.get('quick-E4E3'):  # E4/E3 genotype
            apo_e_recommendation = """You have the APO E E4 / E3 genetic variant, which DOES increase your risk for Alzheimer's 
Dementia, cardiovascular disease, and potentially other neurodegenerative diseases. This finding is significant. 
Details about each of these interventions will follow."""
        else:  # No E4 variant
            apo_e_recommendation = """You do not have the APO E genetic risk for Alzheimer's Dementia. You should consider ADDITIONAL 
IMMUNE SYSTEM TESTING and/or TOXICITY TESTING to clarify your risk for TOXIC CONTRIBUTORS of neurodegenerative 
disease."""

        
        story.append(Paragraph(apo_e_recommendation, body_style))
        story.append(Spacer(1, 20))
        
        # Lab Results Processing Section with processed content
        story = self._add_processed_lab_results_sections(story, processed_content, body_style, supplement_style)
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _process_all_content_controls(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], 
                                     hhq_responses: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Intelligent conditional processing system using all lab thresholds and compound logic.
        Based on comprehensive lab panel analysis and HHQ integration.
        ENSURES ALL LAB VALUES ARE REPRESENTED IN THE ROADMAP.
        """
        processed = {}
        
        # Set default values
        if hhq_responses is None:
            hhq_responses = {}
        
        # Get client info
        gender = client_data.get('gender', '').lower()
        client_name = client_data.get('name', '')
        firstname = client_name.split()[0] if client_name else 'Patient'
        
        # Basic client information
        processed.update({
            'fullname': client_name,
            'firstname': firstname,
            'today': datetime.now().strftime('%B %d, %Y'),
            'lab-date': datetime.now().strftime('%B %d, %Y')
        })
        
        # Get comprehensive lab ranges
        ranges = self._get_comprehensive_lab_ranges()
        
        # Calculate compound lab values and ratios
        calculated_values = self._calculate_compound_lab_values(lab_results)
        lab_results.update(calculated_values)
        
        # CRITICAL: Process ALL lab values first to ensure complete coverage
        processed.update(self._process_all_lab_values_comprehensive(lab_results, ranges, gender))
        
        # Process specific marker categories (these will add to, not replace, the comprehensive processing)
        processed.update(self._process_inflammatory_markers(lab_results, hhq_responses, ranges))
        processed.update(self._process_cardiovascular_markers(lab_results, hhq_responses, ranges))
        processed.update(self._process_metabolic_markers(lab_results, hhq_responses, ranges))
        processed.update(self._process_thyroid_markers(lab_results, hhq_responses, ranges))
        processed.update(self._process_nutrient_markers(lab_results, hhq_responses, ranges))
        processed.update(self._process_genetic_markers(lab_results, hhq_responses))
        
        # Gender-specific hormone processing
        if gender == 'male':
            processed.update(self._process_male_hormone_markers(lab_results, hhq_responses, ranges))
            processed['quick-male-hormones'] = True
            processed['quick-female-hormones'] = False
        else:
            processed.update(self._process_female_hormone_markers(lab_results, hhq_responses, ranges))
            processed['quick-female-hormones'] = True
            processed['quick-male-hormones'] = False
        
        # Process compound conditions that combine multiple markers
        processed.update(self._process_compound_conditions(lab_results, hhq_responses, ranges))
        
        # Process HHQ-based conditions and interactions
        processed.update(self._process_hhq_based_conditions(hhq_responses, lab_results))
        
        # Process advanced protocols (hormones, supplements, specialized interventions)
        processed.update(self._process_advanced_protocols(lab_results, hhq_responses, ranges))
        
        return processed

    def _process_all_lab_values_comprehensive(self, lab_results: Dict[str, Any], ranges: Dict, gender: str) -> Dict[str, Any]:
        """
        COMPREHENSIVE processing that ensures ALL lab values get represented in the roadmap.
        This is the safety net to make sure no lab value is missed.
        """
        processed = {}
        
        # Map all possible lab values to content controls
        lab_mappings = {
            # Inflammatory markers
            'INFLAM_CRP': 'quick-hsCRP',
            'INFLAM_HOMOCYS': 'quick-homocysteine', 
            'INFLAM_ESR': 'quick-ESR',
            'INFLAM_FERRITIN': 'quick-ferritin',
            
            # Lipid panel
            'LIPID_CHOL': 'cholesterol-row',
            'LIPID_HDL': 'quick-HDL',
            'LIPID_LDL': 'quick-LDL', 
            'LIPID_TRIG': 'quick-triglycerides',
            'LIPID_NONHDL': 'quick-nonHDL',
            
            # Complete blood count
            'CBC_WBC': 'quick-WBC',
            'CBC_RBC': 'quick-RBC',
            'CBC_HGB': 'quick-hemoglobin',
            'CBC_HCT': 'quick-hematocrit',
            'CBC_PLT': 'quick-platelets',
            
            # Comprehensive metabolic panel
            'CHEM_GLU': 'glucose-elevated',
            'CHEM_BUN': 'quick-BUN',
            'CHEM_CREAT': 'quick-creatinine',
            'CHEM_EGFR': 'quick-eGFR',
            'CHEM_NA': 'quick-sodium',
            'CHEM_K': 'quick-potassium',
            'CHEM_CL': 'quick-chloride',
            'CHEM_CO2': 'quick-CO2',
            
            # Liver function
            'LFT_ALT': 'quick-ALT',
            'LFT_AST': 'quick-AST',
            'LFT_ALKP': 'quick-alkaline-phosphatase',
            'LFT_BILI': 'quick-bilirubin',
            'LFT_ALB': 'quick-albumin',
            
            # Thyroid panel
            'THY_TSH': 'TSH-elevated',
            'THY_T4F': 'quick-FT4',
            'THY_T3F': 'FT3-low',
            'THY_RT3': 'quick-reverseT3',
            'THY_T4': 'quick-T4',
            'THY_T3': 'quick-T3',
            
            # Vitamins & nutrients
            'VIT_D25': 'D-optimal',
            'VIT_B12': 'quick-B12',
            'VIT_FOLATE': 'quick-folate',
            'VIT_E': 'quick-vitE',
            
            # Minerals
            'MIN_FE': 'quick-iron',
            'MIN_TIBC': 'quick-TIBC',
            'MIN_FERR': 'quick-ferritin',
            'MIN_ZN': 'zinc-status',
            'MIN_CU': 'quick-copper',
            'MIN_MG': 'magnesium-status',
            
            # Male hormones
            'MHt_TEST_TOT': 'testosterone-low',
            'MHt_TEST_FREE': 'free-testosterone-low',
            'MHt_PSA': 'quick-PSA',
            'NEURO_DHEAS': 'quick-DHEA-low',
            
            # Female hormones
            'FHt_E2': 'quick-estradiol',
            'FHt_PROG': 'quick-progesterone',
            'FHt_FSH': 'quick-FSH',
            'FHt_LH': 'quick-LH',
            
            # Metabolic
            'METAB_INS': 'insulin-elevated',
            'METAB_HBA1C': 'HbA1c',
            'METAB_CPEP': 'quick-C-peptide',
            
            # Specialty markers
            'OMEGA_CHECK': 'OmegaCheck',
            'SPEC_IGF1': 'quick-IGF1',
            'SPEC_CORTISOL': 'quick-cortisol',
        }
        
        # Process every single lab value
        for lab_key, lab_value in lab_results.items():
            if lab_value is None:
                continue
                
            # Get the content control name for this lab
            control_name = lab_mappings.get(lab_key, f'lab-{lab_key.lower()}')
            
            # Determine if the value should trigger the control
            should_trigger = self._evaluate_lab_threshold(lab_key, lab_value, ranges, gender)
            processed[control_name] = should_trigger
            
            # Also create value-specific controls for key markers
            if lab_key in ['INFLAM_CRP', 'VIT_D25', 'THY_TSH', 'LIPID_CHOL']:
                processed[f'{control_name}-value'] = str(lab_value)
        
        # Ensure specific critical controls are always evaluated
        critical_controls = [
            'quick-hsCRP', 'cholesterol-row', 'glucose-elevated', 'TSH-elevated',
            'D-optimal', 'testosterone-low', 'insulin-elevated', 'HbA1c'
        ]
        
        for control in critical_controls:
            if control not in processed:
                processed[control] = False
                
        return processed

    def _evaluate_lab_threshold(self, lab_key: str, lab_value: float, ranges: Dict, gender: str) -> bool:
        """
        Evaluate whether a lab value should trigger its content control.
        Returns True if the value indicates an issue that should be addressed.
        """
        try:
            lab_value = float(lab_value)
        except (ValueError, TypeError):
            return False
            
        # Gender-specific range mapping
        range_map = {
            'INFLAM_CRP': 'CRP',
            'INFLAM_HOMOCYS': 'Homocysteine',
            'LIPID_CHOL': 'TotalChol',
            'LIPID_HDL': 'HDL_M' if gender == 'male' else 'HDL_F',
            'LIPID_LDL': 'LDL',
            'LIPID_TRIG': 'Triglycerides',
            'CHEM_GLU': 'Glucose',
            'THY_TSH': 'TSH',
            'THY_T4F': 'FT4',
            'THY_T3F': 'FT3',
            'VIT_D25': 'VitD',
            'VIT_B12': 'B12',
            'MIN_ZN': 'Zinc',
            'MIN_MG': 'Magnesium',
            'MHt_TEST_TOT': 'TestTotal_M',
            'MHt_TEST_FREE': 'TestFree_M',
            'NEURO_DHEAS': 'DHEAS_M' if gender == 'male' else 'DHEAS_F',
            'FHt_E2': 'Estradiol_F',
            'FHt_PROG': 'Progesterone_F',
            'METAB_INS': 'Insulin',
            'METAB_HBA1C': 'HbA1c',
        }
        
        range_key = range_map.get(lab_key)
        if not range_key or range_key not in ranges:
            # If no specific range, consider values outside very broad normal ranges as triggers
            return lab_value < 1 or lab_value > 1000  # Default conservative check
            
        range_info = ranges[range_key]
        
        # Determine if value is outside optimal range (triggers intervention)
        below_min = lab_value < range_info.get('optimal_min', 0)
        above_max = lab_value > range_info.get('optimal_max', float('inf'))
        
        return below_min or above_max
    
    def _get_comprehensive_lab_ranges(self) -> Dict[str, Dict[str, float]]:
        """
        Complete lab reference ranges from panel analysis.
        Returns optimal health ranges, not just 'normal' ranges.
        """
        return {
            # Inflammatory Markers
            'CRP': {'optimal_max': 0.9, 'unit': 'mg/dL'},
            'IL6': {'optimal_max': 3.0, 'unit': 'pg/mL'},
            'TNF': {'optimal_max': 6.0, 'unit': 'pg/mL'},
            'MPO': {'optimal_max': 400, 'unit': 'pmol/L'},
            'Fibrinogen': {'optimal_max': 550, 'unit': 'mg/dL'},
            'SerumTryptase': {'optimal_min': 15, 'unit': 'ng/dL'},
            'Galectin3': {'optimal_max': 15, 'unit': 'ng/mL'},
            'Homocysteine': {'optimal_max': 7, 'unit': 'mmol/L'},
            
            # Cardiovascular
            'TotalChol': {'optimal_min': 150, 'unit': 'mg/dL'},
            'sdLDL': {'optimal_max': 20, 'unit': 'mg/dL'},
            'oxLDL': {'optimal_max': 60, 'unit': 'U/L'},
            'LDLp': {'optimal_max': 1000, 'unit': ''},
            'DDimer': {'optimal_max': 1.0, 'unit': ''},
            
            # Metabolic
            'Glucose': {'optimal_min': 65, 'optimal_max': 95, 'unit': 'mg/dL'},
            'Insulin': {'optimal_max': 4.5, 'unit': 'mIU/mL'},
            'HbA1c': {'optimal_max': 5.6, 'unit': '%'},
            'AG_Ratio': {'optimal_min': 1.8, 'unit': ''},
            'ALT': {'optimal_max': 25, 'unit': 'IU/L'},
            'AST': {'optimal_max': 10, 'unit': 'IU/L'},
            'eGFR': {'optimal_min': 60, 'unit': ''},
            
            # Thyroid
            'TSH': {'optimal_max': 2.0, 'unit': 'ng/dL'},
            'FT3': {'optimal_min': 3.2, 'optimal_max': 4.2, 'unit': 'pg/mL'},
            'FT4': {'optimal_min': 1.3, 'optimal_max': 1.8, 'unit': 'ng/dL'},
            'RT3': {'optimal_max': 15, 'unit': 'ng/dL'},
            'TPO': {'optimal_max': 30, 'unit': 'IU/mL'},
            'TgAb': {'optimal_max': 1.0, 'unit': 'IU/mL'},
            
            # Nutrients
            'VitD': {'optimal_min': 50, 'optimal_max': 80, 'unit': 'ng/dL'},
            'VitE': {'optimal_min': 12, 'optimal_max': 20, 'unit': 'mcg/mL'},
            'VitB12': {'optimal_min': 500, 'optimal_max': 1500, 'unit': 'pg/mL'},
            'Folate': {'optimal_min': 10, 'optimal_max': 25, 'unit': 'ng/mL'},
            'OmegaCheck': {'optimal_min': 5.4, 'unit': '% by weight'},
            'Omega63Ratio': {'optimal_max': 4.0, 'unit': ''},
            'AA_EPA_Ratio': {'optimal_max': 8.0, 'unit': ''},
            'MgRBC': {'optimal_min': 5.2, 'optimal_max': 6.5, 'unit': 'mg/dL'},
            'Zinc': {'optimal_min': 90, 'optimal_max': 110, 'unit': 'mcg/dL'},
            'CZ_Ratio': {'optimal_min': 0.8, 'optimal_max': 1.2, 'unit': ''},
            'Selenium': {'optimal_min': 110, 'optimal_max': 150, 'unit': 'ng/mL'},
            
            # Male Hormones
            'TestTotal_M': {'optimal_min': 690, 'unit': 'ng/dL'},
            'TestFree_M': {'optimal_min': 12, 'optimal_max': 15, 'unit': 'ng/dL'},
            'DHT_M': {'optimal_max': 54, 'unit': 'ng/d'},
            'DHEAS_M': {'optimal_min': 150, 'optimal_max': 300, 'unit': 'pg/dL'},
            'PSA': {'optimal_max': 4.0, 'unit': ''},
            
            # Female Hormones
            'Estradiol_F': {'target': 90, 'unit': 'pg/mL'},
            'Progesterone_F': {'optimal_min': 5, 'optimal_max': 7, 'unit': 'ng/mL'},
            'TestTotal_F': {'optimal_min': 50, 'optimal_max': 75, 'unit': 'ng/dL'},
            'DHEAS_F': {'target': 277, 'unit': 'pg/dL'},
            
            # Neuro/Adrenal
            'Pregnenolone': {'optimal_min': 50, 'optimal_max': 100, 'unit': 'ng/dL'},
            'Cortisol': {'optimal_min': 10, 'optimal_max': 18, 'unit': 'mcg/dL'},
            
            # CBC
            'WBC': {'optimal_min': 3.4, 'optimal_max': 10.8, 'unit': ''},
            'Neutrophils': {'optimal_min': 1.4, 'optimal_max': 7.0, 'unit': 'x10E3/uL'},
            'Lymphocytes': {'optimal_min': 0.7, 'optimal_max': 3.1, 'unit': 'x10E3/uL'},
        }
    
    def _calculate_compound_lab_values(self, lab_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate compound lab values and ratios."""
        calculated = {}
        
        # HOMA-IR calculation
        glucose = self._get_lab_value(lab_results, ['CHEM_GLU', 'Glucose', 'MBP_Gluc'])
        insulin = self._get_lab_value(lab_results, ['METAB_INS', 'Insulin', 'Insul'])
        if glucose and insulin:
            calculated['HOMA_IR'] = (glucose * insulin) / 405.45
        
        # T-HDL Ratio (Triglycerides / HDL)
        trig = self._get_lab_value(lab_results, ['LIPID_TRIG', 'Triglycerides', 'Trig'])
        hdl = self._get_lab_value(lab_results, ['LIPID_HDL', 'HDL Cholesterol', 'HDL'])
        if trig and hdl:
            calculated['T_HDL_Ratio'] = trig / hdl
        
        # A/G Ratio
        albumin = self._get_lab_value(lab_results, ['LFT_ALB', 'Albumin', 'MBP_Album'])
        total_protein = self._get_lab_value(lab_results, ['Total_Protein'])
        if albumin and total_protein:
            globulin = total_protein - albumin
            if globulin > 0:
                calculated['AG_Ratio'] = albumin / globulin
        
        # Copper/Zinc Ratio
        copper = self._get_lab_value(lab_results, ['MIN_CU', 'Copper', 'Copper'])
        zinc = self._get_lab_value(lab_results, ['MIN_ZN', 'Zinc', 'Zinc'])
        if copper and zinc:
            calculated['CZ_Ratio'] = copper / zinc
        
        # E:P Ratio (Female hormones)
        estradiol = self._get_lab_value(lab_results, ['FHt_E2', 'Estradiol', 'FHH_EST'])
        progesterone = self._get_lab_value(lab_results, ['FHt_PROG', 'Progesterone', 'FHH_PROG'])
        if estradiol and progesterone:
            calculated['EP_Ratio'] = estradiol / progesterone
        
        return calculated
    
    def _process_inflammatory_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process inflammatory markers and related conditions."""
        processed = {}
        
        # CRP processing
        crp = self._get_lab_value(labs, ['INFLAM_CRP', 'C-Reactive Protein', 'C-Reactive-Protein,-Cardiac'])
        if crp:
            processed['quick-hsCRP'] = crp > ranges['CRP']['optimal_max']
            if crp <= 0.9:
                processed['CRP-below-09'] = True
            elif crp <= 3.0:
                processed['CRP-09-3'] = True
            else:
                processed['CRP-above-3'] = True
        
        # Omega status for compound conditions
        omega_check = self._get_lab_value(labs, ['OMEGA_CHECK', 'OmegaCheck'])
        if omega_check:
            processed['OmegaCheck'] = omega_check
            # Compound condition: CRP + Omega
            if crp and omega_check:
                processed['quick-CRP-09-omega-<5'] = (crp > 0.9 and omega_check < 5.4)
        
        # Root canal + inflammation compound condition
        if hhq.get('hh_root_canal') and crp and crp > ranges['CRP']['optimal_max']:
            processed['root-canal-inflammation'] = True
        
        # Homocysteine
        homocysteine = self._get_lab_value(labs, ['INFLAM_HOMOCYS', 'Homocysteine'])
        if homocysteine:
            processed['quick-homocysteine'] = homocysteine > ranges['Homocysteine']['optimal_max']
        
        return processed
    
    def _process_cardiovascular_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process cardiovascular markers and smoking interactions."""
        processed = {}
        
        # Cholesterol processing
        total_chol = self._get_lab_value(labs, ['LIPID_CHOL', 'Cholesterol, Total', 'TC'])
        if total_chol:
            processed['cholesterol-row'] = total_chol < ranges['TotalChol']['optimal_min']
        
        # T-HDL ratio
        t_hdl = labs.get('T_HDL_Ratio')
        if t_hdl:
            processed['T-HDL-ratio'] = t_hdl > 3.5  # Elevated risk threshold
        
        # Smoking compound conditions
        current_smoker = hhq.get('hh_current_smoker', False)
        processed['Current-Smoker'] = current_smoker
        
        # CAC (Coronary Artery Calcium) - typically from HHQ or imaging
        cac_score = hhq.get('cac_score', 0)  # Assume HHQ captures this
        processed['quick-CAC'] = cac_score > 100
        
        return processed
    
    def _process_metabolic_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process metabolic markers including diabetes risk."""
        processed = {}
        
        # Glucose processing
        glucose = self._get_lab_value(labs, ['CHEM_GLU', 'Glucose'])
        if glucose:
            if glucose < ranges['Glucose']['optimal_min']:
                processed['glucose-low'] = True
            elif glucose > ranges['Glucose']['optimal_max']:
                processed['glucose-elevated'] = True
                processed['quick-diabetes-risk'] = True
        
        # Insulin and HOMA-IR
        insulin = self._get_lab_value(labs, ['METAB_INS', 'Insulin'])
        homa_ir = labs.get('HOMA_IR')
        if insulin:
            processed['insulin-elevated'] = insulin > ranges['Insulin']['optimal_max']
        if homa_ir:
            processed['HOMA-IR-elevated'] = homa_ir > 2.5  # Insulin resistance threshold
        
        # HbA1c
        hba1c = self._get_lab_value(labs, ['METAB_HBA1C', 'A1c'])
        if hba1c:
            processed['HbA1c'] = hba1c > ranges['HbA1c']['optimal_max']
        
        # A/G Ratio
        ag_ratio = labs.get('AG_Ratio')
        if ag_ratio:
            processed['quick-AG-ratio'] = ag_ratio < ranges['AG_Ratio']['optimal_min']
        
        return processed
    
    def _process_thyroid_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process thyroid function with compound conditions."""
        processed = {}
        
        # Individual thyroid markers
        tsh = self._get_lab_value(labs, ['THY_TSH', 'TSH'])
        ft3 = self._get_lab_value(labs, ['THY_T3F', 'FT3'])
        rt3 = self._get_lab_value(labs, ['RT3', 'Reverse T3'])
        
        if tsh:
            processed['TSH-elevated'] = tsh > ranges['TSH']['optimal_max']
        if ft3:
            processed['FT3-low'] = ft3 < ranges['FT3']['optimal_min']
        if rt3:
            processed['quick-reverseT3'] = rt3 > ranges['RT3']['optimal_max']
        
        # Compound thyroid condition
        thyroid_dysfunction = False
        if tsh and tsh > ranges['TSH']['optimal_max']:
            thyroid_dysfunction = True
        if ft3 and ft3 < ranges['FT3']['optimal_min']:
            thyroid_dysfunction = True
        if rt3 and rt3 > ranges['RT3']['optimal_max']:
            thyroid_dysfunction = True
        
        processed['TSH-T3-rT3'] = thyroid_dysfunction
        
        return processed
    
    def _process_male_hormone_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process male hormone markers and age-related conditions."""
        processed = {}
        
        # Testosterone
        test_total = self._get_lab_value(labs, ['MHt_TEST_TOT', 'Testosterone, Total'])
        test_free = self._get_lab_value(labs, ['MHt_TEST_FREE', 'Free Testosterone'])
        
        if test_total:
            processed['testosterone-low'] = test_total < ranges['TestTotal_M']['optimal_min']
        if test_free:
            processed['free-testosterone-low'] = test_free < ranges['TestFree_M']['optimal_min']
        
        # DHEA-s processing
        dheas = self._get_lab_value(labs, ['NEURO_DHEAS', 'DHEA-Sulfate'])
        vit_d = self._get_lab_value(labs, ['VIT_D25', 'Vitamin D'])
        
        if dheas:
            if dheas < ranges['DHEAS_M']['optimal_min']:
                processed['quick-DHEA-low'] = True
            if dheas > ranges['DHEAS_M']['optimal_max']:
                processed['quick-DHEA-high'] = True
        
        # Compound DHEA + Vitamin D condition
        if dheas and vit_d:
            processed['quick-DHEA-AS-VD'] = (dheas < ranges['DHEAS_M']['optimal_min'] and 
                                           vit_d < ranges['VitD']['optimal_min'])
        
        return processed
    
    def _process_female_hormone_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process female hormone markers and menopause-related conditions."""
        processed = {}
        
        # Hormone balance
        estradiol = self._get_lab_value(labs, ['FHt_E2', 'Estradiol'])
        progesterone = self._get_lab_value(labs, ['FHt_PROG', 'Progesterone'])
        ep_ratio = labs.get('EP_Ratio')
        
        if estradiol:
            processed['estradiol-status'] = estradiol
        if progesterone:
            processed['progesterone-low'] = progesterone < ranges['Progesterone_F']['optimal_min']
        
        # E:P ratio evaluation
        if ep_ratio:
            if ep_ratio > 10:
                processed['EP-ratio-excellent'] = True
            elif ep_ratio > 5:
                processed['EP-ratio-good'] = True
            else:
                processed['EP-ratio-poor'] = True
        
        # Menopause-related conditions
        menopause_status = self._determine_menopause_status(hhq)
        processed['menopause-status'] = menopause_status
        
        # Breast cancer history compound conditions
        if hhq.get('hh_breast_cancer'):
            processed['Quick-Breast-CA'] = True
            # Compound: Breast CA + sleep/anxiety issues
            if (hhq.get('hh_cant_stay_asleep') or hhq.get('hh_persistent_anxiety_medications')):
                processed['BreastCA-Insomnia-Anxiety'] = True
        
        return processed
    
    def _process_nutrient_markers(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process vitamin and mineral status."""
        processed = {}
        
        # Vitamin D comprehensive processing
        vit_d = self._get_lab_value(labs, ['VIT_D25', 'Vitamin D', '25OHVID'])
        if vit_d:
            if vit_d < 30:
                processed['D-deficient'] = True
            elif vit_d < 50:
                processed['D-insufficient'] = True
                processed['quick-VitD-row'] = True
            elif 50 <= vit_d <= 55:
                processed['D-50-55'] = True
            elif vit_d > 80:
                processed['D-high'] = True
            else:
                processed['D-optimal'] = True
        
        # Vitamin E
        vit_e = self._get_lab_value(labs, ['VIT_E', 'Vitamin E'])
        if vit_e:
            processed['quick-vitE'] = (vit_e < ranges['VitE']['optimal_min'] or 
                                     vit_e > ranges['VitE']['optimal_max'])
        
        # Omega fatty acids
        omega_63_ratio = self._get_lab_value(labs, ['OMEGA_6_3_RATIO', 'Omega6:3'])
        if omega_63_ratio:
            processed['omega-63-ratio-elevated'] = omega_63_ratio > ranges['Omega63Ratio']['optimal_max']
        
        # Minerals
        zinc = self._get_lab_value(labs, ['MIN_ZN', 'Zinc'])
        mg_rbc = self._get_lab_value(labs, ['MIN_MG_RBC', 'Magnesium, RBC'])
        
        if zinc:
            processed['zinc-status'] = 'low' if zinc < ranges['Zinc']['optimal_min'] else 'optimal'
        if mg_rbc:
            processed['magnesium-status'] = 'low' if mg_rbc < ranges['MgRBC']['optimal_min'] else 'optimal'
        
        return processed
    
    def _process_genetic_markers(self, labs: Dict, hhq: Dict) -> Dict:
        """Process genetic markers (APO E, MTHFR)."""
        processed = {}
        
        print(f"DEBUG: All lab keys: {list(labs.keys())}")
        
        # APO E processing - check all possible key variations
        apo_e_keys = ['APO1', 'APO2', 'apo1', 'apo2', 'APOE', 'apoe', 'APO_E', 'APO E', 
                      'APO E Genotyping Result', 'apoe_genotype', 'APOE_1', 'APOE_2']
        
        apo_e1 = None
        apo_e2 = None
        
        # Find APO E values
        for key in apo_e_keys:
            if key in labs and labs[key] is not None:
                apo_e_value = str(labs[key]).strip()
                print(f"DEBUG: Found APO E in key '{key}': {apo_e_value}")
                
                # Parse combined values like "E3/E4" or "E3,E4"
                if '/' in apo_e_value:
                    parts = apo_e_value.split('/')
                    apo_e1 = parts[0].strip()
                    apo_e2 = parts[1].strip() if len(parts) > 1 else parts[0].strip()
                elif ',' in apo_e_value:
                    parts = apo_e_value.split(',')
                    apo_e1 = parts[0].strip()
                    apo_e2 = parts[1].strip() if len(parts) > 1 else parts[0].strip()
                else:
                    # Single value or first allele
                    if not apo_e1:
                        apo_e1 = apo_e_value
                    elif not apo_e2:
                        apo_e2 = apo_e_value
                
                break  # Use first found value
        
        print(f"DEBUG: Final APO E values - apo_e1: {apo_e1}, apo_e2: {apo_e2}")
        
        # Construct the full genotype string
        if apo_e1 and apo_e2:
            # Clean up the values
            apo_e1_clean = apo_e1.replace('*', '').strip()
            apo_e2_clean = apo_e2.replace('*', '').strip()
            
            full_genotype = f"{apo_e1_clean}/{apo_e2_clean}" if apo_e1_clean != apo_e2_clean else apo_e1_clean
            processed['genome-type'] = full_genotype
            
            print(f"DEBUG: Setting genome-type to: {full_genotype}")
            
            # Determine APO E status
            if 'E4' in str(apo_e1_clean) or 'E4' in str(apo_e2_clean):
                processed['quick-E4'] = True
                if 'E4' in str(apo_e1_clean) and 'E4' in str(apo_e2_clean):
                    processed['APO-E4-homozygous'] = True
                else:
                    processed['APO-E4-heterozygous'] = True
            elif ('E3' in str(apo_e1_clean) and 'E4' in str(apo_e2_clean)) or ('E4' in str(apo_e1_clean) and 'E3' in str(apo_e2_clean)):
                processed['quick-E4E3'] = True
            else:
                processed['quick-notE4'] = True
        elif apo_e1:  # Only one value found
            apo_e1_clean = apo_e1.replace('*', '').strip()
            processed['genome-type'] = apo_e1_clean
            
            # Process single allele status (same logic as paired alleles)
            if 'E4' in str(apo_e1_clean):
                processed['quick-E4'] = True
                processed['APO-E4-heterozygous'] = True  # Assume heterozygous for single allele
            else:
                processed['quick-notE4'] = True
        else:
            processed['genome-type'] = 'Not Available'
            print("DEBUG: No APO E values found")
        
        # Glutathione value - check multiple possible keys
        glut_keys = ['METAB_GLUT', 'Glutathione', 'Total Glutathione', 'GLUTATHIONE', 'glutathione']
        glut_value = None
        
        for key in glut_keys:
            if key in labs and labs[key] is not None:
                glut_value = labs[key]
                print(f"DEBUG: Found Glutathione in key '{key}': {glut_value}")
                break
        
        if glut_value:
            processed['GLUT_VALUE'] = f"{glut_value} μg/mL"
        else:
            processed['GLUT_VALUE'] = 'Not Available'
        
        # MTHFR processing - check all possible key variations
        mthfr_keys = ['MTHFR_1', 'MTHFR_2', 'mthfr_1', 'mthfr_2', 'MTHFR C677T', 'MTHFR A1298C',
                      'C677T', 'A1298C', 'mthfr_c677t', 'mthfr_a1298c']
        
        mthfr1 = 'Not Detected'
        mthfr2 = 'Not Detected'
        
        # Look for C677T variant
        for key in ['MTHFR_1', 'mthfr_1', 'MTHFR C677T', 'C677T', 'mthfr_c677t']:
            if key in labs and labs[key] is not None:
                mthfr1 = str(labs[key]).strip()
                print(f"DEBUG: Found MTHFR C677T in key '{key}': {mthfr1}")
                break
        
        # Look for A1298C variant  
        for key in ['MTHFR_2', 'mthfr_2', 'MTHFR A1298C', 'A1298C', 'mthfr_a1298c']:
            if key in labs and labs[key] is not None:
                mthfr2 = str(labs[key]).strip()
                print(f"DEBUG: Found MTHFR A1298C in key '{key}': {mthfr2}")
                break
        
        print(f"DEBUG: Final MTHFR values - C677T: {mthfr1}, A1298C: {mthfr2}")
        
        # Set the actual MTHFR values for template replacement
        processed['MTHFR_C677T'] = mthfr1
        processed['MTHFR_A1298C'] = mthfr2
        
        # Determine if variants are present
        if mthfr1 and 'Not Detected' not in str(mthfr1).upper() and 'NOT DETECTED' not in str(mthfr1).upper():
            processed['quick-MTHFR1'] = True
        else:
            processed['quick-MTHFR1'] = False
            
        if mthfr2 and 'Not Detected' not in str(mthfr2).upper() and 'NOT DETECTED' not in str(mthfr2).upper():
            processed['quick-MTHFR2'] = True
        else:
            processed['quick-MTHFR2'] = False
        
        # Overall MTHFR variant status
        processed['has-MTHFR-variants'] = processed['quick-MTHFR1'] or processed['quick-MTHFR2']
        
        print(f"DEBUG: Final processed genetics: {processed}")
        
        return processed
    
    def _process_compound_conditions(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """Process complex compound conditions that combine multiple factors."""
        processed = {}
        
        # Snoring + BMI compound condition
        snores = hhq.get('hh_snores', False)
        # BMI would need to be calculated from height/weight if available
        # For now, approximate with sleep apnea indicators
        if snores and hhq.get('hh_partner_report_apnea'):
            processed['snoring-BMI-compound'] = True
        
        # Alcohol + homocysteine + B12 compound condition
        alcohol_use = hhq.get('hh_alcohol_4days', False) or hhq.get('hh_1to3_alcohol_week', False)
        homocysteine = self._get_lab_value(labs, ['INFLAM_HOMOCYS'])
        b12 = self._get_lab_value(labs, ['VIT_B12'])
        
        if alcohol_use and homocysteine and b12:
            if homocysteine > ranges['Homocysteine']['optimal_max'] and b12 < ranges['VitB12']['optimal_min']:
                processed['alcohol-homocys-B12-compound'] = True
        
        # Fatigue compound conditions
        chronic_fatigue = hhq.get('hh_chronic_fatigue_syndrome', False)
        if chronic_fatigue:
            processed['quick-fatigue'] = True
            # Add other fatigue-related lab markers
            thyroid_issues = processed.get('TSH-T3-rT3', False)
            if thyroid_issues:
                processed['fatigue-thyroid-compound'] = True
        
        return processed
    
    def _process_hhq_based_conditions(self, hhq: Dict, labs: Dict) -> Dict:
        """
        Process HHQ-based conditions and interactions with lab values.
        Now includes ALL extracted content controls from professional template.
        """
        processed = {}
        
        # Medical History Conditions
        processed['Quick-Breast-CA'] = hhq.get('hh_breast_cancer', False)
        processed['quick-root-canal'] = hhq.get('hh_root_canal', False)
        processed['quick-allergies'] = hhq.get('hh_chronic_allergies', False) or hhq.get('hh_seasonal_allergies', False)
        processed['quick-fatigue'] = hhq.get('hh_chronic_fatigue', False) or hhq.get('hh_fatigue', False)
        processed['quick-parkinsons'] = hhq.get('hh_diag_parkinsons', False)
        processed['quick-gallbladder'] = hhq.get('hh_gallbladder_removed', False)
        processed['quick-histamine-diet'] = hhq.get('hh_histamine_intolerance', False)
        processed['quick-mcas'] = hhq.get('hh_mast_cell_activation', False)
        processed['quick-likes-soda'] = hhq.get('hh_soda_consumption', False)
        processed['quick-depression-mood-disorder'] = hhq.get('hh_depression', False) or hhq.get('hh_anxiety_medications', False)
        
        # Sleep and Lifestyle Conditions  
        processed['quick-sleep-hormones'] = hhq.get('hh_cant_stay_asleep', False) or hhq.get('hh_sleep_medications', False)
        processed['prodrome-sleep'] = hhq.get('hh_insomnia', False) or hhq.get('hh_sleep_prescription', False)
        processed['freq-uti'] = hhq.get('hh_frequent_uti', False)
        processed['Current-Smoker'] = hhq.get('hh_current_smoker', False)
        processed['quick-crp5-etoh'] = hhq.get('hh_alcohol_consumption', False)
        
        # Female-specific conditions
        processed['quick-using-hrt'] = hhq.get('hh_hormone_replacement_therapy', False)
        processed['BreastCA-Insomnia-Anxiety'] = (hhq.get('hh_breast_cancer', False) and 
                                                 (hhq.get('hh_cant_stay_asleep', False) or 
                                                  hhq.get('hh_persistent_anxiety_medications', False)))
        
        # Cognitive and Neurological Conditions
        processed['quick-brain-fog'] = hhq.get('hh_brain_fog', False)
        processed['quick-memory-issues'] = hhq.get('hh_memory_problems', False)
        processed['quick-head-injury'] = hhq.get('hh_head_injury', False) or hhq.get('hh_concussion', False)
        processed['quick-tbi'] = hhq.get('hh_traumatic_brain_injury', False)
        
        # GI and Digestive Conditions
        processed['quick-chronic-constipation'] = hhq.get('hh_chronic_constipation', False)
        processed['quick-ibs'] = hhq.get('hh_irritable_bowel', False)
        processed['quick-gi-health'] = hhq.get('hh_digestive_issues', False)
        processed['quick-celiac'] = hhq.get('hh_celiac_disease', False)
        processed['quick-gluten-sensitivity'] = hhq.get('hh_gluten_sensitivity', False)
        
        # Autoimmune Conditions
        processed['quick-hashimotos-autoimmune'] = hhq.get('hh_hashimotos', False) or hhq.get('hh_thyroid_autoimmune', False)
        processed['quick-autoimmune-disease'] = hhq.get('hh_autoimmune_disease', False)
        processed['quick-fibromyalgia'] = hhq.get('hh_fibromyalgia', False)
        processed['quick-rheumatoid-arthritis'] = hhq.get('hh_rheumatoid_arthritis', False)
        
        # Cardiovascular Conditions
        processed['quick-heart-disease'] = hhq.get('hh_heart_disease', False)
        processed['quick-high-blood-pressure'] = hhq.get('hh_high_blood_pressure', False)
        processed['quick-stroke'] = hhq.get('hh_stroke', False) or hhq.get('hh_tia', False)
        
        # Cancer History
        processed['quick-cancer-history'] = hhq.get('hh_cancer_history', False)
        processed['quick-prostate-cancer'] = hhq.get('hh_prostate_cancer', False)
        
        # Metabolic Conditions
        processed['quick-diabetes'] = hhq.get('hh_diabetes', False) or hhq.get('hh_type_2_diabetes', False)
        processed['quick-insulin-resistance'] = hhq.get('hh_insulin_resistance', False)
        processed['quick-metabolic-syndrome'] = hhq.get('hh_metabolic_syndrome', False)
        
        # Age and Gender-specific Protocols
        processed['quick-over-50'] = hhq.get('hh_age_over_50', False)
        processed['quick-postmenopausal'] = hhq.get('hh_postmenopausal', False)
        processed['quick-perimenopausal'] = hhq.get('hh_perimenopausal', False)
        
        # Exercise and Physical Conditions
        processed['quick-sedentary'] = hhq.get('hh_sedentary_lifestyle', False)
        processed['quick-exercise-intolerance'] = hhq.get('hh_exercise_intolerance', False)
        processed['quick-muscle-weakness'] = hhq.get('hh_muscle_weakness', False)
        
        # Stress and Mental Health
        processed['quick-chronic-stress'] = hhq.get('hh_chronic_stress', False)
        processed['quick-anxiety'] = hhq.get('hh_anxiety', False)
        processed['quick-panic-attacks'] = hhq.get('hh_panic_attacks', False)
        
        # Compound Conditions - Lab + HHQ interactions
        crp = self._get_lab_value(labs, ['INFLAM_CRP', 'C-Reactive Protein'])
        omega_check = self._get_lab_value(labs, ['OMEGA_CHECK', 'OmegaCheck'])
        homocysteine = self._get_lab_value(labs, ['INFLAM_HOMOCYS', 'Homocysteine'])
        
        # Root canal + elevated CRP = compound inflammation risk
        if hhq.get('hh_root_canal', False) and crp and crp > 3.0:
            processed['root-canal-inflammation-compound'] = True
            
        # Alcohol + elevated homocysteine + low B12 = compound neurological risk  
        vit_b12 = self._get_lab_value(labs, ['VIT_B12', 'Vitamin B12'])
        if (hhq.get('hh_alcohol_consumption', False) and 
            homocysteine and homocysteine > 10.4 and 
            vit_b12 and vit_b12 < 500):
            processed['alcohol-homocysteine-b12-compound'] = True
            
        # Sleep apnea + cognitive decline compound
        if (hhq.get('hh_sleep_apnea', False) and 
            (hhq.get('hh_brain_fog', False) or hhq.get('hh_memory_problems', False))):
            processed['sleep-apnea-cognitive-compound'] = True
            
        # Diabetes + APO E4 = additive problems
        apo_e = self._get_lab_value(labs, ['APO1', 'APO E Genotyping Result'])
        if (hhq.get('hh_diabetes', False) and 
            apo_e and 'E4' in str(apo_e)):
            processed['diabetes-apo-e4-compound'] = True
            
        # Snoring + BMI >25 = compound hypoxia risk
        bmi = hhq.get('hh_bmi', 0)
        if hhq.get('hh_snoring', False) and bmi > 25:
            processed['snoring-bmi-compound'] = True
            
        return processed
    
    def _determine_menopause_status(self, hhq: Dict) -> str:
        """Determine menopause status from HHQ responses."""
        if hhq.get('hh_natural_menopause'):
            return 'natural_menopause'
        elif hhq.get('hh_perimenopause'):
            return 'perimenopause'
        elif hhq.get('hh_t_hysterectomy_before40') or hhq.get('hh_t_hysterectomy_after40'):
            return 'surgical_menopause'
        else:
            return 'premenopausal'
    
    def _get_lab_value(self, labs: Dict, possible_keys: List[str]) -> Optional[float]:
        """Get lab value by checking multiple possible key names."""
        for key in possible_keys:
            if key in labs and labs[key] is not None:
                try:
                    return float(labs[key])
                except (ValueError, TypeError):
                    continue
        return None
    
    def _calculate_homa_ir(self, glucose, insulin):
        """Calculate HOMA-IR from glucose and insulin values"""
        try:
            if glucose and insulin:
                glucose_val = float(glucose)
                insulin_val = float(insulin)
                return round((insulin_val * glucose_val) / 405, 2)
        except:
            pass
        return 'Not Available'
    
    def _add_processed_lab_results_sections(self, story, processed_content: Dict[str, Any], body_style, supplement_style):
        """Add detailed lab results sections using processed content controls"""
        
        # Vitamin D Section
        vit_d = processed_content.get('quick-VitD')
        if vit_d:
            try:
                vit_d_val = float(vit_d)
                vit_d_text = f"Your baseline Vitamin D level is {vit_d_val}."
                
                if vit_d_val >= 60:
                    vit_d_rec = "This level is close to the optimal parameters and though no additional intervention is recommended, you may want to check your VITAMIN D level a few times per year to make sure that it does not drop."
                elif vit_d_val >= 50:
                    vit_d_rec = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was 50-59, you are encouraged to supplement with 4,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                elif vit_d_val >= 40:
                    vit_d_rec = "Since your VITAMIN D was 40-49, you are encouraged to supplement with 6,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                elif vit_d_val >= 30:
                    vit_d_rec = "Since your VITAMIN D was 30-39, you are encouraged to supplement with 8,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                else:
                    vit_d_rec = "Since your VITAMIN D was < 30, you are encouraged to supplement with 10,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                
                story.append(Paragraph(vit_d_text, body_style))
                story.append(Paragraph(vit_d_rec, supplement_style))
                story.append(Spacer(1, 15))
            except:
                pass
        
        # Omega-3 Section
        omega_ratio = processed_content.get('lab-omega-6-3-ratio')
        if omega_ratio:
            try:
                omega_val = float(omega_ratio)
                omega_text = f"Your OMEGA 6:3 ratio was {omega_val}-to-1."
                
                if omega_val > 4:
                    omega_rec = """If you are not taking an OMEGA-3, consider starting a high-quality, triglyceride-based OMEGA-3 
supplement. OMEGA-3's are considered to be anti-inflammatory and often help to calm systemic inflammation. You are 
encouraged to continue a high-potency, high-quality OMEGA-3 supplements. Recommended brands include Triple 
Strength OMEGA-3 FISH OIL by Sports Research (Costco), PRO-OMEGA 2000 or ULTIMATE OMEGA 2X by Nordic 
Naturals. The maintenance dose is 3 caps per day."""
                    story.append(Paragraph(omega_text, body_style))
                    story.append(Paragraph(omega_rec, supplement_style))
                else:
                    story.append(Paragraph(omega_text + " This is within optimal range.", body_style))
                
                story.append(Spacer(1, 15))
            except:
                pass
        
        # Magnesium Section
        mag_rbc = processed_content.get('quick-MagRBC')
        if mag_rbc:
            try:
                mag_val = float(mag_rbc)
                mag_text = f"Your baseline MAGNESIUM RBC level is {mag_val}."
                
                if mag_val < 5.2:
                    mag_rec = """This level falls within the optimal parameters and no additional intervention is recommended. 
Consider starting MAGNESIUM THREONATE 2000 mg at night."""
                    story.append(Paragraph(mag_text, body_style))
                    story.append(Paragraph(mag_rec, supplement_style))
                else:
                    story.append(Paragraph(mag_text + " This is within optimal range.", body_style))
                
                story.append(Spacer(1, 15))
            except:
                pass
        
        # MTHFR Genetics Section
        mthfr_1 = processed_content.get('quick-MTHFR1', 'Not Detected')
        mthfr_2 = processed_content.get('quick-MTHFR2', 'Not Detected')
        
        if mthfr_1 != 'Not Detected' or mthfr_2 != 'Not Detected':
            mthfr_text = f"MTHFR GENETIC PROFILES: You have genetic variants - C677T: {mthfr_1}, A1298C: {mthfr_2}"
            mthfr_rec = """Consider starting a methylated B complex supplement. We recommend SUPER METHYL-SP from Apex Energetics or 
METHYLPRO. The dosing is 1 capsule/day. We also recommend METHYLPRO B-COMPLEX + 5 mg L-METHYLFOLATE."""
            
            story.append(Paragraph(mthfr_text, body_style))
            story.append(Paragraph(mthfr_rec, supplement_style))
            story.append(Spacer(1, 15))
        
        # Cholesterol Section
        cholesterol = processed_content.get('quick-cholesterol')
        if cholesterol:
            try:
                chol_val = float(cholesterol)
                chol_text = f"Your TOTAL CHOLESTEROL level was {chol_val}."
                story.append(Paragraph(chol_text, body_style))
                story.append(Spacer(1, 10))
            except:
                pass
        
        # Copper/Zinc Ratio Section
        cz_ratio = processed_content.get('quick-CZratio-14')
        if cz_ratio and cz_ratio != 'Not Available':
            cz_text = f"Your COPPER-to-ZINC RATIO is {cz_ratio}."
            if float(cz_ratio) > 1.4:
                cz_rec = "This ratio is elevated. Consider zinc supplementation and reducing copper exposure."
                story.append(Paragraph(cz_text, body_style))
                story.append(Paragraph(cz_rec, supplement_style))
            else:
                story.append(Paragraph(cz_text + " This is within optimal range.", body_style))
            story.append(Spacer(1, 15))
        
        return story
    
    def _image_exists(self, category: str, image_name: str) -> bool:
        """Check if an image file exists."""
        if category in self.visual_assets and image_name in self.visual_assets[category]:
            return os.path.exists(self.visual_assets[category][image_name])
        return False
    
    def _get_supplement_image(self, supplement_name: str) -> Optional[str]:
        """Get the image path for a supplement based on its name."""
        supp_lower = supplement_name.lower()
        
        if 'vitamin d' in supp_lower and self._image_exists('supplements', 'vitamin_d'):
            return self.visual_assets['supplements']['vitamin_d']
        elif 'omega' in supp_lower and self._image_exists('supplements', 'omega3'):
            return self.visual_assets['supplements']['omega3']
        elif 'magnesium' in supp_lower and self._image_exists('supplements', 'magnesium'):
            return self.visual_assets['supplements']['magnesium']
        elif 'b-complex' in supp_lower or 'methylated' in supp_lower and self._image_exists('supplements', 'b_complex'):
            return self.visual_assets['supplements']['b_complex']
        
        return None
    
    def _get_key_lab_findings(self, lab_results: Dict[str, Any]) -> List[str]:
        """Extract key lab findings for summary."""
        findings = []
        
        # Vitamin D
        vit_d = lab_results.get('VIT_D25', 0)
        if vit_d:
            if vit_d < 30:
                findings.append(f"Vitamin D is low at {vit_d} ng/mL (optimal: >50)")
            elif vit_d < 50:
                findings.append(f"Vitamin D is suboptimal at {vit_d} ng/mL (optimal: >50)")
            else:
                findings.append(f"Vitamin D is optimal at {vit_d} ng/mL")
        
        # Omega ratio
        omega_ratio = lab_results.get('OMEGA_6_3_RATIO', 0)
        if omega_ratio and omega_ratio > 4:
            findings.append(f"Omega-6:3 ratio is elevated at {omega_ratio}:1 (optimal: <4:1)")
        
        # Magnesium
        mg_rbc = lab_results.get('MIN_MG_RBC', 0)
        if mg_rbc and mg_rbc < 5.2:
            findings.append(f"Magnesium RBC is low at {mg_rbc} mg/dL (optimal: >5.2)")
        
        # Homocysteine
        homocysteine = lab_results.get('INFLAM_HOMOCYS', 0)
        if homocysteine and homocysteine > 10:
            findings.append(f"Homocysteine is elevated at {homocysteine} μmol/L (optimal: <10)")
        
        # B12
        b12 = lab_results.get('VIT_B12', 0)
        if b12 and b12 < 500:
            findings.append(f"Vitamin B12 is suboptimal at {b12} pg/mL (optimal: >500)")
        
        return findings
    
    def _get_genetic_recommendations(self, apo_e: str) -> List[str]:
        """Get recommendations based on APO E genotype."""
        recommendations = []
        
        if 'E4' in apo_e:
            recommendations.extend([
                "Prioritize omega-3 supplementation for brain health",
                "Consider curcumin for neuroprotection",
                "Emphasize regular cardiovascular exercise",
                "Monitor cognitive function regularly"
            ])
        else:
            recommendations.extend([
                "Standard omega-3 supplementation",
                "Focus on overall brain health optimization"
            ])
        
        return recommendations

    def _process_advanced_protocols(self, labs: Dict, hhq: Dict, ranges: Dict) -> Dict:
        """
        Process advanced hormone and supplement protocols from professional template.
        Includes pregnenolone, DHEA, cortisol, and specialized supplement considerations.
        """
        processed = {}
        
        # Pregnenolone Protocols
        pregnenolone = self._get_lab_value(labs, ['NEURO_PREG', 'Pregnenolone'])
        if pregnenolone:
            if pregnenolone >= 150 and pregnenolone <= 200:
                processed['quick-pregnenolone-101'] = True  # Optimal range
            elif pregnenolone < 150:
                processed['quick-prog-50-100'] = True  # Needs supplementation
                if pregnenolone < 100:
                    processed['quick-prog-50'] = True  # Higher dose needed
            processed['quick-pregnenolone-lab-value'] = str(pregnenolone)
        
        # DHEA-S Advanced Protocols  
        dheas = self._get_lab_value(labs, ['NEURO_DHEAS', 'DHEA-Sulfate'])
        vit_d = self._get_lab_value(labs, ['VIT_D25', 'Vitamin D'])
        
        if dheas:
            processed['quick-dhea-lab-value'] = str(dheas)
            
            # Gender-specific DHEA ranges
            gender = hhq.get('gender', '').lower()
            if gender == 'male':
                if dheas >= 200 and dheas <= 250:
                    processed['quick-dhea-151'] = True  # Optimal for men
                elif dheas < 150:
                    processed['quick-dhea-150'] = True  # Low, needs supplementation
                elif dheas >= 200 and dheas <= 249:
                    processed['quick-dhea-200-249'] = True  # Good range
            else:  # Female
                if dheas >= 150 and dheas <= 200:
                    processed['quick-dhea-151'] = True  # Optimal for women
                elif dheas < 150:
                    processed['quick-dhea-150'] = True  # Low, needs supplementation
                    
            # DHEA + Cardiovascular Disease compound
            if dheas < 150:
                processed['quick-dhea-asvd'] = True  # Low DHEA = higher CAD risk
                
            # DHEA + Prostate Cancer History
            if hhq.get('hh_prostate_cancer', False) and dheas < 150:
                processed['quick-dhea-lupron'] = True  # Special consideration needed
        
        # Cortisol Support Protocols
        cortisol = self._get_lab_value(labs, ['SPEC_CORTISOL', 'Cortisol'])
        if cortisol:
            processed['quick-cortisol-lab-value'] = str(cortisol)
            if cortisol >= 15:
                processed['cortisol-5'] = True  # Optimal range
            else:
                processed['quick-cortisol-15'] = True  # Low, needs support
                
        # Thyroid Advanced Protocols
        tsh = self._get_lab_value(labs, ['THY_TSH', 'TSH'])
        free_t3 = self._get_lab_value(labs, ['THY_T3F', 'Free T3'])
        reverse_t3 = self._get_lab_value(labs, ['THY_RT3', 'Reverse T3'])
        
        # Complex thyroid function assessment
        if tsh and free_t3 and reverse_t3:
            if tsh > 2.5 and free_t3 < 3.2 and reverse_t3 > 20:
                processed['TSH-T3-rT3'] = True  # Complex thyroid dysfunction
                processed['quick-reverse-t3-elevated'] = True
                
        # Reverse T3 specific protocols
        if reverse_t3:
            if reverse_t3 > 20:
                processed['quick-reverse-t3-elevated'] = True
                processed['reverse-t3-free-t3-value'] = str(reverse_t3)
                
        # Autoimmune thyroid considerations
        if hhq.get('hh_hashimotos', False) or hhq.get('hh_thyroid_autoimmune', False):
            processed['quick-hashimotos-autoimmune'] = True
            
        # Vitamin Support Protocols
        vit_e = self._get_lab_value(labs, ['VIT_E', 'Vitamin E'])
        if vit_e:
            if vit_e < 5.5:
                processed['quick-vitE'] = True  # Low vitamin E
                
        # Male Hormone Advanced Protocols
        if hhq.get('gender', '').lower() == 'male':
            test_total = self._get_lab_value(labs, ['MHt_TEST_TOT', 'Testosterone'])
            test_free = self._get_lab_value(labs, ['MHt_TEST_FREE', 'Free Testosterone'])
            shbg = self._get_lab_value(labs, ['MHt_SHBG', 'SHBG'])
            
            if test_total:
                processed['mh1-tt-lab-value'] = str(test_total)
            if test_free:
                processed['mh1-free-t-lab-value'] = str(test_free)
            if shbg:
                processed['mh1-shbg-lab-value'] = str(shbg)
                if shbg > 45:
                    processed['quick-male-hormones-shbg'] = True  # Elevated SHBG
                    
            # Sleep + hormone optimization compound
            if (hhq.get('hh_cant_stay_asleep', False) and 
                test_free and test_free < 12):
                processed['quick-sleep-hormones'] = True
                
            # ZMA and prostate health protocols
            if test_free and test_free < 12:
                processed['zma-testosterone-support'] = True
                processed['quick-men-prostate-health'] = True
                
        # Female Hormone Advanced Protocols  
        if hhq.get('gender', '').lower() == 'female':
            estradiol = self._get_lab_value(labs, ['FHt_E2', 'Estradiol'])
            progesterone = self._get_lab_value(labs, ['FHt_PROG', 'Progesterone'])
            fsh = self._get_lab_value(labs, ['FHt_FSH', 'FSH'])
            
            if fsh:
                processed['lab-fsh-result-value'] = str(fsh)
            if estradiol:
                processed['lab-progesterone-female-value'] = str(estradiol)  # Note: template uses this for E2
            if progesterone:
                processed['lab-testosterone-female-value'] = str(progesterone)  # Note: template mixing
                
            # ReCODE PM Probiotic protocol
            if (hhq.get('hh_digestive_issues', False) or 
                hhq.get('hh_chronic_constipation', False)):
                processed['recode-pm-daily-probiotic'] = True
                
            # ATP Fuel optimization
            if hhq.get('hh_chronic_fatigue', False):
                processed['atp-fuel-supplement'] = True
                
        # Advanced Supplement Protocols
        
        # MK-7 (Mesaquinone) for cardiovascular support
        if hhq.get('hh_heart_disease', False) or hhq.get('hh_high_blood_pressure', False):
            processed['mk2-cardiovascular-support'] = True
            processed['quick-mk2-protocol'] = True
            
        # Statin interactions
        if hhq.get('hh_takes_statin', False):
            processed['statin-takes-statin'] = True
            processed['quick-takes-statin'] = True
            
        # Triglyceride/Plasmalogen assessment
        triglycerides = self._get_lab_value(labs, ['LIPID_TRIG', 'Triglycerides'])
        if triglycerides and triglycerides < 70:
            processed['trig-plasmalogens'] = True  # Extremely low triglycerides
            processed['prodrome-scan'] = True  # Consider Prodrome scan
            
        # CAC Score protocols
        if hhq.get('hh_cac_score_done', False):
            cac_score = hhq.get('hh_cac_score_value', 0)
            if cac_score == 0:
                processed['quick-CAC'] = True  # No calcification
            elif cac_score > 100:
                processed['cac-score-high'] = True  # Significant calcification
                
        return processed

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
        'CBC_RBC': 4.5,
        'CBC_HGB': 15.0,
        'CBC_HCT': 45.0,
        'CBC_MCV': 80.0,
        'CBC_PLT': 450000,
        'CBC_NEUT_ABS': 2.0,
        'CBC_LYMPH_ABS': 1.5,
        'CHEM_GLU': 100,
        'CHEM_BUN': 20,
        'CHEM_CREAT': 1.2,
        'CHEM_EGFR': 120,
        'CHEM_NA': 140,
        'CHEM_K': 5.0,
        'CHEM_CL': 105,
        'CHEM_CA': 8.5,
        'LFT_ALB': 4.0,
        'LFT_ALT': 25,
        'LFT_AST': 20,
        'LFT_ALKP': 120,
        'LFT_TBILI': 0.5,
        'LIPID_CHOL': 200,
        'LIPID_TRIG': 120,
        'LIPID_HDL': 60,
        'LIPID_LDL': 120,
        'FHt_FSH': 76.1,
        'FHt_E2': 30,
        'FHt_PROG': 0.5,
        'FHt_TEST': 5.0,
        'MHt_TEST_TOT': 5.0,
        'MHt_TEST_FREE': 0.5,
        'MHt_PSA': 2.0,
        'THY_TSH': 2.5,
        'THY_T3F': 0.5,
        'THY_T4F': 1.0,
        'THY_TGAB': 0.5,
        'NEURO_PREG': 0.5,
        'NEURO_DHEAS': 0.5,
        'VIT_D25': 73.2,
        'VIT_B12': 500,
        'VIT_E': 15.0,
        'MIN_ZN': 100,
        'MIN_CU': 15,
        'MIN_SE': 1.5,
        'MIN_MG_RBC': 5.2,
        'INFLAM_CRP': 2.0,
        'INFLAM_URIC': 5.0,
        'INFLAM_HOMOCYS': 10,
        'METAB_INS': 10,
        'METAB_HBA1C': 5.5,
        'METAB_GLUT': 222,
        'OMEGA_CHECK': 100,
        'OMEGA_6_3_RATIO': 4.9,
        'OMEGA_3_TOT': 100,
        'OMEGA_6_TOT': 100,
        'OMEGA_AA': 0.5,
        'OMEGA_AA_EPA': 0.5,
        'APO1': 'E2/E4',
        'APO2': 'E2/E4',
        'MTHFR_1': 'Not Detected',
        'MTHFR_2': 'Not Detected'
    }
    
    try:
        roadmap = generator.generate_roadmap(sample_client_data, sample_lab_results)
        print("Roadmap generated successfully!")
        print(f"Length: {len(roadmap)} characters")
    except Exception as e:
        print(f"Error generating roadmap: {str(e)}") 