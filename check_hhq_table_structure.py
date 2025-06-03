#!/usr/bin/env python3

from app.utils.supabase_client import get_supabase_client, return_supabase_client

def check_table_structure():
    """Check the structure of the health_history_questions table."""
    client = get_supabase_client()
    try:
        # Get one question to see the structure
        response = client.table('health_history_questions') \
            .select('*') \
            .limit(1) \
            .execute()
        
        if response.data:
            question = response.data[0]
            print("Sample question structure:")
            for key, value in question.items():
                print(f"  {key}: {type(value).__name__} = {value}")
        else:
            print("No questions found in table")
            
    except Exception as e:
        print(f"Error checking table structure: {e}")
        raise
    finally:
        return_supabase_client(client)

if __name__ == "__main__":
    check_table_structure() 