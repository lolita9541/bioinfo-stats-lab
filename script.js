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

function setLanguage(lang) {
  currentLanguage = lang;
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';

  document.querySelectorAll('[data-zh][data-en]').forEach(el => {
    el.textContent = el.dataset[lang];
  });

  zhBtn.classList.toggle('active', lang === 'zh');
  enBtn.classList.toggle('active', lang === 'en');

  localStorage.setItem('bioinfoSiteLanguage', lang);
  renderTutorials();
}

zhBtn.addEventListener('click', () => setLanguage('zh'));
enBtn.addEventListener('click', () => setLanguage('en'));

const tutorialFallback = [
  {
    category: 'MICROBIOME',
    title_zh: 'Alpha / Beta Diversity',
    title_en: 'Alpha / Beta Diversity',
    summary_zh: '如何選擇多樣性指標、解讀 PCoA 與 PERMANOVA。',
    summary_en: 'Choosing diversity metrics and interpreting PCoA and PERMANOVA.'
  },
  {
    category: 'STATISTICS',
    title_zh: 'Regression Strategy',
    title_en: 'Regression Strategy',
    summary_zh: '從研究問題到 covariates、confounders 與模型診斷。',
    summary_en: 'From research question to covariates, confounders and model diagnostics.'
  },
  {
    category: 'IMMUNE REPERTOIRE',
    title_zh: 'MiXCR → immunarch',
    title_en: 'MiXCR → immunarch',
    summary_zh: 'TCR clonotype、diversity、gene usage 與 public clone 工作流程。',
    summary_en: 'A workflow for TCR clonotypes, diversity, gene usage and public clones.'
  }
];

let tutorialData = [];

async function loadTutorialIndex() {
  try {
    const res = await fetch('/content/tutorials/index.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('tutorial index missing');
    tutorialData = await res.json();
  } catch (err) {
    tutorialData = tutorialFallback;
  }
  renderTutorials();
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderTutorials() {
  const grid = document.querySelector('.tutorial-grid');
  if (!grid) return;

  const items = tutorialData.length ? tutorialData : tutorialFallback;
  grid.innerHTML = items.map(item => {
    const title = currentLanguage === 'zh' ? (item.title_zh || item.title_en || '') : (item.title_en || item.title_zh || '');
    const summary = currentLanguage === 'zh' ? (item.summary_zh || item.summary_en || '') : (item.summary_en || item.summary_zh || '');
    const category = item.category || 'TUTORIAL';
    const href = item.url || '#';
    const cta = href === '#' ? 'Coming soon →' : (currentLanguage === 'zh' ? '閱讀文章 →' : 'Read article →');

    return `
      <article>
        <span>${escapeHtml(category)}</span>
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(summary)}</p>
        <b><a href="${escapeHtml(href)}">${escapeHtml(cta)}</a></b>
      </article>`;
  }).join('');
}

setLanguage(currentLanguage);
loadTutorialIndex();
