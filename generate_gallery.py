#!/usr/bin/env -S uv run --script

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALBUMS_DIR = ROOT / "albums"
STYLE_LINK = "style.css"


def generate_album_index(album_path, rel_path):
    photos = [f for f in os.listdir(album_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
    photos.sort()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{album_path.name}</title>
  <link rel="stylesheet" href="../../{STYLE_LINK}">
</head>
<body>
  <h1>{album_path.name.replace('-', ' ').title()}</h1>
  <a href="../../index.html">← Back to Albums</a>
  <div class="gallery">
"""

    for photo in photos:
        html += f'    <img src="{photo}" alt="{photo}">\n'

    html += """  </div>
<div id="lightbox" class="lightbox-overlay" onclick="this.classList.remove('show')">
  <button id="prev-btn" style="position: absolute; left: 20px;">←</button>
  <img id="lightbox-img" src="" alt="">
  <button id="next-btn" style="position: absolute; right: 20px;">→</button>
</div>
<script>
  const images = Array.from(document.querySelectorAll('.gallery img'));
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  let currentIndex = 0;

  function showImage(index) {
    currentIndex = (index + images.length) % images.length;
    lightboxImg.src = images[currentIndex].src;
    lightbox.classList.add('show');
  }

  images.forEach((img, index) => {
    img.addEventListener('click', () => showImage(index));
  });

  document.getElementById('prev-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    showImage(currentIndex - 1);
  });

  document.getElementById('next-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    showImage(currentIndex + 1);
  });
</script>
</body>
</html>
"""

    with open(album_path / "index.html", "w", encoding="utf-8") as f:
        f.write(html)


def generate_main_index(albums):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Photo Albums</title>
  <link rel="stylesheet" href="{STYLE_LINK}">
</head>
<body>
  <h1>Photo Albums</h1>
  <ul class="albums">
"""

    for album in albums:
        path = f"albums/{album}/index.html"
        title = album.replace("-", " ").title()
        html += f'    <li><a href="{path}">{title}</a></li>\n'

    html += """  </ul>
</body>
</html>
"""

    with open(ROOT / "index.html", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if not ALBUMS_DIR.exists():
        print("albums/ directory not found.")
        return

    albums = [d.name for d in ALBUMS_DIR.iterdir() if d.is_dir()]
    albums.sort()

    for album in albums:
        album_path = ALBUMS_DIR / album
        generate_album_index(album_path, f"albums/{album}")

    generate_main_index(albums)
    print("Gallery generation complete.")


if __name__ == "__main__":
    main()
