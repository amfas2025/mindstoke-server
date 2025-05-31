from app.models.apo_section import APOSection
from app.visualization.apo_wireframe import APOWireframe

def main():
    # Create an APO section instance
    apo_section = APOSection()
    
    # Set some test data
    apo_section.genetic_profile.apo_e1 = 4
    apo_section.genetic_profile.apo_e2 = 4
    apo_section.lab_values.cz_ratio = 1.5
    apo_section.lifestyle_factors.frequent_carb_sugar = True
    
    # Generate recommendations
    recommendations = apo_section.generate_recommendations()
    
    # Get risk level
    risk_level = apo_section.get_risk_level()
    
    # Create wireframe
    wireframe = APOWireframe()
    html = wireframe.generate_wireframe(
        genetic_profile=vars(apo_section.genetic_profile),
        lab_values=vars(apo_section.lab_values),
        risk_level=risk_level,
        recommendations=recommendations
    )
    
    # Save the wireframe to a file
    with open('apo_wireframe.html', 'w') as f:
        f.write(html)
    
    print("Generated wireframe saved to apo_wireframe.html")
    print(f"Risk Level: {risk_level}")
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")

if __name__ == "__main__":
    main() 