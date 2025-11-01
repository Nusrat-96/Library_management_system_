document.addEventListener("DOMContentLoaded", function () {
    // Select all password fields
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach(field => {
        // Create wrapper div
        const wrapper = document.createElement('div');
        wrapper.classList.add('password-wrapper');

        // Insert wrapper before field
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        // Create eye icon
        const icon = document.createElement('i');
        icon.classList.add('fa-solid', 'fa-eye', 'toggle-password');
        wrapper.appendChild(icon);

        // Add click event
        icon.addEventListener('click', function () {
            if (field.type === "password") {
                field.type = "text";
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                field.type = "password";
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });
});
