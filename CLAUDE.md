# Fram eller bak?

## Git
- Pusha alltid direkt till `main` (ingen feature-gren, ingen PR) om inget annat sägs.

## Bygga
- Källkoden finns i `src/app.html`. `index.html` är den byggda sidan med stationsdata inbäddad (`<script id="stations-data">`).
- `build.py` kräver pipelinens scratch-katalog (`FEB_SP`). Om den saknas: ersätt allt i `index.html` utom stationsdata-blobben med innehållet i `src/app.html` (samma head-tillägg som `make_site.py` lägger till).
