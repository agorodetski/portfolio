const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');
const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();

if (toggle && nav) {
  document.body.classList.add('nav-ready');
  toggle.hidden = false;
  const closeMenu = (restoreFocus = false) => {
    nav.dataset.open = 'false';
    toggle.setAttribute('aria-expanded', 'false');
    if (restoreFocus) toggle.focus();
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.dataset.open = String(open);
  });
  nav.addEventListener('click', (event) => {
    if (!event.target.closest('a')) return;
    // Return focus before hiding the navigation so keyboard focus is never stranded.
    closeMenu(window.matchMedia('(max-width: 760px)').matches);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  window.matchMedia('(max-width: 760px)').addEventListener('change', () => closeMenu());
}
