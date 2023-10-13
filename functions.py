from models import *

# Stock
categories = Category.query.all()
products_ = Product.query.all()
def stock():
    result=[]
    categories_ids=[] # bütün productların category İD-si
    for product in products_:
        categories_ids.append(product.category_id)
    for category in categories:
        count = 0
        for c_id in categories_ids:
            if category.id == c_id:
                count += 1
        new_dict = {category: count}
        result.append(new_dict)
    return result

stock()
stocks = stock()
# End Stock