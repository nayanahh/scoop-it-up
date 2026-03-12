// Simple confirmation for logout
function confirmLogout() {
    return confirm("Are you sure you want to logout?");
}

// Increase / Decrease quantity (future use)
function increaseQty(inputId) {
    let input = document.getElementById(inputId);
    input.value = parseInt(input.value) + 1;
    input.form.submit();
}

function decreaseQty(inputId) {
    let input = document.getElementById(inputId);
    if (input.value > 1) {
        input.value = parseInt(input.value) - 1;
        input.form.submit();
    }
}
