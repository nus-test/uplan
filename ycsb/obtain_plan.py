from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')  # Adjust if needed
db = client['ycsb']  # Replace with your database name

# Load the exported profile logs or directly query the system.profile collection
profile_data = db.system.profile.find()  # Alternatively, load from a JSON file

count = 0

for entry in profile_data:
    # Ensure the operation has a 'command' field and is a query
    if 'command' in entry and ('find' in entry['command'] or 'aggregate' in entry['command']):
        command = entry['command']
        
        # Handle 'find' commands
        if 'find' in command:
            collection_name = command['find']
            filter_criteria = command.get('filter', {})  # Query criteria
            collection = db[collection_name]
            
            # Get the query plan using `explain()`
            plan = collection.find(filter_criteria).explain()
            count = count + 1
            with open("ycsb/queryplan_raw/" + str(count) + ".mongodb", 'w', encoding='UTF-8') as plan_file:
                plan_file.write(json.dumps(plan, indent=2))
        
        # Handle 'aggregate' commands
        elif 'aggregate' in command:
            collection_name = command['aggregate']
            pipeline = command.get('pipeline', [])  # Aggregation pipeline
            collection = db[collection_name]
            
            # Get the query plan using `explain()`
            plan = collection.aggregate(pipeline).explain()
            count = count + 1
            with open("ycsb/queryplan_raw/" + str(count) + ".mongodb", 'w', encoding='UTF-8') as plan_file:
                plan_file.write(json.dumps(plan, indent=2))


print("Query plans saved to query_plans.json")
