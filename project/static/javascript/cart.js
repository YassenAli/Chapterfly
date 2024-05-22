function addToCart(id, name, price, img, category) {
    alert(name+' has been added to the cart');
    let existingBook = false;
    const prefix = 'cart_cont';
    let cart = [];

    // Check if the cart already exists in localStorage
    if (localStorage.getItem(prefix)) {
        cart = JSON.parse(localStorage.getItem(prefix));
    }

    // Check if the book is already in the cart
    existingBook = cart.find(book => book.id == id);

    if (existingBook) {
        existingBook.quantity++;
    } else {
        // If the book is not in the cart, add it with a quantity of 1
        let book = {id, name, price, img, category, quantity: 1};
        cart.push(book);
    }
    localStorage.setItem(prefix, JSON.stringify(cart));
}

function updateCart() {
    let cartDisplay = document.getElementById('cart_cont');

    // Get the cart data from localStorage
    let cart = JSON.parse(localStorage.getItem('cart_cont'));

    // Clear the current cart display
    cartDisplay.innerHTML = '';

    if (cart.length === 0) {
        cartDisplay.innerHTML = "<p class='empty'>Your books cart is empty!</p>";
    }

    let totalPrice = 0;
    let counter = 0;

    // Add each book in the cart to the display
    //for (let i = 0; i < cart.length; i++){
    cart.forEach( book => {
        let div = document.createElement('div');
        div.className = 'cart_item row mb-4 d-flex justify-content-between align-items-center';
        div.id = 'cart_item' + book.id;

        // Create a new button element for deleting the book
        let del = document.createElement('div');
        del.className = 'col-md-1 col-lg-1 col-xl-1 text-end';
        let button = document.createElement('button');
        button.innerHTML = `<i class="fas fa-times"></i>`;
        button.onclick = function() {
            // Find the index of the book to remove based on its ID
            const removeIndex = cart.findIndex(item => item.id === book.id);
      
            // Check if the book is found (index !== -1)
            if (removeIndex !== -1) {
              // Remove the book from the cart using splice with the found index
              cart.splice(removeIndex, 1);
              localStorage.setItem('cart_cont', JSON.stringify(cart));
              updateCart();
            } else {
              console.warn("Book with ID", book.id, "not found in cart for removal.");
            }
          };

        del.appendChild(button);
        //Buttons
        //Div of buttons
        let divButtons = document.createElement('div');
        divButtons.setAttribute('class', 'col-md-3 col-lg-3 col-xl-2 d-flex');
        //Minus Button
        let minusBtn = document.createElement('button');
        minusBtn.setAttribute('data-mdb-button-init', '');
        minusBtn.setAttribute('data-mdb-ripple-init', '');
        minusBtn.setAttribute('class', 'btn btn-link px-2');
        var minusIcon = document.createElement('i');
        minusIcon.setAttribute('class', 'fas fa-minus');
        minusBtn.appendChild(minusIcon);
        minusBtn.onclick = function() {
            // let book = cart.find(book => book.id == cart[i].id);
            book.quantity--;
            // console.log(book.quantity);
            if (book.quantity == 0) {
                const removeIndex = cart.findIndex(item => item.id === book.id);
                // Remove the book from the cart using splice with the found index
                cart.splice(removeIndex, 1);
            }
            // document.getElementById('quantity' + cart[i].id).value = book.quantity;
            document.getElementById('quantity' + book.id).textContent = book.quantity;
            localStorage.setItem('cart_cont', JSON.stringify(cart));
            updateCart();
        }
        //Plus Button
        let plusBtn = document.createElement('button');
        plusBtn.setAttribute('data-mdb-button-init', '');
        plusBtn.setAttribute('data-mdb-ripple-init', '');
        plusBtn.setAttribute('class', 'btn btn-link px-2');
        var plusIcon = document.createElement('i');
        plusIcon.setAttribute('class', 'fas fa-plus');
        plusBtn.appendChild(plusIcon);
        plusBtn.onclick = function() {
            // let book = cart.find(book => book.id == cart[i].id);

            book.quantity++;
            // console.log(book.quantity);

            document.getElementById('quantity' + book.id).textContent = book.quantity;
            
            localStorage.setItem('cart_cont', JSON.stringify(cart));
            updateCart();
        }
        //quantity control
        // let quntyInput = document.createElement('input');
        // quntyInput.setAttribute('id', 'quantity' + cart[i].id);
        // quntyInput.setAttribute('minlength', '1');
        // quntyInput.setAttribute('name', 'quantity');
        // quntyInput.setAttribute('value', '1');
        // quntyInput.setAttribute('type', 'text');
        // quntyInput.setAttribute('class', 'form-control form-control-sm');
        // quntyInput.setAttribute('placeholder', 'quantity');
        let quntyDiv = document.createElement('div');
        quntyDiv.setAttribute('id', 'quantity'+book.id);
        quntyDiv.setAttribute('name', 'quantity');
        quntyDiv.setAttribute('class', 'form-control form-control-sm');
        quntyDiv.textContent = book.quantity;
        
        divButtons.appendChild(minusBtn);
        divButtons.appendChild(quntyDiv);
        divButtons.appendChild(plusBtn);
        
        //div of price of book
        let divPrice = document.createElement('div');
        divPrice.setAttribute('class', 'col-md-3 col-lg-2 col-xl-2 offset-lg-1');
        let h6 = document.createElement('h6');
        h6.setAttribute('class', 'mb-0');
        h6.textContent = '$ ' + book.price;
        divPrice.appendChild(h6);
        // <!-- onclick="this.parentNode.querySelector('input[type=number]').stepDown()"-->
        // <!--  onclick="this.parentNode.querySelector('input[type=number]').stepUp()" -->
        div.innerHTML = `
        <div class="col-md-2 col-lg-2 col-xl-2">
            <img src="${book.img}" class="img-fluid rounded-3 cart_img" alt="${book.name}" style="width: 65px">
        </div>
        <div class="col-md-3 col-lg-3 col-xl-3">
            <h6 class="text-muted cart_category">${book.category}</h6>
            <h6 class="text-black mb-0 cart_name">${book.name}</h6>
        </div>`;

        div.appendChild(divButtons);
        div.appendChild(divPrice);
        div.appendChild(del);
        cartDisplay.appendChild(div);

        totalPrice += book.price * book.quantity;

        if(counter != cart.length-1){
            let hr = document.createElement('hr');
            hr.className = 'my-4';
            cartDisplay.appendChild(hr);
        }
        counter++;
    });

    // Display the total number of items and total price
    let totalItems = document.getElementById('cart_number');
    var totalQuantity = 0;
    cart.forEach(item => {
        totalQuantity += item.quantity;
    });
    totalItems.textContent = totalQuantity;
    let DisplaytotalPrice = document.getElementById('cart_price');
    DisplaytotalPrice.textContent = totalPrice + ' LE';
    let DisplayPrice = document.getElementById('checkout_price');
    DisplayPrice.textContent = totalPrice + ' LE';
}

function checkout() {
    let cart = JSON.parse(localStorage.getItem('cart_cont'));
    localStorage.setItem('BorrowedBooks', JSON.stringify(cart));

    cart = []; // Clear the cart
    localStorage.setItem('cart_cont', JSON.stringify(cart));

    updateCart();
    
    alert('Thank you for shopping! Your order has been placed.');
}
