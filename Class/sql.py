import mysql.connector
from mysql.connector import errorcode
 
def connect():

    mydb = mysql.connector.connect(
        host="localhost",
        user="testeur",
        passwd="*******",
        database="test"
        )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE pizza (nom VARCHAR(30), code INT(13), description VARCHAR(255), Lieux VARCHAR(20))")
    sql = "INSERT INTO pizza (nom, code, description, lieux) VALUES (%s, %s, %s, %s)"
    val = [
        ('1', '2', '3', '4'),
        ('5', '6', '7', '8'),
    ]

    mycursor.executemany(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "was inserted.") 
    

    #mycursor.execute("DROP TABLE pizza")
    mycursor.execute("SELECT * FROM pizza")
    myresult = mycursor.fetchall()

    #for x in mycursor:
    #   print(x)

    for x in myresult:
       print(x)     

connect()