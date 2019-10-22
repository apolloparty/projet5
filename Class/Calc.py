class Calc:

    def __init__(self, product_nb, product_gbl):
        self.product_nb = product_nb
        self.product_gbl = product_gbl 

    def calc_pages(self):
        product_nb = self.product_nb
        product_gbl = self.product_gbl
        pages = product_gbl/product_nb

        if pages == 0:
            print("Wrong product")
            sys.exit()
        if pages != int(pages):
            pages = int(pages) + 1
        print(pages)
        return pages