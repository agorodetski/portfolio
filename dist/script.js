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

const updateContainers = document.querySelectorAll('[data-updates-source]');

const renderUpdates = async (container) => {
  const source = container.dataset.updatesSource;
  const limit = Number.parseInt(container.dataset.updatesLimit || '6', 10);

  try {
    const response = await fetch(source, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`Updates request failed: ${response.status}`);
    const updates = await response.json();

    container.replaceChildren(...updates.slice(0, limit).map((item) => {
      const article = document.createElement('article');
      article.className = 'update-card';

      const meta = document.createElement('div');
      meta.className = 'update-meta';
      const category = document.createElement('span');
      category.textContent = item.category;
      const date = document.createElement('time');
      date.dateTime = item.date;
      date.textContent = item.dateLabel;
      meta.append(category, date);

      const heading = document.createElement('h3');
      heading.textContent = item.title;
      const summary = document.createElement('p');
      summary.textContent = item.summary;
      const link = document.createElement('a');
      link.className = 'update-link';
      link.href = item.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = `View on ${item.source}`;
      link.setAttribute('aria-label', `${item.title} — view on ${item.source}`);

      article.append(meta, heading, summary, link);
      return article;
    }));
  } catch (error) {
    const status = container.querySelector('.updates-status') || document.createElement('p');
    status.className = 'updates-status';
    status.textContent = 'Current notes are temporarily unavailable. Visit LinkedIn for the latest.';
    container.replaceChildren(status);
  }
};

updateContainers.forEach(renderUpdates);
