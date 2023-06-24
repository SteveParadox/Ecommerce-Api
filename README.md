# EcommerceApi
This is the documentation for the Flask Ecommerce Admin API. It provides endpoints for administering the Ecommerce application.

Table of Contents
Register Admin
Admin Login
Get All Users
Get User by ID
Update User Status
Delete User
Get All Products
Get Product by ID
Create Product
Update Product
Register Admin
Creates a new admin account.

URL: /admin/register
Method: POST
Request Body:
json
Copy code
{
  "name": "Admin Name",
  "email": "admin@example.com",
  "password": "admin123"
}
Response:
json
Copy code
{
  "message": "Admin created!"
}
Admin Login
Allows an admin to log in and obtain an access token.

URL: /admin/login
Method: POST
Request Body:
json
Copy code
{
  "email": "admin@example.com",
  "password": "admin123"
}
Response:
json
Copy code
{
  "message": "Login successful",
  "access_token": "<access_token>"
}
Get All Users
Retrieves a list of all users.

URL: /admin/users
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
[
  {
    "id": 1,
    "name": "User 1",
    "email": "user1@example.com",
    "is_seller": true
  },
  {
    "id": 2,
    "name": "User 2",
    "email": "user2@example.com",
    "is_seller": false
  },
  ...
]
Get User by ID
Retrieves a user by their ID.

URL: /admin/user/<user_id>
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "id": 1,
  "name": "User 1",
  "email": "user1@example.com",
  "is_seller": true
}
Update User Status
Updates the status of a user.

URL: /admin/users/<user_id>/status
Method: PUT
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "status": true
}
Response:
json
Copy code
{
  "message": "Successfully updated user <user_id> status to <new_status>."
}
Delete User
Deletes a user.

URL: /admin/users/<user_id>/delete
Method: DELETE
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Successfully deleted user <user_id>."
}
Get All Products
Retrieves a list of all products.

URL: /admin/products
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "products": [
    {
      "id": 1,
      "name": "Product 1",
      "price": 19.99,
      ...
    },
    {
      "id": 2,
      "name": "Product 2",
      "price": 29.99,
      ...
    },
    ...
  ]
}
Get Product by ID
Retrieves details for a specific product.

URL: /admin/products/<product_id>
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "product": {
    "id": 1,
    "name": "Product 1",
    "price": 19.99,
    ...
  }
}
Create Product
Creates a new product.

URL: /admin/products
Method: POST
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "name": "Product Name",
  "price": 9.99,
  ...
}
Response:
json
Copy code
{
  "product": {
    "id": 1,
    "name": "Product Name",
    "price": 9.99,
    ...
  }
}
Update Product
Updates an existing product.

URL: /admin/products/<product_id>/update
Method: PUT
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "name": "Updated Product Name",
  "price": 14.99,
  ...
}
Response:
json
Copy code
{
  "product": {
    "id": 1,
    "name": "Updated Product Name",
    "price": 14.99,
    ...
  }
}

Delete Product
Deletes a product.

URL: /admin/products/<product_id>/delete
Method: DELETE
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Product deleted successfully"
}
Get All Orders
Retrieves a list of all orders.

URL: /admin/orders
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "orders": [
    {
      "id": 1,
      "status": "Completed",
      "total_price": 99.99,
      "user_id": "John Doe",
      "products": [
        {
          "id": 1,
          "name": "Product 1",
          "price": 19.99,
          "quantity": 2
        },
        {
          "id": 2,
          "name": "Product 2",
          "price": 29.99,
          "quantity": 1
        },
        ...
      ]
    },
    {
      "id": 2,
      "status": "Pending",
      "total_price": 49.99,
      "user_id": "Jane Smith",
      "products": [
        {
          "id": 3,
          "name": "Product 3",
          "price": 9.99,
          "quantity": 3
        },
        ...
      ]
    },
    ...
  ]
}

Get Brands
Retrieves a list of all brands.

URL: /admin/brands
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "brands": [
    "Brand 1",
    "Brand 2",
    ...
  ]
}
Create Category
Creates a new category or retrieves all categories.

URL: /admin/create/category
Method: POST (Create Category) or GET (Retrieve Categories)
Authorization: Bearer <access_token>
Request Body (Create Category):
json
Copy code
{
  "name": ["Category 1", "Category 2", ...]
}
Response (Create Category):
json
Copy code
{
  "id": 1,
  "name": "Category 1"
}
Response (Retrieve Categories):
json
Copy code
[
  {
    "id": 1,
    "name": "Category 1"
  },
  {
    "id": 2,
    "name": "Category 2"
  },
  ...
]
List Admin Categories
Retrieves a list of all categories.

URL: /api/categories
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "Categories": [
    {
      "id": 1,
      "name": "Category 1"
    },
    {
      "id": 2,
      "name": "Category 2"
    },
    ...
  ]
}
Get All Orders
Retrieves a list of all orders.

URL: /admin/orders/all
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "orders": [
    {
      "id": 1,
      "product": "Product 1",
      "quantity": 2,
      "total_price": 99.99
    },
    {
      "id": 2,
      "product": "Product 2",
      "quantity": 1,
      "total_price": 49.99
    },
    ...
  ]
}
Get Order by ID
Retrieves details for a specific order.

URL: /admin/orders/<order_id>
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "orders": {
    "id": 1,
    "description": "Product 1 description",
    "image": "https://example.com/product1.jpg",
    "product": "Product 1",
    "quantity": 2,
    "total_price": 99.99
  }
}

Get Order Status
Retrieves the status of a specific order.

URL: /admin/orders/<order_id>/status
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "orders": {
    "status": "delivered"
  }
}
Delete Order
Deletes a specific order.

URL: /admin/orders/<order_id>
Method: DELETE
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Order deleted successfully"
}
Update Order Status
Updates the status of a specific order.

URL: /orders/<order_id>
Method: PUT
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "status": "shipped"
}
Response:
json
Copy code
{
  "message": "Order status updated successfully"
}

Home
Displays the latest products available.

URL: /api/home
Method: GET
Response:
json
Copy code
{
  "latest_products": [
    {
      "id": 1,
      "name": "Product 1",
      "description": "Description of Product 1",
      "price": 10.99,
      "category": {
        "id": 1,
        "name": "Category 1"
      }
    },
    {
      "id": 2,
      "name": "Product 2",
      "description": "Description of Product 2",
      "price": 19.99,
      "category": {
        "id": 2,
        "name": "Category 2"
      }
    }
  ]
}
Recommended Products
Displays recommended products for the authenticated user.

URL: /recommended/products
Method: GET
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "latest_products": "Coming soon"
}
Search
Performs a search for products based on the provided query.

URL: /api/search?q=<query>
Method: GET
Response:
json
Copy code
[
  {
    "id": 1,
    "name": "Product 1",
    "description": "Description of Product 1",
    "price": 10.99,
    "category": {
      "id": 1,
      "name": "Category 1"
    }
  },
  {
    "id": 2,
    "name": "Product 2",
    "description": "Description of Product 2",
    "price": 19.99,
    "category": {
      "id": 2,
      "name": "Category 2"
    }
  }
]

Create Category
Creates a new category.

URL: /api/create/category
Method: POST
Request Body:
json
Copy code
{
  "name": ["Category 1", "Category 2"]
}
Response:
json
Copy code
{
  "id": 1,
  "name": "Category 1"
}
List Categories
Retrieves a list of all categories.

URL: /api/categories
Method: GET
Response:
json
Copy code
{
  "Categories": [
    {
      "id": 1,
      "name": "Category 1"
    },
    {
      "id": 2,
      "name": "Category 2"
    }
  ]
}
Get All Products
Retrieves a list of all products.

URL: /api/products
Method: GET
Response:
json
Copy code
[
  {
    "id": 1,
    "name": "Product 1",
    "price": 10.99
  },
  {
    "id": 2,
    "name": "Product 2",
    "price": 19.99
  }
]
Get Product Details
Retrieves details of a specific product.

URL: /api/products/<int:product_id>
Method: GET
Response:
json
Copy code
{
  "name": "Product 1",
  "price": 10.99,
  "description": "Description of Product 1"
}
or

json
Copy code
{
  "name": "Product 1",
  "price": 10.99,
  "description": "Description of Product 1",
  "brand": "Brand 1"
}
Search Brands
Performs a search for brands based on the provided query and retrieves associated products.

URL: /api/brand/search?q=<query>
Method: GET
Response:
json
Copy code
[
  {
    "id": 1,
    "name": "Brand 1",
    "products": [
      {
        "id": 1,
        "name": "Product 1",
        "description": "Description of Product 1",
        "price": 10.99,
        "category": {
          "id": 1,
          "name": "Category 1"
        }
      },
      {
        "id": 2,
        "name": "Product 2",
        "description": "Description of Product 2",
        "price": 19.99,
        "category": {
          "id": 2,
          "name": "Category 2"
        }
      }
    ]
  },
  {
    "id": 2,
    "name": "Brand 2",
    "products": [
      {
        "id": 3,
        "name": "Product 3",
        "description": "Description of Product 3",
        "price": 15.99,
        "category": {
          "id": 3,
          "name": "Category 3"
        }
      }
    ]
  }
]

Get Brand Products
Retrieves a list of products belonging to a specific brand.

URL: /brands/<int:brand_id>/products
Method: GET
Response:
json
Copy code
{
  "products": [
    {
      "name": "Product 1",
      "price": 10.99
    },
    {
      "name": "Product 2",
      "price": 19.99
    }
  ]
}
Like Product
Likes a specific product.

URL: /api/products/<int:product_id>/like
Method: POST
Request Headers:
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Product liked successfully!"
}
Dislike Product
Dislikes a specific product.

URL: /products/<int:product_id>/dislike
Method: POST
Request Headers:
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Product disliked successfully."
}
Add Product to Cart
Adds a product to the user's cart.

URL: /products/cart/add
Method: POST
Request Headers:
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "product_id": 1,
  "quantity": 2
}
Response:
json
Copy code
{
  "message": "Product added to cart successfully."
}

View Cart
Retrieves the items in the user's cart.

URL: /products/cart
Method: GET
Request Headers:
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "cart_items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Product 1",
      "quantity": 2,
      "price": 10.99
    },
    {
      "id": 2,
      "product_id": 2,
      "product_name": "Product 2",
      "quantity": 1,
      "price": 19.99
    }
  ]
}
Add Review
Adds a review for a specific product.

URL: /api/products/<int:product_id>/reviews
Method: POST
Request Headers:
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "rating": 4.5,
  "comment": "Great product!"
}
Response:
json
Copy code
{
  "message": "Review added successfully"
}
Get Products by Category
Retrieves a list of products belonging to a specific category.

URL: /products/<category>
Method: GET
Response:
json
Copy code
{
  "category": "Electronics",
  "products": [
    {
      "id": 1,
      "name": "Product 1",
      "price": 10.99,
      "description": "Description 1"
    },
    {
      "id": 2,
      "name": "Product 2",
      "price": 19.99,
      "description": "Description 2"
    }
  ]
}
Place Order
Places an order for the items in the user's cart.

URL: /api/place/order
Method: POST
Request Headers:
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "message": "Orders placed successfully"
}
Get Orders
Retrieves a list of orders placed by the user.

URL: /api/orders
Method: GET
Request Headers:
Authorization: Bearer <access_token>
Response:
json
Copy code
{
  "orders": [
    {
      "id": 1,
      "product": "Product 1",
      "quantity": 2,
      "total_price": 21.98
    },
    {
      "id": 2,
      "product": "Product 2",
      "quantity": 1,
      "total_price": 19.99
    }
  ]
}
Update Order
Updates the details of a specific order.

URL: /api/orders/<int:order_id>/update
Method: PUT
Request Headers:
Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
  "product_id": 2,
  "quantity": 3
}
Response:
json
Copy code
{
  "message": "Order updated successfully"
}
Get Product Review
Retrieves the review for a specific product.

URL: /product/<int:product_id>/review
Method: GET
Response:
json
Copy code
{
  "review": {
    "rating": 4.5,
    "comment": "Great product!"
  }
}
Get Product Ratings
Retrieves a dictionary containing the ratings for each product keyed by product ID.

URL: /product/ratings
Method: GET
Response:
json
Copy code
{
  "product_ratings": {
    "1": [4.5, 5.0],
    "2": [3.5, 4.0, 3.0]
  }
}
