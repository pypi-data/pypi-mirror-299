from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.TYCS 

def update():
    try:
        name = input('Enter the name of person whose data is to be updated: ')
        age = input("Enter the updated age: ")
        db.Employee.update_one(
            {"name": name},
            {"$set": {"age": age}}
        )
        print("\nData Updated Successfully")
    except Exception:
        print(str(Exception))
    finally:
        client.close()

update()







































<?php
   $m = new MongoClient();
   echo "Connection to database successfully";
	
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   $collection->update(array("title"=>"MongoDB"), 
      array('$set'=>array("title"=>"MongoDB Tutorial")));
   echo "Document updated successfully";
	
   $cursor = $collection->find();
	
   echo "Updated document";
	
   foreach ($cursor as $document) {
      echo $document["title"] . "<br>";
   }
?>






MongoClient mongo = new MongoClient("localhost", 27017);
 System.out.println("Connected to the database successfully:");
 MongoDatabase database = mongo.getDatabase("TYCS");
 MongoCollection<Document> collection = database.getCollection("STUDENT_COL");
 System.out.println("Collection TYCSCOLL selected successfully");
 Document filter = new Document("Rollno", 248637);
 Document updateDoc = new Document("$set", new Document("age", 22));
 collection.updateOne(filter, updateDoc);
 System.out.println("Document updated Successfully");
