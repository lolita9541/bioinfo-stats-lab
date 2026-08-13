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

let currentLanguage = localStorage.getItem('bioinfoSiteLanguage') || 'zh';
let tutorialData = [];
let researchData = [];
let serviceData = [];
let aboutData = null;

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function setLanguage(lang) {
  currentLanguage = lang;
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';
  document.querySelectorAll('[data-zh][data-en]').forEach(el => {
    el.textContent = el.dataset[lang];
  });
  zhBtn.classList.toggle('active', lang === 'zh');
  enBtn.classList.toggle('active', lang === 'en');
  localStorage.setItem('bioinfoSiteLanguage', lang);
  renderAllCmsContent();
}

zhBtn.addEventListener('click', () => setLanguage('zh'));
enBtn.addEventListener('click', () => setLanguage('en'));

async function fetchJson(url, fallback) {
  try {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error(url);
    return await res.json();
  } catch (err) {
    console.warn('CMS content fallback:', url, err);
    return fallback;
  }
}

async function loadCmsContent() {
  [tutorialData, researchData, serviceData, aboutData] = await Promise.all([
    fetchJson('/content/tutorials/index.json', []),
    fetchJson('/content/research/index.json', []),
    fetchJson('/content/services/index.json', []),
    fetchJson('/content/site/about.json', null)
  ]);
  renderAllCmsContent();
}

function renderAllCmsContent() {
  renderTutorials();
  renderResearch();
  renderServices();
  renderAbout();
}

function renderTutorials() {
  const grid = document.querySelector('.tutorial-grid');
  if (!grid || !tutorialData.length) return;
  grid.innerHTML = tutorialData.map(item => {
    const title = currentLanguage === 'zh' ? (item.title_zh || item.title_en || '') : (item.title_en || item.title_zh || '');
    const summary = currentLanguage === 'zh' ? (item.summary_zh || item.summary_en || '') : (item.summary_en || item.summary_zh || '');
    const cta = currentLanguage === 'zh' ? '閱讀文章 →' : 'Read article →';
    const image = item.image ? `<img src="${escapeHtml(item.image)}" alt="${escapeHtml(title)}" style="height:160px;object-fit:cover;border-radius:12px;margin-bottom:16px">` : '';
    return `<article>${image}<span>${escapeHtml(item.category || 'TUTORIAL')}</span><h3>${escapeHtml(title)}</h3><p>${escapeHtml(summary)}</p><b><a href="${escapeHtml(item.url || '#')}">${cta}</a></b></article>`;
  }).join('');
}

function renderResearch() {
  const grid = document.querySelector('.research-grid');
  if (!grid || !researchData.length) return;
  grid.innerHTML = researchData.map(item => {
    const title = currentLanguage === 'zh' ? (item.title_zh || item.title_en || '') : (item.title_en || item.title_zh || '');
    const description = currentLanguage === 'zh' ? (item.description_zh || item.description_en || '') : (item.description_en || item.description_zh || '');
    const subtitle = item.title_en || title;
    return `<article class="research-card">
      ${item.image ? `<img src="${escapeHtml(item.image)}" alt="${escapeHtml(title)}">` : ''}
      <h3>${escapeHtml(title)}</h3><small>${escapeHtml(subtitle)}</small><p>${escapeHtml(description)}</p>
    </article>`;
  }).join('');
}

function renderServices() {
  const grid = document.querySelector('.service-grid');
  if (!grid || !serviceData.length) return;
  grid.innerHTML = serviceData.map(item => {
    const title = currentLanguage === 'zh' ? (item.title_zh || item.title_en || '') : (item.title_en || item.title_zh || '');
    const subtitle = item.title_en || title;
    const description = currentLanguage === 'zh' ? (item.description_zh || item.description_en || '') : (item.description_en || item.description_zh || '');
    const items = currentLanguage === 'zh' ? (item.items_zh || item.items_en || []) : (item.items_en || item.items_zh || []);
    const cta = currentLanguage === 'zh' ? '了解更多 →' : 'Learn more →';
    return `<article class="service-card ${escapeHtml(item.color || 'purple')}">
      <div class="service-heading"><span class="service-icon">${escapeHtml(item.icon || '✦')}</span><div><h3>${escapeHtml(title)}</h3><small>${escapeHtml(subtitle)}</small></div></div>
      ${description ? `<p style="font-size:.8rem;color:#747a8f">${escapeHtml(description)}</p>` : ''}
      <ul>${items.map(x => `<li>${escapeHtml(x)}</li>`).join('')}</ul>
      <a href="#contact">${cta}</a>
    </article>`;
  }).join('');
}

function renderAbout() {
  if (!aboutData) return;
  const copy = document.querySelector('.about-copy');
  const points = document.querySelector('.about-points');
  if (copy) {
    const headline = currentLanguage === 'zh' ? aboutData.headline_zh : aboutData.headline_en;
    const intro1 = currentLanguage === 'zh' ? aboutData.intro1_zh : aboutData.intro1_en;
    const intro2 = currentLanguage === 'zh' ? aboutData.intro2_zh : aboutData.intro2_en;
    const button = currentLanguage === 'zh' ? '與我討論研究 →' : 'Discuss a Project →';
    copy.innerHTML = `<p class="section-label">ABOUT ME</p><h2>${escapeHtml(headline || '')}</h2><p>${escapeHtml(intro1 || '')}</p><p>${escapeHtml(intro2 || '')}</p><a class="button outline-small" href="#contact">${button}</a>`;
  }
  if (points && Array.isArray(aboutData.highlights)) {
    points.innerHTML = aboutData.highlights.map(item => {
      const title = currentLanguage === 'zh' ? item.title_zh : item.title_en;
      const desc = currentLanguage === 'zh' ? item.description_zh : item.description_en;
      return `<article><span class="point-icon">${escapeHtml(item.icon || '✦')}</span><div><h3>${escapeHtml(title || '')}</h3><p>${escapeHtml(desc || '')}</p></div></article>`;
    }).join('');
  }
}

setLanguage(currentLanguage);
loadCmsContent();
