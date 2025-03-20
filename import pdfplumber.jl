import pdfplumber
import re
import pandas as pd

# PDF File Path
pdf_path = "labs.pdf"  # Make sure your PDF is named "labs.pdf" in the same directory

# Define the lab tests
lab_tests = [
    "Albumin", "Alkaline Phosphatase", "ALT (SGPT)", "AST (SGOT)", "Bilirubin, Total",
    "BUN", "Calcium", "Chloride", "Cholesterol, Total", "Copper, Serum or Plasma",
    "Cortisol - AM", "Creatinine", "DHEA-Sulfate", "eGFR", "Folate (Folic Acid), Serum",
    "Free Testosterone", "Glucose", "HDL Cholesterol", "Hematocrit", "Hemoglobin",
    "Hemoglobin A1c", "Homocyst(e)ine", "Insulin", "LDL Chol Calc (NIH)", "Lymphs (Absolute)",
    "Magnesium, RBC", "MCV", "Neutrophils (Absolute)", "Omega-3 total", "Omega-6 total",
    "Omega-6/Omega-3 Ratio", "Platelets", "Potassium", "Pregnenolone, MS", "Prostate Specific Ag",
    "RBC", "Selenium, Serum/Plasma", "Sex Horm Binding Glob", "Sodium", "T4, Free (Direct)",
    "Testosterone, Total, LC/MS", "Thyroglobulin Antibody", "Thyroid Peroxidase (TPO) Ab",
    "Total Glutathione", "Triglycerides", "Triiodothyronine (T3), Free", "TSH", "Uric Acid",
    "Vitamin B12", "Vitamin D, 25-Hydroxy", "Vitamin E (Alpha Tocopherol)", "WBC", "Zinc, Plasma or Serum"
]

def clean_value(value):
    if not value:
        return None
    # Remove any non-numeric characters except decimal points and negative signs
    clean = re.sub(r'[^0-9\.-]', '', str(value))
    return clean if clean else None

# Dictionary to store extracted values
extracted_values = {}

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')
        
        # Print entire text for debugging
        print("\nPage Content:")
        print("-------------")
        print(text)
        print("-------------\n")
        
        for line in lines:
            # Print each line for debugging
            print(f"Processing line: {line}")
            
            if '01' in line:
                parts = line.split()
                try:
                    code_index = parts.index('01')
                    if code_index > 0 and code_index + 1 < len(parts):
                        for test in lab_tests:
                            if test in line:
                                value = clean_value(parts[code_index + 1])
                                if value:
                                    extracted_values[test] = value
                                    print(f"Found value for {test}: {value}")
                except ValueError:
                    continue

            # Try regex patterns for each test
            for test in lab_tests:
                if test in line:
                    patterns = [
                        rf"{test}\s+01\s+([\d\.-]+)",
                        rf"{test}\s+([\d\.-]+)",
                        rf"{test}.*?(\d+\.?\d*)"
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, line)
                        if match:
                            value = clean_value(match.group(1))
                            if value and test not in extracted_values:
                                extracted_values[test] = value
                                print(f"Found value (regex) for {test}: {value}")
                            break

# Create DataFrame
df_extracted_labs = pd.DataFrame(
    [(test, extracted_values.get(test, '')) for test in lab_tests],
    columns=["Lab Test", "Value"]
)

# Display results
print("\nExtracted Values:")
print(df_extracted_labs)

# Save to CSV
df_extracted_labs.to_csv("extracted_lab_results.csv", index=False)
print("\n✅ Lab values extracted and saved to 'extracted_lab_results.csv'")
