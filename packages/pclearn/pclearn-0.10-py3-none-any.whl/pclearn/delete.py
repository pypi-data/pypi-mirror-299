from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.TYCS

def delete():
    try:
        id = input('Enter the ID: ')
        db.Employee.delete_one({"_id": id})
        print('\nData Deleted Successfully')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

delete()









































<?php
   $m = new MongoClient();
   echo "Connection to database successfully";
	
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";
   
   $collection->remove(array("title"=>"MongoDB Tutorial"));
   echo "Documents deleted successfully";
   
   $cursor = $collection->find();
	
   echo "Delete document";
	
   foreach ($cursor as $document) {
      echo $document["title"] . "\n";
   }
?>






MongoClient mongo = new MongoClient("localhost", 27017);
 System.out.println("Connected to the database successfully:");
 MongoDatabase database = mongo.getDatabase("TYCS");
 MongoCollection<Document> collection = database.getCollection("STUDENT_COL");
 System.out.println("Collection STUDENT COL selected successfully");
 Document filter = new Document("Rollno", 248637);
 collection.deleteMany(filter);
 System.out.println("Document deleted Successfully");
