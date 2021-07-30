import pytest
from services import client

test_application = {
    "name" : 'Jane Doe',
    "houseNumber" : 23,
    "location" : "DT1 1SS",
    "password" : "Secret_Pa55w0rd",
    "JobSheet": []
}

test_profile =  {
    'id': '5f9045e9-cc05-471f-8193-8b036a2d4599', 
    'status': True, 
    'name': 'John Doe', 
    'houseNumber': 23, 
    'location': 'DT1 1SS', 
    'password': 'Secret_Pa55w0rd', 
    'signup_ts': 1627571049.827422, 
    'joined': 'Thu Jul 29 16:04:09 2021', 
    'JobSheet': []
}

test_client_id = "ec86adf9-a0dd-4026-bc2d-d4e61728e0e4"

test_client_profile = {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.8488379, 'joined': 'Fri Jul 30 16:51:40 2021', 'name': 'Jane Doe', 'houseNumber': 23, 'location': 'DT1 1SS', 'JobSheet': [], 'id': 'ec86adf9-a0dd-4026-bc2d-d4e61728e0e4', 'status': True}

def test_register_client():
    '''Test that the metadata is added to the application'''
    actual = client.register_client(test_application)
    print(f"Actual resp  =  {actual}")
    assert actual['status'] == 200, "Status-Code not as expected"
    assert actual["msg"].startswith("profile created for"), "Name not as expected"
    
def test_process_registration_valid():
    '''Test that the registration is unique.'''
    actual = client.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['id'] != "", "No ID ref generated"
    assert actual["name"] == 'John Doe', "Name not as expected"
    
def test_process_registration_invalid():
    '''Test when the registration id is missing.'''
    expected = 'error'
    test_profile["id"]=""
    actual = client.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual == expected, f"Expected Error got {actual}"
    

@pytest.mark.skip
def test_update_database():
    '''Verify the cypher query is created and executed.'''
    expected_success = 'client created successfully'
    expected_query = """
    WITH $json as data
    UNWIND data as q

    MERGE (client:CLIENT {id:q.id}) ON CREATE
    SET client.name = q.name, client.status = q.status, client.houseNumber = q.houseNumber, 
    client.location = q.location, client.JobSheet = q.JobSheet, client.password = q.password, 
    client.signup_ts = q.signup_ts, client.joined = q.joined, client.status = q.status
    """
    actual = client.update_database(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['success'] == expected_success, f"Expected Error got {actual['success']}"
    assert actual['query'] == expected_query, f"Expected Error got {actual['query']}"
    
    
def test_get_client_profile():
    '''Verify you can collect Client profile from client id.'''
    expected_profile = test_client_profile
    actual = client.get_client_profile(test_client_id)
    print(f"Actual resp  =  {actual['result'][0]['clt']}")
    # assert actual['success'] == expected_success, f"Expected Error got {actual['success']}"
    assert actual['result'][0]["clt"] == expected_profile, f"Expected Error got {actual['result']}"
