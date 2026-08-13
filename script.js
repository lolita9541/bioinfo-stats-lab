const menuButton = document.getElementById('menuButton');
const navLinks = document.getElementById('navLinks');
const zhBtn = document.getElementById('zhBtn');
const enBtn = document.getElementById('enBtn');

menuButton?.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
  });
});

function setLanguage(lang) {
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';

  document.querySelectorAll('[data-zh][data-en]').forEach(el => {
    el.textContent = el.dataset[lang];
  });

  zhBtn.classList.toggle('active', lang === 'zh');
  enBtn.classList.toggle('active', lang === 'en');

  localStorage.setItem('bioinfoSiteLanguage', lang);
}

zhBtn.addEventListener('click', () => setLanguage('zh'));
enBtn.addEventListener('click', () => setLanguage('en'));

setLanguage(localStorage.getItem('bioinfoSiteLanguage') || 'zh');
