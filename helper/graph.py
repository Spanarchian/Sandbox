'''Create the Graph Connection'''
from py2neo import Graph

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

uri = os.environ.get("PRODURI")
user = os.environ.get("USERNAME")
tkn = os.environ.get("PASSWORD")

def get_gdb(env='test'):
    if env!='prod':
        graph = Graph("bolt://localhost:7687")
    else:
        graph = Graph(uri, auth=(user, tkn))
        
    return graph


def clean_aura():
    '''Clean the Aura GDB to allow the unit tests to pass.'''
    print(f"Clear down Aura GDB graph for test execution")
    query = """
        match (cl :CLIENT) where cl.id <> 'ec86adf9-a0dd-4026-bc2d-d4e61728e0e4' 
        match (jb :JOB)-[b]->(c) where jb.id <> '7b45923a-2ea9-43ef-9a5d-0d3b343a6ac1'
        match (cu :CUSTOMER) where cu.id <> "64703c74-4663-4e97-9038-7b74754555eb" 
        delete cl,jb,b,cu
    """
    graph = get_gdb('prod')
    graph.run(query)
    print(f"AURA Graph: ready for test execution.")
    
    