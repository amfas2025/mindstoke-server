#!/usr/bin/env python3

from roadmap_generator import RoadmapGenerator

generator = RoadmapGenerator()

# Test with sample data to verify sections appear in correct order
client_data = {
    'firstname': 'Test',
    'gender': 'M',
    'date_of_birth': '1980-01-01'
}

lab_results = {
    'CBC_RBC': 4.0,    # Slightly low (anemia risk)
    'CBC_HGB': 12.5,   # Low
    'CBC_HCT': 36,     # Low
    'DDimer': 600      # Elevated
}

hhq_responses = {
    'height': '175 cm',
    'weight': '85 kg'  # BMI = 27.8 (overweight)
}

# Generate roadmap
roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)

# Check for section headers in correct order
other_insights_pos = roadmap.find('## **Other Insights From Your Lab Work**')
body_weight_pos = roadmap.find('## **Body Weight Can Be A Predictor of Brain Health**')

print(f'Other Insights position: {other_insights_pos}')
print(f'Body Weight position: {body_weight_pos}')

if other_insights_pos != -1 and body_weight_pos != -1:
    if body_weight_pos > other_insights_pos:
        print('✅ Sections are in correct order: Other Insights → Body Weight')
    else:
        print('❌ Sections are in wrong order')
else:
    print('❌ One or both sections not found')

# Check for BMI value display
if 'Your baseline **BMI** is 27.8 kg/m²' in roadmap:
    print('✅ BMI value is being displayed correctly')
else:
    print('❌ BMI value not found in roadmap')
    
# Check for conditional content based on BMI
if 'OVERNIGHT OXIMETRY' in roadmap:
    print('✅ BMI-OSA conditional content found (BMI > 25)')
else:
    print('❌ BMI-OSA conditional content not found')

# Check for anemia warning
if 'trending towards ANEMIA' in roadmap:
    print('✅ Anemia warning found')
else:
    print('❌ Anemia warning not found') 