import pdfplumber
import re
import pandas as pd

# 🔹 PDF File Path (Make sure the file exists in the same folder)
pdf_path = "labs.pdf"

# 🔹 Define the lab tests we need to extract
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

# 🔹 Dictionary to store extracted values
extracted_values = {}

# 🔹 Open and process the PDF file
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()  # Extract text from the page
        
        if text:
            for test in lab_tests:
                # 🔹 Regular expression to find lab test values
                pattern = rf"{test}\s*([\d\.\-<>]+)\s*([\w/%]*)"
                match = re.search(pattern, text)
                if match:
                    # Remove extra numbers and symbols
                    clean_value = re.sub(r"^\d+\s*", "", match.group(1)).strip()  # Remove leading numbers
                    clean_value = clean_value.replace("H", "").replace("L", "").strip()  # Remove high/low markers
                    extracted_values[test] = clean_value

        # 🔹 Check if the page contains tables
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                for test in lab_tests:
                    if test in row:
                        idx = row.index(test)
                        if idx + 1 < len(row) and row[idx + 1]:  # Ensure next column has data
                            extracted_values[test] = row[idx + 1]

# 🔹 Convert to a DataFrame for easy visualization
df_extracted_labs = pd.DataFrame(list(extracted_values.items()), columns=["Lab Test", "Value"])

# 🔹 Display the results
print(df_extracted_labs)

# 🔹 Save the results to CSV (Optional)
df_extracted_labs.to_csv("extracted_lab_results.csv", index=False)
print("✅ Lab values extracted and saved to 'extracted_lab_results.csv'.")

