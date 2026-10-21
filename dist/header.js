const siteHeader = document.querySelector('.site-header');
const menuToggle = siteHeader.querySelector('.header-menu-toggle');
const headerMenu = document.getElementById(menuToggle.getAttribute('aria-controls'));

function setHeaderMenu(open, restoreFocus = false) {
  headerMenu.hidden = !open;
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
  if (restoreFocus) menuToggle.focus();
}

menuToggle.addEventListener('click', () => setHeaderMenu(headerMenu.hidden));
headerMenu.addEventListener('click', (event) => {
  if (event.target.closest('a')) setHeaderMenu(false, true);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !headerMenu.hidden) setHeaderMenu(false, true);
});
document.addEventListener('pointerdown', (event) => {
  if (!siteHeader.contains(event.target)) {
    setHeaderMenu(false, headerMenu.contains(document.activeElement));
  }
});
document.addEventListener('focusin', (event) => {
  if (!siteHeader.contains(event.target)) setHeaderMenu(false);
});
