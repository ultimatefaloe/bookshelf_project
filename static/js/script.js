/* =========================================================
   Mobile navigation toggle
   ========================================================= */
(function () {
  const toggle = document.getElementById("nav-toggle");
  const menu = document.getElementById("mobile-menu");
  const iconOpen = document.getElementById("icon-open");
  const iconClose = document.getElementById("icon-close");

  if (!toggle || !menu) return;

  function openMenu() {
    menu.classList.remove("hidden");
    iconOpen?.classList.add("hidden");
    iconClose?.classList.remove("hidden");
    toggle.setAttribute("aria-expanded", "true");
  }

  function closeMenu() {
    menu.classList.add("hidden");
    iconOpen?.classList.remove("hidden");
    iconClose?.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", function () {
    const isOpen = !menu.classList.contains("hidden");
    isOpen ? closeMenu() : openMenu();
  });

  // Close when a link inside the menu is clicked (nice for SPA-feel)
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  // Close on Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !menu.classList.contains("hidden")) {
      closeMenu();
      toggle.focus();
    }
  });

  // Auto-close when resizing up to desktop
  window.addEventListener("resize", function () {
    if (window.innerWidth >= 768) closeMenu();
  });
})();

/* =========================================================
   Delete modal
   ========================================================= */
(function () {
  const modal = document.getElementById("delete-modal");
  const form = document.getElementById("delete-form");
  const titleEl = document.getElementById("delete-modal-title");
  if (!modal || !form) return;

  // Build the delete URL. Adjust the template if your URL differs.
  // const deleteUrlTemplate = "{% url 'shelf:delete_book' 0 %}"; // 0 is a placeholder pk
  const deleteUrlTemplate = window.URLS?.deleteBook || "";

  window.openDeleteModal = function (bookId, bookTitle) {
    form.action = deleteUrlTemplate.replace(/0\/?$/, bookId + "/");
    if (titleEl)
      titleEl.textContent = bookTitle ? `"${bookTitle}"` : "this book";

    modal.classList.remove("hidden");
    modal.classList.add("flex");
    document.body.style.overflow = "hidden";
  };

  window.closeDeleteModal = function () {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.style.overflow = "";
  };

  // Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) {
      window.closeDeleteModal();
    }
  });
})();
