# Vastra Handloom

An elegant, fully-featured Flask E-commerce platform designed to showcase and sell authentic traditional Indian handloom products (such as Sarees, Kurtas, Shirts, and Stoles). The project is built using a modern, lightweight Python stack with Flask and SQLite, backed by a beautifully crafted, responsive, and dynamic UI powered by Vanilla CSS and JavaScript.

---

## 🌟 Features

- **Product Catalog & Details**: Browse products categorized by category, material (Cotton, Silk, Linen, Khadi), and weave type (Ikat, Banarasi, Jamdani, Handloom-Plain).
- **Advanced Filtering & Search**: Instant, dynamic filter and sort options (by price, name, and featured status) paired with keyword search to easily locate products.
- **Interactive Shopping Cart**: Custom session-based shopping cart allowing users to add, update quantities (with automatic stock validation), and remove items in real-time.
- **Secure Checkout System**: Complete checkout flow collecting customer shipping and contact details, and storing orders and order items in a structured database.
- **Interactive, Premium UI**: Custom responsive layout with clean aesthetics, micro-animations, hover effects, and a seamless checkout experience.
- **Database Initializer**: Automatic SQLite database seeding with rich, mock handloom product data on startup.

---

## 🛠️ Technology Stack

- **Backend**: Python, [Flask](https://flask.palletsprojects.com/)
- **Database / ORM**: SQLite, [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- **Frontend**: Semantic HTML5, Custom Vanilla CSS (Responsive Flexbox/Grid layouts), Custom Vanilla JavaScript
- **Sessions**: Flask Session management for shopping cart persistence

---

## 📁 Project Structure

```text
Handloom_Project/
│
├── app.py                # Main Flask application (Routes, Controllers, Cart logic)
├── database.py           # Database initializer & mock data seeder
├── models.py             # SQLAlchemy schemas (Product, Order, OrderItem models)
├── requirements.txt      # Python dependencies
├── .gitignore            # Git exclusion rules
│
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Premium custom stylesheet
│   ├── js/
│   │   └── main.js       # Cart interactions, filters, and UI animations
│   └── images/           # Product and layout images
│
└── templates/            # HTML templates
    ├── base.html         # Base layout with navigation and footer
    ├── index.html        # Home / landing page with featured items
    ├── products.html     # Product listing with filters and search
    ├── product_detail.html# Detailed view of a single product
    ├── cart.html         # Shopping cart review
    ├── checkout.html     # Checkout details form
    ├── order_success.html# Post-checkout confirmation
    └── orders.html       # Admin / order list view (optional tracking)
```

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally on your machine.

### Prerequisites

Make sure you have **Python 3.8+** installed on your system.

### Installation

1. **Clone the Repository** (or download the source code):
   ```bash
   git clone <your-repository-url>
   cd Handloom_Project
   ```

2. **Create and Activate a Virtual Environment**:
   *On macOS/Linux:*
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   *On Windows:*
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Website**:
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000/
   ```

The application will automatically initialize the database `handloom.db` and seed it with starter handloom products on its first run!

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
