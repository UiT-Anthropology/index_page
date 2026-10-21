const mapWrap = document.querySelector('.polar-map-wrap');
const countryLabel = mapWrap.querySelector('.map-country-label');
let activeCountry = null;
function positionLabel(clientX, clientY) {
  const rect = mapWrap.getBoundingClientRect();
  const width = countryLabel.offsetWidth;
  const x = Math.max(width / 2 + 4, Math.min(rect.width - width / 2 - 4, clientX - rect.left));
  const y = Math.max(12, Math.min(rect.height - 48, clientY - rect.top - 46));
  countryLabel.style.left = `${x}px`;
  countryLabel.style.top = `${y}px`;
}
function showCountry(country, event) {
  activeCountry?.classList.remove('is-hovered');
  activeCountry = country;
  country.classList.add('is-hovered');
  countryLabel.textContent = country.dataset.country;
  if (event?.clientX !== undefined) positionLabel(event.clientX, event.clientY);
  else {
    // SVG geometry may extend beyond the clipped disc; use the visible map center for keyboard labels.
    const rect = mapWrap.getBoundingClientRect();
    positionLabel(rect.left + rect.width / 2, rect.top + rect.height * .57);
  }
  countryLabel.classList.add('is-visible');
}
function hideCountry() {
  activeCountry?.classList.remove('is-hovered');
  activeCountry = null;
  countryLabel.classList.remove('is-visible');
}
for (const country of mapWrap.querySelectorAll('.map-country')) {
  country.addEventListener('pointerenter', event => showCountry(country, event));
  country.addEventListener('pointermove', event => positionLabel(event.clientX, event.clientY));
  country.addEventListener('pointerleave', hideCountry);
  country.addEventListener('focus', () => showCountry(country));
  country.addEventListener('blur', hideCountry);
  country.addEventListener('click', event => showCountry(country, event));
  country.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); showCountry(country); }
    if (event.key === 'Escape') hideCountry();
  });
}
mapWrap.addEventListener('pointerleave', hideCountry);
window.addEventListener('resize', hideCountry);
document.querySelectorAll('[data-map-target]').forEach(button => {
  button.addEventListener('click', () => {
    hideCountry();
    mapWrap.querySelector(`[data-pin="${button.dataset.mapTarget}"]`).click();
  });
});
document.addEventListener('pointerdown', event => {
  if (!event.target.closest('.map-country')) hideCountry();
});
window.addEventListener('scroll', () => {
  if (activeCountry && document.activeElement === activeCountry) showCountry(activeCountry);
  else hideCountry();
}, { passive: true });
