# Library Service API

A modern RESTful API for managing library borrowings, book inventory, and automated payments using Stripe. This project is built with Django Rest Framework and fully containerized with Docker.

## 📋 Project Status & Roadmap
The project development is tracked on Trello. You can view the current tasks and progress here:
[DRF Practice Trello Board](https://trello.com/b/wzL5VQk7/drf-practice)

## 🚀 Features
- **User Management**: Custom user model with JWT Authentication.
- **Book Inventory**: Management of books with real-time inventory updates.
- **Borrowing System**: Automated borrowing process with date validation.
- **Stripe Integration**: Secure payment processing for borrowings.
- **Automated Status Updates**: Payments automatically switch to `PAID` status upon successful transaction.

## 🛠 Tech Stack
- **Framework**: Django & Django Rest Framework
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Payments**: Stripe API
- **Auth**: SimpleJWT

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd library-service-drf
2. Environment Variables
Create a .env file in the root directory and add your credentials:


POSTGRES_DB=library
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_pub_key
3. Run with Docker
Bash

docker-compose up --build
The API will be available at http://127.0.0.1:8000/api/.

📖 API Usage
Borrowings
POST /api/borrowings/ - Create a new borrowing. It automatically validates inventory and creates a Stripe session.

GET /api/borrowings/<id>/ - Retrieve details, including the payment link.

POST /api/borrowings/<id>/return/ - Return a book and update inventory.

Payments
GET /api/payments/ - List all payments.

GET /api/payments/success/ - Callback URL for successful Stripe payments.

🧪 Testing with Stripe
To test the payment flow:

Create a borrowing to get a session_url.

Use the Stripe test card: 4242 4242 4242 4242.

Verify that the payment status changes to PAID.