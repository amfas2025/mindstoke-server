# Lab Mapping Utility
# Maps extracted LabCorp test names to Armgasys variable names

# Complete mapping dictionary from extracted names to Armgasys variables
LAB_NAME_MAPPING = {
    # Complete Blood Count (CBC)
    "WBC": "CBC_WBC",
    "Neutrophils (Absolute)": "CBC_ANC",
    "Lymphs (Absolute)": "CBC_ALC",
    "RBC": "CBC_RBC",
    "Hemoglobin": "CBC_Hb",
    "Hematocrit": "CBC_HCT",
    "Platelets": "CBC_Plt",
    "MCV": "CBC_MCV",
    
    # Metabolic Panel (CMP)
    "Glucose": "MBP_Gluc",
    "Sodium": "MBP_Na+",
    "Potassium": "MBP_K+",
    "Chloride": "MBP_Cl-",
    "Calcium": "MBP_Ca++",
    "BUN": "MBP_BUN",
    "Creatinine": "lab-creatinine",
    "eGFR": "MBP_eGFR",
    "Alkaline Phosphatase": "MBP_Alk-Phos",
    "ALT (SGPT)": "MBP_ALT",
    "AST (SGOT)": "MBP_AST",
    "Albumin": "MBP_Album",
    "Bilirubin, Total": "MPS_Bilirubin",
    
    # Cardiovascular
    "Cholesterol, Total": "TC",
    "Triglycerides": "Trig",
    "HDL Cholesterol": "HDL",
    "LDL Chol Calc (NIH)": "LDL",
    
    # Thyroid Testing
    "TSH": "TSH",
    "Triiodothyronine (T3), Free": "FT3",
    "T4, Free (Direct)": "FT4",
    "Thyroglobulin Antibody": "Tg-Ab",
    
    # Diabetes
    "Insulin": "Insul",
    "Hemoglobin A1c": "A1c",
    
    # Homocysteine
    "Homocyst(e)ine": "Homocyst(e)ine",
    "Vitamin B12": "B12",
    
    # Inflammatory Markers
    "C-Reactive Protein, Cardiac": "C-Reactive-Protein,-Cardiac",
    
    # Basic Toxin Screen
    "Uric Acid": "BTS_UricAcid",
    "Total Glutathione": "Serum-glutathione",
    
    # Nutrient Testing
    "Vitamin D, 25-Hydroxy": "25OHVitD",
    "Vitamin E (Alpha Tocopherol)": "VitE",
    "Magnesium, RBC": "Magnesium,-RBC",
    "OmegaCheck(TM)": "OmegaCheck",
    "Omega-6/Omega-3 Ratio": "Omega6-3",
    "Omega-6 total": "Omega-6-Total",
    "Omega-3 total": "Omega-3-Total",
    "Arachidonic Acid/EPA Ratio": "Arachidonic-Acid/EPA-Ratio",
    "Arachidonic Acid": "ArachAcid",
    
    # Metals and Antioxidants
    "Copper, Serum or Plasma": "Copper",
    "Zinc, Plasma or Serum": "Zinc",
    "Selenium, Serum/Plasma": "Selen",
    
    # Neuro/Adrenal Hormones
    "Pregnenolone, MS": "PREGNENCL",
    "Cortisol - AM": "Cortisol-AM",
    
    # Male-specific tests  
    "Free Testosterone": "FreeTest",
    "Testosterone, Total, LC/MS": "TotalTest-LCMS",
    "Prostate Specific Ag": "PSA",
    
    # Genetics
    "MTHFR C677T": "MTHFR_1",
    "MTHFR A1298C": "MTHFR_2",
}

# Gender-specific hormone mapping
MALE_HORMONE_MAPPING = {
    "FSH": "MeHt_FSH",
    "Testosterone": "MeHt_TT",
    "Estradiol": "MeHt_E2",
    "DHEA-Sulfate": "MeHt_DHEA",
}

FEMALE_HORMONE_MAPPING = {
    "FSH": "FHt_FSH",
    "Estradiol": "FHt_EST",
    "DHEA-Sulfate": "FHt_DHEA",
    "Testosterone": "FHt_TT",  # Women also have testosterone
}

def map_lab_name_to_armgasys(test_name, client_gender="unknown"):
    """
    Map extracted lab test name to Armgasys variable name.
    
    Args:
        test_name (str): Original extracted test name
        client_gender (str): "male", "female", or "unknown"
    
    Returns:
        str: Armgasys variable name or None if no mapping found
    """
    # Check standard mapping first
    if test_name in LAB_NAME_MAPPING:
        return LAB_NAME_MAPPING[test_name]
    
    # Check gender-specific hormone mapping
    if client_gender.lower() == "male" and test_name in MALE_HORMONE_MAPPING:
        return MALE_HORMONE_MAPPING[test_name]
    elif client_gender.lower() == "female" and test_name in FEMALE_HORMONE_MAPPING:
        return FEMALE_HORMONE_MAPPING[test_name]
    
    # Default to male hormones if gender unknown
    elif client_gender.lower() == "unknown" and test_name in MALE_HORMONE_MAPPING:
        return MALE_HORMONE_MAPPING[test_name]
    
    return None

def map_special_values(test_name, value, client_gender="unknown"):
    """
    Handle special value mappings like APO E genotyping.
    
    Returns:
        list: List of (variable_name, mapped_value) tuples
    """
    results = []
    
    if test_name == "APO E Genotyping Result":
        # Handle APO E special mapping - split into APO1 and APO2 fields
        value_str = str(value).upper().strip()
        
        # Parse the genotype (e.g., "E2/E4", "E3/E3", "E3/E4")
        if "/" in value_str:
            alleles = value_str.split("/")
            if len(alleles) == 2:
                apo1 = alleles[0].strip()
                apo2 = alleles[1].strip()
                
                results.append(("APO1", apo1))
                results.append(("APO2", apo2))
            else:
                # Fallback if format is unexpected
                results.append(("APO1", value_str))
                results.append(("APO2", ""))
        else:
            # Single value or unexpected format
            results.append(("APO1", value_str))
            results.append(("APO2", ""))
    
    elif test_name in ["MTHFR C677T", "MTHFR A1298C"]:
        # Handle MTHFR results
        value_str = str(value).upper()
        if "NOT DETECTED" in value_str or "NORMAL" in value_str:
            mapped_value = "normal"
        elif "DETECTED" in value_str or "HETEROZYGOUS" in value_str:
            mapped_value = "heterozygous"
        elif "HOMOZYGOUS" in value_str:
            mapped_value = "homozygous"
        else:
            mapped_value = value_str.lower()
        
        variable_name = LAB_NAME_MAPPING.get(test_name)
        if variable_name:
            results.append((variable_name, mapped_value))
    
    return results

def get_all_mapped_results(lab_results, client_gender="unknown"):
    """
    Process all lab results and return mapped data for Armgasys.
    
    Args:
        lab_results (dict): Dictionary of {test_name: value} from extraction
        client_gender (str): Client's gender for hormone mapping
    
    Returns:
        list: List of dictionaries ready for database insertion
    """
    mapped_results = []
    
    for test_name, result_data in lab_results.items():
        # Extract value and metadata
        if isinstance(result_data, dict):
            value = result_data.get('value', '')
            unit = result_data.get('unit', '')
            reference_range = result_data.get('reference_range', '')
        else:
            value = str(result_data)
            unit = ''
            reference_range = ''
        
        # Try special value mapping first (APO E, MTHFR)
        mapped_entries = map_special_values(test_name, value, client_gender)
        
        if mapped_entries:
            # Handle special mappings
            for armgasys_var, armgasys_value in mapped_entries:
                mapped_results.append({
                    'original_test_name': test_name,
                    'original_value': str(value),
                    'unit': unit,
                    'reference_range': reference_range,
                    'armgasys_variable_name': armgasys_var,
                    'armgasys_value': armgasys_value
                })
        else:
            # Handle regular lab mappings
            armgasys_var = map_lab_name_to_armgasys(test_name, client_gender)
            if armgasys_var:
                mapped_results.append({
                    'original_test_name': test_name,
                    'original_value': str(value),
                    'unit': unit,
                    'reference_range': reference_range,
                    'armgasys_variable_name': armgasys_var,
                    'armgasys_value': str(value)
                })
    
    return mapped_results 