import re

app_file = 'interactiveStudy/src/app.js'
with open(app_file, 'r', encoding='utf-8') as f:
    js = f.read()

# Add logic for mapping headers visible on screen to a "Top scroll" indicator
header_js = """
  // Replace missing interactive checkboxes setup since we removed it by accident earlier maybe? We'll put it later.
  // Add intersection observer to track which section we're in
  if (window.__sectionObserver) {
    window.__sectionObserver.disconnect();
  }
  
  const headers = Array.from(document.querySelectorAll('#content h1, #content h2'));
  const observer = new IntersectionObserver((entries) => {
    // Determine current active header based on scroll position
    const visibleHeaders = headers.filter(h => {
       const rect = h.getBoundingClientRect();
       return rect.top <= window.innerHeight * 0.4 && rect.bottom >= -window.innerHeight;
    });
    
    if(visibleHeaders.length > 0) {
      // get the last one that passed the threshold
      const h = visibleHeaders[visibleHeaders.length - 1];
      let txt = h.textContent.replace('▶', '').replace('▼', '').replace('Table of Contents', 'Overview').trim();
      
      let titleEl = document.getElementById('topbar-title');
      let stepMeta = window.STEP_META[window.currentStepIndex];
      titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title} <span class="sub-header" style="opacity:0.6;font-size:0.8em;margin-left:10px;cursor:pointer;" onclick="window.scrollTo({top:0,behavior:'smooth'})">❯ ${txt} <span style="font-size:0.8em;">▲</span></span>`;
    } else if (window.scrollY < 100) {
      let titleEl = document.getElementById('topbar-title');
      let stepMeta = window.STEP_META[window.currentStepIndex];
      titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title}`;
    }
  }, { rootMargin: '-10px 0px -80% 0px', threshold: [0, 1] });

  headers.forEach(h => observer.observe(h));
  window.__sectionObserver = observer;
"""

# inject inside renderStep
js = js.replace('// Wrap tables in scrollable container', header_js + '\n\n  // Wrap tables in scrollable container')

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(js)
