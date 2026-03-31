import re

app_file = 'interactiveStudy/src/app.js'
with open(app_file, 'r', encoding='utf-8') as f:
    js = f.read()

# Make ToC collapsable and add smooth scrolling
# The simplest approach is manipulating the rendered DOM

js_append = """
  // Set IDs for headers so anchors work
  contentEl.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
    if (!h.id) {
      let anchor = h.textContent.toLowerCase()
                    .replace(/[^\\w\\s-]/g, '')
                    .replace(/\\s+/g, '-')
                    .replace(/-+/g, '-');
      h.id = anchor;
    }
  });

  // Smooth scroll for internal links
  contentEl.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Make Table of Contents collapsable
  const tocHeader = Array.from(contentEl.querySelectorAll('h2')).find(h => h.textContent.trim() === 'Table of Contents');
  if (tocHeader) {
    tocHeader.style.cursor = 'pointer';
    tocHeader.style.userSelect = 'none';
    tocHeader.innerHTML = '&#9654; Table of Contents'; // Right pointing triangle
    
    // The ul is exactly the next element sibling
    const tocList = tocHeader.nextElementSibling;
    if (tocList && tocList.tagName.toLowerCase() === 'ul') {
      tocList.style.display = 'none'; // Collapsed by default
      
      tocHeader.addEventListener('click', () => {
        if (tocList.style.display === 'none') {
          tocList.style.display = 'block';
          tocHeader.innerHTML = '&#9660; Table of Contents'; // Down pointing triangle
        } else {
          tocList.style.display = 'none';
          tocHeader.innerHTML = '&#9654; Table of Contents';
        }
      });
    }
  }
"""

js = js.replace('// Make external links open in new tab', js_append + '\n  // Make external links open in new tab')
with open(app_file, 'w', encoding='utf-8') as f:
    f.write(js)
