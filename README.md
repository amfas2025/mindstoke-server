# Mind Stoke Platform

Internal AMFAS platform for generating personalized health roadmaps based on lab results, health history questionnaires, and cognitive assessments.

## Quick Start

```bash
cd /Users/jstoker/Documents/mindstoke-server
python run.py
```

Server runs on: http://localhost:5001

## 🚨 IMPORTANT: For New Developers/AI Assistants

**READ FIRST**: See `MINDSTOKE_CONTEXT.md` for complete project context, architecture, and development guidelines.

## Core Requirement
**ALL lab values must be represented in generated roadmaps** - this drives all technical decisions.

## Key Files
- `roadmap_generator.py` - Core roadmap generation engine
- `MINDSTOKE_CONTEXT.md` - Complete project documentation
- `app/routes/roadmap.py` - Flask API routes
- `roadmap-template/new-patient-roadmap.txt` - Master template

## Test Client
- ID: `78659670-c75f-4c9e-b9d9-49a18db641b6`
- Debug: http://localhost:5001/roadmap/debug/78659670-c75f-4c9e-b9d9-49a18db641b6

## Phase 1 Features
- ✅ Lab PDF upload and extraction
- ✅ HHQ completion via dynamic links  
- ✅ Cognitive assessment upload
- ✅ Comprehensive roadmap generation
- ✅ Historical data storage

---

For complete documentation and AI assistant onboarding, see `MINDSTOKE_CONTEXT.md`. 