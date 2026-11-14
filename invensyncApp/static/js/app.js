document.addEventListener("DOMContentLoaded", function () {
    var sidebar = document.getElementById("app-sidebar");
    var toggle = document.querySelector("[data-menu-toggle]");
    var scrim = document.querySelector("[data-sidebar-scrim]");

    function setMenuOpen(isOpen) {
        if (!sidebar || !toggle || !scrim) return;
        sidebar.classList.toggle("is-open", isOpen);
        scrim.classList.toggle("is-visible", isOpen);
        toggle.setAttribute("aria-expanded", String(isOpen));
        toggle.setAttribute("aria-label", isOpen ? "Close navigation" : "Open navigation");
    }

    if (toggle) {
        toggle.addEventListener("click", function () {
            setMenuOpen(!sidebar.classList.contains("is-open"));
        });
    }
    if (scrim) scrim.addEventListener("click", function () { setMenuOpen(false); });
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") setMenuOpen(false);
    });

    document.querySelectorAll("[data-dismiss]").forEach(function (button) {
        button.addEventListener("click", function () {
            var message = button.closest(".message");
            if (message) message.remove();
        });
    });

    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!window.confirm(form.getAttribute("data-confirm"))) event.preventDefault();
        });
    });
});
