import requests
import json

# Define your Neo4j credentials and URL
NEO4J_URL = 'http://localhost:7474/db/neo4j/tx/commit'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '12345678'

count = 0
with open('wdbench/queries.cypher', 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.strip()
        if line:
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                'statements': [
                    {
                        'statement': line,
                        'resultDataContents': ['row', 'graph'],
                        'includeStats': True
                    }
                ]
            }
            response = requests.post(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD), headers=headers, data=json.dumps(data))
            result = response.json()
            plan = result['results'][0]['plan']['root']
            # save plan to a file
            count = count + 1
            with open("wdbench/queryplan_raw/" + str(count) + ".neo4j", 'w', encoding='UTF-8') as plan_file:
                plan_file.write(json.dumps(plan, indent=2))