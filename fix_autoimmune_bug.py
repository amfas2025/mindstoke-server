#!/usr/bin/env python3

def fix_autoimmune_bug():
    """Fix the autoimmune bug by removing problematic lines from roadmap_generator.py"""
    
    # Read the file
    with open('roadmap_generator.py', 'r') as f:
        lines = f.readlines()
    
    # Find and remove the problematic autoimmune logic
    new_lines = []
    skip_lines = False
    
    for i, line in enumerate(lines):
        # Start skipping at the problematic comment
        if '# Trigger autoimmune section for inflammatory conditions' in line and 'risk_scores.get' in lines[i+2]:
            skip_lines = True
            continue
        
        # Stop skipping after the autoimmune_triggered assignment
        if skip_lines and 'processed[\'autoimmune-disease-section\'] = autoimmune_triggered' in line:
            skip_lines = False
            continue
            
        # Skip lines in between
        if skip_lines:
            continue
            
        new_lines.append(line)
    
    # Write the corrected file
    with open('roadmap_generator.py', 'w') as f:
        f.writelines(new_lines)
    
    print("✅ Fixed autoimmune bug - removed problematic lines from _process_hhq_based_conditions")

if __name__ == "__main__":
    fix_autoimmune_bug() 