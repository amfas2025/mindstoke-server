#!/usr/bin/env python3
"""
Test script to verify the "Other Insights From Your Lab Work" section
"""

from roadmap_generator import RoadmapGenerator
import re
import pytest

def test_other_insights_section():
    """Test the complete Other Insights From Your Lab Work section."""
    generator = RoadmapGenerator()
    
    # Test Case 1: Normal CBC values (should not trigger anemia or other warnings)
    lab_results_normal = {
        'CBC_RBC': 4.5,
        'CBC_HGB': 14.0,
        'CBC_HCT': 42,
        'CBC_PLT': 250,
        'CBC_MCV': 90,
        'CBC_WBC': 6.0,
        'CBC_NEUT_ABS': 3.5,
        'CBC_LYMPH_ABS': 2.0,
        'DDimer': 200,
        'Sodium': 140,
        'Potassium': 4.0,
        'Chloride': 102,
        'Calcium': 9.5,
        'eGFR': 90,
        'Creatinine': 1.0,
        'ALT': 25,
        'AST': 22,
        'AlkPhos': 80
    }
    
    client_data = {
        'firstname': 'John',
        'gender': 'M',
        'date_of_birth': '1980-01-01'
    }
    
    hhq_responses = {}
    
    processed = generator._process_all_content_controls(client_data, lab_results_normal, hhq_responses)
    
    # Normal values should not trigger warnings
    assert processed.get('quick-anemia') != True
    assert processed.get('quick-macrocytosis') != True
    assert processed.get('Coags') != True
    assert processed.get('quick-immune-elevated') != True
    assert processed.get('quick-immune-suppressed') != True
    assert processed.get('quick-lytes') != True
    assert processed.get('kidney-fn') != True
    assert processed.get('ALT-alcohol') != True
    
    # Test Case 2: Anemia risk scenario
    lab_results_anemia = {
        'CBC_RBC': 3.8,  # Low
        'CBC_HGB': 12.0,  # Low
        'CBC_HCT': 35,    # Low
        'CBC_MCV': 105,   # High (macrocytosis)
        'CBC_PLT': 200,
        'CBC_WBC': 5.0,
        'CBC_NEUT_ABS': 3.0,
        'CBC_LYMPH_ABS': 1.5
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_anemia, hhq_responses)
    
    # Should trigger anemia and macrocytosis warnings
    assert processed.get('quick-anemia') == True
    assert processed.get('quick-macrocytosis') == True
    
    # Test Case 3: Elevated D-dimer (coagulation risk)
    lab_results_coags = {
        'CBC_RBC': 4.5,
        'CBC_HGB': 14.0,
        'CBC_HCT': 42,
        'CBC_PLT': 250,
        'DDimer': 750,  # Elevated
        'CBC_WBC': 5.0,
        'CBC_NEUT_ABS': 3.0,
        'CBC_LYMPH_ABS': 1.5
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_coags, hhq_responses)
    
    # Should trigger coagulation risk
    assert processed.get('Coags') == True
    assert processed.get('quick-D-Dimer') == 750
    
    # Test Case 4: Immune system issues
    lab_results_immune = {
        'CBC_WBC': 12.5,  # Elevated
        'CBC_NEUT_ABS': 8.0,  # Elevated
        'CBC_LYMPH_ABS': 0.8,  # Low
        'CBC_RBC': 4.5,
        'CBC_HGB': 14.0,
        'CBC_HCT': 42,
        'CBC_PLT': 200
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_immune, hhq_responses)
    
    # Should trigger both elevated and suppressed immune markers
    assert processed.get('quick-immune-elevated') == True
    assert processed.get('quick-immune-suppressed') == True
    
    # Test Case 5: Low platelets with medication interaction
    lab_results_platelets = {
        'CBC_PLT': 120,  # Low
        'CBC_RBC': 4.5,
        'CBC_HGB': 14.0,
        'CBC_HCT': 42,
        'CBC_WBC': 5.0,
        'CBC_NEUT_ABS': 3.0,
        'CBC_LYMPH_ABS': 1.5
    }
    
    hhq_with_nsaids = {
        'medications': 'I take ibuprofen for headaches'
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_platelets, hhq_with_nsaids)
    
    # Should trigger low platelets and medication interaction
    assert processed.get('quick-platelets-low') == True
    assert processed.get('platelet-medication-interaction') == True
    
    # Test Case 6: Electrolyte abnormalities
    lab_results_electrolytes = {
        'Sodium': 130,     # Low
        'Potassium': 5.5,  # High
        'Chloride': 95,    # Low
        'Calcium': 11.0    # High
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_electrolytes, hhq_responses)
    
    # Should trigger electrolyte warning
    assert processed.get('quick-lytes') == True
    
    # Test Case 7: Kidney function issues
    lab_results_kidney = {
        'eGFR': 45,        # Low
        'Creatinine': 1.8  # High
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_kidney, hhq_responses)
    
    # Should trigger kidney function warning
    assert processed.get('kidney-fn') == True
    
    # Test Case 8: Severe kidney function issues
    lab_results_kidney_severe = {
        'eGFR': 25,        # Very low
        'Creatinine': 2.5  # Very high
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_kidney_severe, hhq_responses)
    
    # Should trigger both kidney function warnings
    assert processed.get('kidney-fn') == True
    assert processed.get('kidney-fn-30') == True
    
    # Test Case 9: Liver function elevation with alcohol
    lab_results_liver = {
        'ALT': 65,    # High
        'AST': 55,    # High
        'AlkPhos': 140  # High
    }
    
    hhq_with_alcohol = {
        'alcohol_use': 'I drink wine with dinner occasionally'
    }
    
    processed = generator._process_all_content_controls(client_data, lab_results_liver, hhq_with_alcohol)
    
    # Should trigger liver function warnings
    assert processed.get('ALT-alcohol') == True
    assert processed.get('ALT-low') == True
    
    print("✅ All Other Insights section tests passed!")

if __name__ == "__main__":
    test_other_insights_section() 