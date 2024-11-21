document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript is loaded.');

    // Login form submission
    const logform = document.getElementById('login-form');
    if (logform) {
        logform.addEventListener('submit', async function (event) {
            console.log('login-form is submitted!');
            event.preventDefault();

            const UserName = document.getElementById('username').value;
            const Password = document.getElementById('password').value;
            console.log(`username=${UserName}&password=${Password} Login!`);

            try {
                const response = await fetch(`/login?username=${UserName}&password=${Password}`);
                const data = await response.text();
                console.log(data);

                if (data.includes("Login Successful")) {
                    alert("Logged In Successfully");
                    window.location.href = '/dashboard'; // Redirect after successful login
                } else {
                    alert('Invalid username or password!');
                }
            } catch (error) {
                console.error('Error during login:', error);
            }
        });
    } else {
        console.warn('Login form not found.');
    }

    // Single-monitor form submission
    const monitorForm = document.getElementById('single-monitor-form');
    if (monitorForm) {
        monitorForm.addEventListener('submit', async function (event) {
            console.log('single-monitor-form is submitted!');
            event.preventDefault();

            const domainInput = document.getElementById('single').value.trim();
            const errorMessage = document.getElementById('error-message');
            console.log(domainInput);

            const domainRegex = /^(?!:\/\/)([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$/;

            if (!domainRegex.test(domainInput)) {
                errorMessage.style.display = "block"; // Display error as block
                errorMessage.textContent = "Please enter a valid domain name.";
            } else {
                errorMessage.style.display = "none"; // Hide the error message
                try {
                    const response = await fetch(`/add_domain/${domainInput}`);
                    const data = await response.text();
                    console.log(data);
                    alert('Domain is monitored');
                    location.reload();
                } catch (error) {
                    console.error('Error adding domain:', error);
                }
            }
        });
    } else {
        console.warn('Single-monitor form not found.');
    }


    // Bulk-monitor form submission
    const bulkForm = document.getElementById('bulk-monitor-form');
    if (bulkForm) {
        bulkForm.addEventListener('submit', async function (event) {
            console.log('bulk-monitor-form is submitted!');
            event.preventDefault();

            const bulkFileInput = document.getElementById('bulk').value.trim();
            const errorMessage = document.getElementById('error-message');
            console.log(bulkFileInput);            
            let fileName =bulkFileInput.replaceAll("/","%5C")
            fileName = fileName.replaceAll("\\","%5C")
            console.log(fileName);            

            try {
                    const response = await fetch(`bulk_upload/${fileName}`);
                    const data = await response.text();
                    console.log(data);
                    alert('Bulk upload');
                    location.reload();
                } catch (error) {
                    console.error('Error adding domain:', error);
                }
            }
        );
    }else {
        console.warn('Bulk-monitor form not found.');
    }
});
