#!/usr/bin/env python3

from app.utils.supabase_client import fetch_health_history_questions

questions = fetch_health_history_questions()
print(f'Total questions: {len(questions)}')

sections = set()
for i, q in enumerate(questions):
    if i < 10:  # Show first 10 as examples
        sections.add(q.get('section'))
        question_text = q.get('question_text', '')
        truncated_text = question_text[:100] + '...' if len(question_text) > 100 else question_text
        print(f'Section: {q.get("section")}, Variable: {q.get("variable_name")}, Text: {truncated_text}')
    sections.add(q.get('section'))

print(f'\nAll sections: {sorted(list(sections))}')

# Check if there are any existing height/weight related questions
height_weight_questions = [q for q in questions if 'height' in q.get('variable_name', '').lower() or 'weight' in q.get('variable_name', '').lower() or 'height' in q.get('question_text', '').lower() or 'weight' in q.get('question_text', '').lower()]

if height_weight_questions:
    print('\nExisting height/weight questions found:')
    for q in height_weight_questions:
        print(f'  {q.get("variable_name")}: {q.get("question_text")}')
else:
    print('\nNo existing height/weight questions found.') 