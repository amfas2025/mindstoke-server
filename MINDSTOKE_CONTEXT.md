# Mind Stoke Platform - Development Context

## Project Overview
Mind Stoke is an internal AMFAS platform for processing client health data and generating personalized PDF roadmaps for brain/body health optimization. Staff upload labs, clients complete HHQ (Health History Questionnaire), cognitive assessments are added, and the system generates comprehensive health roadmaps.

## Critical Technical Architecture

### Core Components
- **Flask Server**: Python backend on port 5001 (`/Users/jstoker/Documents/mindstoke-server`)
- **Supabase Database**: Client records, lab results, HHQ responses, roadmap history
- **Roadmap Generator**: `roadmap_generator.py` - the heart of the system
- **Lab Extractor**: `lab_extractor.py` - extracts data from LabCorp PDFs
- **Template**: `/roadmap-template/new-patient-roadmap.txt` - master roadmap template

### The Core Problem We Solved
**CRITICAL**: The roadmap generator MUST ensure ALL lab values are represented in generated roadmaps. The key enhancement is the `_process_all_content_controls()` method in `roadmap_generator.py` that:

1. **Processes every single lab value** against comprehensive thresholds
2. **Creates intelligent content controls** based on ranges (e.g., vitamin D: D-60+, D-55-59, D-50-55, etc.)  
3. **Handles gender-specific ranges** for hormones
4. **Processes HHQ responses** for lifestyle triggers
5. **Creates compound conditions** (lab + HHQ combinations)
6. **Applies safety nets** to prevent missed lab values

### Key Methods in RoadmapGenerator Class
```python
_process_all_content_controls()           # CORE: Ensures ALL labs processed
_process_all_lab_values_comprehensive()   # Processes every lab with thresholds
_evaluate_lab_threshold()                 # Intelligent threshold evaluation  
_get_comprehensive_lab_ranges()           # Gender-specific lab ranges
_process_hhq_based_conditions()           # HHQ response processing
_apply_safety_nets()                      # Prevents missed lab values
```

## Current Test Client Data
- **Client ID**: `78659670-c75f-4c9e-b9d9-49a18db641b6`
- **Debug URL**: `http://localhost:5001/roadmap/debug/78659670-c75f-4c9e-b9d9-49a18db641b6`
- **Has**: 58 lab results, 229 HHQ responses, complete data for testing

## Debugging Tools Available
1. **Debug Endpoint**: `/roadmap/debug/<client_id>` - shows processed content controls
2. **Server Logs**: Check console for processing details
3. **Test Scripts**: Many test files in root directory for specific scenarios

## Current Server Status
```bash
cd /Users/jstoker/Documents/mindstoke-server && python run.py
# Server runs on http://localhost:5001
```

## Lab Processing Architecture
The system processes these lab categories comprehensively:
- **CBC**: WBC, RBC, Hemoglobin, Platelets
- **Chemistry**: Glucose, BUN, Creatinine, Electrolytes  
- **Liver Function**: ALT, AST, Alkaline Phosphatase
- **Thyroid**: TSH, T3, T4
- **Vitamins**: D, B12, E, Folate
- **Minerals**: Magnesium, Zinc, Copper
- **Omega Fatty Acids**: OmegaCheck, ratios
- **Genetics**: APO E, MTHFR variants
- **Hormones**: Gender-specific ranges

## Template System
Uses Handlebars-style syntax:
- `{{#control-name}}content{{/control-name}}` - conditional blocks
- `{{^control-name}}content{{/control-name}}` - inverted conditionals  
- `{{lab-value}}` - simple value replacement

## Key Requirement
**"We need to make sure all labs are being generated in the roadmap as there is never a situation we don't have lab values in the roadmap"** - This is the core business requirement that drives all technical decisions.

## Files You'll Work With Most
- `roadmap_generator.py` - Core processing engine
- `app/routes/roadmap.py` - Flask routes for roadmap generation
- `roadmap-template/new-patient-roadmap.txt` - Master template
- `lab_extractor.py` - Lab data extraction from PDFs

## Getting Started Checklist
1. Check server is running on port 5001
2. Test debug endpoint with known client ID
3. Verify `_process_all_content_controls()` method exists and is comprehensive
4. Test roadmap generation to ensure lab representation
5. Use existing test scripts for specific scenarios

## Development History & Context
- **Phase 1 Focus**: Internal AMFAS staff use only
- **Core Challenge Solved**: Comprehensive lab value representation in roadmaps
- **Key Enhancement**: Intelligent content control processing system
- **Current Status**: Enhanced roadmap generator with comprehensive lab processing

This platform ensures every client gets a comprehensive, personalized roadmap based on their complete lab profile and health history.

---

## For AI Assistants
**Copy this entire document to new AI chat sessions to get them immediately productive on the Mind Stoke platform.** 