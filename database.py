from models import db, Product, StoreSettings

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_data()

def seed_data():
    # Seed default store settings if empty
    if StoreSettings.query.first() is None:
        default_settings = StoreSettings(
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
            contact_address="Artisan Loom Center, Sector 4, Varanasi, Uttar Pradesh - 221001"
        )
        db.session.add(default_settings)
        db.session.commit()
        print("Database seeded with default brand configuration settings!")

    # Check if products already exist
    if Product.query.first() is not None:
        return
        
    products = [
        Product(
            name="Royal Indigo Silk Ikat Saree",
            description="This exquisite royal blue and white saree is hand-woven by master artisans using the heritage Ikat technique. Made from pure mulberry silk, it features delicate geometric motifs and a matching solid silk blouse piece. A perfect blend of heritage craft and modern luxury.",
            price=6499.00,
            image_url="/static/images/ikat_saree.jpg",
            category="Saree",
            material="Silk",
            weave="Ikat",
            stock=5,
            featured=True
        ),
        Product(
            name="Heritage Mustard Khadi Kurta",
            description="Spun from 100% organic cotton, this textured mustard yellow Khadi kurta represents Indian heritage craft at its best. It offers maximum comfort, breathable fabric, and is dyed using natural vegetable dyes. Complete with coconut shell buttons and a classic mandarin collar.",
            price=1899.00,
            image_url="/static/images/khadi_kurta.jpg",
            category="Kurta",
            material="Khadi",
            weave="Handloom-Plain",
            stock=15,
            featured=True
        ),
        Product(
            name="Earthy Olive Linen Shirt",
            description="Woven from premium organic flax, this olive green casual linen shirt features a relaxed silhouette and a textured hand-woven finish. Highly breathable and lightweight, it feels softer with every wash. Designed for effortless, sustainable everyday style.",
            price=2499.00,
            image_url="/static/images/linen_shirt.jpg",
            category="Shirt",
            material="Linen",
            weave="Handloom-Plain",
            stock=10,
            featured=True
        ),
        Product(
            name="Imperial Magenta Banarasi Saree",
            description="A masterpiece of heritage weave, this luxury magenta pink Banarasi saree features opulent golden zari borders and intricate floral buttis. Hand-woven over three weeks in Varanasi, this pure silk saree exudes royal elegance, making it ideal for weddings and grand festivities.",
            price=12999.00,
            image_url="/static/images/banarasi_saree.jpg",
            category="Saree",
            material="Silk",
            weave="Banarasi",
            stock=3,
            featured=True
        ),
        Product(
            name="Dabu Indigo Block-Printed Stole",
            description="This premium handloom cotton stole showcases beautiful white block prints on a rich indigo blue base. Hand-dyed using natural indigo, it is finished with delicate hand-knotted tassels. A versatile accessory to elevate any ethnic or western ensemble.",
            price=999.00,
            image_url="/static/images/indigo_stole.jpg",
            category="Stole",
            material="Cotton",
            weave="Handloom-Plain",
            stock=25,
            featured=True
        )
    ]
    
    for p in products:
        db.session.add(p)
    
    db.session.commit()
    print("Database successfully seeded with handloom products!")
