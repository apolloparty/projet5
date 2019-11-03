#!/usr/bin/python3
# -*- coding: Utf-8 -*

import mysql.connector
import Class.Sql as S
import Class.Searching as Se
import Class.Calc as C
import Class.Listing as L
import Class.User_interface as U
import Class.Config as Conf

host, user, passwd, database = Conf.Config().config()
mydb = mysql.connector.connect(
    host = f"{host}",
    user = f"{user}",
    passwd = f"{passwd}",
    database = f"{database}"
    )
mycursor = mydb.cursor()
while 1:
    reboot = U.User_interface(mycursor).introduct()
    category, category_name = U.User_interface(mycursor).chosen_cat()
    name, product_type, category = U.User_interface(mycursor).chosen_prod(category)
    product_nb, product_gbl, product_dict = Se.Searching(name).first_search()
    pages = C.Calc(product_nb, product_gbl).calc_pages()
    if reboot == "1":
        S.Sql(name, category_name, category, mydb, product_type).drop_table(mycursor)
        global_dict = Se.Searching(name).global_search(pages)
        global_dict.update(product_dict)
        names_list, codes_list, description_list, store_list, product_show \
            = L.Listing(product_nb, pages, name).listing()
        S.Sql(name, category_name, category, mydb, product_type).\
            table_category(mycursor)
        S.Sql(name, category_name, category, mydb, product_type).\
            table_product(mycursor, names_list, codes_list,\
                    description_list, store_list, product_show)
    selected1 = S.Sql(name, category_name, category, mydb, product_type).\
        show_product(mycursor)
    selected2 = S.Sql(name, category_name, category, mydb, product_type).\
        alt_product(mycursor, selected1)
    S.Sql(name, category_name, category, mydb, product_type).\
        save_product(mycursor, selected1, selected2)
    S.Sql(name, category_name, category, mydb, product_type).\
        display_saved(mycursor)
