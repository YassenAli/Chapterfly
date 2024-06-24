function changePhoto() {
    const changePhotoBtn = document.getElementById('changePhotoBtn');
    const profileImg = document.getElementById('profileImg');

    changePhotoBtn.addEventListener('click', function() {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';

        fileInput.addEventListener('change', function() {
            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = function(event) {
                profileImg.src = event.target.result;
                // Save the profile picture to local storage
                localStorage.setItem('profilePicture', event.target.result);
            };

            reader.readAsDataURL(file);
        });

        document.body.appendChild(fileInput);
        fileInput.click();
        document.body.removeChild(fileInput);
    });
}

function getPhoto() {
    const savedPhoto = localStorage.getItem('profilePicture');
    if (savedPhoto) {
        const userProfileImg = document.getElementById("profileImg");
        userProfileImg.src = savedPhoto;
    }
}

function getName(){
    // function to get name from log in information
    const username = localStorage.getItem('userName');
    return username;
    //continue
}

document.addEventListener("DOMContentLoaded", function() {
    getPhoto();
    const usernameElement = document.getElementById("username-profile");
    const username = getName();
    if (username) {
        usernameElement.innerText = username;
    } else {
        console.error("Username not found in local storage.");
    }
});

function logout(){
    localStorage.removeItem( "loggedIn" );
    window.location.href='main.html';
}