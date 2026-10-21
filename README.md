# SPECIES — Sustainable Species in the Arctic

A static research website using the project's supplied Drive materials. It includes seven case pages, a contributor directory, field notes, media and an About page while retaining the original Arctic visual design. See `CONTENT-REVIEW.md` for sources and outstanding editorial questions.

## Content maintenance

Edit `data/species.json`, then run `python build-species.py` and `python check-species.py`. The latter checks local links, fragments, image alternative text and remaining placeholders across the 19 pages. The homepage's existing layout is retained by the generator.

Use the bundled Python runtime with Pillow and pypdf to run `prepare-species-assets.py` when regenerating web images from the supplied originals. Credits are stored alongside the editorial content.

## Design references

| Reference | Useful pattern | Application here |
| --- | --- | --- |
| [Stanford Ethnography Lab](https://ethnographylab.stanford.edu/projects) | Research organized by clear themes and questions | Project areas provide an easy route into future findings |
| [Kiriwina](https://kiriwinaproject.org/) | Field research made accessible through visual storytelling | Environmental observation sits alongside lived experience |
| [Goldsmiths Centre for Visual Anthropology](https://www.gold.ac.uk/visual-anthropology/research/) | Film and photography treated as research material | A distinct Multimedia section |
| [NSIDC](https://nsidc.org/home) | Strong Arctic imagery and direct routes to research | A landscape-led hero with clear content pathways |

The fourth navigation item is **Field Notes**, intended for methods, field observations, and questions that emerge during the work.

## Files

- `dist/index.html`: static page content
- `dist/styles.css`: core styles
- `dist/layout.css`: full-width four-panel glass navigation and English typography adjustments
- `dist/assets/arctic-laser-hero.png`: conceptual image generated with the built-in image generation tool; it is not a photograph of a real field site

To preview locally, run `node preview-server.mjs` in this directory and open `http://127.0.0.1:8000`.




## Arctic map

Run `node generate-map.mjs` followed by `python build-species.py` to regenerate the country geometry and seven species pins. `map_content.py` maintains representative geographic anchors and the separate button positions joined by leader lines. Muskoxen includes Kangerlussuaq and Zackenberg. These points describe research settings, not species ranges or precise field sites. Country geometry uses Natural Earth 1:50m Admin 0 (public domain): https://www.naturalearthdata.com/downloads/50m-cultural-vectors/. Greenland is labelled as part of the Kingdom of Denmark. `dist/map.css` and `dist/map.js` provide country highlighting, fading labels, and species navigation.
