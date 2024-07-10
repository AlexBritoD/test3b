import unittest
from app import create_app, db
from app.models import Product, Order

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product(self):
        response = self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('product_id', response.json)
        
        response = self.client.post('/api/products', json={'sku': 'TEST2'})
        self.assertEqual(response.status_code, 400)
        
        self.client.post('/api/products', json={'sku': 'TEST3', 'name': 'Another Product'})
        response = self.client.post('/api/products', json={'sku': 'TEST3', 'name': 'Duplicate SKU'})
        self.assertEqual(response.status_code, 400)

    def test_update_stock(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        
        response = self.client.patch('/api/inventories/product/1', json={'stock': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['new_stock'], 150)
        
        response = self.client.patch('/api/inventories/product/1', json={'stock': -200})
        self.assertEqual(response.status_code, 400)

        response = self.client.patch('/api/inventories/product/999', json={'stock': 30})
        self.assertEqual(response.status_code, 404)

    def test_create_order(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        
        response = self.client.post('/api/orders', json={'product_id': 1, 'quantity': 10})
        self.assertEqual(response.status_code, 201)
        self.assertIn('order_id', response.json)
        
        response = self.client.post('/api/orders', json={'product_id': 1, 'quantity': 100})
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post('/api/orders', json={'product_id': 999, 'quantity': 1})
        self.assertEqual(response.status_code, 404)

    def test_get_product(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        
        response = self.client.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sku'], 'TEST1')
        
        response = self.client.get('/api/products/999')
        self.assertEqual(response.status_code, 404)

    def test_delete_product(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        
        response = self.client.delete('/api/products/1')
        self.assertEqual(response.status_code, 204)
        
        response = self.client.delete('/api/products/999')
        self.assertEqual(response.status_code, 404)

    def test_get_order(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        self.client.post('/api/orders', json={'product_id': 1, 'quantity': 10})
        
        response = self.client.get('/api/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['product_id'], 1)
        
        response = self.client.get('/api/orders/999')
        self.assertEqual(response.status_code, 404)

    def test_delete_order(self):
        self.client.post('/api/products', json={'sku': 'TEST1', 'name': 'Test Product'})
        self.client.post('/api/orders', json={'product_id': 1, 'quantity': 10})
        
        response = self.client.delete('/api/orders/1')
        self.assertEqual(response.status_code, 204)
        
        response = self.client.delete('/api/orders/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
