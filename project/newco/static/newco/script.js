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

function enableInputs(str,bool) {
    var elements = document.getElementsByClassName('en');

    console.log(elements);
    for (var i = 0; i < elements.length; i++) {
        if(bool){
            elements[i].removeAttribute('disabled');
            elements[i].style.borderBottom = '2px #858786 solid'
            document.getElementById('edit-div').hidden=true;
            if(document.getElementById('del-btn')){
                document.getElementById('del-btn').hidden=true;
            }
            document.getElementById('save-div').removeAttribute('hidden');
            document.getElementById('cncl-btn').removeAttribute('hidden');
        }else{
            elements[i].disabled = true;
            elements[i].style.borderBottom = 'initial'
            document.getElementById('edit-div').hidden=bool;
            if(document.getElementById('del-btn')){
                document.getElementById('del-btn').hidden=false;
            }
            document.getElementById('save-div').hidden=true;
            document.getElementById('cncl-btn').hidden=true;
            
        }
    }    
}

document.addEventListener('DOMContentLoaded', function() {
    
    const classname = "navbar-item-focus"; 
    var navbarItems = document.querySelectorAll('.navbar-item');
    function setActiveNavItem() {
        var currentUrl = window.location.href;

        navbarItems.forEach(function(item) {
            var targetUrl = item.getAttribute('href');

            if (currentUrl.includes(targetUrl)) {
                navbarItems.forEach(function(navItem) {
                    navItem.classList.remove(classname);
                });
                item.classList.add(classname);
            }
        });
    }
    setActiveNavItem();
    navbarItems.forEach(function(item) {
        item.addEventListener('click', function() {
            navbarItems.forEach(function(navItem) {
                navItem.classList.remove(classname);
            });
            item.classList.add(classname);
        });
    });
});

function openFileInput() {
    var fileInput = document.getElementById("pfp");
    if (fileInput) {
      fileInput.click();
    }
}

if (!window.location.pathname.endsWith('/update_aadhar')){
    document.getElementById('pfpimg').addEventListener('mouseleave', function() {
        document.querySelector('#icon').style.opacity = 0;
    });
    document.getElementById('pfpimg').addEventListener('mouseenter', function() {
        document.querySelector('#icon').style.opacity = 0.8;
    });
    
    console.log(!window.location.pathname.endsWith('/update_aadhar'))
}

function handleFileInputChange(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    // Check if a file was selected
    if (file) {
        // Get the file name and display it
        const fileName = file.name;
        console.log("Selected file:", fileName);

        // Optional: You can display the selected image preview
        const reader = new FileReader();
        reader.onload = function(event) {
            const imageUrl = event.target.result;
            // Display the image preview
            const imgPreview = document.getElementById('pfpimg');
            imgPreview.src = imageUrl;
        };
        reader.readAsDataURL(file);

           // Optional: You can enable the save button or perform other actions
        // const saveButton = document.getElementById('save-div');
        // saveButton.hidden = false;
        const pfpanchor = document.getElementById('pfp-a')
        pfpanchor.click()
    }
}

function validateAadhar(e) {
    
    var text = document.getElementById('aadharNumber').value;
    var file = document.getElementById('aadharPhoto').value; // This will get the file name, not its length
    var pdfpsd = document.getElementById('pdf_psd').value; // This will get the file name, not its length
    
    console.log(document.getElementById('aadharNumber').value);
    console.log(document.getElementById('aadharPhoto').value); // This will get the file name, not its length
    console.log(document.getElementById('pdf_psd').value); // This will get the file name, not its length

    
    if (text.length === 12 && file && pdfpsd.length === 8) { // Checking if Aadhar number is 12 digits and file is selected
        document.getElementById('subbtn').click();
        console.log('submitted')
        return    
    } else {
        e.preventDefault()
        alert("Please enter a valid 12-digit Aadhar number and select a PDF file.\nDownload pdf file from UIDAI and upload it with its password");
    }
    
    console.log('not working')
}