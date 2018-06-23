from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
from datetime import date
connection = pymysql.connect(host='localhost', user='root', password="n@rman23",
                             db='store_adv', charset='utf8', cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
	return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def add_category():
    catName = request.POST.get('name')
    if catName == '':
        Result = {
            "STATUS": "error",
            "MSG": "No entry",
            "CODE": 400
        }
    else:
        try:
            with connection.cursor() as cursor:
                sql1 = "SELECT name from categories"
                cursor.execute(sql1)
                get_categories = cursor.fetchall()
                for element in get_categories:
                    if element['name'] == catName:
                        Result = {
                            "STATUS": "error",
                            "MSG": "category already exist",
                            "CODE": 200
                        }
                        return json.dumps(Result)
                name = json.dumps(catName)
                sql = "INSERT INTO categories(name) VALUES({})".format(name)
                cursor.execute(sql)
                connection.commit()
                cat_id = cursor.lastrowid
                Result={
                    "STATUS": "success",
                    "CAT_ID": cat_id,
                    "CODE": 201
                }
        except:
            Result = {
                "STATUS": "error",
                "MSG": "INTERNAL ERROR",
                "CODE": 500
            }
    return json.dumps(Result)


@post("/product")
def add_product():
    get_id = json.dumps(request.POST.get('id'))
    getTitle = json.dumps(request.POST.get('title'))
    getCategory = request.POST.get('category')
    getPrice = request.POST.get('price')
    getDescription = json.dumps(request.POST.get('desc'))
    getImg_Url = json.dumps(request.POST.get('img_url'))
    getFavorite = request.POST.get('favorite')
    getDate = str(date.today())
    get_date=json.dumps(getDate)
    if getFavorite == 'on':
        getFavorite = 1
    else:
        getFavorite = 0
    if getCategory== '""':
        Result = {
            "STATUS": "success",
            "MSG": "Category not found",
            "CODE": 404
        }
    else:
        try:
            with connection.cursor() as cursor:
                sql1 = "SELECT title from products"
                cursor.execute(sql1)
                get_product = cursor.fetchall()
                for element in get_product:
                    getTitle2 = request.POST.get('title')
                    if element['title'] == getTitle2:
                        Result = {
                            "STATUS": "error",
                            "MSG": "product already exist",
                            "CODE": 200
                        }
                        return json.dumps(Result)
                if get_id == '""':
                    sql = "INSERT INTO products(category,price,title,description,img_url,date_created,favorite)VALUES({},{},{},{},{},{},{})".format(
                        getCategory, getPrice, getTitle, getDescription, getImg_Url, get_date, getFavorite, )
                else:
                    sql = "UPDATE products SET category={},price={},title={},description={},img_url={},date_created={},favorite={} WHERE id={}".format(
                        getCategory, getPrice, getTitle, getDescription, getImg_Url, get_date, getFavorite, get_id)
                cursor.execute(sql)
                connection.commit()
                product_id = cursor.lastrowid
            Result={
                "STATUS": "success",
                "MSG": "INTERNAL ERROR",
                "PRODUCT_ID": product_id,
                "CODE": 201
            }
        except:
            Result = {
                "STATUS": "error",
                "MSG": "INTERNAL ERROR",
                "CODE": 500
            }
    return json.dumps(Result)


@get("/categories")
def categorie():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            get_categories = cursor.fetchall()
        Result={
            "STATUS": "success",
            "MSG": "INTERNAL ERROR",
            "CATEGORIES": get_categories,
            "CODE": 200
        }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@get("/products")
def products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            get_product = cursor.fetchall()
        if get_product is None:
            Result = {
                "STATUS": "success",
                "MSG": "Product non found",
                "PRODUCTS": get_product,
                "CODE": 404
            }
        else:
            Result = {
                "STATUS": "success",
                "MSG": "product fetched successfully",
                "PRODUCTS": get_product,
                "CODE": 200
            }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@get("/category/<id>/products")
def categorie_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products as p LEFT JOIN categories as c ON p.category = c.id where p.category={} order by favorite desc , date_created desc;".format(id)
            cursor.execute(sql)
            get__category_product = cursor.fetchall()
        Result = {
            "STATUS": "success",
            "MSG": "INTERNAL ERROR",
            "PRODUCTS": get__category_product,
            "CODE": 200
        }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@get("/product/<id>")
def specific_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id={}".format(id)
            cursor.execute(sql)
            get_specific_product = cursor.fetchall()
        Result = {
            "STATUS": "success",
            "MSG": "INTERNAL ERROR",
            "PRODUCT": get_specific_product,
            "CODE": 200
        }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@route("/product/<id>", method="DELETE")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id={}".format(id)
            cursor.execute(sql)
            connection.commit()
        Result = {
            "STATUS": "success",
            "MSG": "INTERNAL ERROR",
            "CODE": 200
        }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@route("/category/<id>", method ="DELETE")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id={}".format(id)
            cursor.execute(sql)
            connection.commit()
        Result = {
            "STATUS": "success",
            "MSG": "INTERNAL ERROR",
            "CODE": 200
        }
    except:
        Result = {
            "STATUS": "error",
            "MSG": "INTERNAL ERROR",
            "CODE": 500
        }
    return json.dumps(Result)


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()

