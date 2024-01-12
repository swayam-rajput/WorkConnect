
function validateRegistration() {
    resetErrors();
    // alert('func called')
    var username = document.getElementById('username');
    var email = document.getElementById('email');
    var phno = document.getElementById('phno');
    var age = document.getElementById('age');
    var password = document.getElementById('password');
    var cpassword = document.getElementById('cpassword');

    var borderbottom = '2px red solid';
    if (!username.value.match(/^\w+$/)) {
        username.style.borderBottom = borderbottom;

    }

    if (!isValidEmail(email.value)) {
        email.style.borderBottom = borderbottom;

    }

    if (!phno.value.match(/^\d{10}$/)) {
        phno.style.borderBottom = borderbottom;
    }

    if (age.value == '' ||  (age.value < 0)) {
        age.style.borderBottom = borderbottom;

    }

    if (!password.value.match(/[\w]{1,32}/)) {
        password.style.borderBottom = borderbottom;
        return false;
    }

    if (password.value !== cpassword.value) {
        cpassword.style.borderBottom = borderbottom;

    }

    return true;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function resetErrors() {
    var errorElements = document.querySelectorAll('input');
    errorElements.forEach(function (element) {
        element.style.borderBottom = 'initial';
    });
}