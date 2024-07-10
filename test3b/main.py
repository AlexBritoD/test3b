from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    
    if not Product.query.first():
        products = [
            Product(sku='TEST1', name='Producto de prueba 1', stock=5),
            Product(sku='TEST2', name='Producto de prueba 2', stock=8),
            Product(sku='TEST3', name='Producto de prueba 3', stock=150)
        ]
        db.session.add_all(products)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)