function emailvaluate(){
    var text = document.getElementById('username').value
    document.getElementById('email').value = `${text}@gmail.com`
    console.log('called')
}
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

function validateJobForm() {
    // Get form inputs
    var title = document.getElementById('job-title').value.trim();
    var description = document.getElementById('job-description').value.trim();
    var jobType = document.getElementById('job-type').value.trim();
    var salary = document.getElementById('salary').value.trim();
    var location = document.getElementById('location').value.trim();
    var borderbottom = '2px red solid';
    // Validate each field
    if (title === '') {
        document.getElementById('job-title').style.borderBottom = borderbottom;
        return false;
    }

    if (description === '') {
        document.getElementById('job-description').style.borderBottom = borderbottom;
        return false;
    }

    if (jobType === '') {
        document.getElementById('job-type').style.borderBottom = borderbottom;
        return false;
    }

    if (salary === '') {
        document.getElementById('salary').style.borderBottom = borderbottom;
        return false;
    }

    if (location === '') {
        document.getElementById('location').style.borderBottom = borderbottom;
        return false;
    }
    return true;
}

function enableInputs(str) {
    var elements = document.getElementsByClassName('en');
    for (var i = 0; i < elements.length; i++) {
        elements[i].removeAttribute('disabled');
        elements[i].style.borderBottom = '2px #858786 solid'
    }
    console.log(str)
    button = document.getElementById('edit-btn');
    button.textContent = 'Save';
    button.onclick= ()=>{
        window.location.href=str;
    }
    
}