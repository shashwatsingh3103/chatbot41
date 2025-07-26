from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String(1))
    state = Column(String)
    street_address = Column(String)
    postal_code = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String)
    created_at = Column(DateTime)

    orders = relationship("Order", back_populates="user")
    order_items = relationship("OrderItem", back_populates="user")

class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    products = relationship("Product", back_populates="distribution_center")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    cost = Column(Float)
    category = Column(String)
    name = Column(String)
    brand = Column(String)
    retail_price = Column(Float)
    department = Column(String)
    sku = Column(String)
    distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))

    distribution_center = relationship("DistributionCenter", back_populates="products")
    inventory_items = relationship("InventoryItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime)
    sold_at = Column(DateTime, nullable=True)
    cost = Column(Float)
    product_category = Column(String)
    product_name = Column(String)
    product_brand = Column(String)
    product_retail_price = Column(Float)
    product_department = Column(String)
    product_sku = Column(String)
    product_distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))

    product = relationship("Product", back_populates="inventory_items")
    order_items = relationship("OrderItem", back_populates="inventory_item")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
    gender = Column(String(1))
    created_at = Column(DateTime)
    returned_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    num_of_item = Column(Integer)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    status = Column(String)
    created_at = Column(DateTime)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    sale_price = Column(Float)

    order = relationship("Order", back_populates="order_items")
    user = relationship("User", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    inventory_item = relationship("InventoryItem", back_populates="order_items")

# --- Engine and create tables ---

def create_db_and_tables(db_url="sqlite:///ecommerce.db"):
    engine = create_engine(db_url, echo=True)  # echo=True shows SQL logs
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()
