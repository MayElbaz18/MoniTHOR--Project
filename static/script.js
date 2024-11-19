const logform = document.getElementById('login-form');

logform.addEventListener('submit', function(event) {
    console.log('login-form is submitted!');
    event.preventDefault();

    let UserName = document.getElementById('username').value;
    let Password = document.getElementById('password').value;
    console.log(`username=${UserName}&password=${Password} Login!`);
    Login(UserName, Password)
})

async function Login(UserName, Password) {
    let response = await fetch(`/login?username=${UserName}&password=${Password}`)
    let data = await response.text();
    console.log(data)
    
    if (data.includes("Login Successful")) {
        // Redirect to the dashboard page after successful login
        window.location.href = '/0';
    } else {
        // If login failed, show an error message
        alert('Invalid username or password!');
    }
}
const regform = document.getElementById('register-form');

regform.addEventListener('submit', function(event) {
    console.log('register-form is submitted!');
    event.preventDefault();

    let UserName = document.getElementById('username').value;
    let Password1 = document.getElementById('password1').value;
    let Password2 = document.getElementById('password2').value;
    console.log(`username=${UserName}&password1=${Password1}&password2=${Password2} Register!`);
    Register(UserName, Password1, Password2)
})

async function Register(UserName, Password1, Password2) {
    let response = await fetch(`/register?username=${UserName}&password1=${Password1}&password2=${Password2}`);
    let data = await response.text();
    console.log(data);

    if (data("Registered successfully")) {
        // Redirect to the login page after successful registration
        alert('Registered successfully')
        window.location.href = '/login';
    } else {
        // If registration failed, show the server's error message
        alert(data);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    console.log('JavaScript is loaded.');

    // Function to handle form submissions via AJAX
    function ajaxFormSubmit(form, url) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            const formData = new FormData(form);
            const jsonData = JSON.stringify(Object.fromEntries(formData));
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.message) {
                    alert(data.message);
                }
                // Update the DOM or navigate if necessary
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
