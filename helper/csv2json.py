import csv, json

client_list = '../test_dataset/CleanMartUK_TestData_client_csv.csv'
custom_list = '../test_dataset/CleanMartUK_TestData_cust_csv.csv'
job_list = '../test_dataset/CleanMartUK_TestData_job_csv.csv'
client_json = '../test_dataset/CleanMartUK_TestData_client.json'
custom_json = '../test_dataset/CleanMartUK_TestData_cust.json'
job_json = '../test_dataset/CleanMartUK_TestData_job.json'

def read_csv(req_path, req_dest):
    set = []
    data = {}
    with open(req_path, newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        for row in spamreader:    
            data = {}
            id = row['Username']
            data[id] = row
            set.append(data)
          
    with open(req_dest, 'w')as jsonfile:
        jsonfile.write(json.dumps(set,indent=4))      

            
read_csv(client_list, client_json)
read_csv(job_list, job_json)
read_csv(custom_list, custom_json)

