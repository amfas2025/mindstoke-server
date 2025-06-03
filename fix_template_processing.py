#!/usr/bin/env python3
"""
Fix the template processing issues in roadmap_generator.py
"""

import re
from datetime import datetime

def fix_client_info_replacement():
    """
    Fix the _replace_client_info method to handle {{firstname}}, {{today}}, {{lab-date}} placeholders
    """
    
    fix_code = '''
    def _replace_client_info(self, roadmap: str, client_data: Dict[str, Any]) -> str:
        """Replace basic client information placeholders."""
        
        # Handle Handlebars-style placeholders
        firstname = client_data.get('firstname', client_data.get('name', 'Patient'))
        roadmap = roadmap.replace('{{firstname}}', firstname)
        
        # Handle today's date
        today = client_data.get('today', datetime.now().strftime('%B %d, %Y'))
        roadmap = roadmap.replace('{{today}}', today)
        
        # Handle lab date
        lab_date = client_data.get('lab-date', client_data.get('labs_date', 'your recent labs'))
        roadmap = roadmap.replace('{{lab-date}}', lab_date)
        
        # Legacy replacements (keep for backward compatibility)
        name = client_data.get('name', firstname)
        roadmap = roadmap.replace('_______', name)  # Main name placeholder
        roadmap = roadmap.replace('___________', name)  # Secondary name placeholder
        roadmap = roadmap.replace('Dear _-', f'Dear {name},')
        
        # Date replacements (legacy)
        report_date = datetime.now().strftime('%B %d, %Y')
        roadmap = roadmap.replace('Report Date: _', f'Report Date: {report_date}')
        roadmap = roadmap.replace('Report Date: __', f'Report Date: {report_date}')
        
        # Labs drawn date (legacy)
        labs_date = client_data.get('labs_date', report_date)
        roadmap = roadmap.replace('Labs Drawn: _____', f'Labs Drawn: {labs_date}')
        
        return roadmap
    '''
    
    return fix_code

def fix_conditional_logic_approach():
    """
    Explanation of how to fix the conditional logic issues
    """
    
    approach = '''
    CONDITIONAL LOGIC FIXES NEEDED:
    
    1. APO E Genetics Issue:
       - Template has both {{#quick-E4}} and {{#quick-nonE4}} sections
       - The processor should set ONLY ONE of these to True
       - Currently both are being set to True
    
    2. Vitamin D Issue:
       - Multiple overlapping vitamin D conditions are being triggered
       - Need exclusive logic: only ONE dosing recommendation should appear
    
    3. The _process_all_content_controls method needs to:
       - Set mutually exclusive conditions properly
       - Use if/elif logic instead of multiple if statements
       - Ensure only appropriate sections are shown
    
    SOLUTION APPROACH:
    In the _process_all_content_controls method, we need to fix:
    
    # APO E Logic (should be mutually exclusive)
    genome_type = lab_results.get('genome-type', '').upper()
    if 'E4' in genome_type:
        processed['quick-E4'] = True
        processed['quick-nonE4'] = False
        if 'E4/E4' in genome_type:
            processed['quick-E4E4'] = True
        elif 'E4/E3' in genome_type or 'E3/E4' in genome_type:
            processed['quick-E4E3'] = True
    else:
        processed['quick-E4'] = False  
        processed['quick-nonE4'] = True
        processed['quick-E4E4'] = False
        processed['quick-E4E3'] = False
    
    # Vitamin D Logic (should be mutually exclusive)
    vit_d = self._get_lab_value(lab_results, ['VIT_D25', 'quick-vitD'])
    if vit_d:
        # Clear all vitamin D conditions first
        processed['D-less-30'] = False
        processed['D-30-39'] = False 
        processed['D-40-49'] = False
        processed['D-50-59'] = False
        processed['D-optimal'] = False
        
        # Set only the appropriate condition
        if vit_d < 30:
            processed['D-less-30'] = True
        elif vit_d < 40:
            processed['D-30-39'] = True
        elif vit_d < 50:
            processed['D-40-49'] = True
        elif vit_d < 60:
            processed['D-50-59'] = True
        else:
            processed['D-optimal'] = True
    '''
    
    return approach

def create_test_for_fixes():
    """
    Create a test to verify the fixes work
    """
    
    test_code = '''
#!/usr/bin/env python3
"""
Test the fixed template processing
"""

from roadmap_generator import RoadmapGenerator

def test_fixed_processing():
    """Test that the fixes resolve the template issues"""
    
    # Test data
    client_data = {
        'firstname': 'Sarah',
        'today': 'December 2, 2025', 
        'lab-date': 'October 15, 2024'
    }
    
    lab_results = {
        'genome-type': 'E3/E4',  # Should trigger ONLY E4 conditions
        'VIT_D25': 32,           # Should trigger ONLY D-30-39 condition
        'glutathione-level': 180
    }
    
    generator = RoadmapGenerator()
    roadmap = generator.generate_roadmap(client_data, lab_results, {})
    
    # Test 1: Client info replacement
    print("🧪 Testing Client Info Replacement")
    if '{{firstname}}' not in roadmap and 'Sarah' in roadmap:
        print("✅ Firstname replacement: FIXED")
    else:
        print("❌ Firstname replacement: STILL BROKEN")
    
    if '{{today}}' not in roadmap and 'December 2, 2025' in roadmap:
        print("✅ Today replacement: FIXED")
    else:
        print("❌ Today replacement: STILL BROKEN")
    
    # Test 2: APO E exclusive logic
    print("\\n🧪 Testing APO E Exclusive Logic")
    apo_section = roadmap.split('## **MTHFR Genetics')[0]
    
    has_e4_risk = "greater risk of Alzheimer's" in apo_section
    has_non_e4 = "do not have the APO E genetic risk" in apo_section
    
    if has_e4_risk and not has_non_e4:
        print("✅ APO E logic: FIXED (only E4 messages)")
    elif not has_e4_risk and has_non_e4:
        print("✅ APO E logic: FIXED (only non-E4 messages)")
    else:
        print("❌ APO E logic: STILL BROKEN (conflicting messages)")
    
    # Test 3: Vitamin D exclusive dosing
    print("\\n🧪 Testing Vitamin D Exclusive Dosing")
    vit_d_doses = re.findall(r'(\\d+,?\\d*)\\s*iu.*?VITAMIN D3', roadmap, re.IGNORECASE)
    unique_doses = set(vit_d_doses)
    
    if len(unique_doses) == 1:
        print(f"✅ Vitamin D dosing: FIXED (single recommendation: {unique_doses})")
    else:
        print(f"❌ Vitamin D dosing: STILL BROKEN (multiple: {unique_doses})")
    
    return roadmap

if __name__ == "__main__":
    test_fixed_processing()
    '''
    
    return test_code

def main():
    print("🔧 TEMPLATE PROCESSING FIXES")
    print("=" * 40)
    
    print("1. CLIENT INFO REPLACEMENT FIX:")
    print(fix_client_info_replacement())
    
    print("\n2. CONDITIONAL LOGIC APPROACH:")
    print(fix_conditional_logic_approach())
    
    print("\n3. Creating test file...")
    
    # Create the test file
    test_code = create_test_for_fixes()
    with open('test_template_fixes.py', 'w') as f:
        f.write(test_code)
    
    print("✅ Created test_template_fixes.py")
    print("\nNEXT STEPS:")
    print("1. Apply the client info replacement fix to roadmap_generator.py")
    print("2. Fix the conditional logic in _process_all_content_controls method")
    print("3. Run test_template_fixes.py to verify fixes")

if __name__ == "__main__":
    main() 