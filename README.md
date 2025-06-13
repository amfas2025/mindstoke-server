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

# Mind Stoke – Phase 1 Product Requirements Document (PRD)
**Version**: 0.1  
**Created by**: Jeff Stoker  
**Last updated**: May 24, 2025  
**Target Completion**: Late July 2025  

---

## 1. Overview

Mind Stoke is an internal-use platform designed for AMFAS staff to intake client data (labs, health history, and cognitive assessments), extract key information, and generate a personalized PDF Roadmap for brain and body health optimization.

---

## 2. Phase 1 Goals

- Allow AMFAS staff to upload labs and auto-extract data
- Store structured HHQ responses from clients via dynamic links
- Upload and extract cognitive assessment data (CNS or MoCA)
- Generate a personalized Roadmap PDF once all three inputs are complete
- Save all client data historically in Supabase
- No client or practitioner access required at this stage

---

## 3. Users

**Internal AMFAS staff only**

All logged-in staff can:
- View and manage client records
- Upload labs
- Upload cognitive assessments
- Confirm HHQ completion
- Trigger/download Roadmaps

---

## 4. Client Record Creation

Client records are created automatically via Zapier when a protocol is purchased via the AMFAS website. Fields to capture in Supabase:

- Full name
- Email
- Phone number
- Date of birth
- Address
- Assessment status
- Assessment type
- Cognitive test uploads (CNS or MoCA)

---

## 5. Lab Upload

- PDF upload via drag-and-drop or file selector
- Data extracted from LabCorp reports using existing extraction logic
- Extracted values stored in Supabase, tied to client ID
- Triggers: No Roadmap generation until HHQ and cognitive test are also completed

---

## 6. Health History Questionnaire (HHQ)

- Clients receive a dynamic link to complete their HHQ
- No login required
- Responses stored as structured tags in Supabase (e.g., `hh-brain_fog`)
- Roadmap logic uses tags; no admin override or summary required in Phase 1

---

## 7. Cognitive Assessment

### CNS Vital Signs:
- PDF uploaded by staff
- Extract domains: Patient Score, Standard Score, Percentile, Validity Indicator, Category
- 15 domains stored per test
- Stored historically in Supabase

### MoCA:
- PDF uploaded by staff
- Store MoCA score (e.g. 24/30)
- Store date and uploaded_by
- No special Roadmap logic differences from CNS

---

## 8. Roadmap Generation

- Automatically or manually triggered **only when labs + HHQ + cognitive test are present**
- Output: Downloadable PDF stored in Supabase under the client record
- Staff manually sends PDF to client via email or Circle
- Roadmap includes optional screenshot (manually added) of cognitive test

---

## 9. Authentication

- Internal user login for AMFAS staff only
- No client or external practitioner logins required in Phase 1

---

## 10. Data Storage & History

- All assessments (labs, HHQ, cognitive) stored historically in Supabase
- Roadmap PDF also saved to Supabase for future reference
- No overwriting of past assessments

---

## 11. Out of Scope (Future Phases)

- Client login portal
- Emailing Roadmap directly from system
- Practitioner dashboards
- AI explanation of Roadmaps
- Trends tracking
- CNS API integration
- Automated SMS/email reminders

---

## 12. Version Control Guidelines

### Branch Strategy
- Main branch: Contains stable, production-ready code
- Feature branches: Created for new features or fixes
- No direct commits to main branch

### When to Create Branches
- New feature development
- Bug fixes
- Lab content updates
- Roadmap template modifications

### Commit Guidelines
- Commit only when feature/fix is working
- Include clear commit messages
- Don't commit partial or broken changes
- Don't commit logs or temporary files

### Backup and Merge Process
1. Create feature branch from main
2. Develop and test in feature branch
3. Push feature branch to GitHub regularly
4. Only merge to main when thoroughly tested
5. Keep main branch as "known working" version

### Protected Files and Data
- Environment variables (.env)
- Log files
- Test files
- Temporary files
- Sensitive client data

These guidelines ensure code stability and protect client data while allowing for efficient development. 