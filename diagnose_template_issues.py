#!/usr/bin/env python3
"""
Diagnostic script to identify specific template rendering issues
"""

from roadmap_generator import RoadmapGenerator
import re

def diagnose_template_issues():
    """Identify specific issues in template rendering"""
    print("🔍 DIAGNOSING TEMPLATE ISSUES")
    print("=" * 50)
    
    # Create test data
    client_data = {
        'firstname': 'Sarah',
        'lastname': 'Johnson', 
        'today': 'December 2, 2025',
        'lab-date': 'October 15, 2024'
    }
    
    lab_results = {
        'genome-type': 'E3/E4',
        'glutathione-level': 180,
        'VIT_D25': 32,
        'quick-vitD': 32
    }
    
    hhq_responses = {}
    
    # Generate roadmap
    generator = RoadmapGenerator()
    roadmap = generator.generate_roadmap(client_data, lab_results, hhq_responses)
    
    print("🔍 ISSUE 1: Missing Client Information")
    print("-" * 30)
    
    # Check for empty placeholders
    welcome_line = [line for line in roadmap.split('\n') if 'Welcome' in line]
    if welcome_line:
        print(f"Welcome line: {welcome_line[0]}")
        if '**Welcome **' in welcome_line[0]:
            print("❌ Firstname placeholder not replaced")
        else:
            print("✅ Firstname placeholder working")
    
    # Check date placeholders
    date_line = [line for line in roadmap.split('\n') if 'generated on' in line]
    if date_line:
        print(f"Date line: {date_line[0]}")
        if 'generated on  based' in date_line[0]:
            print("❌ Date placeholders not replaced")
        else:
            print("✅ Date placeholders working")
    
    print("\n🔍 ISSUE 2: Duplicate Vitamin D Recommendations")
    print("-" * 30)
    
    # Find all vitamin D dosing recommendations
    vit_d_doses = re.findall(r'(\d+,?\d*)\s*iu.*?VITAMIN D3', roadmap, re.IGNORECASE)
    print(f"Vitamin D dosing recommendations found: {vit_d_doses}")
    
    if len(vit_d_doses) > 1:
        print(f"❌ Multiple dosing recommendations found: {set(vit_d_doses)}")
        print("This suggests overlapping conditionals")
    else:
        print("✅ Single dosing recommendation (correct)")
    
    print("\n🔍 ISSUE 3: APO E Conflicting Messages")
    print("-" * 30)
    
    # Check for conflicting APO E messages
    apo_e_section = roadmap.split('## **MTHFR Genetics')[0]  # Get APO E section only
    
    e4_risk_patterns = [
        "greater risk of Alzheimer's",
        "APO E4 genes",
        "increased your risk for Alzheimer's"
    ]
    
    non_e4_patterns = [
        "do not have the APO E genetic risk",
        "ADDITIONAL IMMUNE SYSTEM TESTING"
    ]
    
    e4_found = any(pattern in apo_e_section for pattern in e4_risk_patterns)
    non_e4_found = any(pattern in apo_e_section for pattern in non_e4_patterns)
    
    print(f"E4 risk messages found: {e4_found}")
    print(f"Non-E4 messages found: {non_e4_found}")
    
    if e4_found and non_e4_found:
        print("❌ CONFLICT: Both E4 and non-E4 messages appearing")
    elif e4_found:
        print("✅ Correct: Only E4 messages (client has E3/E4)")
    else:
        print("❌ Unexpected: Neither message type found")
    
    print("\n🔍 ISSUE 4: Template Variable Replacement")
    print("-" * 30)
    
    # Check for unreplaced variables
    unreplaced_vars = re.findall(r'{{([^}]+)}}', roadmap)
    if unreplaced_vars:
        print(f"❌ Unreplaced variables found: {unreplaced_vars[:10]}...")  # Show first 10
        print(f"Total unreplaced variables: {len(unreplaced_vars)}")
    else:
        print("✅ All variables replaced successfully")
    
    print("\n🔍 ISSUE 5: Conditional Block Analysis")
    print("-" * 30)
    
    # Look for unclosed conditional blocks
    open_blocks = re.findall(r'{{#([^}]+)}}', roadmap)
    close_blocks = re.findall(r'{{/([^}]+)}}', roadmap)
    
    print(f"Open conditional blocks found: {len(open_blocks)}")
    print(f"Close conditional blocks found: {len(close_blocks)}")
    
    if open_blocks:
        print(f"❌ Unclosed conditionals detected: {open_blocks[:5]}...")
    else:
        print("✅ No unclosed conditional blocks")
    
    print("\n🔍 ISSUE 6: Section Length Analysis")
    print("-" * 30)
    
    sections = roadmap.split('## **')
    section_lengths = {section.split('\n')[0]: len(section) for section in sections if section.strip()}
    
    print("Section lengths:")
    for section_name, length in list(section_lengths.items())[:10]:
        print(f"  {section_name[:30]}: {length} chars")
    
    # Check for unusually long sections (might indicate duplicate content)
    avg_length = sum(section_lengths.values()) / len(section_lengths)
    long_sections = [name for name, length in section_lengths.items() if length > avg_length * 2]
    
    if long_sections:
        print(f"\n⚠️  Unusually long sections (possible duplicates): {long_sections}")
    
    return roadmap

def test_specific_conditionals():
    """Test specific conditional logic that's causing issues"""
    print("\n🧪 TESTING SPECIFIC CONDITIONALS")
    print("=" * 40)
    
    generator = RoadmapGenerator()
    
    # Test APO E logic
    print("Testing APO E conditional logic:")
    
    # Test E3/E4 genotype
    test_data = {
        'firstname': 'Test',
        'genome-type': 'E3/E4'
    }
    
    # Check what the generator's conditional logic produces
    template_content = generator.template_content
    
    # Find APO E section in template
    apo_section_start = template_content.find('## **APO E Genetic Profile')
    apo_section_end = template_content.find('## **MTHFR Genetics')
    apo_section = template_content[apo_section_start:apo_section_end]
    
    # Look for conditional patterns
    e4_conditions = re.findall(r'{{#(quick-E4[^}]*?)}}', apo_section)
    non_e4_conditions = re.findall(r'{{#(quick-nonE4[^}]*?)}}', apo_section)
    
    print(f"E4-related conditions: {e4_conditions}")
    print(f"Non-E4 conditions: {non_e4_conditions}")
    
    # Test vitamin D logic
    print("\nTesting Vitamin D conditional logic:")
    vit_d_conditions = re.findall(r'{{#(.*?D.*?)}}', template_content[:5000])  # First 5000 chars
    print(f"Vitamin D conditions found: {set(vit_d_conditions)}")

if __name__ == "__main__":
    roadmap = diagnose_template_issues()
    test_specific_conditionals()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS COMPLETE")
    print("=" * 50)
    print("Review the issues above to fix template rendering problems.") 