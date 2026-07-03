// Vastra Handlooms - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initial UI setups
    setupCartDrawer();
    setupCreditCardInteraction();
    setupFilters();
});

// Toast message helper
function showToast(message, type = 'success') {
    // Remove existing toasts if any
    const existing = document.querySelector('.toast-container');
    let container = existing;
    if (!existing) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Add check icon or warning icon
    const icon = type === 'success' ? 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>` :
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
        
    toast.innerHTML = `${icon} <span>${message}</span>`;
    container.appendChild(toast);
    
    // Automatically remove after 3s
    setTimeout(() => {
        toast.remove();
        if (container.children.length === 0) {
            container.remove();
        }
    }, 3000);
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toLocaleString('en-IN', {
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    });
}

// Cart Drawer management
function setupCartDrawer() {
    const cartBtn = document.getElementById('cart-toggle');
    const closeBtn = document.getElementById('cart-close');
    const overlay = document.getElementById('cart-overlay');
    const drawer = document.getElementById('cart-drawer');
    
    if (!drawer) return; // Not on page if admin/etc.
    
    if (cartBtn) {
        cartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openCartDrawer();
        });
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeCartDrawer);
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeCartDrawer);
    }
}

function openCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-overlay');
    if (drawer && overlay) {
        drawer.classList.add('active');
        overlay.classList.add('active');
        fetchCartJSON(); // Refresh content when opening
    }
}

function closeCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    const overlay = document.getElementById('cart-overlay');
    if (drawer && overlay) {
        drawer.classList.remove('active');
        overlay.classList.remove('active');
    }
}

// Fetch Cart items and build HTML dynamically
function fetchCartJSON() {
    fetch('/cart/json')
        .then(response => response.json())
        .then(data => {
            updateCartUI(data);
        })
        .catch(err => console.error("Error fetching cart data:", err));
}

function updateCartUI(data) {
    // Update badge count
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(badge => {
        badge.textContent = data.total_quantity;
        badge.style.display = data.total_quantity > 0 ? 'flex' : 'none';
    });
    
    // Update Cart Drawer Items List
    const itemsList = document.querySelector('.cart-items-list');
    if (!itemsList) return;
    
    if (data.total_quantity === 0) {
        itemsList.innerHTML = `
            <div class="cart-empty-msg">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
                <p>Your shopping cart is empty.</p>
                <a href="/products" class="btn btn-outline" style="margin-top: 1rem;">Browse Products</a>
            </div>
        `;
        document.querySelector('.cart-summary-total').textContent = formatCurrency(0);
        const checkoutBtn = document.getElementById('drawer-checkout-btn');
        if (checkoutBtn) checkoutBtn.style.display = 'none';
    } else {
        let html = '';
        data.items.forEach(item => {
            html += `
                <div class="cart-item" data-id="${item.product_id}">
                    <img src="${item.image_url}" alt="${item.name}" class="cart-item-img">
                    <div class="cart-item-info">
                        <h4 class="cart-item-title">${item.name}</h4>
                        <div class="cart-item-meta">${item.material} / ${item.weave}</div>
                        <div class="cart-item-price">${formatCurrency(item.price)}</div>
                        <div class="qty-control">
                            <button type="button" class="qty-btn minus" onclick="changeQty(${item.product_id}, -1)">−</button>
                            <input type="text" class="qty-input" value="${item.quantity}" readonly>
                            <button type="button" class="qty-btn plus" onclick="changeQty(${item.product_id}, 1)">+</button>
                        </div>
                    </div>
                    <button class="cart-item-remove" onclick="removeCartItem(${item.product_id})" title="Remove item">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                </div>
            `;
        });
        itemsList.innerHTML = html;
        document.querySelector('.cart-summary-total').textContent = formatCurrency(data.total_amount);
        const checkoutBtn = document.getElementById('drawer-checkout-btn');
        if (checkoutBtn) checkoutBtn.style.display = 'block';
    }
    
    // Also if on CART Page, refresh page tables
    updateCartPageUI(data);
}

// Actions from drawer or catalog
function addToCart(productId, quantity = 1) {
    fetch(`/cart/add/${productId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(res => res.json())
    .then(data => {
        updateCartUI(data);
        showToast("Product added to your cart!");
        openCartDrawer();
    })
    .catch(err => {
        console.error(err);
        showToast("Could not add product.", "error");
    });
}

function changeQty(productId, amount) {
    fetch(`/cart/update/${productId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ change: amount })
    })
    .then(res => res.json())
    .then(data => {
        updateCartUI(data);
    })
    .catch(err => console.error(err));
}

function removeCartItem(productId) {
    fetch(`/cart/remove/${productId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        updateCartUI(data);
        showToast("Product removed from cart.");
    })
    .catch(err => console.error(err));
}

// CART Page Specific script
function updateCartPageUI(data) {
    // Check if we are on the main cart page
    const cartTable = document.querySelector('.cart-table tbody');
    if (!cartTable) return;
    
    if (data.total_quantity === 0) {
        // Reload page to show empty cart state
        window.location.reload();
        return;
    }
    
    // Update main table
    let rows = '';
    data.items.forEach(item => {
        rows += `
            <tr data-id="${item.product_id}">
                <td>
                    <div class="cart-product-cell">
                        <img src="${item.image_url}" alt="${item.name}">
                        <div>
                            <h4 class="cart-product-title">${item.name}</h4>
                            <p class="cart-product-meta">${item.material} • ${item.weave}</p>
                        </div>
                    </div>
                </td>
                <td>${formatCurrency(item.price)}</td>
                <td>
                    <div class="qty-control">
                        <button type="button" class="qty-btn" onclick="changeQty(${item.product_id}, -1)">−</button>
                        <input type="text" class="qty-input" value="${item.quantity}" readonly>
                        <button type="button" class="qty-btn" onclick="changeQty(${item.product_id}, 1)">+</button>
                    </div>
                </td>
                <td class="cart-item-total" style="font-weight: 700;">
                    ${formatCurrency(item.price * item.quantity)}
                </td>
                <td>
                    <button class="cart-item-remove" style="position:static;" onclick="removeCartItem(${item.product_id})" title="Remove item">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    </button>
                </td>
            </tr>
        `;
    });
    cartTable.innerHTML = rows;
    
    // Update summary card
    const subtotalEl = document.getElementById('summary-subtotal');
    const totalEl = document.getElementById('summary-total');
    if (subtotalEl) subtotalEl.textContent = formatCurrency(data.total_amount);
    if (totalEl) totalEl.textContent = formatCurrency(data.total_amount);
}

// 3D Credit Card interactions during checkout
function setupCreditCardInteraction() {
    const cardNumInput = document.getElementById('card-number');
    const cardHolderInput = document.getElementById('card-name');
    const cardExpiryInput = document.getElementById('card-expiry');
    const cardCvvInput = document.getElementById('card-cvv');
    const cardWrapper = document.querySelector('.credit-card-mockup');
    
    if (!cardNumInput) return; // Not on checkout page
    
    // Card Number Input formatting and mirroring
    cardNumInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        let formattedValue = '';
        for (let i = 0; i < value.length; i++) {
            if (i > 0 && i % 4 === 0) formattedValue += ' ';
            formattedValue += value[i];
        }
        e.target.value = formattedValue.slice(0, 19); // Max length 16 digits + 3 spaces
        
        // Mirror to card front
        let cardDisplay = formattedValue;
        while (cardDisplay.length < 19) {
            let idx = cardDisplay.length;
            if (idx === 4 || idx === 9 || idx === 14) cardDisplay += ' ';
            else cardDisplay += '•';
        }
        document.querySelector('.card-number-display').textContent = cardDisplay;
    });
    
    // Card Holder Input mirror
    cardHolderInput.addEventListener('input', function(e) {
        const value = e.target.value;
        document.querySelector('.card-holder-display').textContent = value ? value.toUpperCase() : 'Card Holder Name';
    });
    
    // Expiry Input formatting and mirroring
    cardExpiryInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        if (value.length > 2) {
            value = value.slice(0,2) + '/' + value.slice(2,4);
        }
        e.target.value = value.slice(0, 5); // MM/YY
        
        let display = value;
        if (display.length === 0) display = 'MM/YY';
        else if (display.length === 1) display = display + 'M/YY';
        else if (display.length === 2) display = display + '/YY';
        document.querySelector('.card-expiry-display').textContent = display;
    });
    
    // Flip card to CVV back on CVV input focus
    cardCvvInput.addEventListener('focus', function() {
        cardWrapper.classList.add('flipped');
    });
    
    cardCvvInput.addEventListener('blur', function() {
        cardWrapper.classList.remove('flipped');
    });
    
    cardCvvInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        e.target.value = value.slice(0, 4); // Max 3 or 4 digits
        document.querySelector('.card-cvv-stripe').textContent = value;
    });
}

// Catalog filter handler
function setupFilters() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;
    
    const checkboxes = filterForm.querySelectorAll('input[type="checkbox"]');
    const sortSelect = document.getElementById('sort-by');
    
    // Trigger submit on filter / sort change
    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => filterForm.submit());
    });
    
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            // Append sort parameters to search and submit form
            const sortVal = sortSelect.value;
            const sortInput = document.createElement('input');
            sortInput.type = 'hidden';
            sortInput.name = 'sort';
            sortInput.value = sortVal;
            filterForm.appendChild(sortInput);
            filterForm.submit();
        });
    }
}
