from supabase import create_client as supabase_create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_wtf import CSRFProtect
import time
from functools import wraps
import logging
import uuid
import json
from .lab_mapping import get_all_mapped_results
import httpx

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Debug prints
logger.info("DEBUG: SUPABASE_URL = %s", os.getenv("SUPABASE_URL"))
logger.info("DEBUG: SUPABASE_KEY = %s", os.getenv("SUPABASE_KEY"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Please check your .env file.")

# Connection pool settings
MAX_POOL_SIZE = 5
POOL_TIMEOUT = 30  # seconds
CONNECTION_TIMEOUT = 10  # seconds

# Global pool for connection reuse
supabase_pool = []

def get_supabase_client():
    """Get a Supabase client from the pool or create a new one."""
    global supabase_pool
    
    # Try to get an existing client from the pool
    start_time = time.time()
    while supabase_pool and (time.time() - start_time) < POOL_TIMEOUT:
        client = supabase_pool.pop()
        try:
            # Test the connection with a timeout
            client.table("clients").select("count").limit(1).execute()
            return client
        except Exception as e:
            logger.warning("Failed to reuse client from pool: %s", str(e))
            continue
    
    # Create a new client if pool is empty or all clients are invalid
    try:
        # Create client with default configuration
        client = supabase_create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Add headers to the underlying session
        if hasattr(client, 'postgrest'):
            client.postgrest.session.headers.update({
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Prefer": "return=representation"
            })
        
        # Add the client to the pool
        if not supabase_pool:
            supabase_pool = []
        supabase_pool.append(client)
        
        return client
        
    except Exception as e:
        logger.error("Failed to create new Supabase client: %s", str(e))
        raise

def return_supabase_client(client):
    """Return a client to the pool for reuse."""
    global supabase_pool
    if len(supabase_pool) < MAX_POOL_SIZE:
        supabase_pool.append(client)

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry database operations on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error("Function %s failed after %d retries: %s", func.__name__, max_retries, str(e))
                        raise
                    else:
                        logger.warning("Function %s attempt %d failed: %s. Retrying in %d seconds...", 
                                     func.__name__, attempt + 1, str(e), delay)
                        time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure()
def fetch_clients():
    """Fetch all clients from Supabase."""
    client = get_supabase_client()
    try:
        logger.info("Attempting to fetch clients from Supabase...")
        
        # Use explicit headers
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Try direct REST query
        url = f"{SUPABASE_URL}/rest/v1/clients"
        logger.info(f"Querying URL: {url}")
        
        response = httpx.get(
            url,
            headers=headers,
            params={
                "select": "*",
                "order": "created_at.desc"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} clients")
            return data
        else:
            logger.error(f"Error response from Supabase: {response.status_code}")
            logger.error(f"Response headers: {response.headers}")
            logger.error(f"Response body: {response.text}")
            return []
            
    except Exception as e:
        logger.error(f"Error fetching clients from Supabase: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
        return []
    finally:
        return_supabase_client(client)

@retry_on_failure()
def create_client(client_data):
    """Create a new client with retry logic."""
    client = get_supabase_client()
    try:
        result = client.table("clients").insert(client_data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error creating client in Supabase: {e}")
        return None
    finally:
        return_supabase_client(client)

@retry_on_failure()
def update_client(client_id, client_data):
    """Update a client with retry logic."""
    client = get_supabase_client()
    try:
        result = client.table("clients").update(client_data).eq("id", client_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error updating client in Supabase: {e}")
        return None
    finally:
        return_supabase_client(client)

@retry_on_failure()
def delete_client(client_id):
    """Delete a client with retry logic."""
    client = get_supabase_client()
    try:
        client.table("clients").delete().eq("id", client_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting client from Supabase: {e}")
        return False
    finally:
        return_supabase_client(client)

@retry_on_failure()
def insert_lab_results_to_supabase(client_id, collected_at, lab_values):
    """Insert lab results with retry logic."""
    client = get_supabase_client()
    try:
        data = {
            "client_id": client_id,
            "collected_at": collected_at,
            "created_at": datetime.utcnow().isoformat(),
            **lab_values
        }
        result = client.table("labs").insert(data).execute()
        if result.data:
            return result.data[0]
        else:
            print("Error: No data returned from Supabase insert.")
            return None
    except Exception as e:
        print(f"Error inserting lab results into Supabase: {e}")
        return None
    finally:
        return_supabase_client(client)

@retry_on_failure()
def fetch_hhq_responses_for_client(client_id):
    """Fetch HHQ responses with retry logic."""
    client = get_supabase_client()
    try:
        result = client.table("hhq_responses").select("*").eq("client_id", client_id).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Error fetching HHQ responses from Supabase: {e}")
        return []
    finally:
        return_supabase_client(client)

@retry_on_failure()
def fetch_hhq_by_token(token):
    """Fetch HHQ by token with retry logic."""
    client = get_supabase_client()
    try:
        result = client.table("hhq_responses").select("*").eq("unique_token", token).single().execute()
        return result.data if result.data else None
    except Exception as e:
        print(f"Error fetching HHQ by token: {e}")
        return None
    finally:
        return_supabase_client(client)

@retry_on_failure()
def fetch_client_by_id(client_id):
    """Fetch client by ID with retry logic."""
    client = get_supabase_client()
    try:
        logger.info(f"Attempting to fetch client with ID: {client_id}")
        
        # Use explicit headers
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Try direct REST query first
        url = f"{SUPABASE_URL}/rest/v1/clients"
        logger.info(f"Querying URL: {url}")
        
        response = httpx.get(
            url,
            headers=headers,
            params={
                "id": f"eq.{client_id}",
                "select": "*"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                logger.info(f"Successfully found client {client_id}")
                return data[0]
            else:
                logger.warning(f"No client found with ID {client_id}")
                return None
        else:
            logger.error(f"Error response from Supabase: {response.status_code}")
            logger.error(f"Response headers: {response.headers}")
            logger.error(f"Response body: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching client by id from Supabase: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
        return None
    finally:
        return_supabase_client(client)

@retry_on_failure()
def fetch_health_history_questions():
    """Fetch health history questions with retry logic."""
    client = get_supabase_client()
    try:
        response = client.table('health_history_questions') \
            .select('*') \
            .order('section') \
            .order('question_order') \
            .execute()
        
        if response.data:
            return response.data
        return []
    except Exception as e:
        print(f"Error fetching health history questions: {e}")
        return []
    finally:
        return_supabase_client(client)

@retry_on_failure()
def upsert_individual_hhq_answers(client_id, answers_dict, attempt_id):
    """Upsert HHQ answers for a specific attempt_id (do not create a new attempt_id unless a new link is generated)."""
    if not attempt_id:
        raise ValueError("attempt_id is required for upsert_individual_hhq_answers")
    client = get_supabase_client()
    try:
        taken_at = datetime.utcnow().isoformat()
        snapshot = json.dumps(answers_dict)  # Store full snapshot

        payloads = []
        for variable_name, value in answers_dict.items():
            # Handle different value types based on the field
            if variable_name in ['hh-height', 'hh-weight']:
                # Store text values as-is for height and weight
                response_value = str(value) if value else ''
            else:
                # Store boolean values as 'True'/'False' for other fields
                response_value = 'True' if value else 'False'
                
            payloads.append({
                'client_id': client_id,
                'question_variable_name': variable_name,
                'response_value': response_value,
                'attempt_id': attempt_id,
                'taken_at': taken_at,
                'responses': snapshot
            })
        print(f"[DEBUG] Upserting for client_id={client_id} attempt_id={attempt_id} payloads={payloads}")
        if payloads:
            # First, delete any existing responses for this client and attempt
            client.table('hhq_responses').delete().eq('client_id', client_id).eq('attempt_id', attempt_id).execute()
            # Then insert all responses in batches to improve performance
            batch_size = 50  # Process in smaller batches to avoid timeouts
            for i in range(0, len(payloads), batch_size):
                batch = payloads[i:i + batch_size]
                client.table('hhq_responses').insert(batch).execute()
                print(f"[DEBUG] Inserted batch {i//batch_size + 1}/{(len(payloads) + batch_size - 1)//batch_size}")
        return_supabase_client(client)
    except Exception as e:
        print(f"Error upserting answers for client {client_id}: {e}")
        return_supabase_client(client)
        raise

@retry_on_failure()
def fetch_hhq_responses_dict(client_id):
    """Fetch HHQ responses as dictionary with retry logic."""
    client = get_supabase_client()
    try:
        result = client.table('hhq_responses') \
            .select('question_variable_name, response_value') \
            .eq('client_id', client_id) \
            .execute()
        
        responses = {}
        for row in result.data:
            variable_name = row['question_variable_name']
            response_value = row['response_value']
            # Convert response values back to boolean
            if response_value.lower() in ['true', '1', 'yes']:
                responses[variable_name] = True
            elif response_value.lower() in ['false', '0', 'no']:
                responses[variable_name] = False
            else:
                responses[variable_name] = response_value
                
        return responses
    except Exception as e:
        print(f"Error fetching HHQ responses: {e}")
        return {}
    finally:
        return_supabase_client(client)

@retry_on_failure()
def create_hhq_attempt(client_id):
    """Create a new HHQ attempt for a client, pre-filling from the most recent finalized attempt if available."""
    client = get_supabase_client()
    try:
        attempt_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        # Fetch all attempts for this client, order by finalized_at desc
        result = client.table('hhq_attempts') \
            .select('*') \
            .eq('client_id', client_id) \
            .order('finalized_at', desc=True) \
            .execute()
        prefill_answers = {}
        last_finalized_attempt = None
        if result.data and len(result.data) > 0:
            for attempt in result.data:
                if attempt.get('finalized_at') is not None:
                    last_finalized_attempt = attempt
                    break
            if last_finalized_attempt:
                last_attempt_id = last_finalized_attempt['id']
                # Fetch all responses for that attempt
                responses_result = client.table('hhq_responses').select('question_variable_name, response_value').eq('client_id', client_id).eq('attempt_id', last_attempt_id).execute()
                for row in responses_result.data:
                    prefill_answers[row['question_variable_name']] = row['response_value']
        # Insert new attempt
        client.table('hhq_attempts').insert({
            'id': attempt_id,
            'client_id': client_id,
            'created_at': now,
            'finalized_at': None
        }).execute()
        return_supabase_client(client)
        return attempt_id, prefill_answers
    except Exception as e:
        return_supabase_client(client)
        raise

@retry_on_failure()
def fetch_hhq_responses_dict_for_attempt(client_id, attempt_id):
    """Fetch HHQ responses as dictionary for a specific attempt."""
    client = get_supabase_client()
    try:
        result = client.table('hhq_responses') \
            .select('question_variable_name, response_value') \
            .eq('client_id', client_id) \
            .eq('attempt_id', attempt_id) \
            .execute()
        
        responses = {}
        for row in result.data:
            variable_name = row['question_variable_name']
            response_value = row['response_value']
            # Convert response values back to boolean
            if response_value.lower() in ['true', '1', 'yes']:
                responses[variable_name] = True
            elif response_value.lower() in ['false', '0', 'no']:
                responses[variable_name] = False
            else:
                responses[variable_name] = response_value
        
        return responses
    except Exception as e:
        print(f"Error fetching HHQ responses for attempt: {e}")
        return {}
    finally:
        return_supabase_client(client)

@retry_on_failure()
def upsert_hhq_answers_partial(client_id, answers_dict, attempt_id):
    """Upsert only the provided HHQ answers without overwriting existing ones."""
    if not attempt_id:
        raise ValueError("attempt_id is required for upsert_hhq_answers_partial")
    if not answers_dict:
        return  # Nothing to save
        
    client = get_supabase_client()
    try:
        taken_at = datetime.utcnow().isoformat()
        
        payloads = []
        for variable_name, value in answers_dict.items():
            # Handle different value types based on the field
            if variable_name in ['hh-height', 'hh-weight']:
                # Store text values as-is for height and weight
                response_value = str(value) if value else ''
            else:
                # Store boolean values as 'True'/'False' for other fields
                response_value = 'True' if value else 'False'
                
            payloads.append({
                'client_id': client_id,
                'question_variable_name': variable_name,
                'response_value': response_value,
                'attempt_id': attempt_id,
                'taken_at': taken_at,
                'responses': json.dumps({variable_name: value})
            })
        
        print(f"[DEBUG] Partial upsert for client_id={client_id} attempt_id={attempt_id} payloads={len(payloads)} items")
        
        if payloads:
            # Delete existing responses for these specific questions only
            question_names = list(answers_dict.keys())
            for question_name in question_names:
                client.table('hhq_responses').delete().eq('client_id', client_id).eq('attempt_id', attempt_id).eq('question_variable_name', question_name).execute()
            
            # Insert new responses in batches
            batch_size = 50
            for i in range(0, len(payloads), batch_size):
                batch = payloads[i:i + batch_size]
                client.table('hhq_responses').insert(batch).execute()
                print(f"[DEBUG] Inserted batch {i//batch_size + 1}/{(len(payloads) + batch_size - 1)//batch_size}")
        
        return_supabase_client(client)
    except Exception as e:
        print(f"Error partial upserting answers for client {client_id}: {e}")
        return_supabase_client(client)
        raise

@retry_on_failure()
def save_lab_results(client_id, lab_results):
    """Save lab results to Supabase."""
    client = get_supabase_client()
    try:
        logger.info(f"Attempting to save lab results for client {client_id}")
        
        # Format the data for Supabase
        current_time = datetime.utcnow().isoformat()
        lab_entries = []
        
        for test_name, result in lab_results.items():
            # Handle both dictionary and string result formats
            if isinstance(result, dict):
                value = result.get('value', '')
                unit = result.get('unit', '')
                reference_range = result.get('reference_range', '')
            else:
                value = str(result)
                unit = ''
                reference_range = ''
            
            entry = {
                'client_id': client_id,
                'test_name': test_name,
                'value': value,
                'unit': unit,
                'reference_range': reference_range,
                'uploaded_at': current_time
            }
            lab_entries.append(entry)
        
        if not lab_entries:
            logger.warning(f"No lab entries to save for client {client_id}")
            return None
            
        # Insert into the lab_results table
        result = client.table('lab_results').insert(lab_entries).execute()
        
        if result.data:
            logger.info(f"Successfully saved {len(lab_entries)} lab results for client {client_id}")
            return result.data
        else:
            logger.error(f"No data returned when saving lab results for client {client_id}")
            return None
            
    except Exception as e:
        logger.error(f"Error saving lab results to Supabase: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
        raise
    finally:
        return_supabase_client(client)

@retry_on_failure()
def fetch_lab_results_for_client(client_id):
    """Fetch all lab results for a specific client."""
    client = get_supabase_client()
    try:
        result = client.table('lab_results') \
            .select('*') \
            .eq('client_id', client_id) \
            .execute()
        
        # Convert to expected format for roadmap generation
        lab_results = []
        for row in result.data:
            lab_result = {
                'test_name': row.get('original_test_name', ''),
                'value': row.get('original_value', ''),
                'unit': row.get('unit', ''),
                'reference_range': row.get('reference_range', ''),
                'armgasys_variable': row.get('armgasys_variable_name', ''),
                'armgasys_value': row.get('armgasys_value', ''),
                'date_collected': row.get('date_collected', ''),
                'uploaded_at': row.get('uploaded_at', '')
            }
            lab_results.append(lab_result)
        
        return lab_results
        
    except Exception as e:
        print(f"Error fetching lab results for client {client_id}: {e}")
        return []
    finally:
        return_supabase_client(client)

# Optional: one-time manual test block
if __name__ == "__main__":
    from pprint import pprint

    test_data = {
        "client_id": "25bef016-21cb-4766-874d-8bc6cb482ea4",
        "collected_at": "2025-05-13T10:00:00",
        "lab_values": {
            "estradiol": 55.2,
            "progesterone": 1.2,
            "tsh": 2.4,
            "vitamin_d_25_hydroxy": 42.1
        }
    }

    result = insert_lab_results_to_supabase(
        client_id=test_data["client_id"],
        collected_at=test_data["collected_at"],
        lab_values=test_data["lab_values"]
    )

    print("🧪 Insert result:")
    pprint(result)
