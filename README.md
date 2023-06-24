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
