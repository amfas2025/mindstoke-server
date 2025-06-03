#!/usr/bin/env python3

from app.utils.supabase_client import get_supabase_client, return_supabase_client

def add_height_weight_questions():
    """Add height and weight questions to the health_history_questions table."""
    client = get_supabase_client()
    try:
        # First, check the current max question_order for Social History section
        response = client.table('health_history_questions') \
            .select('question_order') \
            .eq('section', 'Social History') \
            .order('question_order', desc=True) \
            .limit(1) \
            .execute()
        
        max_order = 0
        if response.data:
            max_order = int(response.data[0]['question_order'])
        
        print(f"Current max question_order in Social History: {max_order}")
        
        # Define the new questions (matching the table structure)
        height_question = {
            'variable_name': 'hh-height',
            'section': 'Social History',
            'display_text': 'Height',
            'question_text': 'What is your height? (Please enter in feet and inches like "5\'10\"" or centimeters like "180 cm")',
            'question_order': max_order + 1
        }
        
        weight_question = {
            'variable_name': 'hh-weight',
            'section': 'Social History',
            'display_text': 'Current Weight',
            'question_text': 'What is your current weight? (Please enter in pounds like "165 lbs" or kilograms like "75 kg")',
            'question_order': max_order + 2
        }
        
        # Insert the questions
        questions_to_insert = [height_question, weight_question]
        
        for question in questions_to_insert:
            print(f"Inserting question: {question['variable_name']}")
            
            # Check if question already exists
            existing = client.table('health_history_questions') \
                .select('variable_name') \
                .eq('variable_name', question['variable_name']) \
                .execute()
            
            if existing.data:
                print(f"  Question {question['variable_name']} already exists, skipping...")
                continue
            
            # Insert the question
            result = client.table('health_history_questions').insert(question).execute()
            if result.data:
                print(f"  Successfully inserted {question['variable_name']}")
            else:
                print(f"  Failed to insert {question['variable_name']}")
        
        print("\nHeight and weight questions added successfully!")
        
    except Exception as e:
        print(f"Error adding questions: {e}")
        raise
    finally:
        return_supabase_client(client)

if __name__ == "__main__":
    add_height_weight_questions() 