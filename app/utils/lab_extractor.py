import pdfplumber
import re
import pandas as pd
import os
from datetime import datetime
from typing import Dict, List

# Configuration
INPUT_DIR = "client_labs/"  # Directory containing client PDFs
OUTPUT_DIR = "extracted_results/"  # Directory for output CSVs

# Define the lab tests, including all required tests
lab_tests = [
    "Albumin",
    "Alkaline Phosphatase",
    "ALT (SGPT)",
    "APO E Genotyping Result",
    "Arachidonic Acid",
    "Arachidonic Acid/EPA Ratio",
    "AST (SGOT)",
    "Bilirubin, Total",
    "BUN",
    "C-Reactive Protein, Cardiac",
    "Calcium",
    "Chloride",
    "Cholesterol, Total",
    "Copper, Serum or Plasma",
    "Cortisol - AM",
    "Creatinine",
    "DHEA-Sulfate",
    "eGFR",
    "Estradiol",
    "Folate (Folic Acid), Serum",
    "Free Testosterone",
    "FSH",
    "Glucose",
    "HDL Cholesterol",
    "Hematocrit",
    "Hemoglobin",
    "Hemoglobin A1c",
    "Homocyst(e)ine",
    "Insulin",
    "LDL Chol Calc (NIH)",
    "Lymphs (Absolute)",
    "Magnesium, RBC",
    "MCV",
    "MTHFR C677T",
    "MTHFR A1298C",
    "Neutrophils (Absolute)",
    "Omega-3 total",
    "Omega-6 total",
    "Omega-6/Omega-3 Ratio",
    "OmegaCheck(TM)",
    "Platelets",
    "Potassium",
    "Pregnenolone, MS",
    "Progesterone",
    "Prostate Specific Ag",
    "RBC",
    "Selenium, Serum/Plasma",
    "Sex Horm Binding Glob",
    "Sodium",
    "T4, Free (Direct)",
    "Testosterone",
    "Testosterone, Total, LC/MS",
    "Thyroglobulin Antibody",
    "Thyroid Peroxidase (TPO) Ab",
    "Total Glutathione",
    "Triglycerides",
    "Triiodothyronine (T3), Free",
    "TSH",
    "Uric Acid",
    "Vitamin B12",
    "Vitamin D, 25-Hydroxy",
    "Vitamin E (Alpha Tocopherol)",
    "WBC",
    "Zinc, Plasma or Serum"
]

# Labs that often come out incorrect in the new code:
labs_to_fix_with_old_code = [
    "Copper, Serum or Plasma",
    "DHEA-Sulfate",
    "Hemoglobin",
    "Homocyst(e)ine",
    "Magnesium, RBC",
    "TSH"
    # Add more if you see other labs that are consistently off
]

# Specific patterns for certain lab tests (when the formatting is known to be tricky)
lab_patterns = {
    'Copper, Serum or Plasma': r'Copper, Serum or Plasma.*?(\d+(?:\.\d+)?)\s+(?:Low|High)?\s*ug/dL',
    'DHEA-Sulfate': r"DHEA-Sulfate\s+01\s+(\d+\.\d+)",
    'Hemoglobin': r'Hemoglobin\s+01\s+(\d+\.\d+)',  # Updated for consistency
    'Magnesium, RBC': r'Magnesium, RBC.*?(\d+(?:\.\d+)?)\s+mg/dL',
    'Omega-3 total': r'Omega-3 total\s+\d+\s+(\d+(?:\.\d+)?)',
    'Omega-6 total': r'Omega-6 total\s+\d+\s+(\d+(?:\.\d+)?)',
    'Omega-6/Omega-3 Ratio': r'Omega-6/Omega-3 Ratio\s+\d+\s+(\d+(?:\.\d+)?)',
    'Pregnenolone, MS': r"Pregnenolone,\s*MS\s+\d{2}\s+(?:<)?(\d+)\s+ng/dL",
    'Prostate Specific Ag': r"Prostate Specific Ag(?:,\s*Serum)?\s+01\s+(\d+\.\d+)",
    'Selenium, Serum/Plasma': r'Selenium.*?(\d+(?:\.\d+)?)\s+ug/L',
    'Thyroglobulin Antibody': r'Thyroglobulin Antibody.*?<(\d+(?:\.\d+)?)',
    'Total Glutathione': r'Total Glutathione\s+07\s+(\d+)',
    'Zinc, Plasma or Serum': r'Zinc.*?(\d+(?:\.\d+)?)\s+ug/dL',
    'T4, Free (Direct)': r'T4,Free\(Direct\)\s+01\s+(\d+\.\d+)|Thyroxine \(T4\) Free, Direct\s+01\s+(\d+\.\d+)',
    'LDL Chol Calc (NIH)': r'LDL Chol Calc \(NIH\)\s+(\d+(?:\.\d+)?)',
    'Vitamin E (Alpha Tocopherol)': r'Vitamin E(?:\(Alpha Tocopherol\)| Alpha Tocopherol)\s*(?:A,\s+04)?\s*(?:\n\s*)*(\d+\.\d+)\s*(?:Low)?\s*mg/L',
    'Free Testosterone': r'Free Testosterone\(Direct\)\s+04\s+(\d+\.\d+)\s+(?:Low|High)?\s*pg/mL',
    'Sex Horm Binding Glob': r'Sex Horm Binding Glob,\s*Serum\s+01\s+(\d+\.\d+)\s*(?:Low|High)?\s*nmol/L',
    'Testosterone, Total, LC/MS': r'Testosterone, Total, LC/MS\s+A,\s+04\s+(\d+\.\d+)\s*(?:Low|High)?\s*ng/dL',
    'APO E Genotyping Result': r'APO E Genotyping Result:\s*\d+\s+(.*?)(?:\s|$)',
    'Arachidonic Acid': r"Arachidonic Acid\s+\d+\s+(\d+\.\d+)",
    'Arachidonic Acid/EPA Ratio': r"Arachidonic Acid/EPA Ratio\s+\d+\s+(\d+\.\d+)",
    'C-Reactive Protein, Cardiac': r"C-Reactive Protein, Cardiac\s+01\s+(\d+\.\d+)",
    'Estradiol': r"Estradiol\s+01\s+<?(\d+\.?\d*)",
    'MTHFR C677T': r"C677T\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|MTHFR,\s*DNA\s*Analysis\s*\d+\s*Result:\s*(?:C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?)|MTHFR\s*C677T\s*(?:Result:\s*)?(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.665C>T\s*\(p\. Ala222Val\),\s*legacy name:\s*C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?",
    'MTHFR A1298C': r"A1298C\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|MTHFR,\s*DNA\s*Analysis\s*\d+\s*Result:\s*(?:A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?)|MTHFR\s*A1298C\s*(?:Result:\s*)?(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.1286A>C\s*\(p\. Glu429Ala\),\s*legacy name:\s*A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?",
    'OmegaCheck(TM)': r'OmegaCheck\(TM\)\s+\d+\s+(\d+(?:\.\d+)?)',
    'Progesterone': r"Progesterone\s+01\s+(\d+\.\d+)",
    'Testosterone': r"Testosterone\s+01\s+(\d+)",
    'FSH': r"FSH\s+01\s+(\d+\.\d+)\s+mIU/mL",
    'TSH': r'TSH\s+01\s+(\d+\.\d+)',
    'Folate (Folic Acid), Serum': r"Folate \(Folic Acid\), Serum\s+01\s+(\d+\.\d+)",
    'Homocyst(e)ine': r"Homocyst\(e\)ine\s+01\s+(\d+\.\d+)",
    'Insulin': r"Insulin\s+01\s+(\d+\.\d+)",
    'Potassium': r"Potassium\s+01\s+(\d+\.\d+)",
    'Uric Acid': r"Uric Acid\s+01\s+(\d+\.\d+)",
    'Triiodothyronine (T3), Free': r"Triiodothyronine \(T3\), Free\s+01\s+(\d+\.\d+)",
    'Vitamin B12': r"Vitamin B12\s+01\s+(\d+)",
    # Adding the missing lab patterns
    'BUN': r"BUN\s+01\s+(\d+(?:\.\d+)?)",
    'Calcium': r"Calcium\s+01\s+(\d+(?:\.\d+)?)",
    'Chloride': r"Chloride\s+01\s+(\d+(?:\.\d+)?)",
    'Creatinine': r"Creatinine\s+01\s+(\d+(?:\.\d+)?)",
    'eGFR': r"eGFR.*?(?:>)?(\d+(?:\.\d+)?)",
    'Glucose': r"Glucose\s+01\s+(\d+(?:\.\d+)?)",
    'Hematocrit': r"Hematocrit\s+01\s+(\d+(?:\.\d+)?)",
    'Lymphs (Absolute)': r"Lymphs \(Absolute\)\s+01\s+(\d+(?:\.\d+)?)",
    'MCV': r"MCV\s+01\s+(\d+(?:\.\d+)?)",
    'Neutrophils (Absolute)': r"Neutrophils \(Absolute\)\s+01\s+(\d+(?:\.\d+)?)",
    'Platelets': r"Platelets\s+01\s+(\d+)",
    'RBC': r"RBC\s+01\s+(\d+(?:\.\d+)?)",
    'Sodium': r"Sodium\s+01\s+(\d+(?:\.\d+)?)",
    'WBC': r"WBC\s+01\s+(\d+(?:\.\d+)?)"
}

# Define page-specific lab patterns globally
page_patterns = {
    1: {
        "Potassium": r"Potassium\s+01\s+(\d+\.\d+)",
        "Hemoglobin": r"Hemoglobin\s+01\s+(\d+\.\d+)"
    },
    2: {
        "Arachidonic Acid/EPA Ratio": r"Arachidonic Acid/EPA Ratio\s+\d+\s+(\d+\.\d+)",
        "Arachidonic Acid": r"Arachidonic Acid\s+\d+\s+(\d+\.\d+)",
        "Albumin": r"Albumin\s+01\s+(\d+\.\d+)",
        "Alkaline Phosphatase": r"Alkaline Phosphatase\s+01\s+(\d+)",
        "AST (SGOT)": r"AST \(SGOT\)\s+01\s+(\d+)",
        "ALT (SGPT)": r"ALT \(SGPT\)\s+01\s+(\d+)",
        "Bilirubin, Total": r"Bilirubin, Total\s+01\s+(\d+\.\d+)",
        "OmegaCheck(TM)": r"OmegaCheck\(TM\)\s+\d+\s+(\d+\.\d+)",
        "Omega-6/Omega-3 Ratio": r"Omega-6/Omega-3 Ratio\s+\d+\s+(\d+\.\d+)",
        "Omega-3 total": r"Omega-3 total\s+\d+\s+(\d+\.\d+)",
        "Omega-6 total": r"Omega-6 total\s+\d+\s+(\d+\.\d+)"
    },
    3: {
        "Cholesterol, Total": r"Cholesterol, Total\s+01\s+(\d+)",
        "Triglycerides": r"Triglycerides\s+01\s+(\d+)",
        "HDL Cholesterol": r"HDL Cholesterol\s+01\s+(\d+)",
        "LDL Chol Calc (NIH)": r"LDL Chol Calc \(NIH\)\s+01\s+(\d+)",
        "APO E Genotyping Result": r"APO E Genotyping Result:\s*\d+\s+(.*?)(?:\s|$)"
    },
    5: {
        "Pregnenolone, MS": r"Pregnenolone,\s*MS\s+\d{2}\s+(?:<)?(\d+)\s+ng/dL",  # Updated
        "Hemoglobin A1c": r"Hemoglobin A1c\s+01\s+(\d+\.\d+)",
        "Vitamin E (Alpha Tocopherol)": r'Vitamin E(?:\(Alpha Tocopherol\)| Alpha Tocopherol)\s*(?:A,\s+04)?\s*(?:\n\s*)*(\d+\.\d+)\s*(?:Low)?\s*mg/L',  # Updated
        "MTHFR C677T": r"C677T\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|MTHFR,\s*DNA\s*Analysis\s*\d+\s*Result:\s*(?:C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?)|MTHFR\s*C677T\s*(?:Result:\s*)?(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.665C>T\s*\(p\. Ala222Val\),\s*legacy name:\s*C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?",
        "MTHFR A1298C": r"A1298C\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|MTHFR,\s*DNA\s*Analysis\s*\d+\s*Result:\s*(?:A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?)|MTHFR\s*A1298C\s*(?:Result:\s*)?(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.1286A>C\s*\(p\. Glu429Ala\),\s*legacy name:\s*A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?"
    },
    6: {
        "MTHFR C677T": r"c\.665C>T\s*\(p\. Ala222Val\),\s*legacy name:\s*C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?",
        "MTHFR A1298C": r"c\.1286A>C\s*\(p\. Glu429Ala\),\s*legacy name:\s*A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?"
    },
    7: {
        "DHEA-Sulfate": r"DHEA-Sulfate\s+01\s+(\d+\.\d+)",
        "Folate (Folic Acid), Serum": r"Folate \(Folic Acid\), Serum\s+01\s+(\d+\.\d+)",
        "FSH": r"FSH\s+01\s+(\d+\.\d+)\s+mIU/mL",
        "TSH": r'TSH\s+01\s+(\d+\.\d+)',
        "Testosterone": r"Testosterone\s+01\s+(\d+)",  # Keep for females, but we'll check sex
        "Total Glutathione": r"Total Glutathione\s+07\s+(\d+)",
        "T4, Free (Direct)": r"T4,Free\(Direct\)\s+01\s+(\d+\.\d+)|Thyroxine \(T4\) Free, Direct\s+01\s+(\d+\.\d+)"  # Enhanced pattern
    },
    8: {
        "C-Reactive Protein, Cardiac": r"C-Reactive Protein, Cardiac\s+01\s+(\d+\.\d+)",
        "Homocyst(e)ine": r"Homocyst\(e\)ine\s+01\s+(\d+\.\d+)",
        "Uric Acid": r"Uric Acid\s+01\s+(\d+\.\d+)",
        "Thyroid Peroxidase (TPO) Ab": r"Thyroid Peroxidase \(TPO\) Ab\s+01\s+<?(\d+)",
        "Vitamin D, 25-Hydroxy": r"Vitamin D, 25-Hydroxy\s+01\s+(\d+\.\d+)"
    },
    9: {
        "Insulin": r"Insulin\s+01\s+(\d+\.\d+)",
        "Triiodothyronine (T3), Free": r"Triiodothyronine \(T3\), Free\s+01\s+(\d+\.\d+)",
        "Cortisol - AM": r"Cortisol - AM\s+01\s+(\d+\.\d+)",
        "Magnesium, RBC": r"Magnesium, RBC\s+(?:B|A),\s+07\s+(\d+\.\d+)",  # Updated for B, 07 or A, 07
        "Thyroglobulin Antibody": r"Thyroglobulin Antibody\s+04\s+(\d+(?:\.\d+)?)\s+(?:Low|High)?\s*IU/mL",  # Updated
        "Vitamin B12": r"Vitamin B12\s+01\s+(\d+)",
        "Zinc, Plasma or Serum": r"Zinc, Plasma or Serum\s+A,\s+04\s+(\d+)",
        "Copper, Serum or Plasma": r"Copper, Serum or Plasma\s+A,\s+04\s+(\d+)",
        "Sex Horm Binding Glob": r"Sex Horm Binding Glob,\s*Serum\s+01\s+(\d+\.\d+)\s*(?:Low|High)?\s*nmol/L",  # Updated
        "Progesterone": r"Progesterone\s+01\s+(\d+\.\d+)"  # Added
    }
}

def clean_value(raw_value, test=None):
    """Clean the extracted value by removing unwanted characters, preserving multi-digit numbers for specific tests."""
    if not raw_value:
        return None
    print(f"Debug - Cleaning value for {test or 'unknown'} (input): {raw_value}")  # Detailed debug print
    
    if test == "Pregnenolone, MS":
        cleaned = re.sub(r'[^0-9]', '', str(raw_value))  # Keep full number (e.g., 44)
        print(f"Debug - Cleaning value for Pregnenolone, MS (output): {cleaned}")
        return cleaned
    elif test in ["APO E Genotyping Result", "Thyroglobulin Antibody", "Thyroid Peroxidase (TPO) Ab"]:
        # For these tests, just clean spaces and return
        cleaned = str(raw_value).strip()
        print(f"Debug - Minimal cleaning for {test}: {cleaned}")
        return cleaned
    elif test in ["MTHFR C677T", "MTHFR A1298C"]:
        # For MTHFR, extract and simplify to "Detected/Not Detected, (Homozygous/Heterozygous)" if present
        match = re.search(r"(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?", raw_value)
        if match:
            status = match.group(1)
            zygosity = match.group(2) or ""  # Capture zygosity if it exists
            # For MTHFR C677T, include ", homozygous" if present; for MTHFR A1298C, omit zygosity
            if test == "MTHFR C677T" and "homozygous" in raw_value.lower():
                cleaned = f"{status}, homozygous"  # Use "homozygous" explicitly for consistency
            elif test == "MTHFR A1298C":
                cleaned = f"{status}"
            else:
                cleaned = f"{status}"
            print(f"Debug - Cleaning value for {test} (simplified output): {cleaned}")
            return cleaned
        return raw_value  # Fall back to raw value if no match
    else:
        # For other tests, keep the current cleaning logic
        cleaned = re.sub(r'[^0-9\.-]', '', str(raw_value))
        print(f"Debug - Cleaning value for {test or 'unknown'} (final output): {cleaned}")
        return cleaned if cleaned else None

# This dictionary will hold our extracted lab values and patient sex
extracted_values = {}
patient_sex = None  # Track patient sex for sex-specific labs

def extract_with_patterns(line, test):
    """
    Try to extract the lab value for a given test from a line.
    1) Check if there's a specific pattern in lab_patterns.
    2) Otherwise, use fallback generic patterns.
    """
    # 1) Use specific pattern if available
    if test in lab_patterns:
        pattern = lab_patterns[test]
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            print(f"Debug - Line for {test}: {line}")  # Debug print for specific patterns
            value = match.group(1) if test not in ["APO E Genotyping Result", "Estradiol", "Thyroglobulin Antibody", "Thyroid Peroxidase (TPO) Ab", "MTHFR C677T", "MTHFR A1298C"] else match.group(0)
            return clean_value(value, test)
            
    # 2) Fallback generic patterns
    generic_patterns = [
        rf"{re.escape(test)}\s+01\s+([\d\.-]+)",
        rf"{re.escape(test)}\s+([\d\.-]+)",
        rf"{re.escape(test)}.*?(\d+\.?\d*)"
    ]
    for pattern in generic_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            print(f"Debug - Line for {test} (generic): {line}")  # Debug print for generic patterns
            value = match.group(1)
            return clean_value(value, test)
    return None

def extract_from_line_with_code(line):
    """
    If a line contains '01', use simple splitting logic to grab a value
    from the next element. Returns (test, value) if successful.
    """
    if '01' in line:
        parts = line.split()
        try:
            code_index = parts.index('01')
            for test in lab_tests:
                if test in line and code_index + 1 < len(parts):
                    # Skip female-specific tests for males
                    if test in ["Estradiol", "FSH", "Progesterone", "Testosterone"] and patient_sex == "Male":
                        print(f"Debug - Skipping {test} for male patient")
                        return None, None
                    return test, clean_value(parts[code_index + 1], test)
        except ValueError:
            pass
    return None, None

# -------------------- Old Approach Fallback --------------------
def extract_with_old_approach(page_text, test):
    """
    This mimics the older 'one-line' approach that worked well for certain labs.
    It captures: TestName <value> <optional unit>
    Then does minimal cleaning (removing leading digits, H/L markers).
    """
    pattern = rf"{re.escape(test)}\s+([\d\.\-<>]+)\s*([\w/%]+)?"
    match = re.search(pattern, page_text)
    if match:
        raw_value = match.group(1).strip()
        unit = match.group(2) if match.group(2) else ""
        # Clean the extracted value
        clean_val = re.sub(r"^\d+\s*", "", raw_value).replace("H", "").replace("L", "").strip()
        return f"{clean_val} {unit}".strip()
    return None

def fallback_old_approach(page_text):
    """
    For labs known to be off with the new code,
    if the extracted value is empty or suspicious (like '04'),
    try the old approach on the entire page text.
    """
    for test in labs_to_fix_with_old_code:
        current_val = extracted_values.get(test, "")
        # If it's empty or a known "bad" placeholder, run old approach:
        if not current_val or current_val in ("04", "07", "25"): 
            old_val = extract_with_old_approach(page_text, test)
            if old_val:
                extracted_values[test] = old_val

def process_page_patterns(page_text, page_number):
    """Process patterns specific to a page, with debug for failures."""
    global patient_sex  # Use global to track patient sex
    if page_number == 1 and not patient_sex:  # Extract sex from Page 1
        if "Sex: Male" in page_text:
            patient_sex = "Male"
        elif "Sex: Female" in page_text:
            patient_sex = "Female"
        print(f"Debug - Determined patient sex: {patient_sex}")

    if page_number in page_patterns:
        for test, pattern in page_patterns[page_number].items():
            # More robust check for test presence, handling variations and line breaks
            test_variations = [test]
            if test == "Vitamin E (Alpha Tocopherol)":
                test_variations = ["Vitamin E (Alpha Tocopherol)", "Vitamin E(Alpha Tocopherol)"]
            elif test == "T4, Free (Direct)":
                test_variations = ["T4, Free (Direct)", "Thyroxine (T4) Free, Direct"]
            found_in_text = any(variation in page_text or any(variation in line for line in page_text.split('\n')) for variation in test_variations)
            if found_in_text or test in ["MTHFR C677T", "MTHFR A1298C"]:  # Force check for MTHFR even if not explicitly found
                print(f"Debug - Raw Text for Page {page_number} ({test}): {page_text}")
                try:
                    match = re.search(pattern, page_text, re.IGNORECASE | re.DOTALL)  # Use DOTALL for multi-line matching
                    if match:
                        print(f"Debug - Found {test} in raw text: {match.group(0)}")
                        # Use the full match (group(0)) for MTHFR tests to include status and zygosity
                        value = match.group(0) if test in ["MTHFR C677T", "MTHFR A1298C"] else match.group(1) if match.group(1) else match.group(2) if test in ["T4, Free (Direct)", "Vitamin E (Alpha Tocopherol)"] and match.group(2) else match.group(1)
                        if value:
                            print(f"Debug - {test} match group 1 or 2: {value}")
                            cleaned_value = clean_value(value, test)
                            if cleaned_value:
                                extracted_values[test] = cleaned_value
                                print(f"Debug - Final {test} value set: {cleaned_value}")
                    else:
                        print(f"Debug - Pattern {pattern} for {test} failed to match in page {page_number} (checking for MTHFR results)")
                except re.error as e:
                    print(f"Debug - Regex error for {test} on page {page_number}: {e}")
            else:
                print(f"Debug - Test {test} not found in page {page_number} text (variations checked: {test_variations})")

def process_remaining_labs(page_text, tables, page, page_number):
    """Process remaining labs using various methods, no excluded_tests for Page 7."""
    excluded_tests = ["Potassium", "Hemoglobin", "Copper, Serum or Plasma"]  # Removed "Progesterone" from excluded tests
    if page_number == 7:  # Force extraction for Page 7 labs, bypassing excluded_tests
        excluded_tests = []  # Remove all exclusions for Page 7 to ensure all labs are processed
    
    # 1) Line code extraction
    lines = page_text.split('\n')
    for line in lines:
        test_from_code, value_from_code = extract_from_line_with_code(line)
        if test_from_code and value_from_code and test_from_code not in extracted_values:
            if test_from_code not in excluded_tests:
                # For female-specific tests, only extract if patient is female
                if test_from_code in ["Estradiol", "FSH", "Progesterone"] and patient_sex != "Female":
                    print(f"Debug - Skipping {test_from_code} for non-female patient")
                    continue
                extracted_values[test_from_code] = value_from_code
                print(f"Debug - Added {test_from_code} from line code: {value_from_code}")

    # 2) Pattern-based extraction
    for line in lines:
        for test in lab_tests:
            if test not in extracted_values and test in line and test not in excluded_tests:
                # For female-specific tests, only extract if patient is female
                if test in ["Estradiol", "FSH", "Progesterone"] and patient_sex != "Female":
                    print(f"Debug - Skipping {test} for non-female patient")
                    continue
                value = extract_with_patterns(line, test)
                if value:
                    extracted_values[test] = value
                    print(f"Debug - Added {test} from pattern: {value}")

    # 3) Table processing
    if tables:
        for table_idx, table in enumerate(tables):
            table_text = " ".join(str(cell) for row in table for cell in row if cell)
            print(f"Debug - Full Table {table_idx} on page {page_number}: {table_text}")
            
            for row_idx, row in enumerate(table):
                for cell_idx, cell in enumerate(row):
                    if cell:
                        for test in lab_tests:
                            if test not in extracted_values and test in cell and test not in excluded_tests:
                                # For female-specific tests, only extract if patient is female
                                if test in ["Estradiol", "FSH", "Progesterone"] and patient_sex != "Female":
                                    print(f"Debug - Skipping {test} for non-female patient")
                                    continue
                                value = None
                                if cell_idx + 1 < len(row) and row[cell_idx + 1]:
                                    value = extract_with_patterns(row[cell_idx + 1], test)
                                elif cell_idx - 1 >= 0 and row[cell_idx - 1]:
                                    value = extract_with_patterns(row[cell_idx - 1], test)
                                else:
                                    value = extract_with_patterns(cell, test)
                                if value:
                                    extracted_values[test] = value
                                    print(f"Debug - Added {test} from table: {value}")

    # 4) Fallback processing for MTHFR across all pages
    if "MTHFR" in page_text:
        # Try word-level extraction for MTHFR
        words = page.extract_words()
        word_text = " ".join(word["text"] for word in words if word["text"].strip())
        print(f"Debug - Word-level extraction for page {page_number} (MTHFR): {word_text}")
        
        # Try table extraction for MTHFR
        table_text = " ".join(str(cell) for table in tables for row in table for cell in row if cell)
        print(f"Debug - Table-level extraction for page {page_number} (MTHFR): {table_text}")
        
        # Search all text for MTHFR results
        mthfr_match = re.search(r"MTHFR(?:,\s*DNA\s*Analysis)?\s*\d*\s*Result:\s*(.*)|c\.665C>T\s*\(p\. Ala222Val\),\s*legacy name:\s*C677T.*|c\.1286A>C\s*\(p\. Glu429Ala\),\s*legacy name:\s*A1298C.*", page_text + " " + word_text + " " + table_text, re.IGNORECASE | re.DOTALL)
        if mthfr_match:
            result_text = mthfr_match.group(1) or mthfr_match.group(0) or ""
            print(f"Debug - MTHFR Result Text Found: {result_text}")
            # Try to extract C677T and A1298C from the result text or any text
            c677t_match = re.search(r"C677T\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.665C>T\s*\(p\. Ala222Val\),\s*legacy name:\s*C677T\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?", result_text or (page_text + " " + word_text + " " + table_text), re.IGNORECASE)
            a1298c_match = re.search(r"A1298C\s*[-:\s]*(Detected|Not Detected)\s*\(?(Homozygous|Heterozygous)?\)?|c\.1286A>C\s*\(p\. Glu429Ala\),\s*legacy name:\s*A1298C\s*[-:\s]*(Detected|Not Detected),\s*(?:homozygous|heterozygous)?", result_text or (page_text + " " + word_text + " " + table_text), re.IGNORECASE)
            if c677t_match:
                c677t_value = c677t_match.group(0)
                extracted_values["MTHFR C677T"] = clean_value(c677t_value, "MTHFR C677T")
                print(f"Debug - Final MTHFR C677T value set: {extracted_values['MTHFR C677T']}")
            if a1298c_match:
                a1298c_value = a1298c_match.group(0)
                extracted_values["MTHFR A1298C"] = clean_value(a1298c_value, "MTHFR A1298C")
                print(f"Debug - Final MTHFR A1298C value set: {extracted_values['MTHFR A1298C']}")
        else:
            print(f"Debug - No MTHFR Result text found in page {page_number}")

    # 5) Fallback processing
    for test in labs_to_fix_with_old_code:
        if test not in excluded_tests and (test not in extracted_values or not extracted_values[test]):
            current_val = extracted_values.get(test, "")
            if not current_val or current_val in ("04", "07", "25"): 
                old_val = extract_with_old_approach(page_text, test)
                if old_val:
                    extracted_values[test] = old_val
                    print(f"Debug - Added {test} from old approach: {old_val}")

def process_pdf(filepath):
    """Process a PDF file and extract lab results."""
    print(f"Starting PDF processing for file: {filepath}")  # Debug print
    
    # Update patterns for missing labs
    lab_patterns.update({
        'BUN': r"BUN\s+01\s+(\d+(?:\.\d+)?)",
        'Calcium': r"Calcium\s+01\s+(\d+(?:\.\d+)?)",
        'Chloride': r"Chloride\s+01\s+(\d+(?:\.\d+)?)",
        'Creatinine': r"Creatinine\s+01\s+(\d+(?:\.\d+)?)",
        'eGFR': r"eGFR.*?(?:>)?(\d+(?:\.\d+)?)",
        'Glucose': r"Glucose\s+01\s+(\d+(?:\.\d+)?)",
        'Hematocrit': r"Hematocrit\s+01\s+(\d+(?:\.\d+)?)",
        'Lymphs \(Absolute\)': r"Lymphs \(Absolute\)\s+01\s+(\d+(?:\.\d+)?)",
        'MCV': r"MCV\s+01\s+(\d+(?:\.\d+)?)",
        'Neutrophils \(Absolute\)': r"Neutrophils \(Absolute\)\s+01\s+(\d+(?:\.\d+)?)",
        'Platelets': r"Platelets\s+01\s+(\d+)",
        'RBC': r"RBC\s+01\s+(\d+(?:\.\d+)?)",
        'Sodium': r"Sodium\s+01\s+(\d+(?:\.\d+)?)",
        'WBC': r"WBC\s+01\s+(\d+(?:\.\d+)?)"
    })

    try:
        with pdfplumber.open(filepath) as pdf:
            extracted_data = {}
            
            # Process each page
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processing page {page_num}")  # Debug print
                text = page.extract_text()
                
                # Try page-specific patterns first
                if page_num in page_patterns:
                    for test, pattern in page_patterns[page_num].items():
                        match = re.search(pattern, text)
                        if match:
                            raw_value = match.group(1)
                            cleaned_value = clean_value(raw_value, test)
                            if cleaned_value:
                                print(f"Found {test}: {cleaned_value}")  # Debug print
                                extracted_data[test] = {
                                    'value': cleaned_value,
                                    'unit': extract_unit(text, test),
                                    'reference_range': extract_reference_range(text, test)
                                }
                
                # Try general patterns for any remaining tests
                for test in lab_tests:
                    if test not in extracted_data:
                        # Try specific pattern if available
                        if test in lab_patterns:
                            pattern = lab_patterns[test]
                            match = re.search(pattern, text)
                            if match:
                                raw_value = match.group(1)
                                cleaned_value = clean_value(raw_value, test)
                                if cleaned_value:
                                    print(f"Found {test}: {cleaned_value}")  # Debug print
                                    extracted_data[test] = {
                                        'value': cleaned_value,
                                        'unit': extract_unit(text, test),
                                        'reference_range': extract_reference_range(text, test)
                                    }
            
            print(f"Extraction complete. Found {len(extracted_data)} results")  # Debug print
            return extracted_data
            
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")  # Debug print
        raise

def extract_unit(text, test):
    """Extract the unit for a given test result."""
    # Add units for the new labs
    unit_patterns = {
        'BUN': r'mg/dL',
        'Calcium': r'mg/dL',
        'Chloride': r'mmol/L',
        'Creatinine': r'mg/dL',
        'eGFR': r'mL/min/1.73m2',
        'Glucose': r'mg/dL',
        'Hematocrit': r'%',
        'Lymphs \(Absolute\)': r'K/uL',
        'Platelets': r'K/uL',
        'RBC': r'M/uL',
        'Sodium': r'mmol/L',
        'WBC': r'K/uL',
        'Prostate Specific Ag': r'ng/mL'
    }
    
    if test in unit_patterns:
        pattern = unit_patterns[test]
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ''

def extract_reference_range(text, test):
    """Extract the reference range for a given test result."""
    # Common reference range patterns
    range_patterns = {
        'Albumin': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*g/dL',
        'ALT \(SGPT\)': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*U/L',
        'AST \(SGOT\)': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*U/L',
        'TSH': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*uIU/mL',
        'T4, Free \(Direct\)': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*ng/dL',
        'Vitamin D, 25-Hydroxy': r'Reference Range:\s*([\d\.-]+\s*-\s*[\d\.]+)\s*ng/mL'
    }
    
    if test in range_patterns:
        pattern = range_patterns[test]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ''

def save_results(client_id: str, results: Dict[str, Dict[str, str]], output_path: str):
    """Save extracted lab values to a CSV file for a client."""
    df = pd.DataFrame([(test, results.get(test, {}).get('value', ''), results.get(test, {}).get('unit', ''), results.get(test, {}).get('reference_range', '')) for test in lab_tests], columns=["Lab Test", "Value", "Unit", "Reference Range"])
    output_file = os.path.join(output_path, f"{client_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(output_file, index=False)
    print(f"Results for client {client_id} saved to {output_file}")

def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process all PDFs in the input directory
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        client_id = os.path.splitext(pdf_file)[0]  # Use filename as client ID
        
        print(f"Processing lab report for client {client_id}...")
        results = process_pdf(pdf_path)
        
        if results:
            save_results(client_id, results, OUTPUT_DIR)
        else:
            print(f"No valid lab results extracted for {client_id}")

if __name__ == "__main__":
    main()