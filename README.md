# Order Service API

This Django application provides order management functionality with RESTful endpoints.

## API Endpoints

### Authentication
All endpoints require authentication using JWT or your preferred authentication method.

### Orders

#### Get All Orders
- **URL**: `/orders/`
- **Method**: `GET`
- **Permissions**: Authenticated users can see their own orders. Admins see all orders.
- **Query Parameters**:
  - `status`: Filter orders by status (e.g., `?status=completed`)
- **Response**: List of orders

#### Get Single Order
- **URL**: `/orders/{id}/`
- **Method**: `GET`
- **Permissions**: Order owner or admin
- **Response**: Order details

#### Cancel Order
- **URL**: `/orders/{id}/cancel/`
- **Method**: `POST`
- **Permissions**: Order owner or admin
- **Response**: Success message or error
- **Notes**: Only PENDING orders can be cancelled

#### Update Order Status (Admin only)
- **URL**: `/orders/{id}/update_status/`
- **Method**: `PATCH`
- **Permissions**: Admin only
- **Body**: `{"status": "new_status"}`
- **Valid Statuses**: PENDING, PROCESSING, COMPLETED, CANCELLED
- **Response**: Updated order details

## Status Codes
- 200 OK: Successful request
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found

## Models

### Order
- `user`: ForeignKey to User
- `created_at`: DateTime (auto)
- `updated_at`: DateTime (auto)
- `status`: CharField (PENDING, PROCESSING, COMPLETED, CANCELLED)
- `total`: DecimalField
- `items`: JSONField (contains order items)

## Running Tests
To run the test suite:
```bash
python manage.py test orders
