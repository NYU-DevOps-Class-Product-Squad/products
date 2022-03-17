"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  Product   M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(unittest.TestCase):
    """ Test Cases for Product """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """Create a product and assert that it exists"""
        product = Product(name="Pen", category="Stationary", available=True, price=10)
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Pen")
        self.assertEqual(product.category, "Stationary")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 10)
        product = Product(name="Pen", category="Stationary", available=False, price=10)
        self.assertEqual(product.available, False)
        self.assertEqual(product.price, 10)

    def test_add_a_product(self):
        """Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="Pen", category="Stationary", available=True, price=10)
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(product.id, 1)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """Read a product"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        self.assertEqual(product.id, 1)
        # Fetch it back 
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.create()
        logging.debug(product)
        self.assertEqual(product.id, 1)
        # Change it an save it
        product.category = "Office"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.category, "Office")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, 1)
        self.assertEqual(products[0].category, "Office")

    def test_delete_a_product(self):
        """Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """List Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for i in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_serialize_a_product(self):
        """Test serialization of a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], product.available)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)

    def test_deserialize_a_product(self):
        """Test deserialization of a Product"""
        data = {
            "id": 1,
            "name": "Pants",
            "category": "Clothes",
            "available": True,
            "price": 30,
        }
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Pants")
        self.assertEqual(product.category, "Clothes")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 30)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Product with missing data"""
        data = {"id": 1, "name": "Pants", "category": "Clothes"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_available(self):
        """Test deserialization of bad available attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["available"] = "true"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_product(self):
        """Find a Product by ID"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 3)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.available, products[1].available)

    def test_find_by_category(self):
        """Find Products by Category"""
        Product(name="Pen", category="Stationary", available=True).create()
        Product(name="Pants", category="Clothes", available=False).create()
        products = Product.find_by_category("Clothes")
        self.assertEqual(products[0].category, "Clothes")
        self.assertEqual(products[0].name, "Pants")
        self.assertEqual(products[0].available, False)

    def test_find_by_name(self):
        """Find a Product by Name"""
        Product(name="Pen", category="Stationary", available=True).create()
        Product(name="Pants", category="Clothes", available=False).create()
        products = Product.find_by_name("Pants")
        self.assertEqual(products[0].category, "Clothes")
        self.assertEqual(products[0].name, "Pants")
        self.assertEqual(products[0].available, False)

    def test_find_by_availability(self):
        """Find Products by Availability"""
        Product(name="Pen", category="Stationary", available=True).create()
        Product(name="Pants", category="Clothes", available=False).create()
        Product(name="Pencil", category="Stationary", available=True).create()
        products = Product.find_by_availability(False)
        product_list = list(products)
        self.assertEqual(len(product_list), 1)
        self.assertEqual(products[0].name, "Pants")
        self.assertEqual(products[0].category, "Clothes")
        products = Product.find_by_availability(True)
        product_list = list(products)
        self.assertEqual(len(product_list), 2)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.available, products[1].available)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)