const toggle = document.querySelector('.nav-toggle');
const navigation = document.querySelector('#site-nav');
const year = document.querySelector('#year');

if (year) year.textContent = new Date().getFullYear();

if (toggle && navigation) {
  document.body.classList.add('nav-ready');
  toggle.hidden = false;

  const closeMenu = (restoreFocus = false) => {
    navigation.dataset.open = 'false';
    toggle.setAttribute('aria-expanded', 'false');
    if (restoreFocus) toggle.focus();
  };

  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    navigation.dataset.open = String(open);
  });

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
