// Hospital Management System JavaScript

document.addEventListener("DOMContentLoaded", function () {

    // Delete confirmation
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });


    // Phone number validation
    const phoneInputs = document.querySelectorAll(
        'input[name="phone"]'
    );

    phoneInputs.forEach(function (input) {

        input.addEventListener("input", function () {

            this.value = this.value.replace(/[^0-9]/g, "");

            if (this.value.length > 10) {
                this.value = this.value.substring(0, 10);
            }

        });

    });


    // Age validation
    const ageInputs = document.querySelectorAll(
        'input[name="age"]'
    );

    ageInputs.forEach(function (input) {

        input.addEventListener("input", function () {

            if (this.value < 1) {
                this.value = "";
            }

            if (this.value > 120) {
                this.value = 120;
            }

        });

    });

});