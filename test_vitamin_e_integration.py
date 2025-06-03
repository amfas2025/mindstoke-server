#!/usr/bin/env python3

"""
Integration test for vitamin E condition in full roadmap generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from roadmap_generator import RoadmapGenerator

def test_vitamin_e_integration():
    """Test vitamin E condition in full roadmap generation"""
    
    generator = RoadmapGenerator()
    
    # Test client data with low vitamin E + blood thinner
    client_data = {
        'first_name': 'Test',
        'last_name': 'Client', 
        'name': 'Test Client',
        'gender': 'female',
        'date_of_birth': '1980-01-01'
    }
    
    # Lab results with low vitamin E
    lab_results = {
        'VIT_E': 8.7  # Low vitamin E
    }
    
    # HHQ with blood thinner
    hhq_responses = {
        'hh_blood_thinner': True  # Taking blood thinner
    }
    
    print("=== Testing Vitamin E Integration with Full Roadmap ===")
    print(f"Lab Data: Vitamin E = {lab_results['VIT_E']} mg/L (low)")
    print(f"HHQ Data: Blood thinner = {hhq_responses['hh_blood_thinner']}")
    print()
    
    # Generate roadmap
    try:
        roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
        
        # Check for vitamin E content
        vitamin_e_found = "Your combined **Vitamin E** level is 8.7 mg/L" in roadmap
        supplement_found = "Consider starting a supplement called **COMPLETE E**" in roadmap
        thinner_warning_found = "VITAMIN E can thin the blood" in roadmap
        
        print("✅ Roadmap generated successfully!")
        print(f"   Vitamin E display: {vitamin_e_found}")
        print(f"   Supplement recommendation: {supplement_found}")  
        print(f"   Blood thinner warning: {thinner_warning_found}")
        
        if vitamin_e_found and supplement_found and thinner_warning_found:
            print("🎉 All vitamin E content controls working correctly!")
        else:
            print("⚠️  Some vitamin E content missing - checking roadmap content...")
            
            # Show vitamin E section
            lines = roadmap.split('\n')
            vitamin_e_section = []
            in_vitamin_e = False
            
            for line in lines:
                if "Vitamin E" in line or "VITAMIN E" in line:
                    in_vitamin_e = True
                    vitamin_e_section.append(line)
                elif in_vitamin_e and line.strip() == "":
                    break
                elif in_vitamin_e:
                    vitamin_e_section.append(line)
                    
            print("\n📄 Vitamin E Section Found:")
            for line in vitamin_e_section[:10]:  # Show first 10 lines
                print(f"   {line}")
            
    except Exception as e:
        print(f"❌ Error generating roadmap: {e}")

if __name__ == "__main__":
    test_vitamin_e_integration() 