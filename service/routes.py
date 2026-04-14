######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Store Service with UI
"""

from flask import jsonify, request, abort
from service.models import Product, Category
from service.common import status
from . import app


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")
    if request.headers["Content-Type"] != content_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")


@app.route("/health")
def healthcheck():
    """Health check"""
    return jsonify(message="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Root URL"""
    return app.send_static_file("index.html")


@app.route("/products", methods=["POST"])
def create_products():
    """Creates a Product"""
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    return jsonify(product.serialize()), status.HTTP_201_CREATED


@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Retrieve a single Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product {product_id} not found")
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update a Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a Product"""
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT


@app.route("/products", methods=["GET"])
def list_products():
    """List Products with optional filters"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    products = []
    if name:
        products = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        products = Product.find_by_availability(available.lower() in ["true", "1", "yes"])
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
