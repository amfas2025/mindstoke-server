#!/usr/bin/env python3
"""
Project cleanup script for Mind Stoke roadmap generator.
Organizes debug files and removes clutter, keeping only essential files.
"""

import os
import shutil
from datetime import datetime
import glob

def cleanup_project():
    """Clean up the project directory."""
    
    print("🧹 MIND STOKE PROJECT CLEANUP")
    print("="*50)
    
    # Create archive directory
    archive_dir = "archive_debug_files"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"📁 Created archive directory: {archive_dir}")
    
    # Files to keep (essential for ongoing work)
    essential_files = {
        'test_roadmap_comparison.py',
        'roadmap_generator.py', 
        'risk_factor_mapping.py',
        'apo_test.py',  # Keep this one as it might have useful logic
        'app.py',
        'README.md',
        'requirements.txt'
    }
    
    # Keep the most recent roadmap outputs (last 2)
    txt_files = glob.glob("*.txt")
    roadmap_files = [f for f in txt_files if 'roadmap' in f.lower()]
    roadmap_files.sort(reverse=True)  # Most recent first
    keep_roadmap_files = set(roadmap_files[:2])  # Keep 2 most recent
    
    essential_files.update(keep_roadmap_files)
    essential_files.update(['CHAT_TEMPLATE.txt', 'requirements.txt'])
    
    moved_count = 0
    deleted_count = 0
    
    # Move debug files to archive
    debug_files = glob.glob("debug_*.py")
    print(f"\n📂 Moving {len(debug_files)} debug files to archive...")
    for file in debug_files:
        if file not in essential_files:
            shutil.move(file, os.path.join(archive_dir, file))
            moved_count += 1
            print(f"  📦 Moved: {file}")
    
    # Move old sample roadmap files
    old_roadmap_files = [f for f in roadmap_files if f not in keep_roadmap_files]
    if old_roadmap_files:
        print(f"\n📂 Moving {len(old_roadmap_files)} old roadmap files to archive...")
        for file in old_roadmap_files:
            shutil.move(file, os.path.join(archive_dir, file))
            moved_count += 1
            print(f"  📦 Moved: {file}")
    
    # Clean up any temporary files
    temp_patterns = ['*.tmp', '*.log', '*.bak', '*~']
    for pattern in temp_patterns:
        temp_files = glob.glob(pattern)
        for file in temp_files:
            os.remove(file)
            deleted_count += 1
            print(f"  🗑️ Deleted: {file}")
    
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"📦 Files moved to archive: {moved_count}")
    print(f"🗑️ Temporary files deleted: {deleted_count}")
    
    print(f"\n📋 ESSENTIAL FILES KEPT:")
    for file in sorted(essential_files):
        if os.path.exists(file):
            print(f"  ✅ {file}")
    
    print(f"\n📁 Archive directory created: {archive_dir}/")
    print(f"   (You can delete this entire folder if needed)")
    
    print(f"\n🎯 PROJECT IS NOW CLEAN AND READY FOR:")
    print(f"  1. 🔍 ARMGASYS roadmap comparison")
    print(f"  2. 🎯 Quality improvements")
    print(f"  3. 🚀 Production deployment")

if __name__ == "__main__":
    cleanup_project() 