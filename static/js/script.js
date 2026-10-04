document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide alerts
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);

    });


    // Form validation
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const password = form.querySelector(
                'input[name="password"]'
            );

            if (password && password.value.length < 6) {
                alert("Password must contain at least 6 characters.");
                event.preventDefault();
            }

        });

    });

});