"""
Product Service

Paths:
------
GET /products - Returns a list all of the Products
GET /products/{id} - Returns the Product with a given id number
POST /products - creates a new Product record in the database
PUT /products/{id} - updates a Product record in the database
DELETE /products/{id} - deletes a Product record in the database

Actions:

PUT /products/{id}/disable - Disable a product 
PUT /products/{id}/enable - Enable of a product

"""

from itertools import product
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError
from . import status  # HTTP Status Codes
from . import app  # Import Flask application

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")
    # app.logger.info("Request for Root URL")
    # return (
    #     jsonify(
    #         name="Product REST API Service",
    #         version="1.0",
    #         paths=url_for("list_products", _external=True),
    #     ),
    #     status.HTTP_200_OK,
    # )


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# READ A PRODUCT 
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(product_id))

    app.logger.info("Returning product: %s", product.name)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        raise NotFound("Product with id '{}' was not found.".format(product_id))
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    app.logger.info("Product with ID [%s] updated.", product.id)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)

######################################################################
# LIST ALL PRODUCTS
######################################################################

@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    app.logger.info("Request for product list")
    products = []
    category = request.args.get("category")
    name = request.args.get("name")
    minimum = request.args.get("minimum")
    maximum = request.args.get("maximum")
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    elif minimum and maximum:
        products = Product.query_by_price(minimum, maximum)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a product
    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()

    app.logger.info("Product with ID [%s] delete complete.", product_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Product.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
    
######################################################################
# UPDATE A PRODUCT'S AVAILABILITY to FALSE
######################################################################
@app.route("/products/<int:product_id>/disable", methods=["PUT"])
def disable_product(product_id):
    """Update a Product's availability to false
    IRL, this action would also remove the product from shopping carts, tell the warehouse to order more, and/or something similar
    """
    app.logger.info("Request to disable product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        raise NotFound(
           "Product with id '{}' was not found.".format(product_id))
    product.deserialize(request.get_json())
    product.available = False
    product.update()
    app.logger.info("Product with ID [%s] disabled.", product.id)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)
######################################################################
# UPDATE A PRODUCT'S AVAILABILITY to TRUE
######################################################################
@app.route("/products/<int:product_id>/enable", methods=["PUT"])
def enable_product(product_id):
    """Update a Product's availability to true
    IRL, this action would add the product back to the catalog so users could order it, etc.
    """
    app.logger.info("Request to enable product with id: %s", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        raise NotFound(
           "Product with id '{}' was not found.".format(product_id))
    product.deserialize(request.get_json())
    product.available = True
    product.update()
    app.logger.info("Product with ID [%s] enabled.", product.id)
    return make_response(jsonify(product.serialize()), status.HTTP_200_OK)