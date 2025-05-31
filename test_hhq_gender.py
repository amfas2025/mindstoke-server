from app import create_app
from app.utils.supabase_client import fetch_clients, fetch_client_by_id, fetch_health_history_questions
from app.routes.hhq import SECTION_TITLES

def test_gender_filtering():
    app = create_app()
    with app.app_context():
        # Get all clients
        clients = fetch_clients()
        print("\nAvailable clients:")
        for client in clients:
            print(f"ID: {client.get('id')}, Name: {client.get('first_name')} {client.get('last_name')}, Sex: {client.get('sex')}")
        
        # Test with a male client
        print("\nTesting with male client:")
        male_client = next((c for c in clients if c.get('sex', '').lower() == 'male'), None)
        if male_client:
            print(f"Testing with male client: {male_client.get('first_name')} {male_client.get('last_name')}")
            sections = get_sections_for_client(male_client.get('id'))
            print("Available sections:", sections)
            print("Female section present:", 'Female Hormone Health' in sections)
            print("Male section present:", 'Male Hormone Health History' in sections)
        else:
            print("No male client found for testing")
        
        # Test with a female client
        print("\nTesting with female client:")
        female_client = next((c for c in clients if c.get('sex', '').lower() == 'female'), None)
        if female_client:
            print(f"Testing with female client: {female_client.get('first_name')} {female_client.get('last_name')}")
            sections = get_sections_for_client(female_client.get('id'))
            print("Available sections:", sections)
            print("Female section present:", 'Female Hormone Health' in sections)
            print("Male section present:", 'Male Hormone Health History' in sections)
        else:
            print("No female client found for testing")

def get_sections_for_client(client_id):
    client = fetch_client_by_id(client_id)
    if not client:
        return []
    
    # Get all questions and organize by section
    questions = fetch_health_history_questions()
    if not questions:
        return []
    
    # Group questions by section
    sections = set()
    for question in questions:
        section_name = question.get('section', 'Unknown')
        sections.add(section_name)
    
    # Filter out gender-specific sections
    if client.get('sex', '').lower() == 'male':
        sections.discard('Female Hormone Health')
    elif client.get('sex', '').lower() == 'female':
        sections.discard('Male Hormone Health History')
    
    return sorted(list(sections))

if __name__ == '__main__':
    test_gender_filtering() 