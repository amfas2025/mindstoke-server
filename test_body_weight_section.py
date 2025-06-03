#!/usr/bin/env python3

import pytest
from roadmap_generator import RoadmapGenerator

def test_body_weight_section():
    """Test the Body Weight Can Be A Predictor of Brain Health section."""
    generator = RoadmapGenerator()
    
    # Test Case 1: Normal BMI (20-24.9)
    client_data_normal = {
        'firstname': 'John',
        'gender': 'M',
        'date_of_birth': '1980-01-01'
    }
    
    hhq_responses_normal = {
        'height': '180 cm',
        'weight': '75 kg'
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_normal)
    
    # BMI = 75 / (1.8)^2 = 23.1 (normal range, should trigger quick-bmi20)
    assert processed.get('quick-bmi') == 23.1
    assert processed.get('quick-bmi20') == True
    assert processed.get('quick-BMI-OSA') != True
    
    # Test Case 2: Overweight BMI (>=25)
    hhq_responses_overweight = {
        'height': '170 cm',
        'weight': '80 kg'  
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_overweight)
    
    # BMI = 80 / (1.7)^2 = 27.7 (overweight, should trigger quick-BMI-OSA)
    assert processed.get('quick-bmi') == 27.7
    assert processed.get('quick-BMI-OSA') == True
    assert processed.get('quick-bmi20') != True
    
    # Test Case 3: Height/Weight in feet and pounds
    hhq_responses_imperial = {
        'height': "5'10\"",  # 5 feet 10 inches
        'weight': '165 lbs'
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_imperial)
    
    # Should convert and calculate BMI correctly
    # 5'10" = 177.8 cm, 165 lbs = 74.8 kg, BMI = 23.7
    expected_bmi = round(processed.get('quick-bmi', 0), 1)
    assert 23.0 <= expected_bmi <= 24.0  # Allow for rounding differences
    assert processed.get('quick-bmi20') == True
    
    # Test Case 4: Underweight BMI (<18.5)
    hhq_responses_underweight = {
        'height': '170 cm',
        'weight': '50 kg'
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_underweight)
    
    # BMI = 50 / (1.7)^2 = 17.3 (underweight)
    assert processed.get('quick-bmi') == 17.3
    assert processed.get('quick-bmi-underweight') == True
    
    # Test Case 5: Obese BMI (>=30)
    hhq_responses_obese = {
        'height': '170 cm',
        'weight': '95 kg'
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_obese)
    
    # BMI = 95 / (1.7)^2 = 32.9 (obese)
    assert processed.get('quick-bmi') == 32.9
    assert processed.get('quick-bmi-obese') == True
    assert processed.get('quick-BMI-OSA') == True
    
    # Test Case 6: Height/Weight in client_data instead of HHQ
    client_data_with_measurements = {
        'firstname': 'Jane',
        'gender': 'F',
        'date_of_birth': '1985-01-01',
        'height': 165,  # cm
        'weight': 60    # kg
    }
    
    processed = generator._process_all_content_controls(client_data_with_measurements, {}, {})
    
    # BMI = 60 / (1.65)^2 = 22.0
    assert processed.get('quick-bmi') == 22.0
    assert processed.get('quick-bmi20') == True
    
    # Test Case 7: Missing height or weight (no BMI calculation)
    hhq_responses_incomplete = {
        'height': '170 cm'
        # Missing weight
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_incomplete)
    
    # Should not calculate BMI if missing data
    assert 'quick-bmi' not in processed
    assert processed.get('quick-bmi20') != True
    assert processed.get('quick-BMI-OSA') != True
    
    # Test Case 8: Alternative height format (feet only)
    hhq_responses_feet_only = {
        'height': '6 feet',
        'weight': '180 pounds'
    }
    
    processed = generator._process_all_content_controls(client_data_normal, {}, hhq_responses_feet_only)
    
    # Should convert 6 feet to cm and pounds to kg
    expected_bmi = processed.get('quick-bmi')
    assert expected_bmi is not None
    assert expected_bmi > 20  # Should be a reasonable BMI
    
    print("✅ All Body Weight section tests passed!")

if __name__ == "__main__":
    test_body_weight_section() 