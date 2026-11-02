# SPECIES content integration

The site is generated from `data/species.json` using `python build-species.py`.
`prepare-species-assets.py` needs Pillow and pypdf and creates web copies from the
supplied originals and the six-page Luke PDF. Original media and the PDF are retained.

## Sources

- SPECIES Website Main Content.docx: identity, questions, approach, seven species,
  six detailed cases, and the proposal's contributor list.
- SPECIES_WP3_May_2026_aoa_fvb_aoa.docx: modelling aims, field sites and collaborators.
- SPECIES WP 3 information for website.zip: two profiles and portraits, project
  update and working conceptual diagram. Mac metadata was excluded.
- website_update_2026Sep_Florian.docx: two edited Finland field stories. References
  to missing images and unverified legal, health and monetary claims were omitted.
- website_update_LUKE_202609.pdf: research summary, five biographies and portraits,
  three cattle photos with original photographer credits, two dated activities.
- Heidi_winter_bigger.jpeg and Seal skins.JPG: portrait and materials photograph.

## Editorial points still requiring project input

- Wild ducks have a named case and contributors but no detailed case description.
  The page is deliberately brief; it does not invent a location, methods or findings.
- The main overview and WP3-specific contribution name different combinations of
  collaborators. Profiles preserve source-specific contributions without asserting
  that a collaborator has left the project or assigning an unconfirmed leadership role.
- Niels Martin Schmidt is named in the project overview but not the supplied WP3
  collaborator list. Confirm the current roster with the project lead.
- Confirm Nuccio Mazzullo's name spelling: the field report uses “Mazullo”. The
  site follows the main overview's “Mazzullo”.
- Two fieldwork contributors have no institution specified in the supplied text;
  no institution was guessed. Remaining portrait gaps use initials.
- Most photographs named in the Finland field report are absent from the folder.
  The hides image is not labelled as a particular location or as a photograph of
  the events in the articles. Its photographer is not specified in the source.
- Official project/institution logos, funding acknowledgement, and video/audio
  materials were not supplied in the original Drive set. The current homepage
  includes institution logos obtained separately; their sources are recorded in
  `assets/partners/sources.json`. No funding acknowledgement is inferred.
- Modelling and the conservation toolkit are described as work in development.
  This release does not fabricate a runnable model, datasets or published results.
- The homepage's existing conceptual illustration is retained, with descriptive
  alternative text distinguishing it from a field photograph.

## Structure and verification

The static output has a homepage, About, case directory, seven case pages, a
contributor directory, media collection, field-notes index, six note pages,
a complete research-materials library and seven full-text source pages.
Regions, contributors, notes and media can be filtered without hiding content from
visitors with JavaScript disabled. Cases, contributors, media and notes cross-link.
The existing shared header and homepage scroll animation are retained.

## Complete local source collection (2026-11-02)

All eight supplied Drive files are retained locally, including the test document
as a text export. Five useful ZIP members and eight PDF images are also available
separately. The original ZIP retains its Mac metadata. Full source transcriptions
preserve details omitted from the edited stories, with the author and source
period identified. Statements in original accounts remain attributable to those
accounts rather than being presented as independently verified findings.

See `DRIVE-CONTENT-RECORD.md` for the complete file-to-page mapping and image
credits. Files referenced by the field report but absent from the supplied Drive
collection remain listed as missing source materials. The current collection has
no original fieldwork photographs beyond the supplied hides image, cattle images,
portraits and working diagram.
