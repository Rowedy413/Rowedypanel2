// Simple form validation before submit example (adjust for your form structure)
const form = document.querySelector('form');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const name = form.querySelector('input[placeholder="ABHISHEK SAHU"]').value.trim();
    const email = form.querySelector('input[placeholder="abhisheksahu2200@gmail.com"]').value.trim();
    const phone = form.querySelector('input[placeholder="+919204866795"]').value.trim();
    const subject = form.querySelector('input[placeholder="Email Subject"]').value.trim();
    const message = form.querySelector('textarea[placeholder="Your Message"]').value.trim();

    if (!name || !email || !phone || !subject || !message) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please fill in all the fields!',
        });
        return;
    }

    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Email',
            text: 'Please enter a valid email address!',
        });
        return;
    }

    Swal.fire({
        icon: 'success',
        title: 'Message Sent',
        text: 'Thank you for contacting me!',
    });

    form.reset(); // Clear form after success
});
      
