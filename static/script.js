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

    // Apply AJAX form submission for login and register forms
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        ajaxFormSubmit(loginForm, '/login');
    }

    if (registerForm) {
        ajaxFormSubmit(registerForm, '/register');
    }
});
