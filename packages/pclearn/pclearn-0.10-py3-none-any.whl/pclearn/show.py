from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.TYCS 
def display():
    try:
        id = input("Enter the ID to display record: ")
        for i in db.Employee.find({"_id":id}):
            print(i)
        print("\nRecord displayed")
    except Exception:
        print(str(Exception))
    finally:
        client.close()
display()







































<?php
$m=new MongoClient();
echo "Connection to Database Succesfully";
$db=$m->mydb;
echo "Database my db selected";
$collection=$db->mycol;
echo "Collection selected succesfully";

$cursor=$collection->find();

foreach ($cursor as $doc){
echo "<br>".$doc["title"]."<br>";
echo "<br>".$doc["description"]."<br>";
echo "<br>".$doc["url"]."<br>";
echo "<br>".$doc["like"]."<br>";
}
?>











MongoClient mongo = new MongoClient("localhost", 27017);
 System.out.println("Connected to the database successfully:");
 MongoDatabase database = mongo.getDatabase("TYCS");
 MongoCollection<Document> collection = database.getCollection("STUDENT_COL");
 System.out.println("Collection TYCSCOLL selected successfully");
 FindIterable<Document> iterDoc = collection.find();
 Iterator it = iterDoc.iterator();
 while (it.hasNext()) {
 System.out.println(it.next());
 }
 mongo.close();
