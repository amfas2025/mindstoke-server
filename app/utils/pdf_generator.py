from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

def generate_hhq_pdf(hhq_response, output_path):
    """Generate a PDF report for an HHQ response."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        spaceAfter=12,
        spaceBefore=24,
        textColor=colors.HexColor('#2C3E50')
    ))
    styles.add(ParagraphStyle(
        name='Question',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='Answer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leftIndent=20,
        spaceAfter=12
    ))
    
    # Build content
    content = []
    
    # Header
    content.append(Paragraph('Health History Questionnaire Results', styles['Heading1']))
    content.append(Spacer(1, 0.25*inch))
    
    # Client Information (dict-based)
    client = hhq_response.get('client', {})
    client_name = f"{client.get('first_name', 'N/A')} {client.get('last_name', '')}".strip()
    dob = client.get('date_of_birth', 'N/A')
    if dob and dob != 'N/A':
        if isinstance(dob, str):
            dob = dob[:10]
        elif hasattr(dob, 'strftime'):
            dob = dob.strftime('%B %d, %Y')
    completed_at = hhq_response.get('completed_at', 'N/A')
    if completed_at and completed_at != 'N/A':
        if isinstance(completed_at, str):
            completed_at = completed_at[:19].replace('T', ' ')
        elif hasattr(completed_at, 'strftime'):
            completed_at = completed_at.strftime('%B %d, %Y at %I:%M %p')
    client_info = [
        ['Client Name:', client_name or 'N/A'],
        ['Date of Birth:', dob or 'N/A'],
        ['Completed On:', completed_at or 'N/A']
    ]
    t = Table(client_info, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    content.append(t)
    content.append(Spacer(1, 0.5*inch))
    
    # Section titles from routes
    from app.routes.hhq import SECTION_TITLES
    
    # Question mapping
    from app.forms import HHQForm
    form = HHQForm()
    question_map = {}
    for field in form:
        if hasattr(field, 'label'):
            question_map[field.name] = field.label.text
    
    # Process responses
    responses = hhq_response.get('responses', {})
    
    # Pre-screening section
    content.append(Paragraph('Pre-screening Questions', styles['SectionHeader']))
    pre_fields = ['pre_is_female', 'pre_has_dementia_history']
    for field_name in pre_fields:
        if field_name in responses and field_name in question_map:
            question = question_map[field_name]
            value = responses[field_name]
            answer = 'Yes' if value is True or value == 'on' or value == 'True' else 'No'
            content.append(Paragraph(question, styles['Question']))
            content.append(Paragraph(answer, styles['Answer']))
    content.append(Spacer(1, 0.25*inch))
    
    # Skip sections based on pre-screening
    skip_sections = []
    if responses.get('pre_is_female') is True or responses.get('pre_is_female') == 'on' or responses.get('pre_is_female') == 'True':
        skip_sections.append(16)  # Skip Male Hormone Health
    else:
        skip_sections.append(15)  # Skip Female Hormone Health
    if responses.get('pre_has_dementia_history') is not True and responses.get('pre_has_dementia_history') != 'on' and responses.get('pre_has_dementia_history') != 'True':
        skip_sections.append(1)   # Skip Dementia Diagnosis
    
    # Process each section
    for section_index, section_title in enumerate(SECTION_TITLES):
        if section_index in skip_sections:
            continue
        
        content.append(Paragraph(section_title, styles['SectionHeader']))
        
        # Get all responses for fields that belong to this section
        section_responses = {}
        for field_name, value in responses.items():
            if field_name.startswith('hh_') and field_name in question_map:
                # Add the response if it's checked or True
                if value is True or value == 'on' or value == 'True':
                    section_responses[field_name] = value
        
        if section_responses:
            for field_name, value in section_responses.items():
                question = question_map[field_name]
                answer = 'Yes' if value is True or value == 'on' or value == 'True' else 'No'
                content.append(Paragraph(question, styles['Question']))
                content.append(Paragraph(answer, styles['Answer']))
        else:
            content.append(Paragraph('No conditions reported in this section.', styles['Answer']))
        
        content.append(Spacer(1, 0.25*inch))
    
    # Build PDF
    doc.build(content)
    return output_path 