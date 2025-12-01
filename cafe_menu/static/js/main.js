const qs = (selector, scope = document) => scope.querySelector(selector);
const qsa = (selector, scope = document) => [...scope.querySelectorAll(selector)];

function initPreloader() {
  const preloader = qs("#preloader");
  if (!preloader) return;
  window.addEventListener("load", () => {
    preloader.classList.add("is-hidden");
    document.body.classList.add("is-ready");
  });
}

function initAnimations() {
  const animated = qsa("[data-animate]");
  if (!animated.length) return;

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  animated.forEach(section => observer.observe(section));

  if (window.gsap) {
    window.gsap.from(".hero-copy h1", { opacity: 0, y: 20, duration: 1 });
    window.gsap.from(".hero-card", { opacity: 0, y: 30, stagger: 0.1, delay: 0.2 });
  }
}

function initCategoryFilter() {
  const chips = qsa(".category-chip");
  const cards = qsa(".menu-card");
  if (!chips.length || !cards.length) return;

  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      const category = chip.dataset.category;
      chips.forEach(btn => btn.classList.toggle("is-active", btn === chip));

      cards.forEach(card => {
        const match = category === "all" || card.dataset.category === category;
        card.style.display = match ? "flex" : "none";
      });
    });
  });
}

function initDrawer() {
  const drawer = qs("#productDrawer");
  const overlay = qs("#drawerOverlay");
  if (!drawer || !overlay) return;

  const titleEl = qs("[data-drawer-title]", drawer);
  const descEl = qs("[data-drawer-description]", drawer);
  const priceEl = qs("[data-drawer-price]", drawer);
  const prepEl = qs("[data-drawer-prep]", drawer);
  const calEl = qs("[data-drawer-calories]", drawer);
  const ratingEl = qs("[data-drawer-rating]", drawer);
  const imgEl = qs("[data-drawer-image]", drawer);
  const badgeEl = qs("[data-drawer-badge]", drawer);

  function closeDrawer() {
    drawer.classList.remove("is-open");
    overlay.classList.remove("is-visible");
    drawer.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-hidden", "true");
  }

  function openDrawer(card) {
    titleEl.textContent = card.dataset.name || "";
    descEl.textContent = card.dataset.description || "";
    priceEl.textContent = card.dataset.price || "";
    prepEl.textContent = card.dataset.prep || "-";
    calEl.textContent = card.dataset.calories || "-";
    ratingEl.textContent = card.dataset.rating && card.dataset.rating !== "0" ? card.dataset.rating : "-";

    if (card.dataset.image) {
      imgEl.src = card.dataset.image;
      imgEl.alt = card.dataset.name || "";
    } else {
      imgEl.removeAttribute("src");
      imgEl.alt = "";
    }

    if (card.dataset.badge) {
      badgeEl.textContent = card.dataset.badge;
      badgeEl.style.display = "inline-flex";
    } else {
      badgeEl.textContent = "";
      badgeEl.style.display = "none";
    }

    drawer.classList.add("is-open");
    overlay.classList.add("is-visible");
    drawer.setAttribute("aria-hidden", "false");
    overlay.setAttribute("aria-hidden", "false");
  }

  qsa("[data-open-drawer]").forEach(trigger => {
    trigger.addEventListener("click", event => {
      const card = event.currentTarget.closest(".menu-card");
      if (!card) return;
      openDrawer(card);
    });
  });

  qs("[data-close-drawer]", drawer)?.addEventListener("click", closeDrawer);
  overlay.addEventListener("click", closeDrawer);
  window.addEventListener("keydown", event => {
    if (event.key === "Escape") closeDrawer();
  });
}

function initLanguageGate() {
  const gate = qs("#language-gate");
  if (!gate) return;

  if (gate.dataset.languageSelected === "true") {
    gate.remove();
    return;
  }

  // Ensure preloader is hidden before showing the gate
  window.addEventListener("load", () => {
    gate.style.opacity = "1";
  });
}

function initNavToggle() {
  const toggle = qs("[data-nav-toggle]");
  const nav = qs("[data-nav]");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  qsa("a", nav).forEach(link => {
    link.addEventListener("click", () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initPreloader();
  initAnimations();
  initCategoryFilter();
  initDrawer();
  initLanguageGate();
  initNavToggle();
});

