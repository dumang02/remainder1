// =========================
// File: pages.js
// Path: /static/js/pages.js
// Purpose: Enhance interactivity for forms, tables, reminders
// =========================

document.addEventListener("DOMContentLoaded", function () {
    // Autofocus the first input in every form
    const form = document.querySelector("form");
    if (form) {
        const firstInput = form.querySelector("input, textarea, select");
        if (firstInput) firstInput.focus();
    }

    // Show selected file name on file input
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const label = document.createElement('small');
            label.textContent = `Selected: ${this.files[0]?.name}`;
            this.parentNode.appendChild(label);
        });
    }

    // Highlight active nav link
    const navLinks = document.querySelectorAll('.nav-link');
    const path = window.location.pathname;
    navLinks.forEach(link => {
        if (path.includes(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });

    // Show confirmation on delete button
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this record?')) {
                e.preventDefault();
            }
        });
    });

    // Table row click (optional: highlight or redirect)
    const rows = document.querySelectorAll(".table-clickable tbody tr");
    rows.forEach(row => {
        row.addEventListener("click", () => {
            const link = row.getAttribute("data-href");
            if (link) window.location.href = link;
        });
    });

    // Reminder animation (if used)
    const reminders = document.querySelectorAll(".list-group-item");
    reminders.forEach(item => {
        item.addEventListener("mouseover", () => {
            item.style.backgroundColor = "#e7f1ff";
        });
        item.addEventListener("mouseout", () => {
            item.style.backgroundColor = "";
        });
    });
});
