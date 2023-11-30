import motor.motor_asyncio
from models import Todo

username = "jithin"
password = "tray2807"

uri = f"mongodb://{username}:{password}@localhost:27017/?authMechanism=DEFAULT"


client = motor.motor_asyncio.AsyncIOMotorClient(uri)
database = client['Todo']
collection = database['sample']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)

async def fetch_one_todo(title):
    document = collection.find_one({"title":title})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    # Assuming result.inserted_id is the ID of the inserted document
    inserted_id = result.inserted_id
    # Assuming you want to return the created todo with its ID
    created_todo = await collection.find_one({"_id": inserted_id})
    return created_todo


async def update_todo(title, desc):
    await collection.update_one({"title":title}, {"$set":{
        "description":desc}})
    document  = await collection.find_one({"title":title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title":title})
    return True