from pymongo import MongoClient
client = MongoClient('localhost',27017) #MongoClient('host',port)
db = client.TYCS #client.name_of_the_database
def insert():
    try:
        empID = input("Enter the ID: ")
        empName = input("Enter the Name: ")
        empAge = input("Enter the Age: ")
        empCountry = input("Enter the Country: ")

        db.Employee.insert_one(
            {
                "_id": empID,
                "name": empName,
                "age": empAge,
                "country": empCountry,
            }
        )
        print("\nData Inserted Successfully.")
    except Exception:
        print(str(Exception))
    finally:
        client.close()

insert()








































<?php
$m=new MongoClient();
echo "Connection to Database Succesfully";

$db=$m->mydb;
echo "Database my db selected";
$collection=$db->mycol;
echo "Collection selected succesfully";

$doc=array(
"title" => "MongoDB",
"description" => "database",
"like"=>100,
"url"=>"http://www.mongo.com",
"by"=>"NoSql");

$collection->insert($doc);
echo "Document inserted succesfully";
?>










MongoClient mongo=new MongoClient("localhost",27017);
System.out.println("connected to the database successfully:");
MongoDatabase database=mongo.getDatabase("TYCS");
MongoCollection<Document>collection=database.getCollection("STUDENT_COL");
System.out.println("Collection STUDENT_COL selected successfully");
Document document=new Document();
document.append("ID",1);
document.append("Rollno",248637);
document.append("age",19);
document.append("college","Mulund College of Commerce");
collection.insertOne(document);
System.out.println("Document inserted Successfully");
