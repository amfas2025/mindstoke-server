"""
Lab field mappings for Mind Stoke roadmap generator.
Maps internal lab keys to display names used in LabCorp reports.
"""

LAB_MAPPINGS = {
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