from pymongo import MongoClient
dc_name = "ericgwhuang"
uri = f"mongodb+srv://{dc_name}:{dc_name}@gdg-mongodb.chih-hao.xyz/{dc_name}?authMechanism=SCRAM-SHA-256&tls=true"
tls_ca_file = "mongodb-bundle.pem"
client = MongoClient(uri, tlsCAFile=tls_ca_file)

db = client[f"{dc_name}"]
users = db["users"]

data = {"name": "Eric", "age": 18, "email": "some@email"}
result = users.insert_one(data)

print(users)
