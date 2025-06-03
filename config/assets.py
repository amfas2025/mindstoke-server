"""
Visual assets configuration for Mind Stoke roadmap generator.
Manages paths to logos, supplements, icons, and branding elements.
"""

import os
from typing import Dict, Optional


class AssetConfig:
    """Configuration for visual assets used in roadmap PDF generation."""
    
    def __init__(self, base_path: str = None):
        """Initialize asset configuration with base path."""
        if base_path is None:
            base_path = "/Users/jstoker/Documents/mindstoke-server/app/static/images/roadmap"
        
        self.base_path = base_path
        
        # Asset categories and their files
        self.visual_assets = {
            'logos': {
                'main_logo': os.path.join(base_path, 'logos', 'main_logo.png'),
                'amfas_logo': os.path.join(base_path, 'logos', 'amfas_logo.png'),
            },
            'supplements': {
                'vitamin_d': os.path.join(base_path, 'supplements', 'vitamin_d.png'),
                'omega3': os.path.join(base_path, 'supplements', 'omega3.png'),
                'magnesium': os.path.join(base_path, 'supplements', 'magnesium.png'),
                'b_complex': os.path.join(base_path, 'supplements', 'b_complex.png'),
            },
            'icons': {
                'brain': os.path.join(base_path, 'icons', 'brain.png'),
                'heart': os.path.join(base_path, 'icons', 'heart.png'),
                'supplement': os.path.join(base_path, 'icons', 'supplement.png'),
                'lab': os.path.join(base_path, 'icons', 'lab.png'),
            },
            'branding': {
                'header_bg': os.path.join(base_path, 'branding', 'header_bg.png'),
                'footer_bg': os.path.join(base_path, 'branding', 'footer_bg.png'),
            }
        }
    
    def get_asset_path(self, category: str, asset_name: str) -> Optional[str]:
        """Get the full path to a specific asset."""
        if category in self.visual_assets and asset_name in self.visual_assets[category]:
            return self.visual_assets[category][asset_name]
        return None
    
    def asset_exists(self, category: str, asset_name: str) -> bool:
        """Check if an asset file exists."""
        asset_path = self.get_asset_path(category, asset_name)
        if asset_path:
            return os.path.exists(asset_path)
        return False
    
    def get_supplement_image(self, supplement_name: str) -> Optional[str]:
        """Get supplement image path by supplement name."""
        # Map supplement names to image files
        supplement_mapping = {
            'vitamin_d': 'vitamin_d',
            'vitamin d': 'vitamin_d',
            'omega3': 'omega3',
            'omega-3': 'omega3',
            'fish oil': 'omega3',
            'magnesium': 'magnesium',
            'b_complex': 'b_complex',
            'b complex': 'b_complex',
            'b-complex': 'b_complex',
        }
        
        # Normalize supplement name
        normalized_name = supplement_name.lower().strip()
        if normalized_name in supplement_mapping:
            mapped_name = supplement_mapping[normalized_name]
            if self.asset_exists('supplements', mapped_name):
                return self.get_asset_path('supplements', mapped_name)
        
        return None
    
    def get_all_assets(self) -> Dict[str, Dict[str, str]]:
        """Get all configured visual assets."""
        return self.visual_assets.copy() 