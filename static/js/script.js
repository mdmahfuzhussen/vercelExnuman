const body = document.body;
const navbar = document.querySelector('.navbar');
const darkToggle = document.querySelector('.dark-toggle');
const menuButton = document.querySelector('.menu-icon');
const navLinks = document.querySelector('.navbar-links');
const navAnchors = document.querySelectorAll('.navbar-links a');
const currentYear = document.querySelector('#current-year');
let lastScrollY = window.scrollY;

function syncNavbarHeight() {
  if (!navbar) {
    return;
  }

  document.documentElement.style.setProperty('--nav-height', `${navbar.offsetHeight}px`);
}

if (currentYear) {
  currentYear.textContent = new Date().getFullYear();
}

syncNavbarHeight();
window.addEventListener('resize', syncNavbarHeight);

if (navbar) {
  window.addEventListener(
    'scroll',
    () => {
      const isMobile = window.innerWidth <= 800;
      const currentScrollY = window.scrollY;

      if (!isMobile) {
        navbar.classList.remove('nav-hidden');
        lastScrollY = currentScrollY;
        return;
      }

      const isGoingUp = currentScrollY < lastScrollY;
      const nearTop = currentScrollY < 40;
      const menuIsOpen = navLinks?.classList.contains('open');

      navbar.classList.toggle('nav-hidden', !nearTop && !isGoingUp && !menuIsOpen);
      lastScrollY = currentScrollY;
    },
    { passive: true }
  );
}

if (darkToggle) {
  darkToggle.addEventListener('click', () => {
    const isDarkMode = body.classList.toggle('dark-mode');
    darkToggle.textContent = isDarkMode ? 'Light Mode' : 'Dark Mode';
  });
}

if (menuButton && navLinks) {
  menuButton.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    menuButton.classList.toggle('open', isOpen);
    menuButton.setAttribute('aria-expanded', String(isOpen));
    navbar?.classList.toggle('nav-hidden', false);
    syncNavbarHeight();
  });

  navAnchors.forEach((anchor) => {
    anchor.addEventListener('click', () => {
      navLinks.classList.remove('open');
      menuButton.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
      syncNavbarHeight();
    });
  });
}
