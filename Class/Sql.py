import json
import requests
import sys
import os.path
import mysql.connector
from random import randint
from mysql.connector import errorcode


class Sql:
    """Multiple SQL operation"""
    def __init__(self, name, category_name, category, mydb, product_type):
        self.name = name
        self.category_name = category_name
        self.category = category
        self.mydb = mydb
        self.product_type = product_type

    def drop_table(self, mycursor):
        """Drop the table products"""
        reset = input("\
\nWould you like to reset tables CATEGORY AND PRODUCTS ?\
Press Y, else press anything else : ")
        if reset == "Y":
            mycursor.execute(f"DROP TABLE PRODUCTS")
            mycursor.execute(f"DROP TABLE CATEGORY")
            # reset CATEGORY and PRODUCTS tables

    def table_category(self, mycursor):
        """Create the SQL table category
        
        Use category, category_name and db cursor
        to create table category
        """
        category_name = self.category_name
        category = self.category
        mydb = self.mydb
        x = 0  # increment for product lenght
        y = 0  # increment for lists

        mycursor.execute(f"CREATE TABLE IF NOT EXISTS CATEGORY \
        (category_id INT NOT NULL AUTO_INCREMENT, \
        PRIMARY KEY(category_id), \
        type INT(100), \
        category TEXT(1000))\
        ENGINE=INNODB;")
        sql = f"INSERT INTO CATEGORY (type, category) VALUES (%s, %s)"
        val = [
            (f'{category}', f'Category : {category_name}'),
        ]
        mycursor.executemany(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")

    def table_product(self, mycursor, names_list, codes_list, description_list, store_list, product_show):
        """Create table product

        Using data from list created in Listing()
        Create SQL organized dataquery:
        type, name, url, description, store
        """
        name = self.name
        mydb = self.mydb
        category = self.category
        x = 0  # increment for product lenght
        y = 0  # increment for lists
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS PRODUCTS\
        (product_id INT AUTO_INCREMENT,\
        PRIMARY KEY(product_id),\
        category_id INT(100),\
        type TEXT(1000000),\
        name TEXT(1000000),\
        url TEXT(100000),\
        description TEXT(100000),\
        lieux TEXT(100000),\
        FOREIGN KEY (category_id) REFERENCES CATEGORY(category_id))\
        ENGINE=INNODB;")
        while x != product_show:
            sql = f"INSERT INTO PRODUCTS \
            (type, name, url, description, lieux, category_id) \
            VALUES (%s, %s, %s, %s, %s, %s)"
            val = [
                (f'{name}', f'{names_list[y]}', f'{codes_list[y]}', f'{description_list[y]}', f'{store_list[y]}', f'{category}'),
            ]
            x = x + 1
            y = y + 1
            mycursor.executemany(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "was inserted.")
            # indicate that row is inserted

    def show_product(self, mycursor):
        """Display products from SQL table PRODUCTS

        chose randomnly 10 product of the product type
        """
        name = self.name
        mydb = self.mydb
        selected1 = []
        x = 1

        # rdm_nb = randint(1, product_show)
        mycursor.execute(f"SELECT * FROM PRODUCTS WHERE type = \
        '{name}' ORDER BY RAND() LIMIT 10")
        selected1 = mycursor.fetchall()
        for row in selected1:
            #print(f"\n{row[0]} : ", row[2])
            print("\nName: ", row[3])
            print("URL: ", row[4])
            print("Description: ", row[5])
            print("Store: ", row[6])
        return selected1

    def alt_product(self, mycursor, selected1):
        """Display products from SQL table PRODUCTS

        Chose randomnly 1 product of the product type
        display Name, Url, Description and Store
        """
        mydb = self.mydb
        name = self.name

        selected2 = []
        save = input("\
\nWould you like to see a surrogate product ? \
Write Y, else press anything else : ")
        if save == "Y":
            mycursor.execute(f"SELECT * FROM PRODUCTS WHERE type = \
                '{name}' ORDER BY RAND() LIMIT 1")
            selected2 = mycursor.fetchall()
            for row in selected2:
                print("\nName: ", row[2])
                print("URL: ", row[3])
                print("Description: ", row[4])
                print("Store: ", row[6])
        return selected2

    def save_product(self, mycursor, selected1, selected2):
        """Save the surrogate product in table SAVED

        Save the surrogate product in table
        """
        mydb = self.mydb

        save = input("\
\nWould you like to save the surrogate product in database ? \
Write Y, else press anything else : ")
        if save == "Y":
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS SAVED\
            (id INT AUTO_INCREMENT PRIMARY KEY,\
            product_id INT(255),\
            category_id INT(100),\
            type TEXT(1000000),\
            name TEXT(1000000),\
            url TEXT(100000),\
            description TEXT(100000),\
            lieux TEXT(100000),\
            FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id),\
            FOREIGN KEY (category_id) REFERENCES PRODUCTS(category_id))\
            ENGINE=INNODB;")
            sql = f"INSERT IGNORE INTO SAVED\
            (product_id, category_id, type, name, url, description, lieux)\
            VALUES (%s, %s, %s, %s, %s, %s, %s)"
            mycursor.executemany(sql, selected2)
            mydb.commit()
            print("Product saved in database in table SAVED\n")

    def display_saved(self, mycursor):
        """Display all product from table SAVED"""
        mydb = self.mydb
        save = ""

        save = input("\
Would you like to display saved products ? \
Write Y, else press anything else : \n")
        if save == "Y" or save == "y":
            mycursor.execute(f"SELECT * FROM SAVED")
            saved = mycursor.fetchall()
            for row in saved:
                print("Name: ", row[3])
                print("URL: ", row[4])
                print("Description: ", row[5])
                print("Store: ", row[6])
                print("\n")
