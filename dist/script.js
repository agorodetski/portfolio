const toggle = document.querySelector('.nav-toggle');
const navigation = document.querySelector('#site-nav');
const year = document.querySelector('#year');

if (year) year.textContent = new Date().getFullYear();

// The mobile menu is collapsed by the stylesheet; this only opens and closes it. Without JavaScript,
// a <noscript> rule in each page's <head> shows the ordinary links instead.
if (toggle && navigation) {
  const label = toggle.querySelector('.nav-toggle-label');
  const icon = toggle.querySelector('.nav-toggle-icon');

  const setOpen = (open) => {
    navigation.dataset.open = String(open);
    toggle.setAttribute('aria-expanded', String(open));
    if (label) label.textContent = open ? 'Close' : 'Menu';
    if (icon) icon.textContent = open ? '−' : '+';
  };

  const closeMenu = (restoreFocus = false) => {
    setOpen(false);
    if (restoreFocus) toggle.focus();
  };

  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));

  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  window.matchMedia('(max-width: 780px)').addEventListener('change', () => closeMenu());
}
