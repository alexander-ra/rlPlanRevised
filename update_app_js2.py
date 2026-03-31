import re

app_file = 'interactiveStudy/src/app.js'
with open(app_file, 'r', encoding='utf-8') as f:
    js = f.read()

# Add logic for mapping headers visible on screen to a "Top scroll" indicator
header_js = """
// Add intersection observer to track which section we're in
const headers = Array.from(document.querySelectorAll('#content h1, #content h2'));
let currentSectionText = "Step";

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Find latest header above scroll fold
      const visibleHeaders = headers.filter(h => h.getBoundingClientRect().top < window.innerHeight / 2);
      if(visibleHeaders.length > 0) {
        const h = visibleHeaders[visibleHeaders.length - 1];
        let txt = h.textContent.replace('▶', '').replace('▼', '').replace('Table of Contents', 'Overview').trim();
        // remove emojis or extra stuff roughly
        
        let titleEl = document.getElementById('topbar-title');
        let stepMeta = window.STEP_META[window.currentStepIndex];
        titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title} <span style="opacity:0.6;font-size:0.85em;margin-left:8px;">❯ ${txt}</span>`;
      }
    }
  });
}, { rootMargin: '-10px 0px -80% 0px' });

headers.forEach(h => observer.observe(h));
window.__sectionObserver = observer;

// Remove old observer when step is rendered
"""

# inject inside renderStep
js = js.replace('// Setup interactive checklists', header_js + '\n\n  // Setup interactive checklists')

# Change topbar title logic in navigateTo
js = re.sub(
    r"document.getElementById\('topbar-title'\).textContent =\s*'Step ' \+ meta.num \+ ': ' \+ meta.title;",
    "document.getElementById('topbar-title').innerHTML = 'Step ' + meta.num + ': ' + meta.title;", 
    js
)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(js)
