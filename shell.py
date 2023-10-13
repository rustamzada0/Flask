from app import app
from models import *

with app.app_context():

    # category1=Category("Shirts")
    # category1.save()

    # category2=Category("Jeans")
    # category2.save()

    # category3=Category("Swimwear")
    # category3.save()

    # category4=Category("Sleepwear")
    # category4.save()

    # category5=Category("Sportswear")
    # category5.save()

    # category6=Category("Jumpsuits")
    # category6.save()

    # category7=Category("Blazers")
    # category7.save()

    # category8=Category("Jackets")
    # category8.save()

    # category9=Category("Shoes")
    # category9.save()

#####################################################################################################

    product1=Product("/static/img/pr-1.webp","Product 1", 45, 39, 4, 1, "Məhsul haqqında məlumat")
    product1.save()

    product2=Product("/static/img/pr-2.webp","Product 2", 65, 45, 2, 5, "Məhsul haqqında məlumat")
    product2.save()

    product3=Product("/static/img/pr-3.webp","Product 3", 120, 99, 1, 9, "Məhsul haqqında məlumat")
    product3.save()

    product4=Product("/static/img/pr-4.webp","Product 4", 110, 89, 3, 9, "Məhsul haqqında məlumat")
    product4.save()

    product5=Product("/static/img/pr-5.webp","Product 5", 75, 55, 1, 8, "Məhsul haqqında məlumat")
    product5.save()

    product6=Product("/static/img/pr-6.webp","Product 6", 45, 39, 4, 1, "Məhsul haqqında məlumat")
    product6.save()

    product7=Product("/static/img/pr-7.webp","Product 7", 40, 35, 0, 5, "Məhsul haqqında məlumat")
    product7.save()

    product8=Product("/static/img/pr-8.webp","Product 8", 50, 40, 6, 8, "Məhsul haqqında məlumat")
    product8.save()

    product9=Product("/static/img/pr-9.webp","Product 9", 72, 29, 9, 4, "Məhsul haqqında məlumat")
    product9.save()

######################################################################################################

    # detail1=Detail("/static/img/pr11.webp", 1)
    # detail1.save()

    # detail2=Detail("/static/img/pr12.webp", 1)
    # detail2.save()

    # detail3=Detail("/static/img/pr13.webp", 1)
    # detail3.save()

    # detail4=Detail("/static/img/pr14.webp", 1)
    # detail4.save()

    # detail5=Detail("/static/img/pr15.webp", 1)
    # detail5.save()