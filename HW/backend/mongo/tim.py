from pymongo import MongoClient
PWD = "2G1ix1hjDHtvn2Qt"
uri= f"mongodb+srv://aimccccccccc:{PWD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"

cluster = MongoClient(uri)
db = cluster["test_database"]
users = db["users"]
users.insert_one({"name": "yee"})

