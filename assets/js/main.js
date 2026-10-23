// Mobile navigation
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
}

// Services tabs
const tabs = document.querySelectorAll('[role="tab"]');
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((t) => {
      const selected = t === tab;
      t.setAttribute('aria-selected', selected);
      document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
    });
  });
});

// Project gallery lightbox
const lightbox = document.querySelector('.lightbox');
if (lightbox) {
  const items = [...document.querySelectorAll('.gallery button')];
  const img = lightbox.querySelector('img');
  let index = 0;

  const show = (i) => {
    index = (i + items.length) % items.length;
    img.src = items[index].dataset.full;
    img.alt = items[index].querySelector('img').alt;
  };
  const close = () => { lightbox.hidden = true; document.body.style.overflow = ''; items[index].focus(); };

  items.forEach((item, i) => item.addEventListener('click', () => {
    show(i);
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
    lightbox.querySelector('.lb-close').focus();
  }));
  lightbox.querySelector('.lb-close').addEventListener('click', close);
  lightbox.querySelector('.lb-prev').addEventListener('click', () => show(index - 1));
  lightbox.querySelector('.lb-next').addEventListener('click', () => show(index + 1));
  lightbox.addEventListener('click', (e) => { if (e.target === lightbox) close(); });
  document.addEventListener('keydown', (e) => {
    if (lightbox.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(index - 1);
    if (e.key === 'ArrowRight') show(index + 1);
  });

  let startX = 0;
  lightbox.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
  lightbox.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
  });
}
