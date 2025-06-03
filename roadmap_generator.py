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
from risk_factor_mapping import RiskFactorMapper

# Import configuration classes
from config.lab_mappings import LAB_MAPPINGS
from config.lab_ranges import LabRanges
from config.assets import AssetConfig

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
        
        # Initialize configuration objects
        self.asset_config = AssetConfig()
        self.lab_mappings = LAB_MAPPINGS
        
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
        
        # 6. Remove empty sections that have no applicable content
        roadmap = self._remove_empty_sections(roadmap)
        
        # 7. Clean up any remaining placeholders and improve formatting
        roadmap = self._cleanup_placeholders(roadmap)
        
        return roadmap
    
    def _remove_empty_sections(self, roadmap: str) -> str:
        """Remove sections that are empty or have no content."""
        # For now, just return the roadmap as-is
        # This can be enhanced later if needed
        return roadmap
    
    def _apply_content_controls_to_template(self, roadmap: str, processed_content: Dict[str, Any]) -> str:
        """
        Apply all processed content controls to the roadmap template.
        This replaces content control placeholders with appropriate content or removes them.
        """
        # FIRST: Handle special MTHFR placeholders before general processing
        if 'MTHFR_C677T' in processed_content and 'MTHFR_A1298C' in processed_content:
            mthfr_c677t = processed_content['MTHFR_C677T']
            mthfr_a1298c = processed_content['MTHFR_A1298C']
            
            # Replace the literal placeholder text with variant names
            roadmap = roadmap.replace('{{MTHFR_C677T}}', 'C677T')
            roadmap = roadmap.replace('{{MTHFR_A1298C}}', 'A1298C')
            
            print(f"DEBUG: MTHFR placeholder replacement. C677T: {mthfr_c677t}, A1298C: {mthfr_a1298c}")
        
        # THEN: Process all other content controls
        for control_name, control_value in processed_content.items():
            # Skip MTHFR placeholders as they're handled above
            if control_name in ['MTHFR_C677T', 'MTHFR_A1298C']:
                continue
                
            # Escape special regex characters in control name
            escaped_control_name = re.escape(control_name)
                
            # Handle regular conditional blocks: {{#control_name}}content{{/control_name}}
            block_pattern = f"{{{{#{escaped_control_name}}}}}(.*?){{{{/{escaped_control_name}}}}}"
            
            # Handle inverted conditional blocks: {{^control_name}}content{{/control_name}}
            inverted_block_pattern = f"{{{{\\^{escaped_control_name}}}}}(.*?){{{{/{escaped_control_name}}}}}"
            
            if isinstance(control_value, bool):
                if control_value:
                    # Show regular conditional content, hide inverted conditional content
                    def replace_block(match):
                        return match.group(1)  # Return just the content without the markers
                    roadmap = re.sub(block_pattern, replace_block, roadmap, flags=re.DOTALL)
                    # Remove inverted conditional blocks (since condition is true)
                    roadmap = re.sub(inverted_block_pattern, "", roadmap, flags=re.DOTALL)
                else:
                    # Hide regular conditional content, show inverted conditional content
                    roadmap = re.sub(block_pattern, "", roadmap, flags=re.DOTALL)
                    # Show inverted conditional content
                    def replace_inverted_block(match):
                        return match.group(1)  # Return just the content without the markers
                    roadmap = re.sub(inverted_block_pattern, replace_inverted_block, roadmap, flags=re.DOTALL)
            
            # Handle simple placeholders: {{control_name}}
            placeholder = f"{{{{{control_name}}}}}"
            if isinstance(control_value, (str, int, float)):
                # Replace with the actual value
                roadmap = roadmap.replace(placeholder, str(control_value))
            else:
                # For complex values, convert to string or remove if empty
                roadmap = roadmap.replace(placeholder, str(control_value) if control_value else "")
        
        # Remove the old MTHFR processing logic that was below
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
        
        # Handle Handlebars-style placeholders
        firstname = client_data.get('firstname', client_data.get('name', 'Patient'))
        roadmap = roadmap.replace('{{firstname}}', firstname)
        
        # Handle today's date
        today = client_data.get('today', datetime.now().strftime('%B %d, %Y'))
        roadmap = roadmap.replace('{{today}}', today)
        
        # Handle lab date
        lab_date = client_data.get('lab-date', client_data.get('labs_date', 'your recent labs'))
        roadmap = roadmap.replace('{{lab-date}}', lab_date)
        
        # Legacy replacements (keep for backward compatibility)
        name = client_data.get('name', firstname)
        roadmap = roadmap.replace('_______', name)  # Main name placeholder
        roadmap = roadmap.replace('___________', name)  # Secondary name placeholder
        roadmap = roadmap.replace('Dear _-', f'Dear {name},')
        
        # Date replacements (legacy)
        report_date = datetime.now().strftime('%B %d, %Y')
        roadmap = roadmap.replace('Report Date: _', f'Report Date: {report_date}')
        roadmap = roadmap.replace('Report Date: __', f'Report Date: {report_date}')
        
        # Labs drawn date (legacy)
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
        """Clean up remaining placeholders and improve formatting for better readability."""
        
        # Remove any remaining placeholder patterns
        roadmap = re.sub(r'\{\{[^}]*\}\}', '', roadmap)
        roadmap = re.sub(r'\{[^}]*\}', '', roadmap)
        
        # Clean up excessive whitespace and empty lines
        # Remove multiple consecutive empty lines (more than 2)
        roadmap = re.sub(r'\n\s*\n\s*\n+', '\n\n', roadmap)
        
        # Remove trailing whitespace from lines
        roadmap = re.sub(r'[ \t]+$', '', roadmap, flags=re.MULTILINE)
        
        # Clean up section breaks with too much spacing
        roadmap = re.sub(r'\n\s*---\s*\n\s*\n+', '\n\n---\n\n', roadmap)
        
        # Remove empty sections (lines with just whitespace between headers)
        roadmap = re.sub(r'(##.*?\n)\s*\n\s*\n(##)', r'\1\n\2', roadmap)
        
        # Clean up bullet points with excessive spacing
        roadmap = re.sub(r'\n\s*\n\s*-\s', '\n- ', roadmap)
        
        # Remove sections that are just headers with no content
        roadmap = re.sub(r'##\s*\*\*[^*]+\*\*\s*\n\s*\n\s*(?=##|\Z)', '', roadmap)
        
        # Clean up "Consider the following:" with no following content
        roadmap = re.sub(r'Consider the following:\s*\n\s*\n\s*(?=-|##|\Z)', '', roadmap)
        
        # Remove excessive spacing around bullet points
        roadmap = re.sub(r'\n\n\n+(-\s)', r'\n\n\1', roadmap)
        
        # Clean up spacing before section dividers
        roadmap = re.sub(r'\n\s*\n\s*\n+---', '\n\n---', roadmap)
        
        # Final cleanup: ensure consistent section spacing
        roadmap = re.sub(r'\n{4,}', '\n\n\n', roadmap)
        
        return roadmap.strip()
    
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
                logo = RLImage(self.asset_config.get_asset_path('logos', 'main_logo'), width=1.5*inch, height=0.75*inch)
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
        processed['BariSurg'] = hhq.get('hh_bariatric_surgery', False)
        processed['quick-histamine-diet'] = hhq.get('hh_histamine_intolerance', False)
        processed['quick-mcas'] = hhq.get('hh_mast_cell_activation', False)
        processed['quick-likes-soda'] = hhq.get('hh_soda_consumption', False)
        processed['quick-depression-mood-disorder'] = hhq.get('hh_depression', False) or hhq.get('hh_anxiety_medications', False)
        
        # Supplement and substance history
        processed['quick-taking-NAC'] = hhq.get('hh_taking_nac', False) or hhq.get('hh_supplement_nac', False)
        processed['quick-ETOH-WD'] = hhq.get('hh_alcohol_withdrawal', False) or hhq.get('hh_etoh_withdrawal', False)
        processed['Quick-krill'] = hhq.get('hh_taking_krill_oil', False) or hhq.get('hh_supplement_krill', False) or hhq.get('hh_krill_oil', False)
        processed['Quick-Thinner'] = hhq.get('hh_blood_thinner', False) or hhq.get('hh_anticoagulant', False) or hhq.get('hh_warfarin', False) or hhq.get('hh_coumadin', False)
        
        # Diet and metabolic lifestyle conditions
        processed['quick-likes-sugar'] = hhq.get('hh_likes_sugar', False) or hhq.get('hh_sugar_consumption', False) or hhq.get('hh_high_sugar_diet', False)
        processed['quick-likes-soda'] = hhq.get('hh_likes_soda', False) or hhq.get('hh_soda_consumption', False) or hhq.get('hh_drinks_soda', False)
        
        # APO E4 + sugar combination condition
        apo_e = labs.get('APO1') or labs.get('APO E Genotyping Result')
        has_apo_e4 = apo_e and 'E4' in str(apo_e)
        if has_apo_e4 and processed.get('quick-likes-sugar', False):
            processed['quick-sugars-APOE4'] = True
            
        # Ketone supplementation support (could be based on various factors)
        has_metabolic_dysfunction = (
            hhq.get('hh_diabetes', False) or 
            hhq.get('hh_insulin_resistance', False) or
            hhq.get('hh_brain_fog', False) or
            has_apo_e4
        )
        if has_metabolic_dysfunction:
            processed['ketone-supplement-support'] = True
        
        # Celiac and autoimmune diet conditions
        processed['Celiac'] = hhq.get('hh_celiac_disease', False)
        processed['quick-celiac'] = hhq.get('hh_celiac_disease', False)
        processed['quick-gluten-sensitivity'] = hhq.get('hh_gluten_sensitivity', False)
        
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
        
        # Allergy and Immune System Conditions
        processed['quick-allergies'] = hhq.get('hh_chronic_allergies', False) or hhq.get('hh_seasonal_allergies', False)
        processed['Quick-Allergies'] = hhq.get('hh_chronic_allergies', False) or hhq.get('hh_seasonal_allergies', False)
        
        # Histamine intolerance condition - triggered by chronic allergies + alcohol consumption
        has_chronic_allergies = hhq.get('hh_chronic_allergies', False) or hhq.get('hh_seasonal_allergies', False)
        has_alcohol_consumption = hhq.get('hh_alcohol_consumption', False) or hhq.get('hh_drinks_alcohol', False)
        if has_chronic_allergies and has_alcohol_consumption:
            processed['Quick-Histamine-Diet'] = True
        elif hhq.get('hh_histamine_intolerance', False):
            processed['Quick-Histamine-Diet'] = True
            
        # MCAS condition - triggered by GI headaches + chronic allergies or explicit MCAS history
        has_gi_headaches = hhq.get('hh_gi_headaches', False) or hhq.get('hh_headaches', False)
        if (has_gi_headaches and has_chronic_allergies) or hhq.get('hh_mast_cell_activation', False):
            processed['quick-MCAS'] = True
        
        # Cardiovascular Conditions
        processed['quick-heart-disease'] = hhq.get('hh_heart_disease', False)
        processed['quick-high-blood-pressure'] = hhq.get('hh_high_blood_pressure', False)
        processed['quick-stroke'] = hhq.get('hh_stroke', False) or hhq.get('hh_tia', False)
        
        # Cardiovascular Risk Factors and Interventions
        processed['Current-Smoker'] = hhq.get('hh_current_smoker', False) or hhq.get('hh_smoker', False)
        processed['HxHTN'] = hhq.get('hh_high_blood_pressure', False) or hhq.get('hh_hypertension', False) or hhq.get('hh_elevated_blood_pressure', False)
        processed['quick-takes-statin'] = hhq.get('hh_takes_statin', False) or hhq.get('hh_statin_medication', False) or hhq.get('hh_cholesterol_medication', False)
        
        # Advanced Cardiovascular Risk Assessment
        # Elevated platelets + multiple risk factors = D-DIMER/LEIDEN FACTOR V testing
        platelets = self._get_lab_value(labs, ['CBC_PLT', 'Platelets'])
        apo_e = labs.get('APO1') or labs.get('APO E Genotyping Result')
        has_apo_e4 = apo_e and 'E4' in str(apo_e)
        
        # Assess metabolic health status
        glucose = self._get_lab_value(labs, ['CHEM_GLU', 'Glucose'])
        insulin = self._get_lab_value(labs, ['METAB_INS', 'Insulin'])
        hba1c = self._get_lab_value(labs, ['METAB_HBA1C', 'Hemoglobin A1c'])
        has_metabolic_dysfunction = (
            (glucose and glucose > 100) or
            (insulin and insulin > 7) or
            (hba1c and hba1c > 5.6) or
            hhq.get('hh_diabetes', False) or
            hhq.get('hh_insulin_resistance', False)
        )
        
        # Compound risk assessment for clotting disorders
        if (platelets and platelets > 400 and  # Elevated platelets
            has_apo_e4 and  # APO E4 genetics
            has_metabolic_dysfunction and  # Metabolic health concerns
            hhq.get('hh_cognitive_decline_concerns', False)):  # Cognitive decline concerns
            processed['elevated-platelets-cardiovascular-risk'] = True
        
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
        
        # ================================
        # NOOTROPICS AND BRAIN HEALTH CONDITIONS
        # ================================
        
        # Basic Nootropic Conditions
        # Choline supplement recommendation - general cognitive support
        has_cognitive_risk = (
            hhq.get('hh_brain_fog', False) or
            hhq.get('hh_memory_problems', False) or
            hhq.get('hh_cognitive_decline_concerns', False) or
            has_apo_e4 or
            hhq.get('hh_attention_problems', False) or
            hhq.get('hh_concentration_issues', False)
        )
        if has_cognitive_risk:
            processed['quick-nootropic-choline'] = True
            
        # Lion's Mane for cognitive enhancement
        if has_cognitive_risk or hhq.get('hh_wants_cognitive_enhancement', False):
            processed['quick-nootropic-lionsmane'] = True
            
        # Focus supplement recommendations for those already taking focus supplements
        if (hhq.get('hh_taking_focus_supplement', False) or 
            hhq.get('hh_taking_brain_supplement', False) or
            hhq.get('hh_taking_nootropics', False)):
            processed['quick-focus-supp'] = True
            
        # Sleep Apnea & Prescription Nootropics
        # MODAFINIL/PROVIGIL for CPAP/BIPAP users with cognitive concerns OR TBI patients
        uses_cpap = (hhq.get('hh_sleep_apnea', False) or 
                    hhq.get('hh_uses_cpap', False) or 
                    hhq.get('hh_uses_bipap', False))
        has_tbi = (hhq.get('hh_head_injury', False) or 
                  hhq.get('hh_concussion', False) or 
                  hhq.get('hh_traumatic_brain_injury', False) or
                  hhq.get('hh_tbi', False))
        if (uses_cpap or has_tbi) and has_cognitive_risk:
            processed['Quick-Modafinil'] = True
            
        # Brain Injury & Specialized Protocols
        # BRAIN RESCUE III for brain injury history
        has_brain_injury = (hhq.get('hh_head_injury', False) or 
                          hhq.get('hh_concussion', False) or 
                          hhq.get('hh_traumatic_brain_injury', False) or
                          hhq.get('hh_tbi', False) or
                          hhq.get('hh_brain_injury', False))
        if has_brain_injury:
            processed['brain-rescue-iii'] = True
            
        # Surgery-Weight Loss & Malabsorption
        # BRAIN RESCUE III for bariatric surgery patients with malabsorption
        if hhq.get('hh_bariatric_surgery', False):
            processed['Surg-Weight-loss'] = True
            
        # Omega-3 Optimization for Current Users
        # Upgrade recommendations for those taking omega-3
        if (hhq.get('hh_taking_omega3', False) or 
            hhq.get('hh_taking_fish_oil', False) or
            hhq.get('hh_omega3_supplement', False)):
            processed['Quick-Omega-3'] = True
            
        # Gut-specific omega-3 for GI issues
        has_gi_issues = (hhq.get('hh_digestive_issues', False) or
                        hhq.get('hh_irritable_bowel', False) or
                        hhq.get('hh_chronic_constipation', False) or
                        hhq.get('hh_leaky_gut', False))
        if has_gi_issues:
            processed['MegaOmega'] = True
            
        # Immune System & Viral Support
        # HSV (Herpes Simplex Virus) support
        if (hhq.get('hh_cold_sores', False) or 
            hhq.get('hh_herpes_simplex', False) or
            hhq.get('hh_hsv', False)):
            processed['quick-HSV'] = True
            
        # EBV (Epstein-Barr Virus) support  
        if (hhq.get('hh_epstein_barr', False) or 
            hhq.get('hh_ebv', False) or
            hhq.get('hh_chronic_fatigue_virus', False)):
            processed['quick-EBV'] = True
            
        # Parkinson's Disease Support
        # TRU NIAGEN/NAD+ support for Parkinson's
        if hhq.get('hh_diag_parkinsons', False):
            processed['quick-parkinsons'] = True
            
        # Arthritis & Inflammation Support
        # THERACURMIN HP for arthritic symptoms
        if (hhq.get('hh_arthritis', False) or 
            hhq.get('hh_joint_pain', False) or
            hhq.get('hh_rheumatoid_arthritis', False) or
            hhq.get('hh_osteoarthritis', False)):
            processed['Thercumin'] = True
            
        # Vinpocetine for cerebral blood flow
        # Triggered by circulation issues, memory problems, or high blood pressure
        has_circulation_issues = (hhq.get('hh_circulation_problems', False) or
                                hhq.get('hh_high_blood_pressure', False) or
                                hhq.get('hh_memory_problems', False) or
                                hhq.get('hh_brain_fog', False))
        if has_circulation_issues:
            processed['vinpocetine'] = True
            
        # Current Supplement Integration
        # ATP FUEL supplement (client currently taking)
        if hhq.get('hh_taking_atp_fuel', False):
            processed['atp-fuel-supplement'] = True
            
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
        apo_e = labs.get('APO1') or labs.get('APO E Genotyping Result')
        if (hhq.get('hh_diabetes', False) and 
            apo_e and 'E4' in str(apo_e)):
            processed['diabetes-apo-e4-compound'] = True
            
        # Snoring + BMI >25 = compound hypoxia risk
        bmi = hhq.get('hh_bmi', 0)
        if hhq.get('hh_snoring', False) and bmi > 25:
            processed['snoring-bmi-compound'] = True
            
        # CRP + low Omega-3 = compound inflammation risk
        # CRP >0.9 + OmegaCheck <5.4 = elevated inflammation with poor omega status  
        if crp and omega_check:
            if crp > 0.9 and omega_check < 5.4:
                processed['quick-CRP-09-omega-<5'] = True
        
        # Concussion/TBI + very low Omega 6:3 ratio = OMEGA-3 CHALLENGE
        # History of concussion/TBI OR very low omega 6:3 index justifies OMEGA-3 CHALLENGE
        omega_63_ratio = self._get_lab_value(labs, ['OMEGA_6_3_RATIO', 'Omega-6/Omega-3 Ratio'])
        has_head_injury = (hhq.get('hh_head_injury', False) or 
                          hhq.get('hh_concussion', False) or 
                          hhq.get('hh_traumatic_brain_injury', False) or
                          hhq.get('hh_tbi', False))
        
        if has_head_injury or (omega_63_ratio and omega_63_ratio > 10):  # Very elevated ratio
            processed['checked-omega-63-ratio'] = True
        
        # Neurological omega-3 optimization = suboptimal omega-3 for brain health
        # Triggers when OmegaCheck is low OR has neurological symptoms/conditions
        has_neurological_symptoms = (hhq.get('hh_brain_fog', False) or 
                                    hhq.get('hh_memory_problems', False) or
                                    hhq.get('hh_cognitive_decline', False) or
                                    has_head_injury)
        
        if (omega_check and omega_check < 6.0) or has_neurological_symptoms:
            processed['omega-neurological-suboptimal'] = True
        
        # Taking omega-3 but still suboptimal = need to upgrade/increase dosing
        # Client IS taking omega-3 supplements BUT omega 6:3 ratio still >4:1
        taking_omega3 = (hhq.get('hh_taking_omega3', False) or 
                        hhq.get('hh_taking_fish_oil', False) or
                        hhq.get('hh_omega3_supplement', False) or
                        hhq.get('hh_fish_oil_supplement', False))
        
        if taking_omega3 and omega_63_ratio and omega_63_ratio > 4.0:
            processed['Taking-an-OMEGA'] = True
        
        # ================================
        # COMPREHENSIVE THYROID FUNCTION CONDITIONS
        # ================================
        
        # Get thyroid lab values
        tsh = self._get_lab_value(labs, ['THY_TSH', 'TSH'])
        free_t3 = self._get_lab_value(labs, ['THY_T3F', 'Triiodothyronine (T3), Free'])
        free_t4 = self._get_lab_value(labs, ['THY_T4F', 'T4, Free (Direct)'])
        reverse_t3 = self._get_lab_value(labs, ['RT3', 'Reverse T3'])
        tpo_antibody = self._get_lab_value(labs, ['THY_TPOAB', 'Thyroid Peroxidase (TPO) Ab'])
        tg_antibody = self._get_lab_value(labs, ['THY_TGAB', 'Thyroglobulin Antibody'])
        
        # Set up basic thyroid markers for display
        if tsh is not None:
            processed['quick-TSH'] = f"{tsh:.2f}"
        if free_t3 is not None:
            processed['quick-FT3'] = f"{free_t3:.2f}"
        if free_t4 is not None:
            processed['quick-FT4'] = f"{free_t4:.2f}"
        if reverse_t3 is not None:
            processed['quick-rT3'] = f"{reverse_t3:.1f}"
        if tpo_antibody is not None:
            processed['quick-TPO'] = f"{tpo_antibody:.0f}"
        if tg_antibody is not None:
            processed['quick-tg-ab'] = f"{tg_antibody:.1f}"
        
        # Thyroid row condition - shows detailed thyroid panel when any thyroid markers are available
        if any([reverse_t3, tpo_antibody, tg_antibody]):
            processed['thyroid-row'] = True
        
        # Optimal thyroid function
        # All markers within optimal ranges: TSH 0.4-2.5, Free T3 3.2-4.2, Free T4 1.3-1.8, rT3 <15, TPO <34, TgAb <1
        thyroid_optimal = True
        thyroid_has_dysfunction = False
        
        if tsh is not None and (tsh < 0.4 or tsh > 2.5):
            thyroid_optimal = False
            thyroid_has_dysfunction = True
        if free_t3 is not None and (free_t3 < 3.2 or free_t3 > 4.2):
            thyroid_optimal = False
            thyroid_has_dysfunction = True
        if free_t4 is not None and (free_t4 < 1.3 or free_t4 > 1.8):
            thyroid_optimal = False
            thyroid_has_dysfunction = True
        if reverse_t3 is not None and reverse_t3 > 15:
            thyroid_optimal = False
            thyroid_has_dysfunction = True
        if tpo_antibody is not None and tpo_antibody > 34:
            thyroid_optimal = False
            thyroid_has_dysfunction = True
        if tg_antibody is not None and tg_antibody > 1:
            thyroid_optimal = False
            thyroid_has_dysfunction = True
            
        # Only trigger optimal if truly optimal AND we have thyroid data
        if thyroid_optimal and any([tsh, free_t3, free_t4]) and not thyroid_has_dysfunction:
            processed['thyroid-optimal'] = True
        else:
            # Explicitly set to False when there's dysfunction to prevent optimal message
            processed['thyroid-optimal'] = False
        
        # High TSH (obvious hypothyroidism)
        if tsh is not None and tsh > 7:
            processed['quick-TSH>7'] = True
        else:
            # Explicitly set to False when TSH is not >7
            processed['quick-TSH>7'] = False
        
        # Low TSH scenarios - opportunity to optimize (only if not severely high)
        if tsh is not None and tsh > 2.5 and tsh <= 7:
            processed['low-TSH'] = True
        
        # High thyroid - TSH exceeds optimal + taking thyroid medicine (only if not severely high)
        if (tsh is not None and tsh > 2.5 and tsh <= 7 and 
            (hhq.get('hh_takes_thyroid_medicine', False) or hhq.get('hh_thyroid_medication', False))):
            processed['High-thyroid'] = True
        
        # Complex thyroid dysfunction - TSH + reverse T3 trending wrong
        # TSH elevated OR Free T3 low + Reverse T3 elevated
        complex_thyroid_dysfunction = False
        if ((tsh is not None and tsh > 2.5) or 
            (free_t3 is not None and free_t3 < 3.6)) and \
           (reverse_t3 is not None and reverse_t3 > 15):
            processed['TSH-T3-rT3'] = True
            # Set values for template variables
            if free_t3 is not None:
                processed['FreeT3'] = f"{free_t3:.2f}"
            if reverse_t3 is not None:
                processed['ReverseT3'] = f"{reverse_t3:.1f}"
            complex_thyroid_dysfunction = True
        
        # Elevated reverse T3 condition
        if reverse_t3 is not None and reverse_t3 > 15:
            processed['quick-reverseT3'] = True
        
        # Fatigue + thyroid issues = Free T3 therapy candidate
        # Chronic fatigue + any thyroid dysfunction
        has_chronic_fatigue = (hhq.get('hh_chronic_fatigue', False) or 
                              hhq.get('hh_chronic_fatigue_syndrome', False) or
                              hhq.get('hh_fatigue', False))
        
        thyroid_dysfunction_present = (
            (tsh is not None and tsh > 2.5) or
            (free_t3 is not None and free_t3 < 3.2) or
            (reverse_t3 is not None and reverse_t3 > 15) or
            complex_thyroid_dysfunction
        )
        
        if has_chronic_fatigue and thyroid_dysfunction_present:
            processed['quick-fatigue'] = True
        
        # Hashimoto's autoimmune condition
        # TPO >34 OR TgAb >1 = autoimmune thyroiditis risk
        has_hashimotos_markers = False
        if tpo_antibody is not None and tpo_antibody > 34:
            has_hashimotos_markers = True
        if tg_antibody is not None and tg_antibody > 1:
            has_hashimotos_markers = True
        
        # Also check HHQ for explicit Hashimoto's diagnosis
        if (has_hashimotos_markers or 
            hhq.get('hh_hashimotos', False) or 
            hhq.get('hh_thyroid_autoimmune', False) or
            hhq.get('hh_autoimmune_thyroiditis', False)):
            processed['quick-hashimotos'] = True
        
        # ================================
        # COMPREHENSIVE FEMALE HORMONE CONDITIONS
        # ================================
        
        # Get female hormone lab values
        fsh = self._get_lab_value(labs, ['FHt_FSH', 'FSH'])
        estradiol = self._get_lab_value(labs, ['FHt_E2', 'Estradiol'])
        progesterone = self._get_lab_value(labs, ['FHt_PROG', 'Progesterone'])
        testosterone_female = self._get_lab_value(labs, ['FHt_TT', 'Testosterone'])
        estrone = self._get_lab_value(labs, ['FHt_E1', 'Estrone'])
        prolactin = self._get_lab_value(labs, ['FHt_PROL', 'Prolactin'])
        lh = self._get_lab_value(labs, ['FHt_LH', 'LH'])
        shbg = self._get_lab_value(labs, ['FHt_SHBG', 'SHBG'])
        dht = self._get_lab_value(labs, ['FHt_DHT', 'DHT'])
        
        # Determine menopause status
        menopause_status = self._determine_menopause_status(hhq)
        
        # Only process female hormones for female clients
        if hhq.get('gender') == 'female' or hhq.get('sex') == 'female':
            processed['quick-female-hormones'] = True
            
            # Hormone replacement therapy recommendations
            # Based on suboptimal hormone levels or symptoms
            hormone_dysfunction = False
            
            # Check for suboptimal hormone levels
            if fsh is not None:
                if menopause_status in ['premenopausal', 'perimenopause'] and fsh > 11:
                    hormone_dysfunction = True
                elif menopause_status in ['natural_menopause', 'surgical_menopause'] and fsh > 20:
                    hormone_dysfunction = True
            
            if estradiol is not None:
                if menopause_status in ['premenopausal', 'perimenopause'] and (estradiol < 50 or estradiol > 500):
                    hormone_dysfunction = True
                elif menopause_status in ['natural_menopause', 'surgical_menopause'] and (estradiol < 50 or estradiol > 150):
                    hormone_dysfunction = True
            
            if progesterone is not None and (progesterone < 1 or progesterone > 7):
                hormone_dysfunction = True
                
            if testosterone_female is not None and (testosterone_female < 40 or testosterone_female > 70):
                hormone_dysfunction = True
            
            # Symptom-based triggers for HRT
            has_menopausal_symptoms = (
                hhq.get('hh_hot_flashes', False) or
                hhq.get('hh_night_sweats', False) or
                hhq.get('hh_mood_swings', False) or
                hhq.get('hh_low_libido', False) or
                hhq.get('hh_vaginal_dryness', False) or
                hhq.get('hh_brain_fog', False) or
                hhq.get('hh_memory_problems', False)
            )
            
            has_cognitive_symptoms = (
                hhq.get('hh_brain_fog', False) or
                hhq.get('hh_memory_problems', False) or
                hhq.get('hh_attention_problems', False) or
                hhq.get('hh_cognitive_decline', False)
            )
            
            has_mood_symptoms = (
                hhq.get('hh_depression', False) or
                hhq.get('hh_anxiety', False) or
                hhq.get('hh_mood_disorder', False)
            )
            
            # HRT recommendation triggers
            if (hormone_dysfunction or has_menopausal_symptoms or has_cognitive_symptoms or 
                has_mood_symptoms or menopause_status in ['natural_menopause', 'surgical_menopause']):
                processed['quick-female-hormones-hrt'] = True
            else:
                processed['quick-female-hormones-hrt'] = False
            
            # Currently using HRT
            if (hhq.get('hh_takes_estrogen', False) or 
                hhq.get('hh_takes_progesterone', False) or
                hhq.get('hh_takes_testosterone', False) or
                hhq.get('hh_hormone_replacement', False)):
                processed['quick-using-HRT'] = True
            else:
                processed['quick-using-HRT'] = False
            
            # Breast cancer history considerations
            if hhq.get('hh_breast_cancer', False):
                processed['Quick-Breast-CA'] = True
                
                # Special considerations for sleep/anxiety with breast cancer history
                if (hhq.get('hh_insomnia', False) or 
                    hhq.get('hh_anxiety', False) or
                    hhq.get('hh_depression', False)):
                    processed['BreastCA-Insomnia-Anxiety'] = True
                else:
                    processed['BreastCA-Insomnia-Anxiety'] = False
            else:
                processed['Quick-Breast-CA'] = False
                processed['BreastCA-Insomnia-Anxiety'] = False
            
            # Mood disorder considerations
            if (hhq.get('hh_depression', False) or 
                hhq.get('hh_anxiety', False) or
                hhq.get('hh_mood_disorder', False)):
                processed['Quick-Hormone-Mood-Disorder'] = True
            else:
                processed['Quick-Hormone-Mood-Disorder'] = False
            
            # Sleep issues with antidepressant use
            if (hhq.get('hh_insomnia', False) and 
                (hhq.get('hh_takes_antidepressant', False) or 
                 hhq.get('hh_takes_sleep_medication', False))):
                processed['Prometrium-Sleep'] = True
            else:
                processed['Prometrium-Sleep'] = False
            
            # Frequent UTI considerations
            if hhq.get('hh_frequent_uti', False) or hhq.get('hh_recurrent_uti', False):
                processed['Freq-UTI'] = True
            else:
                processed['Freq-UTI'] = False
        else:
            # Explicitly set female hormone conditions to False for non-female clients
            processed['quick-female-hormones'] = False
            processed['quick-female-hormones-hrt'] = False
            processed['quick-using-HRT'] = False
            processed['Quick-Breast-CA'] = False
            processed['BreastCA-Insomnia-Anxiety'] = False
            processed['Quick-Hormone-Mood-Disorder'] = False
            processed['Prometrium-Sleep'] = False
            processed['Freq-UTI'] = False
        
        # ================================
        # COMPREHENSIVE MALE HORMONE CONDITIONS
        # ================================
        
        # Get male hormone lab values
        total_testosterone = self._get_lab_value(labs, ['MHt_TT', 'MHt_TEST_TOT', 'Testosterone'])
        free_testosterone = self._get_lab_value(labs, ['MHt_FREE_T', 'MHt_TEST_FREE', 'Free Testosterone'])
        shbg_male = self._get_lab_value(labs, ['MHt_SHBG', 'SHBG'])
        psa = self._get_lab_value(labs, ['MHt_PSA', 'PSA'])
        lh_male = self._get_lab_value(labs, ['MHt_LH', 'LH'])
        fsh_male = self._get_lab_value(labs, ['MHt_FSH', 'FSH'])
        prolactin_male = self._get_lab_value(labs, ['MHt_PROL', 'Prolactin'])
        dht_male = self._get_lab_value(labs, ['MHt_DHT', 'DHT'])
        estradiol_male = self._get_lab_value(labs, ['MHt_E2', 'Estradiol'])
        estrone_male = self._get_lab_value(labs, ['MHt_E1', 'Estrone'])
        progesterone_male = self._get_lab_value(labs, ['MHt_PROG', 'Progesterone'])
        
        # Only process male hormones for male clients
        if hhq.get('gender') == 'male' or hhq.get('sex') == 'male':
            processed['quick-male-hormones'] = True
            
            # Testosterone optimization recommendations
            # Based on suboptimal hormone levels or symptoms
            hormone_dysfunction = False
            
            # Check for suboptimal male hormone levels
            if total_testosterone is not None:
                if total_testosterone < 600:  # Combined threshold for treatment consideration
                    hormone_dysfunction = True
                    processed['testosterone-low'] = True
                    # Sub-categorize for specific messaging
                    if total_testosterone < 400:
                        processed['testosterone-clinically-low'] = True
                    else:
                        processed['testosterone-suboptimal'] = True
                else:
                    processed['testosterone-low'] = False
                    processed['testosterone-suboptimal'] = False
                    processed['testosterone-clinically-low'] = False
            
            if free_testosterone is not None:
                if free_testosterone < 12:  # Below optimal range
                    hormone_dysfunction = True
                    processed['free-testosterone-low'] = True
                else:
                    processed['free-testosterone-low'] = False
            
            if shbg_male is not None:
                if shbg_male > 45:  # Elevated SHBG affects free testosterone
                    processed['quick-male-hormones-shbg'] = True
                else:
                    processed['quick-male-hormones-shbg'] = False
            
            # PSA considerations
            if psa is not None:
                if psa > 4.0:  # Elevated PSA
                    processed['Quick-PSA'] = True
                    processed['psa-elevated'] = True
                elif psa > 2.5:  # Borderline elevated
                    processed['Quick-PSA'] = True
                    processed['psa-borderline'] = True
                else:
                    processed['Quick-PSA'] = False
            
            # Symptom-based triggers for hormone optimization
            has_hypogonadal_symptoms = (
                hhq.get('hh_erectile_dysfunction', False) or
                hhq.get('hh_low_libido', False) or
                hhq.get('hh_fatigue', False) or
                hhq.get('hh_muscle_weakness', False) or
                hhq.get('hh_depression', False) or
                hhq.get('hh_brain_fog', False) or
                hhq.get('hh_memory_problems', False)
            )
            
            has_cognitive_symptoms = (
                hhq.get('hh_brain_fog', False) or
                hhq.get('hh_memory_problems', False) or
                hhq.get('hh_attention_problems', False) or
                hhq.get('hh_cognitive_decline', False)
            )
            
            has_sleep_issues = (
                hhq.get('hh_sleep_apnea', False) or
                hhq.get('hh_insomnia', False) or
                hhq.get('hh_uses_cpap', False)
            )
            
            # TRT/HRT recommendation triggers (excluding prostate cancer or elevated PSA)
            has_prostate_contraindication = (
                hhq.get('hh_prostate_cancer', False) or
                (psa is not None and psa > 4.0)
            )
            
            # TRT/HRT recommendation triggers 
            # For prostate cancer patients, still recommend discussion (like breast cancer in females)
            has_severe_psa_elevation = (psa is not None and psa > 4.0)
            
            if (hormone_dysfunction or has_hypogonadal_symptoms or has_cognitive_symptoms):
                # Recommend HRT discussion unless PSA is severely elevated
                if not has_severe_psa_elevation:
                    processed['quick-male-hormones-hrt'] = True
                else:
                    processed['quick-male-hormones-hrt'] = False
            else:
                processed['quick-male-hormones-hrt'] = False
            
            # Currently using TRT
            if (hhq.get('hh_takes_testosterone', False) or 
                hhq.get('hh_hormone_replacement', False) or
                hhq.get('hh_trt', False)):
                processed['quick-using-TRT'] = True
            else:
                processed['quick-using-TRT'] = False
            
            # Prostate cancer history considerations
            if hhq.get('hh_prostate_cancer', False):
                processed['Quick-Prostate-CA'] = True
                
                # LUPRON considerations for prostate cancer patients
                if (hhq.get('hh_takes_lupron', False) or 
                    hhq.get('hh_lupron', False) or
                    hhq.get('hh_hormone_suppression', False)):
                    processed['quick-LUPRON'] = True
                else:
                    processed['quick-LUPRON'] = False
            else:
                processed['Quick-Prostate-CA'] = False
                processed['quick-LUPRON'] = False
            
            # Sleep and hormone connection
            if has_sleep_issues and (hormone_dysfunction or has_hypogonadal_symptoms):
                processed['quick-sleep-hormones'] = True
            else:
                processed['quick-sleep-hormones'] = False
            
            # ZMA testosterone support for natural optimization
            if (hormone_dysfunction and not hhq.get('hh_takes_testosterone', False)):
                processed['zma-testosterone-support'] = True
            else:
                processed['zma-testosterone-support'] = False
            
            # Age-related considerations
            if hhq.get('hh_age_over_50', False) or hhq.get('hh_age_over_65', False):
                processed['quick-age-related-decline'] = True
            else:
                processed['quick-age-related-decline'] = False
            
            # TBI and hormone optimization (Mark Gordon protocol)
            has_brain_injury = (hhq.get('hh_head_injury', False) or 
                              hhq.get('hh_concussion', False) or 
                              hhq.get('hh_traumatic_brain_injury', False) or
                              hhq.get('hh_tbi', False))
            
            if has_brain_injury and (hormone_dysfunction or has_cognitive_symptoms):
                processed['quick-tbi-hormone-protocol'] = True
            else:
                processed['quick-tbi-hormone-protocol'] = False
            
            # Metabolic dysfunction affecting hormones
            has_metabolic_dysfunction = (
                hhq.get('hh_diabetes', False) or
                hhq.get('hh_metabolic_syndrome', False) or
                hhq.get('hh_insulin_resistance', False)
            )
            
            if has_metabolic_dysfunction and hormone_dysfunction:
                processed['metabolic-hormone-connection'] = True
            else:
                processed['metabolic-hormone-connection'] = False
        else:
            # Explicitly set male hormone conditions to False for non-male clients
            processed['quick-male-hormones'] = False
            processed['testosterone-low'] = False
            processed['testosterone-suboptimal'] = False
            processed['free-testosterone-low'] = False
            processed['quick-male-hormones-shbg'] = False
            processed['quick-male-hormones-hrt'] = False
            processed['quick-using-TRT'] = False
            processed['Quick-Prostate-CA'] = False
            processed['quick-LUPRON'] = False
            processed['Quick-PSA'] = False
            processed['quick-sleep-hormones'] = False
            processed['zma-testosterone-support'] = False
            processed['quick-age-related-decline'] = False
            processed['quick-tbi-hormone-protocol'] = False
            processed['metabolic-hormone-connection'] = False
        
        # ================================
        # NEUROLOGICALLY ACTIVE HORMONES
        # ================================
        
        # Get neurologically active hormone lab values
        pregnenolone = self._get_lab_value(labs, ['NEURO_PREG', 'Pregnenolone, MS'])
        dhea_s = self._get_lab_value(labs, ['NEURO_DHEAS', 'DHEA-Sulfate'])
        cortisol = self._get_lab_value(labs, ['NEURO_CORT', 'Cortisol'])
        
        # Store lab values for template display
        if pregnenolone is not None:
            processed['quick-pregnenolone-lab-value'] = f"{pregnenolone:.0f}"
        if dhea_s is not None:
            processed['quick-dhea-lab-value'] = f"{dhea_s:.0f}"
        if cortisol is not None:
            processed['quick-cortisol-lab-value'] = f"{cortisol:.1f}"
        
        # PREGNENOLONE CONDITIONS
        if pregnenolone is not None:
            if 150 <= pregnenolone <= 200:  # Optimal range
                processed['quick-pregnenolone-101'] = True
                processed['quick-PROG-50-100'] = False
                processed['quick-PROG<50'] = False
            elif 50 <= pregnenolone < 150:  # Low, needs supplementation
                processed['quick-PROG-50-100'] = True
                processed['quick-pregnenolone-101'] = False
                processed['quick-PROG<50'] = False
            elif pregnenolone < 50:  # Very low
                processed['quick-PROG<50'] = True
                processed['quick-pregnenolone-101'] = False
                processed['quick-PROG-50-100'] = False
            else:  # Above optimal range
                processed['quick-pregnenolone-101'] = False
                processed['quick-PROG-50-100'] = False
                processed['quick-PROG<50'] = False
        else:
            # No pregnenolone data
            processed['quick-pregnenolone-101'] = False
            processed['quick-PROG-50-100'] = False
            processed['quick-PROG<50'] = False
        
        # DHEA-S CONDITIONS
        if dhea_s is not None:
            if dhea_s >= 250:  # Optimal range
                processed['quick-DHEA-151'] = True
                processed['quick-DHEA-150'] = False
                processed['quick-DHEA-200-249'] = False
            elif dhea_s >= 200:  # Borderline optimal
                processed['quick-DHEA-151'] = True
                processed['quick-DHEA-200-249'] = True  # Lower dose recommendation
                processed['quick-DHEA-150'] = False
            elif dhea_s >= 150:  # Borderline low
                processed['quick-DHEA-151'] = True
                processed['quick-DHEA-150'] = False
                processed['quick-DHEA-200-249'] = False
            else:  # Low, needs supplementation
                processed['quick-DHEA-150'] = True
                processed['quick-DHEA-151'] = False
                processed['quick-DHEA-200-249'] = False
        else:
            # No DHEA-S data
            processed['quick-DHEA-151'] = False
            processed['quick-DHEA-150'] = False
            processed['quick-DHEA-200-249'] = False
        
        # DHEA & CARDIOVASCULAR DISEASE CORRELATION
        # Low DHEA-S levels correlate with increased cardiovascular disease risk
        has_cardiovascular_disease = (
            hhq.get('hh_heart_disease', False) or
            hhq.get('hh_cardiovascular_disease', False) or
            hhq.get('hh_coronary_artery_disease', False) or
            hhq.get('hh_myocardial_infarction', False) or
            hhq.get('hh_heart_attack', False)
        )
        
        if has_cardiovascular_disease and dhea_s and dhea_s < 150:
            processed['quick-DHEA-ASVD'] = True
        else:
            processed['quick-DHEA-ASVD'] = False
        
        # DHEA & LUPRON CONNECTION (Male prostate cancer patients)
        # LUPRON suppresses hormones including DHEA-S
        is_male = hhq.get('gender') == 'male' or hhq.get('sex') == 'male'
        takes_lupron = (
            hhq.get('hh_takes_lupron', False) or
            hhq.get('hh_lupron', False) or
            hhq.get('hh_hormone_suppression', False)
        )
        
        if is_male and takes_lupron and dhea_s and dhea_s < 150:
            processed['quick-DHEA-LUPRON'] = True
        else:
            processed['quick-DHEA-LUPRON'] = False
        
        # CORTISOL SUPPORT CONDITIONS
        if cortisol is not None:
            if cortisol < 15:  # Low cortisol needs support
                processed['quick-cortisol-15'] = True
                
                # Additional categorization for cortisol levels
                if cortisol >= 5:  # Borderline low cortisol (5-15 ng/dL)
                    processed['Cort515'] = True
                    processed['cortisol-borderline'] = True
                    processed['cortisol-very-low'] = False
                else:  # Very low cortisol (<5 ng/dL)
                    processed['Cort515'] = False
                    processed['cortisol-very-low'] = True
                    processed['cortisol-borderline'] = False
                
                # Additional adrenal support for very low cortisol + symptoms
                has_adrenal_symptoms = (
                    hhq.get('hh_chronic_fatigue', False) or
                    hhq.get('hh_adrenal_fatigue', False) or
                    hhq.get('hh_low_energy', False) or
                    hhq.get('hh_morning_fatigue', False)
                )
                
                if cortisol < 10 and has_adrenal_symptoms:
                    processed['cortisol-severe-support'] = True
                else:
                    processed['cortisol-severe-support'] = False
            else:
                # Optimal or high cortisol levels (≥15 ng/dL)
                processed['quick-cortisol-15'] = False
                processed['Cort515'] = False
                processed['cortisol-severe-support'] = False
                processed['cortisol-borderline'] = False
                processed['cortisol-very-low'] = False
                
                # Check for elevated cortisol (>25 ng/dL)
                if cortisol > 25:
                    processed['quick-cortisol-high'] = True
                    processed['cortisol-elevated'] = True
                    
                    # High cortisol with stress symptoms = stress management protocol
                    has_stress_symptoms = (
                        hhq.get('hh_chronic_stress', False) or
                        hhq.get('hh_anxiety', False) or
                        hhq.get('hh_insomnia', False) or
                        hhq.get('hh_high_blood_pressure', False)
                    )
                    
                    if has_stress_symptoms:
                        processed['cortisol-stress-management'] = True
                    else:
                        processed['cortisol-stress-management'] = False
                else:
                    processed['quick-cortisol-high'] = False
                    processed['cortisol-elevated'] = False
                    processed['cortisol-stress-management'] = False
        else:
            processed['quick-cortisol-15'] = False
            processed['Cort515'] = False
            processed['cortisol-severe-support'] = False
            processed['cortisol-borderline'] = False
            processed['cortisol-very-low'] = False
            processed['quick-cortisol-high'] = False
            processed['cortisol-elevated'] = False
            processed['cortisol-stress-management'] = False
        
        # EXERCISE-INDUCED CORTISOL ISSUES
        # Athletes with overtraining syndrome and low cortisol
        is_athlete = (
            hhq.get('hh_athlete', False) or
            hhq.get('hh_exercise_frequently', False) or
            hhq.get('hh_high_intensity_training', False)
        )
        
        has_exercise_symptoms = (
            hhq.get('hh_exercise_intolerance', False) or
            hhq.get('hh_muscle_weakness', False) or
            hhq.get('hh_overtraining', False) or
            hhq.get('hh_performance_decline', False)
        )
        
        if is_athlete and has_exercise_symptoms and cortisol and cortisol < 15:
            processed['exercise-cortisol-support'] = True
        else:
            processed['exercise-cortisol-support'] = False
        
        # COMPOUND NEUROLOGICAL HORMONE CONDITIONS
        # Multiple hormone deficiencies = comprehensive support needed
        has_multiple_deficiencies = (
            processed.get('quick-PROG-50-100', False) or 
            processed.get('quick-PROG<50', False) or
            processed.get('quick-DHEA-150', False) or
            processed.get('quick-cortisol-15', False)
        )
        
        has_neurological_symptoms = (
            hhq.get('hh_brain_fog', False) or
            hhq.get('hh_memory_problems', False) or
            hhq.get('hh_chronic_fatigue', False) or
            hhq.get('hh_depression', False) or
            hhq.get('hh_anxiety', False)
        )
        
        if has_multiple_deficiencies and has_neurological_symptoms:
            processed['neurological-hormone-support'] = True
        else:
            processed['neurological-hormone-support'] = False
        
        
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
    
    def _get_lab_string_value(self, labs: Dict, possible_keys: List[str]) -> Optional[str]:
        """Get lab string value (for genetics, etc.) by checking multiple possible key names."""
        for key in possible_keys:
            if key in labs and labs[key] is not None:
                return str(labs[key])
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
                elif vit_d_val >= 55:
                    vit_d_rec = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was 55-59, you are encouraged to supplement with 4,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                elif vit_d_val >= 50:
                    vit_d_rec = "Your VITAMIN D level is suboptimal, and supplementation is recommended. Since your VITAMIN D was 50-54, you are encouraged to supplement with 6,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                elif vit_d_val >= 40:
                    vit_d_rec = "Since your VITAMIN D was 40-49, you are encouraged to supplement with 8,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                else:
                    vit_d_rec = "Since your VITAMIN D was < 40, you are encouraged to supplement with 10,000 iu of VITAMIN D3 per day, and then recheck your levels in 90 days."
                
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
        return self.asset_config.asset_exists(category, image_name)
    
    def _get_supplement_image(self, supplement_name: str) -> Optional[str]:
        """Get the image path for a supplement based on its name."""
        return self.asset_config.get_supplement_image(supplement_name)
    
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

    def _process_all_content_controls(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], 
                                     hhq_responses: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive content control processor that ensures ALL lab values are evaluated
        and ALL possible content controls are triggered based on intelligent thresholds.
        
        This is the core method that solves the lab representation problem by:
        1. Processing every single lab value against comprehensive thresholds
        2. Evaluating HHQ responses for content triggers
        3. Creating compound conditions from lab + HHQ combinations
        4. Using gender-specific and age-specific range mappings
        5. Ensuring critical controls always get evaluated with safety nets
        
        Returns a dictionary of ALL content controls that should be triggered.
        """
        if hhq_responses is None:
            hhq_responses = {}
            
        processed_content = {}
        
        # 1. COMPREHENSIVE LAB VALUE PROCESSING
        # Process every single lab value with intelligent thresholds
        processed_content.update(self._process_all_lab_values_comprehensive(client_data, lab_results, hhq_responses))
        
        # 2. HHQ-BASED CONDITIONS
        # Process all HHQ responses for content triggers
        processed_content.update(self._process_hhq_based_conditions(hhq_responses, lab_results))
        
        # 3. COMPOUND CONDITIONS
        # Create sophisticated lab + HHQ combination conditions
        ranges = self._get_comprehensive_lab_ranges(client_data.get('gender', 'unknown'))
        processed_content.update(self._process_compound_conditions(lab_results, hhq_responses, ranges))
        
        # 4. GENETIC PROCESSING
        # Handle APO E and MTHFR genetics
        processed_content.update(self._process_genetics_comprehensive(lab_results))
        
        # 5. CBC AND COAGULATION INSIGHTS PROCESSING
        # Handle CBC and coagulation markers for Other Insights section
        processed_content.update(self._process_cbc_and_coagulation_insights(lab_results, hhq_responses, ranges))
        
        # 6. BMI AND WEIGHT INSIGHTS PROCESSING
        # Handle BMI calculations and weight-related conditions for Body Weight section
        processed_content.update(self._process_bmi_and_weight_insights(client_data, hhq_responses))
        
        # 7. RISK PROFILE INSIGHTS PROCESSING
        # Handle risk factor analysis for Other Insights section
        processed_content.update(self._process_risk_profile_insights(hhq_responses))
        
        # 8. SAFETY NETS - Ensure critical controls are always evaluated
        processed_content.update(self._apply_safety_nets(lab_results, hhq_responses, client_data))
        
        return processed_content
    
    def _process_all_lab_values_comprehensive(self, client_data: Dict[str, Any], lab_results: Dict[str, Any], hhq_responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process ALL lab values comprehensively using intelligent thresholds.
        This ensures every lab result triggers appropriate content controls.
        """
        if hhq_responses is None:
            hhq_responses = {}
            
        processed = {}
        gender = client_data.get('gender', 'unknown').lower()
        
        # Get comprehensive lab ranges for this gender
        ranges = self._get_comprehensive_lab_ranges(gender)
        
        # INFLAMMATORY MARKERS
        self._evaluate_lab_threshold(processed, lab_results, 'INFLAM_CRP', 'C-Reactive Protein, Cardiac', 
                                   'quick-CRP', ranges['CRP'])
        self._evaluate_lab_threshold(processed, lab_results, 'INFLAM_HOMOCYS', 'Homocyst(e)ine', 
                                   'quick-homocysteine', ranges['Homocysteine'])
        self._evaluate_lab_threshold(processed, lab_results, 'INFLAM_URIC', 'Uric Acid', 
                                   'quick-uric-acid', ranges['UricAcid'])
        
        # Add specific CRP processing for inflammation section
        crp = self._get_lab_value(lab_results, ['INFLAM_CRP', 'C-Reactive Protein, Cardiac'])
        if crp is not None:
            processed['quick-CRP'] = crp
            
            if crp <= 1.0:  # Optimal CRP
                processed['quick-CRP-above-optimal'] = True  # For optimal message
                processed['quick-CRP-elevated'] = False
            else:  # Elevated CRP > 1.0
                processed['quick-CRP-above-optimal'] = False  # Hide optimal message  
                processed['quick-CRP-elevated'] = True
        
        # Add homocysteine-specific processing
        homocysteine = self._get_lab_value(lab_results, ['INFLAM_HOMOCYS', 'Homocyst(e)ine'])
        if homocysteine:
            processed['homocysteine-value'] = homocysteine
            
            # Check for elevated levels and sub-conditions
            if homocysteine > 7.0:  # Above optimal goal
                processed['quick-homocysteine'] = True  # Override any value set by threshold evaluation
                
                # Sub-condition: Levels > 12 → Trimethylglycine
                if homocysteine > 12.0:
                    processed['quick-Homo12'] = True
                    
                # Sub-condition: Levels > 15 → Creatine monohydrate 
                if homocysteine > 15.0:
                    processed['quick-Homo15'] = True
            else:
                # Explicitly set to False for optimal levels (override threshold evaluation)
                processed['quick-homocysteine'] = False
            
            # Always store related B vitamin values for the template
            b12 = self._get_lab_value(lab_results, ['VIT_B12', 'Vitamin B12'])
            if b12:
                processed['quick-B12-value'] = b12
                
            # Look for folate/folic acid values
            folate = self._get_lab_value(lab_results, ['VIT_FOLATE', 'Folate', 'Folic Acid'])
            if folate:
                processed['quick-folic-acid-value'] = folate
            else:
                processed['quick-folic-acid-value'] = 'Not Available'
        
        # COMPLETE BLOOD COUNT  
        self._evaluate_lab_threshold(processed, lab_results, 'CBC_WBC', 'WBC', 
                                   'quick-WBC', ranges['WBC'])
        self._evaluate_lab_threshold(processed, lab_results, 'CBC_RBC', 'RBC', 
                                   'quick-RBC', ranges['RBC'])
        self._evaluate_lab_threshold(processed, lab_results, 'CBC_HGB', 'Hemoglobin', 
                                   'quick-hemoglobin', ranges['Hemoglobin'])
        self._evaluate_lab_threshold(processed, lab_results, 'CBC_PLT', 'Platelets', 
                                   'quick-platelets', ranges['Platelets'])
        
        # COMPREHENSIVE METABOLIC PANEL
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_GLU', 'Glucose', 
                                   'quick-glucose', ranges['Glucose'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_BUN', 'BUN', 
                                   'quick-BUN', ranges['BUN'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_CREAT', 'Creatinine', 
                                   'quick-creatinine', ranges['Creatinine'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_EGFR', 'eGFR', 
                                   'quick-eGFR', ranges['eGFR'])
        
        # LIPID PANEL - COMPREHENSIVE CHOLESTEROL PROCESSING
        self._evaluate_lab_threshold(processed, lab_results, 'LIPID_CHOL', 'Cholesterol, Total', 
                                   'quick-TC', ranges['TotalCholesterol'])
        self._evaluate_lab_threshold(processed, lab_results, 'LIPID_TRIG', 'Triglycerides', 
                                   'quick-trigly', ranges['Triglycerides'])
        self._evaluate_lab_threshold(processed, lab_results, 'LIPID_HDL', 'HDL Cholesterol', 
                                   'quick-HDL', ranges['HDLCholesterol'])
        self._evaluate_lab_threshold(processed, lab_results, 'LIPID_LDL', 'LDL Chol Calc (NIH)', 
                                   'quick-LDL', ranges['LDLCholesterol'])
        
        # CALCULATE TRIGLYCERIDE TO HDL RATIO
        triglycerides = self._get_lab_value(lab_results, ['LIPID_TRIG', 'Triglycerides'])
        hdl = self._get_lab_value(lab_results, ['LIPID_HDL', 'HDL Cholesterol'])
        
        if triglycerides and hdl:
            trig_hdl_ratio = round(triglycerides / hdl, 2)
            processed['quick-trig-HDL'] = trig_hdl_ratio
            
            # Triglyceride to HDL ratio > 2 indicates insulin resistance
            if trig_hdl_ratio > 2.0:
                processed['quick-trig-HDL-elevated'] = True
                processed['insulin-resistance-indicator'] = True
        
        # CHOLESTEROL THRESHOLD CONDITIONS
        total_chol = self._get_lab_value(lab_results, ['LIPID_CHOL', 'Cholesterol, Total'])
        ldl = self._get_lab_value(lab_results, ['LIPID_LDL', 'LDL Chol Calc (NIH)'])
        
        # Trigger cholesterol-row for elevated total cholesterol or LDL
        if (total_chol and total_chol > 200) or (ldl and ldl > 100):
            processed['cholesterol-row'] = True
            processed['quick-CAC'] = True  # Recommend CAC score for elevated cholesterol
            
        # CARDIOVASCULAR SUPPLEMENT CONDITIONS
        # MegaQuinone K2-7 for cardiovascular support
        has_cardiovascular_risk = (
            (total_chol and total_chol > 200) or
            (ldl and ldl > 100) or
            (triglycerides and triglycerides > 150) or
            (hdl and hdl < 40)
        )
        if has_cardiovascular_risk:
            processed['quick-MK2'] = True
            processed['mk2-cardiovascular-support'] = True
            
        # VERY LOW TRIGLYCERIDES - PLASMALOGEN PATHWAY
        if triglycerides and triglycerides < 50:  # Uncharacteristically low
            processed['trig-plasmalogens-row'] = True
            processed['trig-plasmalogens'] = True
        
        # ELECTROLYTES
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_NA', 'Sodium', 
                                   'quick-sodium', ranges['Sodium'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_K', 'Potassium', 
                                   'quick-potassium', ranges['Potassium'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_CL', 'Chloride', 
                                   'quick-chloride', ranges['Chloride'])
        self._evaluate_lab_threshold(processed, lab_results, 'CHEM_CA', 'Calcium', 
                                   'quick-calcium', ranges['Calcium'])
        
        # LIVER FUNCTION TESTS
        self._evaluate_lab_threshold(processed, lab_results, 'LFT_ALT', 'ALT (SGPT)', 
                                   'quick-ALT', ranges['ALT'])
        self._evaluate_lab_threshold(processed, lab_results, 'LFT_AST', 'AST (SGOT)', 
                                   'quick-AST', ranges['AST'])
        self._evaluate_lab_threshold(processed, lab_results, 'LFT_ALKP', 'Alkaline Phosphatase', 
                                   'quick-alkaline-phosphatase', ranges['AlkalinePhosphatase'])
        self._evaluate_lab_threshold(processed, lab_results, 'LFT_ALB', 'Albumin', 
                                   'quick-albumin', ranges['Albumin'])
        
        # ALBUMIN TO GLOBULIN RATIO (A/G RATIO) PROCESSING
        albumin = self._get_lab_value(lab_results, ['LFT_ALB', 'Albumin'])
        total_protein = self._get_lab_value(lab_results, ['LFT_TP', 'Total Protein'])
        
        if albumin and total_protein:
            globulin = total_protein - albumin
            if globulin > 0:
                ag_ratio = round(albumin / globulin, 2)
                processed['quick-AG-ratio'] = ag_ratio
                
                # A/G Ratio evaluation 
                if ag_ratio >= 1.5:  # Optimal A/G ratio
                    processed['quick-AG-15'] = True
                    processed['ag-ratio-optimal'] = True
                    processed['ag-ratio-low'] = False
                else:  # Low A/G ratio <1.5
                    processed['quick-AG-15'] = False
                    processed['ag-ratio-low'] = True
                    processed['ag-ratio-optimal'] = False
                    
                    # Very low A/G ratio requires more aggressive intervention
                    if ag_ratio < 1.2:
                        processed['ag-ratio-very-low'] = True
                    else:
                        processed['ag-ratio-very-low'] = False
        
        # URIC ACID COMPREHENSIVE PROCESSING
        uric_acid = self._get_lab_value(lab_results, ['INFLAM_URIC', 'Uric Acid'])
        if uric_acid is not None:
            processed['quick-uric-acid'] = uric_acid
            
            # Uric acid threshold conditions
            if uric_acid <= 6.5:  # Optimal uric acid
                processed['UricAcid65'] = True
                processed['uric-acid-elevated'] = False
            else:  # Elevated uric acid >6.5 mg/dL
                processed['UricAcid65'] = False
                processed['uric-acid-elevated'] = True
                
                # Sub-condition for very high uric acid
                if uric_acid > 8.0:
                    processed['uric-acid-very-high'] = True
                else:
                    processed['uric-acid-very-high'] = False
            
            # Gout risk assessment - uric acid >6.5 + history of gout or joint pain
            gout_history = (hhq_responses and (
                hhq_responses.get('hh_gout', False) or
                hhq_responses.get('hh_joint_pain', False) or
                hhq_responses.get('hh_arthritis', False)
            ))
            
            if uric_acid > 6.5 and gout_history:
                processed['UAAcid-Gout'] = True
            else:
                processed['UAAcid-Gout'] = False
        
        # ALCOHOL INTERACTION CONDITIONS
        # Check for alcohol consumption from HHQ  
        alcohol_consumption = False
        if hhq_responses:
            alcohol_consumption = (
                hhq_responses.get('hh_alcohol_consumption', False) or
                hhq_responses.get('hh_drinks_alcohol', False) or
                hhq_responses.get('hh_alcohol_4days', False) or
                hhq_responses.get('hh_1to3_alcohol_week', False) or
                hhq_responses.get('hh_alcohol_daily', False)
            )
        
        # A/G Ratio + Alcohol interaction
        # Low A/G ratio with alcohol consumption = compound liver/protein synthesis issue
        if (albumin and total_protein and 
            alcohol_consumption and 
            processed.get('ag-ratio-low', False)):
            processed['quick-AG-ETOH'] = True
        else:
            processed['quick-AG-ETOH'] = False
        
        # Uric Acid + Alcohol interaction  
        # Elevated uric acid with alcohol consumption = compound inflammation/gout risk
        if (uric_acid and uric_acid > 6.5 and alcohol_consumption):
            processed['quick-uric-acid-ETOH'] = True
        else:
            processed['quick-uric-acid-ETOH'] = False
        
        # THYROID PANEL
        self._evaluate_lab_threshold(processed, lab_results, 'THY_TSH', 'TSH', 
                                   'quick-TSH', ranges['TSH'])
        self._evaluate_lab_threshold(processed, lab_results, 'THY_T3F', 'Triiodothyronine (T3), Free', 
                                   'quick-T3', ranges['T3'])
        self._evaluate_lab_threshold(processed, lab_results, 'THY_T4F', 'T4, Free (Direct)', 
                                   'quick-T4', ranges['T4'])
        
        # VITAMINS & MINERALS
        self._evaluate_lab_threshold(processed, lab_results, 'VIT_D25', 'Vitamin D, 25-Hydroxy', 
                                   'quick-VitD', ranges['VitaminD'])
        self._evaluate_lab_threshold(processed, lab_results, 'VIT_B12', 'Vitamin B12', 
                                   'quick-B12', ranges['VitB12'])
        self._evaluate_lab_threshold(processed, lab_results, 'VIT_E', 'Vitamin E (Alpha Tocopherol)', 
                                   'quick-vitE', ranges['VitaminE'])
        
        # Add vitamin E-specific processing
        vit_e = self._get_lab_value(lab_results, ['VIT_E', 'Vitamin E (Alpha Tocopherol)'])
        if vit_e:
            processed['quick-vitE'] = f"{vit_e} mg/L"  # Display format with units
            
            # Sub-condition: VitE12 (levels >= 12 are optimal)
            if vit_e >= 12.0:
                processed['VitE12'] = True
                
            # Sub-condition: quick-vitE-row (levels < 12 need supplementation)  
            elif vit_e < 12.0:
                processed['quick-vitE-row'] = True
                
            # Sub-condition: quick-vitE-row-elevated (very high levels > 20)
            if vit_e > 20.0:
                processed['quick-vitE-row-elevated'] = True
        
        self._evaluate_lab_threshold(processed, lab_results, 'MIN_ZN', 'Zinc, Plasma or Serum', 
                                   'quick-zinc', ranges['Zinc'])
        self._evaluate_lab_threshold(processed, lab_results, 'MIN_CU', 'Copper, Serum or Plasma', 
                                   'quick-copper', ranges['Copper'])
        self._evaluate_lab_threshold(processed, lab_results, 'MIN_SE', 'Selenium, Serum/Plasma', 
                                   'quick-selenium', ranges['Selenium'])
        self._evaluate_lab_threshold(processed, lab_results, 'MIN_MG_RBC', 'Magnesium, RBC', 
                                   'quick-MagRBC', ranges['Magnesium'])
        
        # CALCULATE COPPER TO ZINC RATIO
        copper = self._get_lab_value(lab_results, ['MIN_CU', 'Copper, Serum or Plasma'])
        zinc = self._get_lab_value(lab_results, ['MIN_ZN', 'Zinc, Plasma or Serum'])
        
        if copper and zinc:
            cz_ratio = round(copper / zinc, 2)
            processed['quick-CZratio-14'] = cz_ratio
            
            # Trigger elevated condition if ratio > 1.4
            if cz_ratio > 1.4:
                processed['quick-CZratio-14-elevated'] = True
                
                # Enhanced treatment for significantly elevated ratios (>1.8) or additional risk factors
                if cz_ratio > 1.8:
                    processed['zinc-liposomalC'] = True
            else:
                processed['quick-CZratio-14-optimal'] = True
        
        # HORMONES (Gender-specific)
        if gender == 'female':
            self._evaluate_lab_threshold(processed, lab_results, 'FHt_E2', 'Estradiol', 
                                       'quick-estradiol', ranges['Estradiol'])
            self._evaluate_lab_threshold(processed, lab_results, 'FHt_PROG', 'Progesterone', 
                                       'quick-progesterone', ranges['Progesterone'])
            self._evaluate_lab_threshold(processed, lab_results, 'FHt_TEST', 'Testosterone', 
                                       'quick-testosterone', ranges['Testosterone'])
        elif gender == 'male':
            self._evaluate_lab_threshold(processed, lab_results, 'MHt_TEST_TOT', 'Testosterone', 
                                       'quick-testosterone', ranges['Testosterone'])
            self._evaluate_lab_threshold(processed, lab_results, 'MHt_TEST_FREE', 'Free Testosterone', 
                                       'quick-free-testosterone', ranges['FreeTestosterone'])
            self._evaluate_lab_threshold(processed, lab_results, 'MHt_PSA', 'PSA', 
                                       'quick-PSA', ranges['PSA'])
        
        # OMEGA FATTY ACIDS
        self._evaluate_lab_threshold(processed, lab_results, 'OMEGA_CHECK', 'OmegaCheck(TM)', 
                                   'OmegaCheck', ranges['OmegaCheck'])
        self._evaluate_lab_threshold(processed, lab_results, 'OMEGA_6_3_RATIO', 'Omega-6/Omega-3 Ratio', 
                                   'lab-omega-6-3-ratio', ranges['Omega63Ratio'])
        self._evaluate_lab_threshold(processed, lab_results, 'OMEGA_AA_EPA', 'Arachidonic Acid/EPA Ratio', 
                                   'AAEPA', ranges['AAEPARatio'])
        self._evaluate_lab_threshold(processed, lab_results, 'OMEGA_AA', 'Arachidonic Acid', 
                                   'AA', ranges['ArachidonicAcid'])
        
        # METABOLIC MARKERS
        self._evaluate_lab_threshold(processed, lab_results, 'METAB_INS', 'Insulin', 
                                   'quick-insulin', ranges['Insulin'])
        self._evaluate_lab_threshold(processed, lab_results, 'METAB_HBA1C', 'Hemoglobin A1c', 
                                   'quick-HbA1c', ranges['HbA1c'])
        
        # Add comprehensive blood sugar/metabolic processing
        glucose = self._get_lab_value(lab_results, ['CHEM_GLU', 'Glucose'])
        insulin = self._get_lab_value(lab_results, ['METAB_INS', 'Insulin'])
        hba1c = self._get_lab_value(lab_results, ['METAB_HBA1C', 'Hemoglobin A1c'])
        homa_ir = None  # Initialize to avoid UnboundLocalError
        
        # Process glucose levels
        if glucose:
            processed['quick-glucose'] = glucose
            if glucose >= 100:  # Above optimal fasting glucose
                processed['quick-glucose-elevated'] = True
                processed['glucose-elevated'] = True
            
        # Process fasting insulin levels  
        if insulin:
            processed['quick-fasting-insulin'] = insulin
            if insulin >= 7:  # Above optimal fasting insulin
                processed['quick-fasting-insulin-elevated'] = True
                processed['insulin-elevated'] = True
                
        # Calculate and process HOMA-IR
        if glucose and insulin:
            homa_ir = round((insulin * glucose) / 405, 2)
            processed['quick-homa-IR'] = homa_ir
            processed['HOMA_IR'] = homa_ir  # Alternative name
            
            if homa_ir >= 1.2:  # Above optimal HOMA-IR
                processed['quick-homa-IR-elevated'] = True
                processed['HOMA-IR-elevated'] = True
                
        # Process A1c levels with APO E4 considerations
        if hba1c:
            processed['quick-a1c'] = hba1c
            
            # Check for APO E4 status for stricter A1c goals
            apo_e = lab_results.get('APO1') or lab_results.get('APO E Genotyping Result')
            has_apo_e4 = apo_e and 'E4' in str(apo_e)
            has_double_e4 = apo_e and 'E4/E4' in str(apo_e)
            
            # A1c threshold conditions
            if hba1c > 6.0:
                processed['quick-A1c>6'] = True
                processed['quick-diabetes-risk'] = True
            elif hba1c > 5.6:
                processed['quick-A1c>56'] = True
                processed['quick-diabetes-risk'] = True
            else:
                processed['quick-A1c<56'] = True
                
            # APO E4-specific A1c goals
            if has_double_e4 and hba1c > 5.3:
                processed['quick-A1c-E4E4-elevated'] = True
            elif has_apo_e4 and hba1c > 5.6:
                processed['quick-A1c-E4-elevated'] = True
                
            # Supplement recommendations for elevated metabolic markers
            if (hba1c > 5.6 or 
                (glucose and glucose > 100) or 
                (insulin and insulin > 7) or 
                (homa_ir and homa_ir > 1.2)):
                processed['lab-a1c-L2b'] = True
        
        return processed
    
    def _evaluate_lab_threshold(self, processed: Dict, lab_results: Dict, lab_key: str, 
                               lab_display_name: str, control_name: str, thresholds: Dict) -> None:
        """
        Intelligent threshold evaluation for a single lab value.
        Creates multiple content controls based on value ranges.
        """
        # Try multiple possible keys for this lab
        possible_keys = [lab_key, lab_display_name]
        value = self._get_lab_value(lab_results, possible_keys)
        
        if value is None:
            return
            
        # Store the raw value for template replacement
        processed[control_name] = value
        
        # Evaluate against thresholds to create conditional content controls
        if 'critical_high' in thresholds and value >= thresholds['critical_high']:
            processed[f"{control_name}-critical-high"] = True
            processed[f"{control_name}-elevated"] = True
        elif 'high' in thresholds and value >= thresholds['high']:
            processed[f"{control_name}-high"] = True
            processed[f"{control_name}-elevated"] = True
        elif 'optimal_max' in thresholds and value > thresholds['optimal_max']:
            processed[f"{control_name}-above-optimal"] = True
        elif 'optimal_min' in thresholds and value >= thresholds['optimal_min']:
            processed[f"{control_name}-optimal"] = True
        elif 'low' in thresholds and value <= thresholds['low']:
            processed[f"{control_name}-low"] = True
        elif 'critical_low' in thresholds and value <= thresholds['critical_low']:
            processed[f"{control_name}-critical-low"] = True
            processed[f"{control_name}-low"] = True
        
        # Create range-specific controls for vitamins
        if control_name == 'quick-VitD':
            # MUTUALLY EXCLUSIVE vitamin D conditions
            if value >= 60:
                processed['D-60+'] = True
                processed['D-55-59'] = False
                processed['D-50-55'] = False
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = False
                processed['D-30-39'] = False
                processed['D-less-30'] = False
                # Set parent conditions - optimal range
                processed['D-optimal'] = True
                processed['quick-VitD-row'] = False
                processed['quick-vitD-simple'] = True
                processed['quick-VitD-row-takingD'] = False
            elif value >= 55:
                processed['D-60+'] = False
                processed['D-55-59'] = True
                processed['D-50-55'] = False
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = False
                processed['D-30-39'] = False
                processed['D-less-30'] = False
                # Set parent conditions - close to optimal
                processed['D-optimal'] = False
                processed['quick-VitD-row'] = False
                processed['quick-vitD-simple'] = True
                processed['quick-VitD-row-takingD'] = False
            elif value >= 50:
                processed['D-60+'] = False
                processed['D-55-59'] = False
                processed['D-50-55'] = True
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = False
                processed['D-30-39'] = False
                processed['D-less-30'] = False
                # Set parent conditions - close to optimal
                processed['D-optimal'] = False
                processed['quick-VitD-row'] = False
                processed['quick-vitD-simple'] = True
                processed['quick-VitD-row-takingD'] = False
            elif value >= 40:
                processed['D-60+'] = False
                processed['D-55-59'] = False
                processed['D-50-55'] = False
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = True
                processed['D-30-39'] = False
                processed['D-less-30'] = False
                # Set parent conditions - suboptimal, needs supplementation
                processed['D-optimal'] = False
                processed['quick-VitD-row'] = True
                processed['quick-vitD-simple'] = False
                processed['quick-VitD-row-takingD'] = False
            elif value >= 30:
                processed['D-60+'] = False
                processed['D-55-59'] = False
                processed['D-50-55'] = False
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = False
                processed['D-30-39'] = True
                processed['D-less-30'] = False
                # Set parent conditions - suboptimal, needs supplementation
                processed['D-optimal'] = False
                processed['quick-VitD-row'] = True
                processed['quick-vitD-simple'] = False
                processed['quick-VitD-row-takingD'] = False
            else:
                processed['D-60+'] = False
                processed['D-55-59'] = False
                processed['D-50-55'] = False
                processed['D-50-59'] = False  # Add missing template condition
                processed['D-40-49'] = False
                processed['D-30-39'] = False
                processed['D-less-30'] = True
                # Set parent conditions - very low, needs supplementation
                processed['D-optimal'] = False
                processed['quick-VitD-row'] = True
                processed['quick-vitD-simple'] = False
                processed['quick-VitD-row-takingD'] = False
        
        elif control_name == 'quick-vitE':
            if value >= 12:
                processed['VitE12'] = True
            elif value >= 8:
                processed['quick-vitE-row'] = True
            else:
                processed['quick-vitE-row-elevated'] = True
        
        elif control_name == 'quick-MagRBC':
            # Special handling for Magnesium RBC - trigger low if below optimal minimum
            if value < thresholds.get('optimal_min', 5.2):  # Below 5.2 mg/dL
                processed['quick-MagRBC-low'] = True
            else:  # 5.2 mg/dL or above
                processed['quick-MagRBC-optimal'] = True
                
            # Add specific quick-MagRBC-52 condition for values around the 5.2 threshold
            if 5.0 <= value <= 5.2:  # Borderline low range around 5.2 threshold
                processed['quick-MagRBC-52'] = True
        
        elif control_name == 'quick-selenium':
            # Special handling for Selenium - trigger low if below optimal minimum
            if value < thresholds.get('optimal_min', 125):  # Below 125 ug/L
                processed['quick-selenium-low'] = True
                
                # Specific sub-condition for very low selenium requiring CLEAR WAY COFACTORS
                if value < 110:  # Very low selenium
                    processed['quick-selen-110'] = True
            else:  # 125 ug/L or above
                processed['quick-selenium-optimal'] = True
                processed['Selenium125'] = True  # Alternative name for optimal condition
    
    def _get_comprehensive_lab_ranges(self, gender: str) -> Dict[str, Dict[str, float]]:
        """
        Get comprehensive lab ranges for intelligent threshold evaluation.
        Delegates to LabRanges configuration class.
        """
        return LabRanges.get_comprehensive_ranges(gender)
    
    def _process_genetics_comprehensive(self, lab_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process genetic markers comprehensively."""
        processed = {}
        
        # APO E Processing
        apo_e = self._get_lab_string_value(lab_results, ['APO1', 'APO E Genotyping Result'])
        genome_type = lab_results.get('genome-type', '')  # Also check for genome-type field
        
        # Use genome-type if available, otherwise use APO1
        apo_genotype = genome_type or apo_e or ''
        
        if apo_genotype:
            apo_str = str(apo_genotype).upper()
            processed['quick-ApoE'] = apo_str
            processed['genome-type'] = apo_genotype  # Store for template replacement
            
            # Set template conditions - MUTUALLY EXCLUSIVE
            if 'E4' in apo_str:
                # Has E4 variant
                processed['quick-E4'] = True
                processed['quick-nonE4'] = False
                processed['quick-apo-e4-genetics'] = True
                
                # Specific E4 variants
                if 'E4/E4' in apo_str:
                    processed['quick-E4E4'] = True
                    processed['quick-E4E3'] = False
                elif 'E4/E3' in apo_str or 'E3/E4' in apo_str:
                    processed['quick-E4E3'] = True
                    processed['quick-E4E4'] = False
                else:
                    # Other E4 combinations (E4/E2, etc.)
                    processed['quick-E4E3'] = False
                    processed['quick-E4E4'] = False
            else:
                # No E4 variant
                processed['quick-E4'] = False
                processed['quick-nonE4'] = True
                processed['quick-E4E3'] = False
                processed['quick-E4E4'] = False
                processed['quick-apo-e4-genetics'] = False
            
            # Legacy specific genotype conditions
            if 'E2/E2' in apo_str:
                processed['quick-ApoE-E2E2'] = True
            elif 'E2/E3' in apo_str:
                processed['quick-ApoE-E2E3'] = True  
            elif 'E2/E4' in apo_str:
                processed['quick-ApoE-E2E4'] = True
            elif 'E3/E3' in apo_str:
                processed['quick-ApoE-E3E3'] = True
            elif 'E3/E4' in apo_str:
                processed['quick-ApoE-E3E4'] = True
            elif 'E4/E4' in apo_str:
                processed['quick-ApoE-E4E4'] = True
        else:
            # No genetic data available
            processed['quick-E4'] = False
            processed['quick-nonE4'] = False
            processed['quick-E4E3'] = False
            processed['quick-E4E4'] = False
            processed['quick-apo-e4-genetics'] = False
        
        # MTHFR Processing
        mthfr_1 = self._get_lab_string_value(lab_results, ['MTHFR_1', 'MTHFR C677T'])
        mthfr_2 = self._get_lab_string_value(lab_results, ['MTHFR_2', 'MTHFR A1298C'])
        
        if mthfr_1:
            processed['quick-MTHFR1'] = str(mthfr_1)
            if 'Detected' in str(mthfr_1):
                processed['MTHFR-depression'] = True
                processed['methylpro'] = True
        
        if mthfr_2:
            processed['quick-MTHFR2'] = str(mthfr_2)
            if 'Detected' in str(mthfr_2):
                processed['methylpro'] = True
        
        return processed
    
    def _apply_safety_nets(self, lab_results: Dict[str, Any], hhq_responses: Dict[str, Any], 
                          client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safety nets to ensure critical content controls are always evaluated.
        This prevents any lab values from being missed in roadmap generation.
        """
        processed = {}
        
        # Ensure all vitamin D ranges are covered
        vit_d = self._get_lab_value(lab_results, ['VIT_D25', 'Vitamin D, 25-Hydroxy'])
        if vit_d:
            # Always trigger at least one vitamin D section
            if not any(key.startswith('D-') for key in processed.keys()):
                if vit_d >= 60:
                    processed['D-60+'] = True
                elif vit_d >= 55:
                    processed['D-55-59'] = True
                # else:
                #     processed['quick-VitD-row'] = True  # COMMENTED OUT - causes parent condition conflicts
        
        # Ensure HHQ-based conditions are captured
        if hhq_responses.get('hh_bariatric_surgery', False):
            processed['BariSurg'] = True
            
        if hhq_responses.get('hh_depression', False):
            processed['MTHFR-depression'] = True
            processed['quick-depression-mood-disorder'] = True
        
        # Ensure gender-specific processing
        gender = client_data.get('gender', '').lower()
        if gender in ['male', 'female']:
            processed[f'gender-{gender}'] = True
        
        return processed
    
    def _process_cbc_and_coagulation_insights(self, lab_results: Dict[str, Any], hhq_responses: Dict[str, Any], ranges: Dict) -> Dict[str, Any]:
        """Process CBC, coagulation, and other lab insights for the Other Insights section."""
        processed = {}
        
        # CBC and Anemia Assessment
        rbc = self._get_lab_value(lab_results, ['CBC_RBC', 'RBC'])
        hemoglobin = self._get_lab_value(lab_results, ['CBC_HGB', 'Hemoglobin', 'HGB'])
        hematocrit = self._get_lab_value(lab_results, ['CBC_HCT', 'Hematocrit', 'HCT'])
        platelets = self._get_lab_value(lab_results, ['CBC_PLT', 'Platelets', 'PLT'])
        mcv = self._get_lab_value(lab_results, ['CBC_MCV', 'MCV'])
        
        # Anemia risk assessment
        anemia_indicators = []
        if rbc and rbc < 4.2:
            anemia_indicators.append('low RBC')
        if hemoglobin and hemoglobin < 13.0:
            anemia_indicators.append('low hemoglobin')
        if hematocrit and hematocrit < 37:
            anemia_indicators.append('low hematocrit')
            
        if anemia_indicators:
            processed['quick-anemia'] = True
            
        # Macrocytosis assessment
        if mcv and mcv > 100:
            processed['quick-macrocytosis'] = True
            
        # D-dimer and coagulation risk
        d_dimer = self._get_lab_value(lab_results, ['DDimer', 'D_Dimer', 'D-Dimer'])
        if d_dimer and d_dimer > 500:
            processed['Coags'] = True
            processed['quick-D-Dimer'] = d_dimer
            
        # Platelet assessment and medication interactions
        if platelets and platelets < 150:
            processed['quick-platelets-low'] = True
            
            # Check for platelet-affecting medications in HHQ
            if hhq_responses:
                medications = str(hhq_responses.get('medications', '')).lower()
                platelet_meds = ['nsaid', 'ibuprofen', 'naproxen', 'aleve', 'meloxicam', 
                               'celebrex', 'aspirin', 'acid reducer', 'omeprazole', 
                               'seizure medication']
                
                if any(med in medications for med in platelet_meds):
                    processed['platelet-medication-interaction'] = True
        
        # Immune system markers
        wbc = self._get_lab_value(lab_results, ['CBC_WBC', 'WBC'])
        neutrophils = self._get_lab_value(lab_results, ['CBC_NEUT_ABS', 'Neutrophils_Abs', 'ABS_NEUT'])
        lymphocytes = self._get_lab_value(lab_results, ['CBC_LYMPH_ABS', 'Lymphocytes_Abs', 'ABS_LYMPH'])
        
        # Immune system status assessment
        immune_elevated = False
        immune_suppressed = False
        
        if wbc:
            if wbc > 11.0:
                immune_elevated = True
            elif wbc < 3.5:
                immune_suppressed = True
                
        if neutrophils:
            if neutrophils > 7.0:
                immune_elevated = True
            elif neutrophils < 1.5:
                immune_suppressed = True
                
        if lymphocytes:
            if lymphocytes > 4.0:
                immune_elevated = True
            elif lymphocytes < 1.0:
                immune_suppressed = True
                
        if immune_elevated:
            processed['quick-immune-elevated'] = True
        if immune_suppressed:
            processed['quick-immune-suppressed'] = True
            
        # Electrolyte assessment
        sodium = self._get_lab_value(lab_results, ['Sodium', 'Na'])
        potassium = self._get_lab_value(lab_results, ['Potassium', 'K'])
        chloride = self._get_lab_value(lab_results, ['Chloride', 'Cl'])
        calcium = self._get_lab_value(lab_results, ['Calcium', 'Ca'])
        
        electrolyte_abnormal = False
        if sodium and (sodium < 135 or sodium > 145):
            electrolyte_abnormal = True
        if potassium and (potassium < 3.5 or potassium > 5.1):
            electrolyte_abnormal = True
        if chloride and (chloride < 98 or chloride > 107):
            electrolyte_abnormal = True
        if calcium and (calcium < 8.5 or calcium > 10.5):
            electrolyte_abnormal = True
            
        if electrolyte_abnormal:
            processed['quick-lytes'] = True
            
        # Kidney function assessment
        egfr = self._get_lab_value(lab_results, ['eGFR', 'GFR'])
        creatinine = self._get_lab_value(lab_results, ['Creatinine', 'CREAT'])
        
        if egfr and egfr < 60:
            processed['kidney-fn'] = True
            if egfr < 30:
                processed['kidney-fn-30'] = True
        elif creatinine and creatinine > 1.3:
            processed['kidney-fn'] = True
            
        # Liver function tests
        alt = self._get_lab_value(lab_results, ['ALT', 'SGPT'])
        ast = self._get_lab_value(lab_results, ['AST', 'SGOT'])
        alk_phos = self._get_lab_value(lab_results, ['AlkPhos', 'ALP', 'Alkaline_Phosphatase'])
        
        liver_elevated = False
        if alt and alt > 40:
            liver_elevated = True
        if ast and ast > 40:
            liver_elevated = True
        if alk_phos and alk_phos > 120:
            liver_elevated = True
            
        if liver_elevated:
            processed['ALT-alcohol'] = True
            # Check if alcohol use is mentioned in HHQ
            if hhq_responses:
                alcohol_use = str(hhq_responses.get('alcohol_use', '')).lower()
                if any(term in alcohol_use for term in ['drink', 'alcohol', 'wine', 'beer', 'spirits']):
                    processed['ALT-low'] = True
                    
        # FIB-4 score calculation (simplified)
        if alt and ast and platelets:
            # This is a simplified version - actual FIB-4 requires age
            fib4_score = (40 * ast) / (platelets * (alt ** 0.5))  # Using age=40 as default
            if fib4_score > 1.5:
                processed['FIB-4-elevated'] = True
                processed['FIB-4-score'] = round(fib4_score, 2)
        
        return processed

    def _process_bmi_and_weight_insights(self, client_data: Dict[str, Any], hhq_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Process BMI and weight-related insights for the Body Weight section."""
        processed = {}
        
        # Calculate BMI if height and weight are available
        height_cm = None
        weight_kg = None
        
        # Try to get height and weight from HHQ responses first (new primary source)
        if hhq_responses:
            # Check for height from HHQ
            height_str = str(hhq_responses.get('hh-height', '')).lower().strip()
            if height_str:
                if 'cm' in height_str:
                    try:
                        height_cm = float(height_str.replace('cm', '').strip())
                    except:
                        pass
                elif 'ft' in height_str or 'feet' in height_str or '"' in height_str or "'" in height_str:
                    # Convert feet/inches to cm
                    try:
                        # Handle formats like "5'10", "5 ft 10 in", "5'10\"", etc.
                        import re
                        feet_inches = re.findall(r'(\d+)', height_str)
                        if len(feet_inches) >= 2:
                            feet = int(feet_inches[0])
                            inches = int(feet_inches[1])
                            height_cm = (feet * 12 + inches) * 2.54
                        elif len(feet_inches) == 1:
                            feet = int(feet_inches[0])
                            height_cm = feet * 12 * 2.54
                    except:
                        pass
                else:
                    # Try to parse as plain number (assume inches if >36, cm if <=36)
                    try:
                        num = float(height_str)
                        if num > 36:  # Likely inches
                            height_cm = num * 2.54
                        else:  # Likely already cm or invalid
                            height_cm = num if num > 120 else None  # Reasonable height range
                    except:
                        pass
            
            # Check for weight from HHQ
            weight_str = str(hhq_responses.get('hh-weight', '')).lower().strip()
            if weight_str:
                if 'kg' in weight_str:
                    try:
                        weight_kg = float(weight_str.replace('kg', '').strip())
                    except:
                        pass
                elif 'lb' in weight_str or 'lbs' in weight_str or 'pound' in weight_str:
                    try:
                        weight_lbs = float(weight_str.replace('lbs', '').replace('lb', '').replace('pounds', '').strip())
                        weight_kg = weight_lbs / 2.205
                    except:
                        pass
                else:
                    # Try to parse as plain number (assume lbs if >50, kg if <=50)
                    try:
                        num = float(weight_str)
                        if num > 50:  # Likely pounds
                            weight_kg = num / 2.205
                        else:  # Likely already kg or invalid
                            weight_kg = num if num > 20 else None  # Reasonable weight range
                    except:
                        pass
        
        # Fall back to legacy client_data fields if HHQ values not available
        if not height_cm and 'height' in client_data:
            try:
                height_cm = float(client_data['height'])
            except:
                pass
                
        if not weight_kg and 'weight' in client_data:
            try:
                weight_kg = float(client_data['weight'])
            except:
                pass
        
        # Calculate BMI if we have both height and weight
        bmi = None
        if height_cm and weight_kg and height_cm > 0:
            height_m = height_cm / 100
            bmi = weight_kg / (height_m * height_m)
            processed['quick-bmi'] = round(bmi, 1)
            
            # BMI-based recommendations
            if bmi >= 20 and bmi < 25:
                processed['quick-bmi20'] = True
            elif bmi >= 25:
                processed['quick-BMI-OSA'] = True  # Recommend sleep study
                
            # Additional BMI categories
            if bmi < 18.5:
                processed['quick-bmi-underweight'] = True
            elif bmi >= 30:
                processed['quick-bmi-obese'] = True
                
        return processed

    def _process_risk_profile_insights(self, hhq_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Process risk profile analysis for the Other Insights section."""
        processed = {}
        
        if not hhq_responses:
            return processed
            
        # Initialize risk factor mapper
        risk_mapper = RiskFactorMapper()
        
        # Calculate risk scores
        risk_scores = risk_mapper.calculate_risk_scores(hhq_responses)
        risk_percentages = risk_mapper.calculate_risk_percentages(risk_scores)
        risk_details = risk_mapper.get_risk_factor_details(hhq_responses)
        
        # Only generate risk profile if there are actual risk factors
        total_risk = sum(risk_scores.values())
        if total_risk > 0:
            processed['risk-profile-generated'] = True
            
            # Calculate percentages 
            for category, percentage in risk_percentages.items():
                processed[f'risk-{category}-percentage'] = round(percentage, 1)
                
            # Get details for each category
            for category, factors_list in risk_details.items():
                if factors_list:
                    processed[f'risk-{category}-details'] = ', '.join(factors_list)
                    processed[f'risk-{category}-factors'] = ', '.join(factors_list)
                    
            # Set high risk flags (>10% of total risk or >1.0 raw score)
            for category, score in risk_scores.items():
                if score >= 1.0 or risk_percentages[category] >= 10.0:
                    processed[f'risk-{category}-high'] = True
                    
            # Get top 3 risk categories for recommendations
            top_risks = risk_mapper.get_top_risk_factors(risk_percentages, 3)
            for i, (category, percentage) in enumerate(top_risks, 1):
                processed[f'top-risk-category-{i}'] = category.title()
                processed[f'top-risk-percentage-{i}'] = round(percentage, 1)
                
            if len(top_risks) > 0:
                processed['risk-profile-recommendations'] = True
        
        # Trigger autoimmune section for inflammatory conditions (always evaluate)
        autoimmune_triggered = (
            risk_scores.get('inflammatory', 0) >= 1.0 or 
            any(hhq_responses.get(condition, False) for condition in [
                'hh-autoimmune-disease', 'hh-arthritis', 'hh-inflammatory-bowel',
                'hh-crohns-disease', 'hh-ulcerative-colitis', 'hh-celiac-disease',
                'hh-chronic-allergies', 'hh-hashimotos', 'hh-lupus', 'hh-multiple-sclerosis'
            ])
        )
        processed['autoimmune-disease-section'] = autoimmune_triggered
        
        # Trigger chronic headaches section for headache/migraine conditions
        headaches_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-chronic-headaches', 'hh-migraines', 'hh-frequent-headaches', 
            'hh-headaches', 'hh-migraine-headaches', 'hh-vascular-headaches',
            'hh-tension-headaches', 'hh-cluster-headaches'
        ])
        processed['quick-headaches'] = headaches_triggered
        
        # Trigger multiple allergies section for allergy/immune conditions
        allergies_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-chronic-allergies', 'hh-multiple-allergies', 'hh-environmental-allergies',
            'hh-food-allergies', 'hh-chemical-sensitivities', 'hh-multiple-chemical-sensitivity',
            'hh-histamine-intolerance', 'hh-chronic-rashes', 'hh-allergic-reactions',
            'hh-seasonal-allergies', 'hh-sinus-congestion', 'hh-chronic-sinusitis'
        ])
        processed['quick-multiple-allergies'] = allergies_triggered
        
        # Trigger gallbladder section for gallbladder removal history
        gallbladder_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-gallbladder-removal', 'hh-gallbladder-surgery', 'hh-cholecystectomy',
            'hh-gallbladder-disease', 'hh-bile-duct-issues', 'hh-gallstones'
        ])
        processed['quick-gallbladder-header'] = gallbladder_triggered
        
        # Trigger Parkinson's section for Parkinson's disease
        parkinsons_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-parkinsons', 'hh-parkinsons-disease', 'hh-parkinson-disease',
            'hh-movement-disorder', 'hh-tremor', 'hh-bradykinesia'
        ])
        processed['quick-parkinsons'] = parkinsons_triggered
        
        # Trigger GI health section for gastrointestinal conditions
        gi_health_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-ibs', 'hh-irritable-bowel', 'hh-acid-reflux', 'hh-gerd', 
            'hh-leaky-gut', 'hh-digestive-issues', 'hh-constipation', 'hh-diarrhea',
            'hh-bloating', 'hh-gas', 'hh-food-sensitivities', 'hh-food-allergies',
            'hh-inflammatory-bowel', 'hh-crohns', 'hh-ulcerative-colitis',
            'hh-celiac', 'hh-gluten-sensitivity', 'hh-microbiome-issues',
            'hh-sibo', 'hh-candida', 'hh-stomach-pain', 'hh-nausea',
            'hh-surgical-weight-loss', 'hh-bariatric-surgery'
        ])
        processed['quick-GI-health'] = gi_health_triggered
        
        # Trigger constipation section for constipation-related conditions
        constipation_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-constipation', 'hh-chronic-constipation', 'hh-bowel-problems',
            'hh-irregular-bowel', 'hh-hard-stools', 'hh-infrequent-bowel',
            'hh-bowel-dysfunction', 'hh-elimination-issues'
        ])
        processed['quick-constipation'] = constipation_triggered
        
        # Trigger HSV section for herpes simplex virus conditions
        hsv_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-hsv', 'hh-herpes', 'hh-cold-sores', 'hh-herpes-simplex',
            'hh-hsv1', 'hh-hsv2', 'hh-viral-outbreaks', 'hh-chronic-viral-infections',
            'hh-recurrent-cold-sores', 'hh-oral-herpes', 'hh-genital-herpes',
            'hh-viral-encephalitis', 'hh-frequent-cold-sores'
        ])
        processed['quick-HSV'] = hsv_triggered
        
        # Trigger EBV section for Epstein Barr Virus conditions
        ebv_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-ebv', 'hh-epstein-barr', 'hh-epstein-barr-virus', 'hh-mono',
            'hh-mononucleosis', 'hh-chronic-fatigue', 'hh-ebv-reactivation',
            'hh-chronic-ebv', 'hh-swollen-lymph-nodes', 'hh-chronic-sore-throat',
            'hh-low-grade-fever', 'hh-chronic-infections', 'hh-immune-suppression',
            'hh-viral-syndrome', 'hh-chronic-viral-infection', 'hh-reactivated-ebv'
        ])
        processed['quick-EBV'] = ebv_triggered
        
        # Trigger toxicity section for toxicity-related conditions and general health optimization
        toxicity_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-chemical-exposure', 'hh-heavy-metals', 'hh-mold-exposure', 'hh-environmental-toxins',
            'hh-pesticide-exposure', 'hh-lead-exposure', 'hh-mercury-exposure', 'hh-arsenic-exposure',
            'hh-cadmium-exposure', 'hh-aluminum-exposure', 'hh-chemical-sensitivity',
            'hh-multiple-chemical-sensitivity', 'hh-toxic-exposure', 'hh-occupational-exposure',
            'hh-dental-amalgams', 'hh-gallbladder-removal', 'hh-gallbladder-surgery',
            'hh-gallbladder-problems', 'hh-bile-dysfunction', 'hh-detox-problems',
            'hh-liver-problems', 'hh-chronic-fatigue', 'hh-brain-fog', 'hh-memory-problems'
        ]) or True  # Show for everyone as part of general health optimization
        processed['toxicity-real'] = toxicity_triggered
        
        # Trigger quick-GDX section for gallbladder-related conditions
        gdx_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-gallbladder-removal', 'hh-gallbladder-surgery', 'hh-cholecystectomy',
            'hh-gallbladder-problems', 'hh-gall-stones', 'hh-gallstones',
            'hh-bile-dysfunction', 'hh-bile-problems', 'hh-gallbladder-disease'
        ])
        processed['quick-GDX'] = gdx_triggered
        
        # Trigger quick-GBDx section for gallbladder-related conditions
        gbdx_triggered = any(hhq_responses.get(condition, False) for condition in [
            'hh-gallbladder-removal', 'hh-gallbladder-surgery', 'hh-cholecystectomy',
            'hh-gallbladder-problems', 'hh-gall-stones', 'hh-gallstones',
            'hh-bile-dysfunction', 'hh-bile-problems', 'hh-gallbladder-disease'
        ])
        processed['quick-GBDx'] = gbdx_triggered
        
        return processed

# Usage example
if __name__ == "__main__":
    # Example usage
    generator = RoadmapGenerator()
    
    # Sample client data
    client_data = {
        'name': 'John Doe',
        'gender': 'male',
        'dob': '1980-01-01'
    }
    
    # Sample lab results
    lab_results = {
        'APO1': 'E3/E4',
        'METAB_GLUT': 250,
        'VIT_D25': 45,
        'INFLAM_CRP': 2.5
    }
    
    # Generate roadmap
    roadmap = generator.generate_roadmap(client_data, lab_results)
    print(roadmap[:500] + "...") 
