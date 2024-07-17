import json
from faker import Faker
from datetime import datetime
import random

fake = Faker()

def read_image_urls(filename='image_urls.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]
    
data = {
    "users": [],
    "cards": [],
    "orders": [],
    "payments": [],
    "inventory": [],
    "cart_items": [],
    "order_items": []
}

def generate_users(num_users=10):
    users = []
    for _ in range(num_users):
        user = {
            "id": _ + 1,
            "name": fake.name(),
            "email": fake.email(),
            "password": fake.password()
        }
        users.append(user)
    return users

def generate_cards(num_cards=20, image_urls=None):
    cards = []
    image_url_index = 0
    for _ in range(num_cards):
        image_url = image_urls[image_url_index] if image_urls and image_url_index < len(image_urls) else fake.image_url()
        card = {
            "id": _ + 1,
            "card_name": fake.word(),
            "artist": fake.name(),
            "group": fake.word(),
            "album": fake.word(),
            "price": round(random.uniform(10.0, 100.0), 2),
            "description": fake.text(),
            "image_url": image_url
        }
        cards.append(card)
        image_url_index += 1
    return cards

def generate_orders(users, num_orders=30):
    orders = []
    for _ in range(num_orders):
        user = random.choice(users)
        order = {
            "id": _ + 1,
            "user_id": user["id"],
            "order_date": fake.date_time_this_year().isoformat(),
            "total_amount": round(random.uniform(50.0, 500.0), 2)
        }
        orders.append(order)
    return orders

def generate_payments(orders):
    payments = []
    for order in orders:
        payment = {
            "id": order["id"],
            "order_id": order["id"],
            "payment_date": fake.date_time_this_year().isoformat(),
            "payment_method": random.choice(['Credit Card', 'PayPal', 'Bank Transfer']),
            "payment_status": random.choice(['Completed', 'Pending', 'Failed'])
        }
        payments.append(payment)
    return payments

def generate_inventory(cards):
    inventory = []
    for card in cards:
        item = {
            "id": card["id"],
            "card_id": card["id"],
            "quantity_available": random.randint(1, 100)
        }
        inventory.append(item)
    return inventory

def generate_cart_items(users, cards):
    cart_items = []
    for user in users:
        for _ in range(random.randint(1, 5)):
            cart_item = {
                "id": len(cart_items) + 1,
                "user_id": user["id"],
                "card_id": random.choice(cards)["id"],
                "quantity": random.randint(1, 10)
            }
            cart_items.append(cart_item)
    return cart_items

def generate_order_items(orders, cards):
    order_items = []
    for order in orders:
        for _ in range(random.randint(1, 5)):
            order_item = {
                "id": len(order_items) + 1,
                "order_id": order["id"],
                "card_id": random.choice(cards)["id"],
                "quantity": random.randint(1, 10)
            }
            order_items.append(order_item)
    return order_items

def main():
    users = generate_users(num_users=25)
    image_urls = read_image_urls() 
    cards = generate_cards(num_cards=49, image_urls=image_urls)
    orders = generate_orders(users, num_orders=100)
    payments = generate_payments(orders)
    inventory = generate_inventory(cards)
    cart_items = generate_cart_items(users, cards)
    order_items = generate_order_items(orders, cards)

    data["users"] = users
    data["cards"] = cards
    data["orders"] = orders
    data["payments"] = payments
    data["inventory"] = inventory
    data["cart_items"] = cart_items
    data["order_items"] = order_items

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
