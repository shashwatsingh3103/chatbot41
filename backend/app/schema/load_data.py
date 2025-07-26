import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tables import *

DATABASE_URL = "sqlite:///ecommerce.db"

def parse_datetime(date_str):
    if pd.isna(date_str) or not date_str:
        return None
    try:
        return pd.to_datetime(date_str).to_pydatetime()
    except Exception:
        return None

def load_users(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_user = session.query(User).filter_by(email=row['email']).first()
        if existing_user:
            existing_user.first_name = row['first_name']
            existing_user.last_name = row['last_name']
            existing_user.age = row['age']
            existing_user.gender = row['gender']
            existing_user.state = row['state']
            existing_user.street_address = row['street_address']
            existing_user.postal_code = row['postal_code']
            existing_user.city = row['city']
            existing_user.country = row['country']
            existing_user.latitude = row['latitude']
            existing_user.longitude = row['longitude']
            existing_user.traffic_source = row['traffic_source']
            existing_user.created_at = parse_datetime(row['created_at'])
        else:
            user = User(
                id=row['id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                age=row['age'],
                gender=row['gender'],
                state=row['state'],
                street_address=row['street_address'],
                postal_code=row['postal_code'],
                city=row['city'],
                country=row['country'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                traffic_source=row['traffic_source'],
                created_at=parse_datetime(row['created_at'])
            )
            session.add(user)
    session.commit()
    print(f"Loaded users from {filepath}")

def load_distribution_centers(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_dc = session.get(DistributionCenter, row['id'])
        if existing_dc:
            existing_dc.name = row['name']
            existing_dc.latitude = row['latitude']
            existing_dc.longitude = row['longitude']
        else:
            dc = DistributionCenter(
                id=row['id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude']
            )
            session.add(dc)
    session.commit()
    print(f"Loaded distribution centers from {filepath}")

def load_products(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_product = session.get(Product, row['id'])
        if existing_product:
            existing_product.cost = row['cost']
            existing_product.category = row['category']
            existing_product.name = row['name']
            existing_product.brand = row['brand']
            existing_product.retail_price = row['retail_price']
            existing_product.department = row['department']
            existing_product.sku = row['sku']
            existing_product.distribution_center_id = row['distribution_center_id']
        else:
            product = Product(
                id=row['id'],
                cost=row['cost'],
                category=row['category'],
                name=row['name'],
                brand=row['brand'],
                retail_price=row['retail_price'],
                department=row['department'],
                sku=row['sku'],
                distribution_center_id=row['distribution_center_id']
            )
            session.add(product)
    session.commit()
    print(f"Loaded products from {filepath}")

def load_inventory_items(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_item = session.get(InventoryItem, row['id'])
        if existing_item:
            existing_item.product_id = row['product_id']
            existing_item.created_at = parse_datetime(row['created_at'])
            existing_item.sold_at = parse_datetime(row['sold_at'])
            existing_item.cost = row['cost']
            existing_item.product_category = row['product_category']
            existing_item.product_name = row['product_name']
            existing_item.product_brand = row['product_brand']
            existing_item.product_retail_price = row['product_retail_price']
            existing_item.product_department = row['product_department']
            existing_item.product_sku = row['product_sku']
            existing_item.product_distribution_center_id = row['product_distribution_center_id']
        else:
            item = InventoryItem(
                id=row['id'],
                product_id=row['product_id'],
                created_at=parse_datetime(row['created_at']),
                sold_at=parse_datetime(row['sold_at']),
                cost=row['cost'],
                product_category=row['product_category'],
                product_name=row['product_name'],
                product_brand=row['product_brand'],
                product_retail_price=row['product_retail_price'],
                product_department=row['product_department'],
                product_sku=row['product_sku'],
                product_distribution_center_id=row['product_distribution_center_id']
            )
            session.add(item)
    session.commit()
    print(f"Loaded inventory items from {filepath}")

def load_orders(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_order = session.get(Order, row['order_id'])
        if existing_order:
            existing_order.user_id = row['user_id']
            existing_order.status = row['status']
            existing_order.gender = row['gender']
            existing_order.created_at = parse_datetime(row['created_at'])
            existing_order.returned_at = parse_datetime(row['returned_at'])
            existing_order.shipped_at = parse_datetime(row['shipped_at'])
            existing_order.delivered_at = parse_datetime(row['delivered_at'])
            existing_order.num_of_item = row['num_of_item']
        else:
            order = Order(
                order_id=row['order_id'],
                user_id=row['user_id'],
                status=row['status'],
                gender=row['gender'],
                created_at=parse_datetime(row['created_at']),
                returned_at=parse_datetime(row['returned_at']),
                shipped_at=parse_datetime(row['shipped_at']),
                delivered_at=parse_datetime(row['delivered_at']),
                num_of_item=row['num_of_item']
            )
            session.add(order)
    session.commit()
    print(f"Loaded orders from {filepath}")

def load_order_items(session, filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        existing_order_item = session.get(OrderItem, row['id'])
        if existing_order_item:
            existing_order_item.order_id = row['order_id']
            existing_order_item.user_id = row['user_id']
            existing_order_item.product_id = row['product_id']
            existing_order_item.inventory_item_id = row['inventory_item_id']
            existing_order_item.status = row['status']
            existing_order_item.created_at = parse_datetime(row['created_at'])
            existing_order_item.shipped_at = parse_datetime(row['shipped_at'])
            existing_order_item.delivered_at = parse_datetime(row['delivered_at'])
            existing_order_item.returned_at = parse_datetime(row['returned_at'])
            existing_order_item.sale_price = row['sale_price']
        else:
            order_item = OrderItem(
                id=row['id'],
                order_id=row['order_id'],
                user_id=row['user_id'],
                product_id=row['product_id'],
                inventory_item_id=row['inventory_item_id'],
                status=row['status'],
                created_at=parse_datetime(row['created_at']),
                shipped_at=parse_datetime(row['shipped_at']),
                delivered_at=parse_datetime(row['delivered_at']),
                returned_at=parse_datetime(row['returned_at']),
                sale_price=row['sale_price']
            )
            session.add(order_item)
    session.commit()
    print(f"Loaded order items from {filepath}")

def main():
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    load_users(session, 'backend/app/data/users.csv')
    load_distribution_centers(session, 'backend/app/data/distribution_centers.csv')
    load_products(session, 'backend/app/data/products.csv')
    load_inventory_items(session, 'backend/app/data/inventory_items.csv')
    load_orders(session, 'backend/app/data/orders.csv')
    load_order_items(session, 'backend/app/data/order_items.csv')

    session.close()
    print("Data loading complete.")

if __name__ == "__main__":
    main()
