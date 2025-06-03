#!/usr/bin/env python3

import sys
sys.path.append('/Users/jstoker/Documents/mindstoke-server')
from app.utils.supabase_client import get_supabase_client, fetch_client_by_id

client_id = '01306260-b1b5-49e2-8ed0-69ff1484c965'

print(f"=== CHECKING APO E VALUE FOR CLIENT {client_id} ===")

client = get_supabase_client()

# Check for APO E using original_test_name
print("\n=== SEARCHING FOR APO E BY original_test_name ===")
apoe_results = client.table('lab_results').select('*').eq('client_id', client_id).ilike('original_test_name', '%apo%').execute()

if apoe_results.data:
    for lab in apoe_results.data:
        print(f"  - {lab.get('original_test_name')}: {lab.get('original_value')} (armgasys: {lab.get('armgasys_variable_name')} = {lab.get('armgasys_value')})")
else:
    print("No APOE results found by original_test_name")

# Check for APO E using armgasys_variable_name
print("\n=== SEARCHING FOR APO E BY armgasys_variable_name ===")
apoe_results2 = client.table('lab_results').select('*').eq('client_id', client_id).ilike('armgasys_variable_name', '%apo%').execute()

if apoe_results2.data:
    for lab in apoe_results2.data:
        print(f"  - {lab.get('armgasys_variable_name')}: {lab.get('armgasys_value')} (original: {lab.get('original_test_name')} = {lab.get('original_value')})")
else:
    print("No APOE results found by armgasys_variable_name")

# Search for any genetics-related tests
print("\n=== SEARCHING FOR GENETICS-RELATED TESTS ===")
genetics_tests = client.table('lab_results').select('*').eq('client_id', client_id).execute()

apoe_found = []
genetics_found = []

for lab in genetics_tests.data:
    original_name = lab.get('original_test_name', '').lower()
    armgasys_name = lab.get('armgasys_variable_name', '').lower()
    
    if 'apo' in original_name or 'apo' in armgasys_name:
        apoe_found.append(lab)
    elif any(term in original_name or term in armgasys_name for term in ['genetic', 'genotype', 'mthfr', 'e2', 'e3', 'e4']):
        genetics_found.append(lab)

if apoe_found:
    print("APO E related tests found:")
    for lab in apoe_found:
        print(f"  - {lab.get('original_test_name')} ({lab.get('armgasys_variable_name')}): {lab.get('original_value')} -> {lab.get('armgasys_value')}")

if genetics_found:
    print("Other genetics-related tests found:")
    for lab in genetics_found:
        print(f"  - {lab.get('original_test_name')} ({lab.get('armgasys_variable_name')}): {lab.get('original_value')} -> {lab.get('armgasys_value')}")

if not apoe_found and not genetics_found:
    print("No APO E or genetics tests found")

print("\n=== CHECKING CLIENT INFO ===")
client_info = fetch_client_by_id(client_id)
if client_info:
    print(f"Client name: {client_info.get('name')}")
else:
    print("Client not found") 