from dataclasses import dataclass
from typing import Dict, Optional, List
from jinja2 import Template

# Data Models
@dataclass
class LabValues:
    cz_ratio: Optional[float] = None
    
@dataclass
class LifestyleFactors:
    frequent_carb_sugar: bool = False

@dataclass
class GeneticProfile:
    apo_e1: Optional[int] = None
    apo_e2: Optional[int] = None

class APOSection:
    def __init__(self):
        self.genetic_profile = GeneticProfile()
        self.lab_values = LabValues()
        self.lifestyle_factors = LifestyleFactors()
        self.recommendations: List[str] = []
        
    def evaluate_rules(self) -> Dict[str, bool]:
        """Evaluates all APO-related rules and returns their status"""
        rules = {
            "quick-CZratio-14": self._check_cz_ratio_rule(),
            "quick-E4": self._check_e4_carrier_rule(),
            "quick-E4E4": self._check_e4e4_rule(),
            "quick-nonE4": self._check_non_e4_rule(),
            "quick-sugars-APOE4": self._check_sugars_apoe4_rule(),
            "zinc-liposomalC": self._check_zinc_liposomal_rule()
        }
        return rules
    
    def _check_cz_ratio_rule(self) -> bool:
        """[C:Z] > 1.3 and ((APO_E1) = 3 or (APO_E2) = 3 or [APO_E1] = 2 or [APO_E2] = 2)"""
        if not self.lab_values.cz_ratio:
            return False
            
        high_cz = self.lab_values.cz_ratio > 1.3
        apo_condition = (self.genetic_profile.apo_e1 in [2, 3] or 
                        self.genetic_profile.apo_e2 in [2, 3])
        return high_cz and apo_condition
    
    def _check_e4_carrier_rule(self) -> bool:
        """(APO_E1 = 4 and APO_E2 <= 3) or ((APO_E1 <= 3 and APO_E2 = 4)"""
        if not all([self.genetic_profile.apo_e1, self.genetic_profile.apo_e2]):
            return False
            
        return ((self.genetic_profile.apo_e1 == 4 and self.genetic_profile.apo_e2 <= 3) or
                (self.genetic_profile.apo_e1 <= 3 and self.genetic_profile.apo_e2 == 4))
    
    def _check_e4e4_rule(self) -> bool:
        """APO_E1 = 4 and APO_E2 = 4"""
        return (self.genetic_profile.apo_e1 == 4 and 
                self.genetic_profile.apo_e2 == 4)
    
    def _check_non_e4_rule(self) -> bool:
        """APO_E1 != 4 and APO_E2 != 4"""
        return (self.genetic_profile.apo_e1 != 4 and 
                self.genetic_profile.apo_e2 != 4)
    
    def _check_sugars_apoe4_rule(self) -> bool:
        """[hh-frequent-carb-sugar] and ((APO_E1) = 4 or (APO_E2) = 4)"""
        if not self.lifestyle_factors.frequent_carb_sugar:
            return False
            
        return (self.genetic_profile.apo_e1 == 4 or 
                self.genetic_profile.apo_e2 == 4)
    
    def _check_zinc_liposomal_rule(self) -> bool:
        """[C:Z] > 1.3 and [APO_E1] < 4 and [APO_E2] < 4"""
        if not self.lab_values.cz_ratio:
            return False
            
        return (self.lab_values.cz_ratio > 1.3 and
                self.genetic_profile.apo_e1 < 4 and
                self.genetic_profile.apo_e2 < 4)
    
    def generate_recommendations(self) -> List[str]:
        """Generates recommendations based on triggered rules"""
        self.recommendations = []
        rules = self.evaluate_rules()
        
        if rules["quick-E4E4"]:
            self.recommendations.append("High Priority: Double E4 carrier status detected - "
                                     "requires specific dietary and lifestyle modifications")
            
        elif rules["quick-E4"]:
            self.recommendations.append("Important: E4 carrier status detected - "
                                     "moderate dietary and lifestyle modifications recommended")
            
        if rules["quick-CZratio-14"]:
            self.recommendations.append("Monitor: Elevated Copper:Zinc ratio requires attention")
            
        if rules["quick-sugars-APOE4"]:
            self.recommendations.append("Dietary Alert: Reduce carbohydrate intake based on "
                                     "E4 status and current consumption patterns")
            
        if rules["zinc-liposomalC"]:
            self.recommendations.append("Supplement Consideration: Evaluate Zinc and "
                                     "Liposomal Vitamin C supplementation")
            
        return self.recommendations

    def get_risk_level(self) -> str:
        """Determines overall risk level based on genetic profile and rules"""
        rules = self.evaluate_rules()
        
        if rules["quick-E4E4"]:
            return "High"
        elif rules["quick-E4"]:
            return "Moderate"
        elif rules["quick-nonE4"]:
            return "Low"
        return "Unknown"

class APOWireframe:
    def __init__(self):
        self.template = Template("""
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            max-width: 800px;
            margin: 0 auto;
            font-family: Arial, sans-serif;
        }
        .section {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .risk-high { background-color: #ffebee; }
        .risk-moderate { background-color: #fff3e0; }
        .risk-low { background-color: #e8f5e9; }
        .risk-unknown { background-color: #f5f5f5; }
        .recommendation {
            margin: 10px 0;
            padding: 10px;
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .genetic-profile {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .lab-values {
            margin-top: 20px;
        }
        .chart-placeholder {
            width: 100%;
            height: 200px;
            background-color: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="section risk-{{ risk_level.lower() }}">
            <h2>APO E Genetic Profile</h2>
            <div class="genetic-profile">
                <div>
                    <strong>APO E1:</strong> {{ genetic_profile.apo_e1 or 'Not Available' }}
                </div>
                <div>
                    <strong>APO E2:</strong> {{ genetic_profile.apo_e2 or 'Not Available' }}
                </div>
            </div>
            
            <div class="lab-values">
                <h3>Related Lab Values</h3>
                <p><strong>Copper:Zinc Ratio:</strong> {{ lab_values.cz_ratio or 'Not Available' }}</p>
            </div>

            <div class="chart-placeholder">
                [Visualization of APO E Status and Related Markers]
            </div>

            <h3>Risk Level: {{ risk_level }}</h3>
            
            <h3>Recommendations</h3>
            {% for rec in recommendations %}
            <div class="recommendation">
                {{ rec }}
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
        """)
    
    def generate_wireframe(self, 
                          genetic_profile: Dict,
                          lab_values: Dict,
                          risk_level: str,
                          recommendations: List[str]) -> str:
        """
        Generates an HTML wireframe for the APO section
        """
        return self.template.render(
            genetic_profile=genetic_profile,
            lab_values=lab_values,
            risk_level=risk_level,
            recommendations=recommendations
        )

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