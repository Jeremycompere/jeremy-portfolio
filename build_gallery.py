"""Build gallery.html from assets/gallery/* folders."""
import os
from PIL import Image

GALLERY_DIR = 'assets/gallery'
ROW_HEIGHT = 280  # target row height in px

GIGS = [
    ('Zamar', 'ZAMAR 6.0 &amp; 7.0'),
    ('Toontopia', 'Toontopia Animation Festival'),
    ('TedX', 'TEDx: Rewriting Limits'),
    ('Wiflow masterclass', 'Wiflow Africa Music Masterclass'),
    ('Wilkinson and peace', 'Wilkinson &amp; Peace Wedding'),
    ('Victor and blessing', 'Victor &amp; Blessing Wedding'),
]

def get_unique_images(folder_path):
    seen_sizes = {}
    imgs = []
    for f in sorted(os.listdir(folder_path)):
        if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        fp = os.path.join(folder_path, f)
        sz = os.path.getsize(fp)
        if sz in seen_sizes:
            continue
        seen_sizes[sz] = True
        img = Image.open(fp)
        w, h = img.size
        imgs.append({'file': f, 'w': w, 'h': h})
    return imgs

def build_rows(images, row_height=ROW_HEIGHT):
    """Group images into rows using flexbox with aspect-ratio-based flex-grow."""
    html = ''
    for img in images:
        ar = img['w'] / img['h']
        flex_grow = ar * 100  # proportional width weight
        src = img['path'].replace('\\', '/')
        html += f'      <img src="{src}" alt="" style="flex-grow:{flex_grow:.0f};flex-basis:{int(ar * row_height)}px;height:{row_height}px;object-fit:cover;">\n'
    return html

sections_html = ''
for folder, title in GIGS:
    folder_path = os.path.join(GALLERY_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
    images = get_unique_images(folder_path)
    for img in images:
        img['path'] = os.path.join(GALLERY_DIR, folder, img['file'])

    section = f'''
    <section class="gallery-section">
      <h2 class="gallery-gig-title">{title}</h2>
      <div class="gallery-grid">
{build_rows(images)}      </div>
    </section>
'''
    sections_html += section

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Jeremy — Full event gallery. Photos from ZAMAR, Toontopia, TEDx, Wiflow, weddings and more.">
  <title>Gallery — Jeremy | Compere &amp; MC</title>
  <link rel="icon" type="image/png" href="assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link href="css/style.css" rel="stylesheet">
  <style>
    /* ── Gallery Page Overrides ── */
    .gallery-hero {{
      padding: 140px 52px 60px;
      text-align: center;
    }}
    .gallery-hero h1 {{
      font-family: 'Sora', sans-serif;
      font-size: clamp(36px, 5vw, 60px);
      font-weight: 700;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
    }}
    .gallery-hero h1 em {{
      font-style: italic; font-weight: 300; color: var(--azure);
    }}
    .gallery-hero p {{
      color: var(--warm-mid); font-size: 14px; font-weight: 300;
      max-width: 480px; margin: 0 auto;
    }}
    .gallery-back {{
      display: inline-flex; align-items: center; gap: 8px;
      font-size: 11px; font-weight: 600; letter-spacing: 0.14em;
      text-transform: uppercase; text-decoration: none;
      color: var(--azure); margin-bottom: 32px;
      transition: color 0.2s;
    }}
    .gallery-back:hover {{ color: var(--ink); }}

    .gallery-section {{
      padding: 0 52px 64px;
    }}
    .gallery-gig-title {{
      font-family: 'Sora', sans-serif;
      font-size: 24px; font-weight: 700;
      letter-spacing: -0.01em;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--rule);
      color: var(--ink);
    }}
    .gallery-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }}
    .gallery-grid img {{
      display: block;
      min-width: 120px;
      max-height: {ROW_HEIGHT}px;
      border-radius: 2px;
      transition: opacity 0.2s;
      cursor: pointer;
    }}
    .gallery-grid img:hover {{
      opacity: 0.85;
    }}

    /* Lightbox */
    .gallery-lightbox {{
      position: fixed; inset: 0; z-index: 9999;
      background: rgba(0,0,0,0.92);
      backdrop-filter: blur(10px);
      display: flex; align-items: center; justify-content: center;
      opacity: 0; visibility: hidden;
      transition: opacity 0.3s, visibility 0.3s;
      cursor: pointer;
    }}
    .gallery-lightbox.active {{
      opacity: 1; visibility: visible;
    }}
    .gallery-lightbox img {{
      max-width: 92vw; max-height: 90vh;
      object-fit: contain;
      border-radius: 4px;
      box-shadow: 0 20px 80px rgba(0,0,0,0.5);
      cursor: default;
    }}
    .gallery-lightbox-close {{
      position: absolute; top: 24px; right: 28px;
      width: 40px; height: 40px;
      background: rgba(255,255,255,0.1);
      border: none; border-radius: 50%;
      color: #fff; font-size: 24px;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: background 0.2s;
    }}
    .gallery-lightbox-close:hover {{
      background: rgba(255,255,255,0.25);
    }}

    @media (max-width: 960px) {{
      .gallery-section {{ padding: 0 16px 48px; }}
      .gallery-hero {{ padding: 120px 24px 40px; }}
    }}
  </style>
</head>
<body>

  <!-- NAVIGATION -->
  <header>
    <nav>
      <a class="nav-logo" href="index.html" style="display:flex;align-items:center;">
        <img src="assets/logo.png" alt="Jeremy Logo" style="height:44px;width:auto;display:block;">
      </a>
      <div class="nav-links">
        <a href="index.html#gigs">Gigs</a>
        <a href="gallery.html" class="active">Gallery</a>
        <a href="index.html#about">About</a>
        <a href="index.html#rates">Rates</a>
        <a href="index.html#contact">Contact</a>
      </div>
    </nav>
  </header>

  <main>
    <div class="gallery-hero">
      <a href="index.html" class="gallery-back">← Back to Home</a>
      <h1>Event <em>Gallery</em></h1>
      <p>A visual journey through Jeremy's events — from orchestra stages to wedding venues.</p>
    </div>
{sections_html}
  </main>

  <!-- FOOTER -->
  <footer>
    <div style="display:flex;align-items:center;gap:12px;">
      <img src="assets/logo.png" alt="Jeremy Small Logo" style="height:28px;width:auto;opacity:0.55;">
      <p style="margin:0;">&copy; 2026 Jeremiah Ibiwoye &middot; Jeremy &middot; Compere &amp; MC &middot; Lagos, Nigeria</p>
    </div>
  </footer>

  <!-- IMAGE LIGHTBOX -->
  <div class="gallery-lightbox" id="gallery-lightbox">
    <button class="gallery-lightbox-close" title="Close">&times;</button>
    <img id="gallery-lightbox-img" src="" alt="">
  </div>

  <script>
    // Lightbox for gallery images
    (function() {{
      var lb = document.getElementById('gallery-lightbox');
      var lbImg = document.getElementById('gallery-lightbox-img');
      var closeBtn = lb.querySelector('.gallery-lightbox-close');

      document.querySelectorAll('.gallery-grid img').forEach(function(img) {{
        img.addEventListener('click', function() {{
          lbImg.src = img.src;
          lb.classList.add('active');
          document.body.style.overflow = 'hidden';
        }});
      }});

      function closeLb() {{
        lb.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(function() {{ lbImg.src = ''; }}, 300);
      }}

      closeBtn.addEventListener('click', closeLb);
      lb.addEventListener('click', function(e) {{
        if (e.target === lb) closeLb();
      }});
      document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape' && lb.classList.contains('active')) closeLb();
      }});
    }})();
  </script>

</body>
</html>
'''

with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('gallery.html created successfully')
