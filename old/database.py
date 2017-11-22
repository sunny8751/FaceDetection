from pymongo import MongoClient
import json

client = MongoClient('mongodb://sunwoo:yUUy0wtR7Sl2EZyO@cluster0-shard-00-00-a4kwu.mongodb.net:27017,cluster0-shard-00-01-a4kwu.mongodb.net:27017,cluster0-shard-00-02-a4kwu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
peopleDB = client.people

def removeMongoPerson(personId):
	peopleDB.remove({"_id": personId})

# param int personId
# param Person person
def addMongoPerson(person):
	newPerson = {
        "_id": person.id,
		"person_group_id": person.personGroupId,
		"num_faces": person.numFaces,
		"name": person.name
	}
	id = peopleDB.insert_one(newPerson).inserted_id
	print("Added person ID to MongoDB:", id)

def printDatabase():
    # matches = people.find_one()
    # for match in matches:
    #     print (match)
    # print(client.database_names())
    print (peopleDB.collection_names())
