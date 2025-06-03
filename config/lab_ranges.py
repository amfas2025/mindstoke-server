"""
Comprehensive lab reference ranges for Mind Stoke roadmap generator.
Gender-specific ranges where appropriate.
"""

from typing import Dict


class LabRanges:
    """Lab reference ranges for intelligent threshold evaluation."""
    
    @classmethod
    def get_comprehensive_ranges(cls, gender: str) -> Dict[str, Dict[str, float]]:
        """
        Get comprehensive lab ranges for intelligent threshold evaluation.
        Gender-specific where appropriate.
        """
        base_ranges = {
            'CRP': {'optimal_max': 1.0, 'high': 3.0, 'critical_high': 10.0},
            'Homocysteine': {'optimal_max': 7.0, 'high': 10.4, 'critical_high': 15.0},
            'UricAcid': {'optimal_max': 6.5, 'high': 8.0, 'critical_high': 10.0},
            'AGRatio': {'optimal_min': 1.5, 'low': 1.2, 'critical_low': 1.0},
            'TotalProtein': {'low': 6.0, 'optimal_min': 6.5, 'optimal_max': 8.5, 'high': 9.0},
            
            # Complete Blood Count
            'WBC': {'low': 3.5, 'optimal_min': 4.0, 'optimal_max': 10.0, 'high': 12.0},
            'RBC': {'low': 4.0, 'optimal_min': 4.2, 'optimal_max': 5.5, 'high': 6.0},
            'Hemoglobin': {'low': 12.0, 'optimal_min': 13.0, 'optimal_max': 16.0, 'high': 18.0},
            'Hematocrit': {'low': 36.0, 'optimal_min': 37.0, 'optimal_max': 48.0, 'high': 52.0},
            'MCV': {'low': 80, 'optimal_min': 82, 'optimal_max': 98, 'high': 100},
            'Platelets': {'low': 150, 'optimal_min': 200, 'optimal_max': 400, 'high': 500},
            
            # Coagulation
            'DDimer': {'optimal_max': 500, 'high': 1000, 'critical_high': 2000},
            
            # Basic Metabolic Panel
            'Glucose': {'low': 70, 'optimal_min': 80, 'optimal_max': 99, 'high': 125},
            'BUN': {'low': 7, 'optimal_min': 10, 'optimal_max': 20, 'high': 25},
            'Creatinine': {'optimal_min': 0.6, 'optimal_max': 1.2, 'high': 1.5},
            'eGFR': {'low': 60, 'optimal_min': 90},
            
            # Electrolytes
            'Sodium': {'low': 135, 'optimal_min': 138, 'optimal_max': 145, 'high': 148},
            'Potassium': {'low': 3.5, 'optimal_min': 3.8, 'optimal_max': 5.0, 'high': 5.5},
            'Chloride': {'low': 98, 'optimal_min': 101, 'optimal_max': 107, 'high': 110},
            'Calcium': {'low': 8.5, 'optimal_min': 9.0, 'optimal_max': 10.5, 'high': 11.0},
            
            # Liver Function
            'ALT': {'optimal_max': 25, 'high': 40, 'critical_high': 80},
            'AST': {'optimal_max': 25, 'high': 40, 'critical_high': 80},
            'AlkalinePhosphatase': {'low': 44, 'optimal_min': 50, 'optimal_max': 120, 'high': 150},
            'Albumin': {'low': 3.5, 'optimal_min': 4.0, 'optimal_max': 5.0, 'high': 5.5},
            
            # Thyroid Function
            'TSH': {'optimal_min': 0.5, 'optimal_max': 2.5, 'high': 4.0, 'critical_high': 10.0},
            'T3': {'low': 2.3, 'optimal_min': 3.0, 'optimal_max': 4.2, 'high': 4.8},
            'T4': {'low': 0.8, 'optimal_min': 1.0, 'optimal_max': 1.8, 'high': 2.2},
            
            # Vitamins & Minerals
            'VitaminD': {'critical_low': 20, 'low': 30, 'optimal_min': 50, 'optimal_max': 80, 'high': 100},
            'VitB12': {'low': 300, 'optimal_min': 500, 'optimal_max': 1000, 'high': 1500},
            'VitaminE': {'low': 5.5, 'optimal_min': 8.0, 'optimal_max': 20.0, 'high': 25.0},
            'Zinc': {'low': 60, 'optimal_min': 80, 'optimal_max': 120, 'high': 150},
            'Copper': {'low': 70, 'optimal_min': 80, 'optimal_max': 140, 'high': 200},
            'Selenium': {'low': 70, 'optimal_min': 125, 'optimal_max': 200, 'high': 300},
            'Magnesium': {'low': 4.2, 'optimal_min': 5.2, 'optimal_max': 6.5, 'high': 7.0},
            
            # Omega Fatty Acids
            'OmegaCheck': {'optimal_min': 5.4, 'high': 8.0},
            'Omega63Ratio': {'optimal_max': 4.0, 'high': 6.0, 'critical_high': 10.0},
            'AAEPARatio': {'optimal_max': 8.0, 'high': 12.0, 'critical_high': 20.0},
            'ArachidonicAcid': {'optimal_max': 10.0, 'high': 15.0},
            
            # Metabolic Markers
            'Insulin': {'optimal_max': 10.0, 'high': 15.0, 'critical_high': 25.0},
            'HbA1c': {'optimal_max': 5.7, 'high': 6.4, 'critical_high': 8.0},
            
            # Lipid Panel
            'TotalCholesterol': {'optimal_max': 200, 'high': 240, 'critical_high': 300},
            'Triglycerides': {'optimal_max': 150, 'high': 200, 'critical_high': 500},
            'HDLCholesterol': {'low': 40, 'optimal_min': 50, 'optimal_max': 80, 'high': 100},
            'LDLCholesterol': {'optimal_max': 100, 'high': 130, 'critical_high': 190},
        }
        
        # Gender-specific adjustments
        if gender == 'female':
            base_ranges.update({
                'Testosterone': {'low': 15, 'optimal_min': 25, 'optimal_max': 85, 'high': 100},
                'Estradiol': {'low': 30, 'optimal_min': 50, 'optimal_max': 300, 'high': 400},
                'Progesterone': {'low': 5, 'optimal_min': 10, 'optimal_max': 25, 'high': 35}
            })
        elif gender == 'male':
            base_ranges.update({
                'Testosterone': {'low': 300, 'optimal_min': 450, 'optimal_max': 900, 'high': 1200},
                'FreeTestosterone': {'low': 9, 'optimal_min': 15, 'optimal_max': 30, 'high': 40},
                'PSA': {'optimal_max': 2.5, 'high': 4.0, 'critical_high': 10.0}
            })
        
        return base_ranges 