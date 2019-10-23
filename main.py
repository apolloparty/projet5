#!/usr/bin/python3
# -*- coding: Utf-8 -*

import mysql.connector
import Class.Sql as S
import Class.Searching as Se
import Class.Calc as C
import Class.Listing as L
import Class.User_interface as U

mydb = mysql.connector.connect(
    host="localhost",
    user="testeur",
    passwd="testeur",
    database="test"
    )
mycursor = mydb.cursor()
reboot = U.User_interface(mycursor).introduct()
category, category_name = U.User_interface(mycursor).chosen_cat()
name, product_type, category = U.User_interface(mycursor).chosen_prod(category)
if reboot == "1":
    product_nb, product_gbl, product_dict = Se.Searching(name).first_search()
    pages = C.Calc(product_nb, product_gbl).calc_pages()
    global_dict = Se.Searching(name).global_search(pages)
    global_dict.update(product_dict)
    names_list, codes_list, description_list, store_list, product_show \
        = L.Listing(product_nb, pages, name).listing()
    # Sql(names_list, codes_list, description_list, store_list,\
    # product_show, name, category_name, category).\
    # drop_table(mycursor)
else:
    S.Sql(name, category_name, category, mydb, product_type).\
        table_category(mycursor)
if reboot == "1":
    S.Sql(name, category_name, category, mydb, product_type).\
        table_product(mycursor, names_list, codes_list,\
                      description_list, store_list, product_show)
else:
    selected1 = S.Sql(name, category_name, category, mydb, product_type).\
        show_product(mycursor)
    selected2 = S.Sql(name, category_name, category, mydb, product_type).\
        alt_product(mycursor, selected1)
    S.Sql(name, category_name, category, mydb, product_type).\
        save_product(mycursor, selected2)
    S.Sql(name, category_name, category, mydb, product_type).\
        display_saved(mycursor)
