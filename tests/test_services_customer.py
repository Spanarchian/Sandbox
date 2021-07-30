import pytest
from services import customer

test_application = {
    "title" : 'Spick N Span',
    "CompanyReg" : '0921343',
    "RegisteredAddress" : "DT1 1SS",
    "password" : "Secret_Pa55w0rd",
    "AreasCovered":["DT1", "DT2"],
    "WorkingDays":[1,2,3,4,5,6,0],
    "services": [1,3,4]
}

test_profile =  {
                "id": "9g644301-e3f1-4752-90d5-99fbfad99xy4",
                "status" : True,
                "title" : 'Spick N Span',
                "CompanyReg" : '0921343',
                "RegisteredAddress" : "1 Main Street, Anytown, Anycounty, Anyland, XX9 9XX",
                "password" : "Secret_Pa55w0rd",
                "signup_ts": None,
                "AreasCovered":["DT1", "DT2"],
                "WorkingDays":[1,2,3,4,5,6],
                "services": [1,3,4],
            }

test_customer_id = "64703c74-4663-4e97-9038-7b74754555eb"

test_customer_profile = {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.9757571, 'RegisteredAddress': 'DT1 1SS', 'joined': 'Fri Jul 30 16:51:40 2021', 'services': [1, 3, 4], 'AreasCovered': ['DT1', 'DT2'], 'id': '64703c74-4663-4e97-9038-7b74754555eb', 'CompanyReg': '0921343', 'WorkingDays': [1, 2, 3, 4, 5, 6, 0]}

def test_register_customer():
    '''Test that the metadata is added to the application'''
    actual = customer.register_customer(test_application)
    print(f"Actual resp  =  {actual}")
    assert actual['status'] == 200, "Status-Code not as expected"
    assert actual["msg"].startswith("profile created for"), "Name not as expected"
    
def test_process_registration_valid():
    '''Test that the registration is unique.'''
    actual = customer.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['id'] != "", "No ID ref generated"
    assert actual["title"] == 'Spick N Span', "Name not as expected"
    
def test_process_registration_invalid():
    '''Test when the registration id is missing.'''
    expected = 'error'
    test_profile["id"]=""
    actual = customer.process_registration(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual == expected, f"Expected Error got {actual}"


@pytest.mark.skip
def test_update_database():
    '''Verify the cypher query is created and executed.'''
    expected_success = 'customer created successfully'
    expected_query = """
    WITH $json as data
    UNWIND data as q
    MERGE (customer :CUSTOMER {id:q.id}) ON CREATE
    SET customer.title = q.title, customer.status = q.status, customer.CompanyReg = q.CompanyReg, 
    customer.RegisteredAddress = q.RegisteredAddress,  customer.password = q.password, 
    customer.signup_ts = q.signup_ts, customer.joined = q.joined,
    customer.AreasCovered = q.AreasCovered,
    customer.WorkingDays = q.WorkingDays,
    customer.services = q.services 
    """
    actual = customer.update_database(test_profile)
    print(f"Actual resp  =  {actual}")
    assert actual['success'] == expected_success, f"Expected Error got {actual['success']}"
    assert actual['query'] == expected_query, f"Expected Error got {actual['query']}"
    
    
def test_get_customer_profile():
    '''Verify you can collect customer profile from client id.'''
    expected_profile = test_customer_profile
    actual = customer.get_customer_profile(test_customer_id)
    print(f"Actual resp  =  {actual['result'][0]['clt']}")
    # assert actual['success'] == expected_success, f"Expected Error got {actual['success']}"
    assert actual['result'][0]["clt"] == expected_profile, f"Expected Error got {actual['result']}"
