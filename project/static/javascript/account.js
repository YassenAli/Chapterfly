// Function to get CSRF token
function getCSRFToken() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return csrfToken;
}

// Function to handle profile photo upload
function updateProfilePhoto() {
    const form = document.getElementById('profilePhotoForm');
    const formData = new FormData(form);
    const csrfToken = getCSRFToken();

    fetch('/update_profile_photo_ajax/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.profile_picture_url) {
            const profileImg = document.getElementById('profileImg');
            profileImg.src = data.profile_picture_url;
        } else {
            console.error('Profile picture URL not found in response.');
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    const profilePhotoForm = document.getElementById('profilePhotoForm');

    profilePhotoForm.addEventListener('submit', function(event) {
        event.preventDefault();

        updateProfilePhoto();
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to retrieve borrowed books
function getBorrowedBooks() {
    const borrowedBooksJSON = localStorage.getItem('BorrowedBooks');

    let borrowedBooks = [];
    if (borrowedBooksJSON) {
        try {
            borrowedBooks = JSON.parse(borrowedBooksJSON);
        } catch (error) {
            console.error('Error parsing borrowed books:', error);
        }
    }

    return borrowedBooks;
}

// Function to display borrowed books
function displayBorrowedBooks(books) {
    const borrowedBooksList = document.getElementById('borrowed-books-list');

    borrowedBooksList.innerHTML = '';

    if (books.length === 0) {
        borrowedBooksList.innerHTML = '<p class="empty">You have no borrowed books.</p>';
        return;
    }

    books.forEach(book => {
        const bookItem = document.createElement('div');
        bookItem.className = 'borrowed-book-item';
        bookItem.innerHTML = `
            <h3>${book.name}</h3>
            <p> <strong>Quantity: </strong>${book.quantity}</p>
            `;

        borrowedBooksList.appendChild(bookItem);
    });
}

// Function to get username
function getName(){
    const username = localStorage.getItem('userName');
    return username;
}

// Function to handle logout
function logout(){
    localStorage.removeItem( "loggedIn" );
    window.location.href='main.html';
}

// Get borrowed books and display them
const borrowedBooks = getBorrowedBooks();
displayBorrowedBooks(borrowedBooks);

// Set username
document.addEventListener("DOMContentLoaded", function() {
    const usernameElement = document.getElementById("username-profile");
    const username = getName();
    if (username) {
        usernameElement.innerText = username;
    } else {
        console.error("Username not found in local storage.");
    }
});

// Logout button click event
const logoutButton = document.getElementById("log-out");
logoutButton.addEventListener('click', logout);
