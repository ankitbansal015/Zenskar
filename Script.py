import requests
import json
import requests
from datetime import datetime

# Constants
API_KEY = 'sandbox_44qNrR5eULWSYkDQdha1Wx-1dHbFlElcxAKNaHODZlg'  # Replace with your API key
ORG_ID = 'bca751e6-7758-4334-b4eb-618771ebcf6a'     # Replace with your Organization ID
BASE_URL = 'https://api.zenskar.com/v2'

# Function to authenticate with Zenskar API
def authenticate():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    return headers

# 1. Create a Customer
def create_customer():
    url = f"{BASE_URL}/customers"
    headers = authenticate()
    customer_data = {
        "name": "Example Customer",
        "phone": "+1234567890",
        "address": "123 Frost Street, New York, United States 10001"
    }
    response = requests.post(url, headers=headers, data=json.dumps(customer_data))
    if response.status_code == 201:
        print("Customer created successfully:", response.json())
        return response.json()['id']  # Return customer ID for later use
    else:
        print("Failed to create customer:", response.json())
        return None

# 2. Create Products and Pricing
def create_product(name, product_type, billing, frequency, price, quantity=None):
    url = f"{BASE_URL}/products"
    headers = authenticate()
    product_data = {
        "name": name,
        "type": product_type,
        "billing": billing,
        "frequency": frequency,
        "price": price
    }
    if quantity is not None:
        product_data["quantity"] = quantity

    response = requests.post(url, headers=headers, data=json.dumps(product_data))
    if response.status_code == 201:
        print(f"Product '{name}' created successfully:", response.json())
        return response.json()['id']  # Return product ID for later use
    else:
        print(f"Failed to create product '{name}':", response.json())
        return None

# 3. Create a Contract
def create_contract(customer_id, product_ids):
    url = f"{BASE_URL}/contracts"
    headers = authenticate()
    contract_data = {
        "customer_id": customer_id,
        "products": product_ids,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    response = requests.post(url, headers=headers, data=json.dumps(contract_data))
    if response.status_code == 201:
        print("Contract created successfully:", response.json())
    else:
        print("Failed to create contract:", response.json())

# Main execution
if __name__ == "__main__":
    customer_id = create_customer()
    if customer_id:
        product1_id = create_product("One Time Fee", "Subscription Fee", "Prepaid", "One-time", 5000)
        product2_id = create_product("Monthly Platform Fee", "Subscription Fee", "Postpaid", "Monthly", 10000)
        quantity = int(input("Enter the number of users for Monthly User Fee: "))
        product3_id = create_product("Monthly User Fee", "Usage Fee", "Postpaid", "Monthly", 60, quantity)

        # Create a contract with the created products
        if product1_id and product2_id and product3_id:
            create_contract(customer_id, [product1_id, product2_id, product3_id])
