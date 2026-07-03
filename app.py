import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from models import db, Product, Order, OrderItem, StoreSettings, Subscriber
from database import init_db

app = Flask(__name__)
app.secret_key = "vastra_handloom_secret_key_2026_xyz"

# SQLite configuration
db_path = os.path.join(app.root_path, 'handloom.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and seed initial data
init_db(app)

@app.context_processor
def inject_settings():
    settings = StoreSettings.query.first()
    if not settings:
        settings = StoreSettings(
            store_name="Vastra Handlooms",
            store_tagline="Authentic Hand-woven Craft",
            primary_color="#A24B31",
            alert_bar_text="FREE SHIPPING ON ORDERS OVER ₹1,999 • SUPPORTING 150+ ARTISAN WEAVERS",
            hero_title="Reviving the Magic of Indian Handlooms",
            hero_subtitle="Preserving Heritage, Thread by Thread",
            hero_description="Explore our premium collection of hand-woven sarees, organic khadi kurtas, lightweight linen shirts, and hand-block printed stoles, direct from the looms of India's master weavers.",
            free_shipping_threshold=1999.00,
            contact_email="support@vastrahandlooms.com",
            contact_phone="+91 98765 43210",
            contact_address="Artisan Loom Center, Varanasi, India"
        )
    return dict(store_settings=settings)

# Helper: Retrieve shopping cart details
def get_cart_data():
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    items = []
    total_amount = 0.0
    total_quantity = 0
    
    # Clean up invalid keys (none-numeric or products deleted from DB)
    keys_to_delete = []
    
    for prod_id_str, qty in list(cart.items()):
        try:
            prod_id = int(prod_id_str)
            product = Product.query.get(prod_id)
            if product is None:
                keys_to_delete.append(prod_id_str)
                continue
            
            # Ensure quantity doesn't exceed stock
            if qty > product.stock:
                qty = product.stock
                cart[prod_id_str] = qty
                session.modified = True
                
            if qty <= 0:
                keys_to_delete.append(prod_id_str)
                continue
                
            item_total = product.price * qty
            total_amount += item_total
            total_quantity += qty
            
            items.append({
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': qty,
                'image_url': product.image_url,
                'material': product.material,
                'weave': product.weave,
                'stock': product.stock
            })
        except ValueError:
            keys_to_delete.append(prod_id_str)
            
    for k in keys_to_delete:
        cart.pop(k, None)
    if keys_to_delete:
        session.modified = True
        
    return {
        'items': items,
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }

# --- STOREFRONT ROUTES ---

@app.route('/')
def index():
    # Fetch featured products
    featured = Product.query.filter_by(featured=True).limit(3).all()
    return render_template('index.html', featured_products=featured)

@app.route('/products')
def products():
    query_str = request.args.get('q', '').strip()
    categories_filter = request.args.getlist('category')
    materials_filter = request.args.getlist('material')
    weaves_filter = request.args.getlist('weave')
    sort_by = request.args.get('sort', 'featured')
    
    # Base query
    q = Product.query
    
    # Filter by search text
    if query_str:
        search_pattern = f"%{query_str}%"
        q = q.filter(
            (Product.name.like(search_pattern)) | 
            (Product.description.like(search_pattern)) |
            (Product.material.like(search_pattern)) |
            (Product.weave.like(search_pattern)) |
            (Product.category.like(search_pattern))
        )
        
    # Filter by checkbox arrays
    if categories_filter:
        q = q.filter(Product.category.in_(categories_filter))
    if materials_filter:
        q = q.filter(Product.material.in_(materials_filter))
    if weaves_filter:
        q = q.filter(Product.weave.in_(weaves_filter))
        
    # Sort
    if sort_by == 'price_low':
        q = q.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        q = q.order_by(Product.price.desc())
    elif sort_by == 'name_asc':
        q = q.order_by(Product.name.asc())
    else: # default/featured first
        q = q.order_by(Product.featured.desc(), Product.id.asc())
        
    product_list = q.all()
    
    # Generate filter lists dynamically from database state
    all_categories = [r[0] for r in db.session.query(Product.category).distinct().all()]
    all_materials = [r[0] for r in db.session.query(Product.material).distinct().all()]
    all_weaves = [r[0] for r in db.session.query(Product.weave).distinct().all()]
    
    active_filters = {
        'category': categories_filter,
        'material': materials_filter,
        'weave': weaves_filter
    }
    
    return render_template(
        'products.html', 
        products=product_list,
        categories=all_categories,
        materials=all_materials,
        weaves=all_weaves,
        active_filters=active_filters,
        active_sort=sort_by,
        query=query_str
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# --- CART API ROUTES ---

@app.route('/cart/json')
def cart_json():
    return jsonify(get_cart_data())

@app.route('/cart')
def view_cart():
    cart_data = get_cart_data()
    return render_template('cart.html', cart_data=cart_data)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    product = Product.query.get_or_404(product_id)
    req_data = request.get_json() or {}
    qty_to_add = int(req_data.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    prod_key = str(product_id)
    current_qty = cart.get(prod_key, 0)
    new_qty = current_qty + qty_to_add
    
    # Restrict to stock limit
    if new_qty > product.stock:
        new_qty = product.stock
        
    cart[prod_key] = new_qty
    session.modified = True
    
    return jsonify(get_cart_data())

@app.route('/cart/update/<int:product_id>', methods=['POST'])
def cart_update(product_id):
    product = Product.query.get_or_404(product_id)
    req_data = request.get_json() or {}
    
    if 'cart' not in session or str(product_id) not in session['cart']:
        return jsonify(get_cart_data()), 400
        
    cart = session['cart']
    prod_key = str(product_id)
    
    if 'change' in req_data:
        delta = int(req_data['change'])
        new_qty = cart[prod_key] + delta
    else:
        new_qty = int(req_data.get('quantity', 1))
        
    # Validation checks
    if new_qty <= 0:
        cart.pop(prod_key, None)
    elif new_qty > product.stock:
        cart[prod_key] = product.stock
    else:
        cart[prod_key] = new_qty
        
    session.modified = True
    return jsonify(get_cart_data())

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def cart_remove(product_id):
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
    return jsonify(get_cart_data())

@app.route('/cart/clear', methods=['POST'])
def cart_clear():
    session['cart'] = {}
    session.modified = True
    return jsonify(get_cart_data())

# --- CHECKOUT & ORDER ROUTES ---

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_data = get_cart_data()
    if cart_data['total_quantity'] == 0:
        flash("Your cart is empty. Please add products before checking out.")
        return redirect(url_for('products'))
        
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        
        # Simple server-side validation
        if not (customer_name and customer_email and customer_phone and shipping_address):
            flash("Please fill in all required shipping fields.")
            return redirect(url_for('checkout'))
            
        # Verify stock check once more before creating order
        for item in cart_data['items']:
            product = Product.query.get(item['product_id'])
            if product.stock < item['quantity']:
                flash(f"Sorry, stock for {product.name} just changed. Only {product.stock} left.")
                return redirect(url_for('view_cart'))
                
        # Create Order database entry
        new_order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            total_amount=cart_data['total_amount'],
            status='Pending'
        )
        db.session.add(new_order)
        db.session.flush() # populates new_order.id
        
        # Create Order Items and deduct inventory stock
        for item in cart_data['items']:
            product = Product.query.get(item['product_id'])
            product.stock -= item['quantity'] # Deduct stock
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        # Clear cart session
        session['cart'] = {}
        session.modified = True
        
        return redirect(url_for('order_success', order_id=new_order.id))
        
    return render_template('checkout.html', cart_data=cart_data)

@app.route('/order-success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)

# --- ADMIN ROUTES ---

@app.route('/admin')
def admin_dashboard():
    # Fetch all orders sorted newest first
    orders = Order.query.order_by(Order.id.desc()).all()
    
    # Calculate metrics
    # Skip cancelled orders in Gross Sales calculations
    sales_orders = Order.query.filter(Order.status != 'Cancelled').all()
    total_sales = sum(o.total_amount for o in sales_orders)
    total_orders = len(orders)
    low_stock = Product.query.filter(Product.stock < 5).count()
    
    avg_order = 0.0
    if len(sales_orders) > 0:
        avg_order = total_sales / len(sales_orders)
        
    metrics = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'low_stock': low_stock,
        'avg_order': avg_order
    }
    
    subscribers = Subscriber.query.order_by(Subscriber.id.desc()).all()
    metrics['subscribers_count'] = len(subscribers)
    
    return render_template('admin/dashboard.html', orders=orders, metrics=metrics, subscribers=subscribers)

@app.route('/admin/order/update/<int:order_id>', methods=['POST'])
def admin_order_update(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f"Order #VH-{10000 + order.id} status successfully updated to {new_status}.")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/products')
def admin_products():
    all_products = Product.query.order_by(Product.id.asc()).all()
    
    # Check if we should populate edit product details
    edit_id = request.args.get('edit_id')
    edit_product = None
    if edit_id:
        try:
            edit_product = Product.query.get(int(edit_id))
        except ValueError:
            pass
            
    return render_template('admin/products.html', products=all_products, edit_product=edit_product)

@app.route('/admin/product/add', methods=['POST'])
def admin_product_add():
    name = request.form.get('name').strip()
    description = request.form.get('description').strip()
    price = float(request.form.get('price', 0.0))
    stock = int(request.form.get('stock', 0))
    category = request.form.get('category')
    material = request.form.get('material')
    weave = request.form.get('weave')
    image_url = request.form.get('image_url')
    featured = 'featured' in request.form
    
    new_prod = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category=category,
        material=material,
        weave=weave,
        image_url=image_url,
        featured=featured
    )
    db.session.add(new_prod)
    db.session.commit()
    
    flash(f"New handloom product '{name}' successfully added to catalog.")
    return redirect(url_for('admin_products'))

@app.route('/admin/product/edit/<int:product_id>', methods=['POST'])
def admin_product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    
    product.name = request.form.get('name').strip()
    product.description = request.form.get('description').strip()
    product.price = float(request.form.get('price', 0.0))
    product.stock = int(request.form.get('stock', 0))
    product.category = request.form.get('category')
    product.material = request.form.get('material')
    product.weave = request.form.get('weave')
    product.image_url = request.form.get('image_url')
    product.featured = 'featured' in request.form
    
    db.session.commit()
    flash(f"Product '{product.name}' details successfully updated.")
    return redirect(url_for('admin_products'))

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def admin_product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    name = product.name
    
    # Delete product
    db.session.delete(product)
    db.session.commit()
    
    flash(f"Product '{name}' successfully removed from inventory catalog.")
    return redirect(url_for('admin_products'))

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    settings = StoreSettings.query.first()
    if request.method == 'POST':
        if not settings:
            settings = StoreSettings()
            db.session.add(settings)
            
        settings.store_name = request.form.get('store_name').strip()
        settings.store_tagline = request.form.get('store_tagline').strip()
        settings.primary_color = request.form.get('primary_color').strip()
        settings.alert_bar_text = request.form.get('alert_bar_text').strip()
        settings.hero_title = request.form.get('hero_title').strip()
        settings.hero_subtitle = request.form.get('hero_subtitle').strip()
        settings.hero_description = request.form.get('hero_description').strip()
        settings.free_shipping_threshold = float(request.form.get('free_shipping_threshold', 1999.00))
        settings.contact_email = request.form.get('contact_email').strip()
        settings.contact_phone = request.form.get('contact_phone').strip()
        settings.contact_address = request.form.get('contact_address').strip()
        
        db.session.commit()
        flash("Brand settings successfully updated!")
        return redirect(url_for('admin_settings'))
        
    return render_template('admin/settings.html', settings=settings)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = None
    if request.is_json:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
    else:
        email = request.form.get('email', '').strip()
        
    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400
        
    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({'success': True, 'message': 'You are already subscribed!'})
        
    try:
        new_subscriber = Subscriber(email=email)
        db.session.add(new_subscriber)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Thank you for subscribing to our artisan newsletter!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
