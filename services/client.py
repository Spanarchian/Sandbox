import time, uuid, logging
from json import dumps, loads
from typing import List, Optional
from pydantic import BaseModel
from helper.graph import get_gdb

graph = get_gdb('prod')

class Client(BaseModel):
    id : str
    status : bool
    name : str
    houseNumber : int
    location : str
    password : str
    JobSheet: List[ str ] = []
    class Config:
        '''Docstring here.'''
        schema_extra = {
            "example": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad91ab3",
                "status" : True,
                "name" : 'John Doe',
                "houseNumber" : 23,
                "location" : "DT1 1SS",
                "password" : "Secret_Pa55w0rd",
                "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e36","c85a5633-2803-4826-ae5a-82474c238d5","0348ae36-202a-4bfc-a92d-849607fd541" ],
            }
        }


def register_client(appliction):
    '''Create client profile with metadata'''
    now = time.time()
    id = str(uuid.uuid4())
    print(f" ID = {id}")
    client = {}
    client["id"] = id
    client["status"]= True
    client["name"]= appliction["name"]
    client["houseNumber"]= appliction["houseNumber"]
    client["location"]= appliction["location"]
    client["password"]= appliction["password"]
    client["signup_ts"]= now
    client["joined"]= time.ctime(now)
    client["JobSheet"]=[]
    resp = process_registration(client)
    if resp != 'error':
        update_database(client)
        return {"status": 200, "msg":f"profile created for {client['id']}" }
    else:
        print(f"application failed - {resp}")
        return {"status": 500, "error":f"ERROR: application failed - {resp}"}
                

def process_registration(application: Client):
    '''Ensure that the application is unique - based on email & address'''
    if application["id"] == "":
        logging.error(f"ID error in {application}")
        return 'error'
    else:
        return application


def update_database(client_profile: Client):
    '''Update Database: with processed and verified client profile.'''
    print(f"Start registration for register_client : {client_profile}")
    query = """
    WITH $json as data
    UNWIND data as q

    MERGE (client:CLIENT {id:q.id}) ON CREATE
    SET client.name = q.name, client.status = q.status, client.houseNumber = q.houseNumber, 
    client.location = q.location, client.JobSheet = q.JobSheet, client.password = q.password, 
    client.signup_ts = q.signup_ts, client.joined = q.joined, client.status = q.status
    """

    print(f"Start graph execution for client {client_profile}")
    graph.run(query,json=client_profile)
    print(f"Complete graph execution for client {client_profile}")
    return {"success":"client created successfully", "query":query}




def update_client(client_id):
    pass

def get_client_profile(client_id):
    print(f"Start retrieval of CLIENT: {client_id}")
    query = """
    match (client:CLIENT) where client.id = $client_id return client as clt
    """

    print(f"Start graph execution for retrieving client {client_id}")
    resp = dumps(graph.run(query, client_id=client_id).data())
    result = loads(resp)
    print(f"Complete graph execution for client {client_id}")
    print(f"result of graph execution for client {result} - {type(result)}")
    return {"result":result, "query":query}
