import os
from flask import Flask, Request, jsonify
import requests

app = Flask(__name__)
fastapi_url = f"http://{os.environ.get('MARKETPLACE_SVC_ADDRESS')}/api"


# ------- User Routes -------

def add_user(request: Request):
    request = request.json
    if not request:
        return jsonify({"error": "User data is required"}), 400

    response = requests.post(f"{fastapi_url}/users/", json=request.json)

    if response.status_code == 201:
        user = response.json().get('user')
        return user, None

    return None, (response.text, response.status_code)


def get_users():
    response = requests.get(f"{fastapi_url}/users/")
    if response.status_code == 200:
        users = response.json().get('users')
        return users, None

    return None, (response.text, response.status_code)


def get_user_by_username(username):
    if not username:
        return jsonify({"error": "Username is required"}), 400

    response = requests.get(f"{fastapi_url}/users/{username}")

    if response.status_code == 200:
        user = response.json().get('user')
        return user, None

    return None, (response.text, response.status_code)


def delete_user(username):
    if not username:
        return jsonify({"error": "Username is required"}), 400

    response = requests.delete(f"{fastapi_url}/users/{username}")

    if response.status_code == 204:
        return None, None

    return None, (response.text, response.status_code)


# ------- Product Routes -------

def add_product(request: Request):
    product_data = request.get_json()

    if not product_data:
        return {"error": "Product data is required"}, 400

    response = requests.post(f"{fastapi_url}/products/", json=product_data)

    if response.status_code == 201:
        product = response.json().get('product')
        return product, None

    return None, (response.text, response.status_code)


def get_products():
    response = requests.get(f"{fastapi_url}/products/")
    if response.status_code == 200:
        products = response.json().get('products')
        return products, None

    return None, (response.text, response.status_code)


def get_product_by_id(product_id):
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    response = requests.get(f"{fastapi_url}/products/{product_id}")

    if response.status_code == 200:
        product = response.json().get('product')
        return product, None

    return None, (response.text, response.status_code)


def update_product_rating(request: Request, product_id):
    request = request.json
    if not request or not product_id:
        return jsonify({"error": "Product data is required"}), 400

    response = requests.post(
        f"{fastapi_url}/products/{product_id}/review/", json=request.json
    )

    if response.status_code == 200:
        product = response.json()
        return product, None

    return None, (response.text, response.status_code)


def delete_product(product_id):
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    response = requests.delete(f"{fastapi_url}/products/{product_id}")

    if response.status_code == 204:
        return None, None

    return None, (response.text, response.status_code)


# ------- Review Routes -------

def add_review(request: Request):
    review_data = request.get_json()

    if not review_data:
        return {"error": "Review data is required"}, 400

    response = requests.post(
        f"{fastapi_url}/reviews/", json=review_data
    )

    if response.status_code == 201:
        review = response.json().get('review')
        return review, None

    return None, (response.text, response.status_code)


def get_reviews():
    response = requests.get(f"{fastapi_url}/reviews/")
    if response.status_code == 200:
        reviews = response.json().get('reviews')
        return reviews, None

    return None, (response.text, response.status_code)


def get_reviews_per_product(product_id):
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    response = requests.get(f"{fastapi_url}/reviews/{product_id}")

    if response.status_code == 200:
        reviews = response.json().get('reviews')
        return reviews, None

    return None, (response.text, response.status_code)


# ------- Transaction Routes -------

def add_transaction(request: Request):
    transaction_data = request.get_json()

    if not transaction_data:
        return {"error": "Transaction data is required"}, 400

    response = requests.post(
        f"{fastapi_url}/transactions/", json=transaction_data
    )

    if response.status_code == 201:
        transaction = response.json().get('transaction')
        return transaction, None

    return None, (response.text, response.status_code)


def get_all_transactions():
    response = requests.get(f"{fastapi_url}/transactions/")
    if response.status_code == 200:
        transactions = response.json().get('transactions')
        return transactions, None

    return None, (response.text, response.status_code)


def get_user_transactions(user_id):
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    response = requests.get(f"{fastapi_url}/transactions/{user_id}")

    if response.status_code == 200:
        transactions = response.json().get('transactions')
        return transactions, None

    return None, (response.text, response.status_code)
