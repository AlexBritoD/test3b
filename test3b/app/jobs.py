from . import scheduler
from .models import Product, db

def check_stock():
    with scheduler.app.app_context():
        low_stock_products = Product.query.filter(Product.stock < 10).all()
        for product in low_stock_products:
            print(f"ALERT: Product {product.name} (SKU: {product.sku}) low stack: {product.stock}")
