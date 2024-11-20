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
