import json
import requests
import sys
import os.path
import mysql.connector
from random import randint
from mysql.connector import errorcode

class Sql:

    def __init__(self, name, category_name, category, mydb, product_type):
        self.name = name
        self.category_name = category_name
        self.category = category
        self.mydb = mydb
        self.product_type = product_type


    def drop_table(self, mycursor):
        name = self.name

        restart = input("\nWrite Y, if you want to drop the table, else push enter : ")
        if restart == "Y":
            mycursor.execute(f"DROP TABLE PRODUCTS") #remise à zéro de la table
        else:
            pass

    def table_category(self, mycursor):
        category_name = self.category_name
        category = self.category
        mydb = self.mydb

        x = 0 #increment for product lenght
        y = 0 #increment for lists
        try:
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS CATEGORY \
            (category_id INT AUTO_INCREMENT PRIMARY KEY, \
            type INT(100), \
            category TEXT(1000))")
            sql = f"INSERT INTO CATEGORY (type, category) VALUES (%s, %s)"
            val = [
            (f'{category}', f'Category : {category_name}'),
            ]
            mycursor.executemany(sql, val)
            mydb.commit()
            #print(mycursor.rowcount, "was inserted.") 
        except mysql.connector.errors.ProgrammingError:
            pass

    def table_product(self, mycursor, names_list, codes_list, description_list, store_list, product_show):
        name = self.name
        mydb = self.mydb
        x = 0 #increment for product lenght
        y = 0 #increment for lists
        try: 
            mycursor.execute(f"CREATE TABLE PRODUCTS \
            (product_id INT AUTO_INCREMENT PRIMARY KEY, \
            type TEXT(1000000), \
            name TEXT(1000000), \
            url TEXT(100000), \
            description TEXT(100000), \
            lieux TEXT(100000))")
        except mysql.connector.errors.ProgrammingError:
            pass

        while x != product_show:
            sql = f"INSERT IGNORE INTO PRODUCTS (type, name, url, description, lieux) VALUES (%s, %s, %s, %s, %s)"
            val = [
            (f'{name}', f'{names_list[y]}', f'{codes_list[y]}', f'{description_list[y]}', f'{store_list[y]}'),
            ]
            x = x + 1
            y = y + 1
            mycursor.executemany(sql, val)
            mydb.commit()
            #print(mycursor.rowcount, "was inserted.") #indicate that row is inserted

    def show_product(self, mycursor):
        name = self.name
        mydb = self.mydb
        selected1 = []
        
        #rdm_nb = randint(1, product_show)
        mycursor.execute(f"SELECT * FROM PRODUCTS WHERE type = '{name}' ORDER BY RAND() LIMIT 10")
        selected1 = mycursor.fetchall()
        for row in selected1:
                print(f"\nProduct_id:", row[0], "Name: ", row[2])
                #print("Type", row[1])
                #print("URL: ", row[3])
                #print("Description: ", row[4])
                #print("Store: ", row[5])
        return selected1
    
    def alt_product(self, mycursor, selected1):
        mydb = self.mydb
        name = self.name
        
        selected2 = []
        save = input("\nWould you like to see a surrogate product ? Write Y, else press enter : ")
        #rdm_nb = randint(1, product_show)
        if save == "Y":
            #rdm_nb = randint(1, product_show)
            mycursor.execute(f"SELECT * FROM PRODUCTS WHERE type = '{name}' ORDER BY RAND() LIMIT 1")
            selected2 = mycursor.fetchall()
            for row in selected2:
                print("\nName: ", row[2])
                print("URL: ", row[3])
                print("Description: ", row[4])
                print("Store: ", row[5])
        return selected2

    def save_product(self, mycursor, selected2):
        mydb = self.mydb
        
        save = input("\nWould you like to save the product in database ? Write Y, else press enter : ")
        if save == "Y":
            try:
                mycursor.execute(f"CREATE TABLE IF NOT EXISTS SAVED (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT(255), type TEXT(1000000), name TEXT(1000000), url TEXT(100000), description TEXT(100000), lieux TEXT(100000))")
            except mysql.connector.errors.ProgrammingError:
                pass
            sql = f"INSERT IGNORE INTO SAVED (product_id, type, name, url, description, lieux) VALUES (%s, %s, %s, %s, %s, %s)"
            mycursor.executemany(sql, selected2)
            mydb.commit()
            print("Product saved in database in table SAVED\n")
    
    def display_saved(self, mycursor):
        mydb = self.mydb
        save = ""

        save = input("Would you like to display saved products ?  Write Y, else press enter : ")
        if save == "Y" or save == "y":
            mycursor.execute(f"SELECT * FROM SAVED")
            saved = mycursor.fetchall()
            for row in saved:
                print("Name: ", row[3])
                print("URL: ", row[4])
                print("Description: ", row[5])
                print("Store: ", row[6])
                print("\n")
        else:
            pass