from typing import Dict, List
from jinja2 import Template

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