#!/usr/bin/env python3

"""
Risk Factor Mapping System for Other Insights Risk Profile
Maps HHQ responses to risk category scores for comprehensive brain health assessment.
"""

from typing import Dict, Any, Tuple

class RiskFactorMapper:
    """Maps HHQ responses to risk category scores."""
    
    def __init__(self):
        """Initialize with risk factor rules from the Risk Factor Rule Editor."""
        # Each rule maps: HHQ variable -> (Inflammatory, Atrophic, Glycotoxic, Toxic, Vascular, Traumatic)
        self.risk_factor_rules = {
            # Vascular Risk Factors
            'hh-leg-lung-clots': (0, 0, 0, 0, 1, 0),
            'hh-dvt-pulmonary-embolism': (0, 0, 0, 0, 1, 0),
            'hh-blood-clots': (0, 0, 0, 0, 1, 0),
            'hh-pulmonary-embolism': (0, 0, 0, 0, 1, 0),
            'hh-heart-attack': (0, 0, 0, 0, 1, 0),
            'hh-stroke': (0, 0, 0, 0, 1, 0),
            'hh-tia': (0, 0, 0, 0, 1, 0),
            'hh-stroke-tia': (0, 0, 0, 0, 1, 0),
            'hh-atherosclerosis': (0, 0, 0, 0, 1, 0),
            'hh-high-blood-pressure': (0, 0, 0, 0, 0.5, 0),
            'hh-cardiac-bypass': (0, 0, 0, 0, 1, 0),
            'hh-angioplasty': (0, 0, 0, 0, 1, 0),
            'hh-cardiac-stent': (0, 0, 0, 0, 1, 0),
            'hh-atrial-fibrillation': (0, 0, 0, 0, 0.5, 0),
            
            # Toxic Risk Factors  
            'hh-electroshock-therapy': (0, 0.25, 0, 0.5, 0.25, 0),
            'hh-welding-soldering': (0, 0, 0, 1, 0, 0),
            'hh-work-home-mold': (0, 0, 0, 1, 0, 0),
            'hh-mold-exposure': (0, 0, 0, 1, 0, 0),
            'hh-chemical-exposure': (0, 0, 0, 1, 0, 0),
            'hh-pesticide-exposure': (0, 0, 0, 1, 0, 0),
            'hh-heavy-metal-exposure': (0, 0, 0, 1, 0, 0),
            'hh-mercury-exposure': (0, 0, 0, 1, 0, 0),
            'hh-lead-exposure': (0, 0, 0, 1, 0, 0),
            'hh-asbestos-exposure': (0, 0, 0, 1, 0, 0),
            'hh-occupational-chemicals': (0, 0, 0, 1, 0, 0),
            'hh-solvent-exposure': (0, 0, 0, 1, 0, 0),
            
            # Inflammatory Risk Factors
            'hh-anti-inflam-meds': (1, 0, 0, 0, 0, 0),
            'hh-frequent-ibuprofen': (1, 0, 0, 0, 0, 0),
            'hh-frequent-nsaid': (1, 0, 0, 0, 0, 0),
            'hh-chronic-pain': (1, 0, 0, 0, 0, 0),
            'hh-arthritis': (1, 0, 0, 0, 0, 0),
            'hh-autoimmune-disease': (1, 0, 0, 0, 0, 0),
            'hh-inflammatory-bowel': (1, 0, 0, 0, 0, 0),
            'hh-crohns-disease': (1, 0, 0, 0, 0, 0),
            'hh-ulcerative-colitis': (1, 0, 0, 0, 0, 0),
            'hh-celiac-disease': (1, 0, 0, 0, 0, 0),
            'hh-food-allergies': (0.5, 0, 0, 0, 0, 0),
            'hh-chronic-allergies': (0.5, 0, 0, 0, 0, 0),
            
            # Traumatic Risk Factors
            'hh-head-injury': (0, 0, 0, 0, 0, 1),
            'hh-concussion': (0, 0, 0, 0, 0, 1),
            'hh-traumatic-brain-injury': (0, 0, 0, 0, 0, 1),
            'hh-tbi': (0, 0, 0, 0, 0, 1),
            'hh-multiple-concussions': (0, 0, 0, 0, 0, 1.5),
            'hh-sports-head-injury': (0, 0, 0, 0, 0, 1),
            'hh-car-accident-head': (0, 0, 0, 0, 0, 1),
            'hh-fall-head-injury': (0, 0, 0, 0, 0, 1),
            
            # Glycotoxic Risk Factors
            'hh-diabetes': (0, 0, 1, 0, 0, 0),
            'hh-type-2-diabetes': (0, 0, 1, 0, 0, 0),
            'hh-insulin-resistance': (0, 0, 1, 0, 0, 0),
            'hh-metabolic-syndrome': (0, 0, 1, 0, 0, 0),
            'hh-high-blood-sugar': (0, 0, 0.5, 0, 0, 0),
            'hh-frequent-carb-sugar': (0, 0, 0.5, 0, 0, 0),
            'hh-sugar-cravings': (0, 0, 0.5, 0, 0, 0),
            'hh-processed-foods': (0, 0, 0.5, 0, 0, 0),
            
            # Atrophic Risk Factors
            'hh-menopause': (0, 1, 0, 0, 0, 0),
            'hh-postmenopausal': (0, 1, 0, 0, 0, 0),
            'hh-low-testosterone': (0, 1, 0, 0, 0, 0),
            'hh-hormone-deficiency': (0, 1, 0, 0, 0, 0),
            'hh-thyroid-disease': (0, 0.5, 0, 0, 0, 0),
            'hh-hypothyroid': (0, 0.5, 0, 0, 0, 0),
            'hh-nutrient-deficiency': (0, 0.5, 0, 0, 0, 0),
            'hh-poor-diet': (0, 0.5, 0, 0, 0, 0),
            'hh-malabsorption': (0, 0.5, 0, 0, 0, 0),
            'hh-weight-loss-surgery': (0, 0.5, 0, 0, 0, 0),
            'hh-bowel-surgery': (0, 0.5, 0, 0, 0, 0),
        }
    
    def calculate_risk_scores(self, hhq_responses: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate risk scores for each category based on HHQ responses.
        
        Args:
            hhq_responses: Dictionary of HHQ responses
            
        Returns:
            Dictionary with risk scores for each category
        """
        risk_scores = {
            'inflammatory': 0.0,
            'atrophic': 0.0, 
            'glycotoxic': 0.0,
            'toxic': 0.0,
            'vascular': 0.0,
            'traumatic': 0.0
        }
        
        for hhq_variable, response_value in hhq_responses.items():
            # Only process True responses (indicating presence of risk factor)
            if response_value is True and hhq_variable in self.risk_factor_rules:
                scores = self.risk_factor_rules[hhq_variable]
                risk_scores['inflammatory'] += scores[0]
                risk_scores['atrophic'] += scores[1]
                risk_scores['glycotoxic'] += scores[2]
                risk_scores['toxic'] += scores[3]
                risk_scores['vascular'] += scores[4]
                risk_scores['traumatic'] += scores[5]
        
        return risk_scores
    
    def calculate_risk_percentages(self, risk_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Convert raw risk scores to percentages for visualization.
        
        Args:
            risk_scores: Raw risk scores from calculate_risk_scores
            
        Returns:
            Dictionary with percentage values for each risk category
        """
        total_score = sum(risk_scores.values())
        
        if total_score == 0:
            return {category: 0.0 for category in risk_scores.keys()}
        
        risk_percentages = {}
        for category, score in risk_scores.items():
            risk_percentages[category] = (score / total_score) * 100
            
        return risk_percentages
    
    def get_top_risk_factors(self, risk_percentages: Dict[str, float], limit: int = 3) -> list:
        """
        Get the top risk factors ordered by percentage.
        
        Args:
            risk_percentages: Risk percentages from calculate_risk_percentages
            limit: Maximum number of risk factors to return
            
        Returns:
            List of tuples (category, percentage) ordered by highest percentage
        """
        sorted_risks = sorted(risk_percentages.items(), key=lambda x: x[1], reverse=True)
        return [(category, percentage) for category, percentage in sorted_risks[:limit] if percentage > 0]
    
    def get_risk_factor_details(self, hhq_responses: Dict[str, Any]) -> Dict[str, list]:
        """
        Get specific risk factors that contributed to each category.
        
        Args:
            hhq_responses: Dictionary of HHQ responses
            
        Returns:
            Dictionary mapping each risk category to list of contributing factors
        """
        risk_details = {
            'inflammatory': [],
            'atrophic': [],
            'glycotoxic': [],
            'toxic': [],
            'vascular': [],
            'traumatic': []
        }
        
        category_names = ['inflammatory', 'atrophic', 'glycotoxic', 'toxic', 'vascular', 'traumatic']
        
        for hhq_variable, response_value in hhq_responses.items():
            if response_value is True and hhq_variable in self.risk_factor_rules:
                scores = self.risk_factor_rules[hhq_variable]
                
                for i, score in enumerate(scores):
                    if score > 0:
                        # Convert variable name to readable format
                        readable_name = hhq_variable.replace('hh-', '').replace('-', ' ').title()
                        risk_details[category_names[i]].append(readable_name)
        
        return risk_details 