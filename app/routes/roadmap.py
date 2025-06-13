from flask import Blueprint, flash, redirect, url_for, render_template, request, make_response, current_app, send_file
from flask_login import login_required, current_user
from app.models import Client, LabResult, HHQResponse, db
from app.utils.supabase_client import fetch_client_by_id, fetch_lab_results_for_client, fetch_hhq_responses_dict, get_supabase_client
from roadmap_generator import RoadmapGenerator
from datetime import datetime, timedelta
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

bp = Blueprint('roadmap', __name__, url_prefix='/roadmap')

@bp.route('/generate/<client_id>')
@login_required
def generate(client_id):
    """Generate and display roadmap for a client."""
    try:
        # Fetch client data
        client = fetch_client_by_id(client_id)
        if not client:
            flash('Client not found.', 'error')
            return redirect(url_for('clients.view', id=client_id))
        
        # Check if all required data is present
        lab_results = fetch_lab_results_for_client(client_id)
        hhq_responses = fetch_hhq_responses_dict(client_id)
        
        current_app.logger.info(f"Lab results count: {len(lab_results) if lab_results else 0}")
        current_app.logger.info(f"HHQ responses count: {len(hhq_responses) if hhq_responses else 0}")
        
        if not lab_results:
            flash('Lab results are required to generate a roadmap. Please upload lab results first.', 'warning')
            return redirect(url_for('clients.view', id=client_id))
        
        # Temporarily remove HHQ requirement to isolate the issue
        # if not hhq_responses:
        #     flash('HHQ responses are required to generate a roadmap. Please complete the HHQ first.', 'warning')
        #     return redirect(url_for('clients.view', id=client_id))
        
        # Set empty HHQ responses if None
        if not hhq_responses:
            hhq_responses = {}
        
        # Prepare client data for roadmap generator
        client_data = {
            'name': f"{client.get('first_name', '')} {client.get('last_name', '')}".strip(),
            'gender': client.get('sex', ''),
            'dob': client.get('date_of_birth'),
            'labs_date': datetime.now().strftime('%B %d, %Y')  # Default to today if not specified
        }
        
        # Convert lab results to expected format (armgasys variable names)
        lab_data = {}
        if lab_results:
            for result in lab_results:
                # Prefer the already-mapped Armgasys variable from Supabase
                armgasys_var = result.get('armgasys_variable', '')
                value = result.get('value', '')

                # Convert string values to float where possible, but keep genetics strings
                try:
                    numeric_value = float(value) if value and str(value).replace('.', '').replace('-', '').isdigit() else value
                except (ValueError, TypeError):
                    numeric_value = value

                if armgasys_var:
                    lab_data[armgasys_var.upper()] = numeric_value
                    continue  # Skip manual mapping if we used the pre-mapped variable

                # Fallback: Map common lab names to Armgasys variables if armgasys_variable missing
                lab_name = result.get('test_name', '')
                lab_mapping = {
                    'WBC': 'CBC_WBC',
                    'RBC': 'CBC_RBC',
                    'Hemoglobin': 'CBC_HGB',
                    'Hematocrit': 'CBC_HCT',
                    'MCV': 'CBC_MCV',
                    'Platelets': 'CBC_PLT',
                    'Neutrophils (Absolute)': 'CBC_NEUT_ABS',
                    'Lymphs (Absolute)': 'CBC_LYMPH_ABS',
                    'Glucose': 'CHEM_GLU',
                    'BUN': 'CHEM_BUN',
                    'Creatinine': 'CHEM_CREAT',
                    'eGFR': 'CHEM_EGFR',
                    'Sodium': 'CHEM_NA',
                    'Potassium': 'CHEM_K',
                    'Chloride': 'CHEM_CL',
                    'Calcium': 'CHEM_CA',
                    'Albumin': 'LFT_ALB',
                    'ALT (SGPT)': 'LFT_ALT',
                    'AST (SGOT)': 'LFT_AST',
                    'Alkaline Phosphatase': 'LFT_ALKP',
                    'Bilirubin, Total': 'LFT_TBILI',
                    'Cholesterol, Total': 'LIPID_CHOL',
                    'Triglycerides': 'LIPID_TRIG',
                    'HDL Cholesterol': 'LIPID_HDL',
                    'LDL Chol Calc (NIH)': 'LIPID_LDL',
                    'Free Testosterone': 'MHt_TEST_FREE',
                    'Testosterone, Total, LC/MS': 'MHt_TEST_TOT',
                    'Prostate Specific Ag': 'MHt_PSA',
                    'TSH': 'THY_TSH',
                    'Triiodothyronine (T3), Free': 'THY_T3F',
                    'T4, Free (Direct)': 'THY_T4F',
                    'Thyroglobulin Antibody': 'THY_TGAB',
                    'Pregnenolone, MS': 'NEURO_PREG',
                    'DHEA-Sulfate': 'NEURO_DHEAS',
                    'Vitamin D, 25-Hydroxy': 'VIT_D25',
                    'Vitamin B12': 'VIT_B12',
                    'Vitamin E (Alpha Tocopherol)': 'VIT_E',
                    'Zinc, Plasma or Serum': 'MIN_ZN',
                    'Copper, Serum or Plasma': 'MIN_CU',
                    'Selenium, Serum/Plasma': 'MIN_SE',
                    'Magnesium, RBC': 'MIN_MG_RBC',
                    'C-Reactive Protein, Cardiac': 'INFLAM_CRP',
                    'Uric Acid': 'INFLAM_URIC',
                    'Homocyst(e)ine': 'INFLAM_HOMOCYS',
                    'Insulin': 'METAB_INS',
                    'Hemoglobin A1c': 'METAB_HBA1C',
                    'Total Glutathione': 'METAB_GLUT',
                    'OmegaCheck(TM)': 'OMEGA_CHECK',
                    'Omega-6/Omega-3 Ratio': 'OMEGA_6_3_RATIO',
                    'Omega-3 total': 'OMEGA_3_TOT',
                    'Omega-6 total': 'OMEGA_6_TOT',
                    'Arachidonic Acid': 'OMEGA_AA',
                    'Arachidonic Acid/EPA Ratio': 'OMEGA_AA_EPA',
                    'APO E Genot E2/E4': 'APO1',  # Fall back mapping for specific test name variant
                    'APO E Genotyping Result': 'APO1',
                    'MTHFR C677T': 'MTHFR_1',
                    'MTHFR A1298C': 'MTHFR_2'
                }
                mapped_name = lab_mapping.get(lab_name, lab_name)
                lab_data[mapped_name.upper()] = numeric_value
        
        # Normalize keys to uppercase for consistency
        lab_data = {k.upper(): v for k, v in lab_data.items()}
        
        # Initialize roadmap generator and process content controls
        current_app.logger.info("About to create RoadmapGenerator")
        generator = RoadmapGenerator()
        current_app.logger.info("RoadmapGenerator created successfully")
        
        # Generate roadmap content (this already processes all content controls internally)
        current_app.logger.info("About to generate roadmap content")
        roadmap_content = generator.generate_roadmap(
            client_data=client_data,
            lab_results=lab_data,
            hhq_responses=hhq_responses
        )
        current_app.logger.info("Roadmap content generated successfully")
        
        # Generate timestamp and supplementary data
        generated_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        # Extract supplement recommendations from roadmap content
        supplements = _extract_supplements_from_roadmap(roadmap_content)
        
        current_app.logger.info("About to render template")
        return render_template('roadmap/roadmap_display.html',
                             client=client,
                             roadmap_content=roadmap_content,
                             generated_date=generated_date,
                             supplements=supplements)
        
    except Exception as e:
        current_app.logger.error(f"Error generating roadmap for client {client_id}: {str(e)}")
        flash(f'Error generating roadmap: {str(e)}', 'error')
        return redirect(url_for('clients.view', id=client_id))

@bp.route('/summary/<client_id>')
@login_required
def roadmap_summary(client_id):
    """Display roadmap summary for a client."""
    try:
        client = fetch_client_by_id(client_id)
        if not client:
            flash('Client not found.', 'error')
            return redirect(url_for('clients.view', id=client_id))
        
        # Get lab results and create key findings
        lab_results = fetch_lab_results_for_client(client_id)
        key_findings = _generate_key_findings(lab_results)
        
        # Get HHQ responses and create priority interventions
        hhq_responses = fetch_hhq_responses_dict(client_id)
        priority_interventions = _generate_priority_interventions(hhq_responses)
        
        # Get supplement recommendations
        supplements = _get_supplement_recommendations(lab_results, hhq_responses)
        
        return render_template('roadmap/roadmap_summary.html',
                             client=client,
                             key_findings=key_findings,
                             priority_interventions=priority_interventions,
                             supplements=supplements)
        
    except Exception as e:
        current_app.logger.error(f"Error generating roadmap summary for client {client_id}: {str(e)}")
        flash(f'Error generating roadmap summary: {str(e)}', 'error')
        return redirect(url_for('clients.view', id=client_id))

@bp.route('/download_visual_pdf/<client_id>')
def download_visual_roadmap_pdf(client_id):
    """Download a visually enhanced roadmap PDF with images"""
    try:
        supabase = get_supabase_client()
        
        # Get client data
        client_result = supabase.table('clients').select('*').eq('id', client_id).execute()
        if not client_result.data:
            flash('Client not found', 'error')
            return redirect(url_for('clients.list'))
        
        client = client_result.data[0]
        
        # Get lab results
        lab_results_result = supabase.table('lab_results').select('*').eq('client_id', client_id).execute()
        lab_results_dict = {}
        if lab_results_result.data:
            for result in lab_results_result.data:
                if result.get('armgasys_variable'):
                    lab_results_dict[result['armgasys_variable']] = result.get('value')
        
        # Get HHQ responses
        hhq_result = supabase.table('hhq_responses').select('*').eq('client_id', client_id).execute()
        hhq_responses = {}
        if hhq_result.data:
            for response in hhq_result.data:
                if response.get('tag'):
                    hhq_responses[response['tag']] = response.get('response')
        
        # Prepare client data
        client_data = {
            'name': f"{client.get('first_name', '')} {client.get('last_name', '')}".strip(),
            'gender': client.get('sex'),
            'dob': client.get('date_of_birth'),
            'labs_date': 'Recent'
        }
        
        # Generate visual PDF
        generator = RoadmapGenerator()
        pdf_path = generator.generate_visual_pdf(client_data, lab_results_dict, hhq_responses)
        
        # Send the PDF file
        return send_file(pdf_path, 
                        as_attachment=True, 
                        download_name=f"visual_roadmap_{client_data['name'].replace(' ', '_')}.pdf",
                        mimetype='application/pdf')
        
    except Exception as e:
        current_app.logger.error(f"Error generating visual PDF for client {client_id}: {str(e)}")
        flash('Error generating visual roadmap PDF', 'error')
        return redirect(url_for('clients.view', id=client_id))

@bp.route('/debug/<client_id>')
@login_required
def debug_roadmap(client_id):
    """Debug endpoint to show roadmap processing details."""
    try:
        # Fetch client data
        client = fetch_client_by_id(client_id)
        if not client:
            return {'error': 'Client not found'}, 404
        
        # Get lab results and HHQ
        lab_results = fetch_lab_results_for_client(client_id)
        hhq_responses = fetch_hhq_responses_dict(client_id)
        
        # Prepare client data
        client_data = {
            'name': f"{client.get('first_name', '')} {client.get('last_name', '')}".strip(),
            'gender': client.get('sex', ''),
            'dob': client.get('date_of_birth'),
            'labs_date': datetime.now().strftime('%B %d, %Y')
        }
        
        # Convert lab results to expected format
        lab_data = {}
        if lab_results:
            for result in lab_results:
                # Prefer the already-mapped Armgasys variable from Supabase
                armgasys_var = result.get('armgasys_variable', '')
                value = result.get('value', '')

                # Convert string values to float where possible, but keep genetics strings
                try:
                    numeric_value = float(value) if value and str(value).replace('.', '').replace('-', '').isdigit() else value
                except (ValueError, TypeError):
                    numeric_value = value

                if armgasys_var:
                    lab_data[armgasys_var.upper()] = numeric_value
                    continue  # Skip manual mapping if we used the pre-mapped variable

                # Fallback: Map common lab names to Armgasys variables if armgasys_variable missing
                lab_name = result.get('test_name', '')
                lab_mapping = {
                    'WBC': 'CBC_WBC',
                    'RBC': 'CBC_RBC',
                    'Hemoglobin': 'CBC_HGB',
                    'Hematocrit': 'CBC_HCT',
                    'MCV': 'CBC_MCV',
                    'Platelets': 'CBC_PLT',
                    'Neutrophils (Absolute)': 'CBC_NEUT_ABS',
                    'Lymphs (Absolute)': 'CBC_LYMPH_ABS',
                    'Glucose': 'CHEM_GLU',
                    'BUN': 'CHEM_BUN',
                    'Creatinine': 'CHEM_CREAT',
                    'eGFR': 'CHEM_EGFR',
                    'Sodium': 'CHEM_NA',
                    'Potassium': 'CHEM_K',
                    'Chloride': 'CHEM_CL',
                    'Calcium': 'CHEM_CA',
                    'Albumin': 'LFT_ALB',
                    'ALT (SGPT)': 'LFT_ALT',
                    'AST (SGOT)': 'LFT_AST',
                    'Alkaline Phosphatase': 'LFT_ALKP',
                    'Bilirubin, Total': 'LFT_TBILI',
                    'Cholesterol, Total': 'LIPID_CHOL',
                    'Triglycerides': 'LIPID_TRIG',
                    'HDL Cholesterol': 'LIPID_HDL',
                    'LDL Chol Calc (NIH)': 'LIPID_LDL',
                    'Free Testosterone': 'MHt_TEST_FREE',
                    'Testosterone, Total, LC/MS': 'MHt_TEST_TOT',
                    'Prostate Specific Ag': 'MHt_PSA',
                    'TSH': 'THY_TSH',
                    'Triiodothyronine (T3), Free': 'THY_T3F',
                    'T4, Free (Direct)': 'THY_T4F',
                    'Thyroglobulin Antibody': 'THY_TGAB',
                    'Pregnenolone, MS': 'NEURO_PREG',
                    'DHEA-Sulfate': 'NEURO_DHEAS',
                    'Vitamin D, 25-Hydroxy': 'VIT_D25',
                    'Vitamin B12': 'VIT_B12',
                    'Vitamin E (Alpha Tocopherol)': 'VIT_E',
                    'Zinc, Plasma or Serum': 'MIN_ZN',
                    'Copper, Serum or Plasma': 'MIN_CU',
                    'Selenium, Serum/Plasma': 'MIN_SE',
                    'Magnesium, RBC': 'MIN_MG_RBC',
                    'C-Reactive Protein, Cardiac': 'INFLAM_CRP',
                    'Uric Acid': 'INFLAM_URIC',
                    'Homocyst(e)ine': 'INFLAM_HOMOCYS',
                    'Insulin': 'METAB_INS',
                    'Hemoglobin A1c': 'METAB_HBA1C',
                    'Total Glutathione': 'METAB_GLUT',
                    'OmegaCheck(TM)': 'OMEGA_CHECK',
                    'Omega-6/Omega-3 Ratio': 'OMEGA_6_3_RATIO',
                    'Omega-3 total': 'OMEGA_3_TOT',
                    'Omega-6 total': 'OMEGA_6_TOT',
                    'Arachidonic Acid': 'OMEGA_AA',
                    'Arachidonic Acid/EPA Ratio': 'OMEGA_AA_EPA',
                    'APO E Genot E2/E4': 'APO1',  # Fall back mapping for specific test name variant
                    'APO E Genotyping Result': 'APO1',
                    'MTHFR C677T': 'MTHFR_1',
                    'MTHFR A1298C': 'MTHFR_2'
                }
                mapped_name = lab_mapping.get(lab_name, lab_name)
                lab_data[mapped_name.upper()] = numeric_value
        
        # Normalize keys to uppercase for consistency
        lab_data = {k.upper(): v for k, v in lab_data.items()}
        
        # Initialize roadmap generator
        generator = RoadmapGenerator()
        
        # Get processed content controls
        processed_content = generator._process_all_content_controls(client_data, lab_data, hhq_responses)
        
        # Generate roadmap content
        roadmap_content = generator.generate_roadmap(
            client_data=client_data,
            lab_results=lab_data,
            hhq_responses=hhq_responses
        )
        
        # Create debug response
        debug_data = {
            'client_data': client_data,
            'lab_count': len(lab_data),
            'hhq_count': len(hhq_responses),
            'processed_controls_count': len(processed_content),
            'processed_controls': processed_content,
            'lab_data_sample': dict(list(lab_data.items())[:10]) if lab_data else {},
            'hhq_sample': dict(list(hhq_responses.items())[:10]) if hhq_responses else {},
            'roadmap_length': len(roadmap_content),
            'roadmap_sample': roadmap_content[:1000] + '...' if len(roadmap_content) > 1000 else roadmap_content,
            'remaining_placeholders': roadmap_content.count('{{') if roadmap_content else 0
        }
        
        return render_template('roadmap/debug.html', debug_data=debug_data)
        
    except Exception as e:
        current_app.logger.error(f"Error in debug roadmap for client {client_id}: {str(e)}")
        return {'error': str(e)}, 500

def _extract_supplements_from_roadmap(content):
    """Extract supplement recommendations from roadmap content."""
    supplements = []
    lines = content.split('\n')
    
    for line in lines:
        if 'supplement' in line.lower() or 'capsule' in line.lower() or 'mg' in line.lower():
            if 'consider starting' in line.lower() or 'recommended' in line.lower():
                supplements.append({
                    'name': line.strip(),
                    'description': 'See roadmap for detailed dosing instructions.'
                })
    
    return supplements[:10]  # Limit to 10 supplements

def _generate_key_findings(lab_results):
    """Generate key lab findings from results."""
    findings = []
    
    if not lab_results:
        return findings
    
    for result in lab_results:
        test_name = result.get('test_name', '')
        value = result.get('value', '')
        reference_range = result.get('reference_range', '')
        
        # Simple logic to identify potentially concerning values
        if 'vitamin d' in test_name.lower():
            try:
                val = float(value)
                if val < 30:
                    findings.append({
                        'finding': f'{test_name}: {value}',
                        'significance': 'Below optimal range for brain health',
                        'category': 'Vitamins',
                        'priority': 'high'
                    })
            except:
                pass
        
        if 'homocyst' in test_name.lower():
            try:
                val = float(value)
                if val > 7:
                    findings.append({
                        'finding': f'{test_name}: {value}',
                        'significance': 'Elevated inflammatory marker',
                        'category': 'Inflammation',
                        'priority': 'medium'
                    })
            except:
                pass
    
    return findings[:5]  # Limit to 5 key findings

def _generate_priority_interventions(hhq_responses):
    """Generate priority interventions based on HHQ responses."""
    interventions = []
    
    if not hhq_responses:
        return interventions
    
    # Basic intervention logic based on common HHQ responses
    if hhq_responses.get('hh-brain_fog'):
        interventions.append({
            'priority': 1,
            'category': 'Cognitive Health',
            'intervention': 'Address Brain Fog',
            'description': 'Implement anti-inflammatory diet and targeted supplements'
        })
    
    if hhq_responses.get('hh-sleep_issues'):
        interventions.append({
            'priority': 2,
            'category': 'Sleep Optimization',
            'intervention': 'Improve Sleep Quality',
            'description': 'Sleep hygiene protocols and potential supplement support'
        })
    
    return interventions

def _get_supplement_recommendations(lab_results, hhq_responses):
    """Get basic supplement recommendations."""
    supplements = [
        'Omega-3 Fish Oil',
        'Vitamin D3',
        'Magnesium Glycinate',
        'B-Complex Vitamin',
        'Probiotics'
    ]
    
    return supplements[:5]  # Return first 5 