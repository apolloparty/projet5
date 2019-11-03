Welcome to my project program.
This program is based on Python using API Openfoodfact JSON extraction and MySQL management.

Overall:
The program extract JSON files from Openfoodfact API (public data free to use) into MySQL Database.
From theses JSON it collect, name, description, store and URL and create named list from them.
With theses lists we make an insertion into three differents tables, CATEGORY, PRODUCTS and SAVED.
CATEGORY table list all categories, PRODUCTS list all JSON collected list, SAVED permit to register your surrogates products.
You may chose to save your surrogate products or reset, display or reset table SAVED, reset or update tables PRODUCTS and CATEGORY.
Depends of your theses choices, the program display from MySQL database. 

How to use:
1. Modify the Config.py with your SQL parameters.
2. Launch the program and select which product you would like surrogate.
3. /!\ For first use and everytime you would like to add another category or product chose "update database".
4. Follow instructions in the program and enjoy.