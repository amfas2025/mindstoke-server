#!/usr/bin/env python3

"""
Test script for the Risk Profile functionality in the Other Insights section.
"""

from risk_factor_mapping import RiskFactorMapper
from roadmap_generator import RoadmapGenerator

def test_risk_factor_mapper():
    """Test the risk factor mapping functionality."""
    print("=== Testing Risk Factor Mapper ===")
    
    # Test sample HHQ responses with various risk factors
    sample_hhq = {
        'hh-head-injury': True,           # Traumatic
        'hh-concussion': True,            # Traumatic  
        'hh-heart-attack': True,          # Vascular
        'hh-high-blood-pressure': True,   # Vascular
        'hh-mold-exposure': True,         # Toxic
        'hh-welding-soldering': True,    # Toxic
        'hh-diabetes': True,              # Glycotoxic
        'hh-frequent-carb-sugar': True,   # Glycotoxic
        'hh-menopause': True,             # Atrophic
        'hh-thyroid-disease': True,       # Atrophic
        'hh-frequent-ibuprofen': True,    # Inflammatory
        'hh-arthritis': True,             # Inflammatory
    }
    
    mapper = RiskFactorMapper()
    
    # Calculate risk scores
    risk_scores = mapper.calculate_risk_scores(sample_hhq)
    print(f"Raw Risk Scores: {risk_scores}")
    
    # Calculate percentages
    risk_percentages = mapper.calculate_risk_percentages(risk_scores)
    print(f"Risk Percentages: {risk_percentages}")
    
    # Get top risk factors
    top_risks = mapper.get_top_risk_factors(risk_percentages, limit=3)
    print(f"Top 3 Risk Categories: {top_risks}")
    
    # Get risk factor details
    risk_details = mapper.get_risk_factor_details(sample_hhq)
    print(f"Risk Factor Details: {risk_details}")
    
    return risk_scores, risk_percentages, top_risks, risk_details

def test_roadmap_generator_integration():
    """Test the risk profile integration in roadmap generator."""
    print("\n=== Testing Roadmap Generator Integration ===")
    
    generator = RoadmapGenerator()
    
    # Sample data
    client_data = {
        'name': 'Test Client',
        'gender': 'female',
        'dob': '1975-01-01'
    }
    
    lab_results = {
        'VIT_D25': 45,
        'INFLAM_CRP': 1.2
    }
    
    # HHQ with multiple risk factors
    hhq_responses = {
        'hh-head-injury': True,
        'hh-stroke': True,
        'hh-mold-exposure': True,
        'hh-diabetes': True,
        'hh-menopause': True,
        'hh-arthritis': True,
        'hh-height': '5\'6"',
        'hh-weight': '150 lbs'
    }
    
    # Test the risk profile processing function directly
    risk_profile_results = generator._process_risk_profile_insights(hhq_responses)
    print(f"Risk Profile Processing Results:")
    for key, value in risk_profile_results.items():
        print(f"  {key}: {value}")
    
    # Test full content controls processing
    all_controls = generator._process_all_content_controls(client_data, lab_results, hhq_responses)
    
    # Extract risk profile related controls
    risk_controls = {k: v for k, v in all_controls.items() if 'risk-' in k}
    print(f"\nRisk-related Content Controls:")
    for key, value in risk_controls.items():
        print(f"  {key}: {value}")
    
    return risk_profile_results, risk_controls

def test_template_generation():
    """Test generating a roadmap with risk profile content."""
    print("\n=== Testing Template Generation ===")
    
    generator = RoadmapGenerator()
    
    client_data = {
        'name': 'Jane Doe',
        'gender': 'female', 
        'dob': '1970-03-15'
    }
    
    lab_results = {
        'VIT_D25': 30,
        'INFLAM_CRP': 2.1,
        'LIPID_CHOL': 220
    }
    
    hhq_responses = {
        'hh-concussion': True,
        'hh-multiple-concussions': True,
        'hh-heart-attack': True,
        'hh-atherosclerosis': True,
        'hh-chemical-exposure': True,
        'hh-mold-exposure': True,
        'hh-diabetes': True,
        'hh-insulin-resistance': True,
        'hh-postmenopausal': True,
        'hh-hormone-deficiency': True,
        'hh-chronic-pain': True,
        'hh-autoimmune-disease': True,
        'hh-height': '165 cm',
        'hh-weight': '70 kg'
    }
    
    try:
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Check if risk profile section is included
        if 'Other Insights From Your Past Medical History' in roadmap:
            print("✅ Risk Profile section found in roadmap")
            
            # Extract the risk profile section
            start_idx = roadmap.find('Other Insights From Your Past Medical History')
            end_idx = roadmap.find('## **', start_idx + 50)  # Find next major section
            if end_idx == -1:
                end_idx = len(roadmap)
            
            risk_section = roadmap[start_idx:end_idx]
            print(f"Risk Profile Section Preview:")
            print(risk_section[:1000] + "..." if len(risk_section) > 1000 else risk_section)
        else:
            print("❌ Risk Profile section not found in roadmap")
            
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        import traceback
        traceback.print_exc()

def test_edge_cases():
    """Test edge cases for risk profile processing."""
    print("\n=== Testing Edge Cases ===")
    
    mapper = RiskFactorMapper()
    generator = RoadmapGenerator()
    
    # Test with no risk factors
    empty_hhq = {}
    empty_scores = mapper.calculate_risk_scores(empty_hhq)
    empty_percentages = mapper.calculate_risk_percentages(empty_scores)
    print(f"Empty HHQ Risk Scores: {empty_scores}")
    print(f"Empty HHQ Percentages: {empty_percentages}")
    
    # Test with only one risk factor
    single_risk_hhq = {'hh-diabetes': True}
    single_scores = mapper.calculate_risk_scores(single_risk_hhq)
    single_percentages = mapper.calculate_risk_percentages(single_scores)
    print(f"Single Risk Factor Scores: {single_scores}")
    print(f"Single Risk Factor Percentages: {single_percentages}")
    
    # Test generator with no HHQ responses
    no_hhq_result = generator._process_risk_profile_insights(None)
    print(f"No HHQ Result: {no_hhq_result}")
    
    # Test generator with empty HHQ
    empty_hhq_result = generator._process_risk_profile_insights({})
    print(f"Empty HHQ Result: {empty_hhq_result}")

if __name__ == "__main__":
    print("Testing Risk Profile Functionality\n")
    
    # Run all tests
    test_risk_factor_mapper()
    test_roadmap_generator_integration()
    test_template_generation()
    test_edge_cases()
    
    print("\n✅ All tests completed!") 