from services import client

test_application = {
    "id": "7f644301-e3f1-4752-90d5-99fbfad91ab3",
    "status" : True,
    "name" : 'John Doe',
    "houseNumber" : 23,
    "location" : "DT1 1SS",
    "password" : "Secret_Pa55w0rd",
    "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e36","c85a5633-2803-4826-ae5a-82474c238d5","0348ae36-202a-4bfc-a92d-849607fd541" ],
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

test_client_id = "3467eb48-34a6-46fd-92f1-2a707249902e"

test_client_profile = {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627578945.460588, 'joined': 'Thu Jul 29 18:15:45 2021', 'name': 'John Doe', 'houseNumber': 23, 'location': 'DT1 1SS', 'JobSheet': [], 'id': '3467eb48-34a6-46fd-92f1-2a707249902e', 'status': True}

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
    

def test_update_database():
    '''Verify the cypher query is created and executed.'''
    expected_success = 'client created successfully'
    expected_query = '\n    WITH $json as data\n    UNWIND data as q\n\n    MERGE (client:CLIENT {id:q.id}) ON CREATE\n    SET client.name = q.name, client.status = q.status, client.houseNumber = q.houseNumber, \n    client.location = q.location, client.JobSheet = q.JobSheet, client.password = q.password, \n    client.signup_ts = q.signup_ts, client.joined = q.joined, client.status = q.status\n    '
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
