const track = document.querySelector('.story-track');
const intro = document.querySelector('.story-intro');
const details = document.querySelector('.story-details');
const colorWash = document.querySelector('.story-color-wash');
const heroNav = document.querySelector('.story-stage .glass-nav');
const heroFoot = document.querySelector('.story-stage .hero-foot');
const polarSection = document.querySelector('.polar-section');
const polarHeading = document.querySelector('.polar-heading');
const polarMap = document.querySelector('.polar-map-wrap > img');
const polarPins = [...document.querySelectorAll('.animal-pin')];
const teamSection = document.querySelector('.team-scroll');
const teamViewport = document.querySelector('.team-viewport');
const teamRow = document.querySelector('.team-row');
const teamCards = [...document.querySelectorAll('.team-card')];
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

const clamp = (value) => Math.min(1, Math.max(0, value));
const ease = (value) => {
  const t = clamp(value);
  return t * t * (3 - 2 * t);
};

let scheduled = false;
let teamStart = 0;
let teamDistance = 0;
let teamTravel = 1;

function layoutTeam() {
  if (reduceMotion.matches || teamCards.length < 2) {
    teamSection.style.removeProperty('height');
    teamRow.style.removeProperty('transform');
    return;
  }

  const last = teamCards[teamCards.length - 1];
  const gutter = teamViewport.clientWidth < 600 ? 24 : 32;
  teamStart = gutter;
  const end = teamViewport.clientWidth - last.offsetWidth - gutter - last.offsetLeft;
  teamDistance = Math.max(0, teamStart - end);
  teamTravel = Math.max(1, teamDistance * 1.2);
  teamSection.style.height = `${window.innerHeight + teamTravel}px`;
}

function updateTeam() {
  if (reduceMotion.matches || teamCards.length < 2) return;
  const progress = clamp(-teamSection.getBoundingClientRect().top / teamTravel);
  const offset = teamStart - teamDistance * progress;
  teamRow.style.transform = `translate3d(${offset.toFixed(1)}px, -50%, 0)`;
}

function updateStory() {
  scheduled = false;
  updateTeam();
  if (reduceMotion.matches) {
    intro.removeAttribute('style');
    details.removeAttribute('style');
    colorWash.removeAttribute('style');
    heroNav.removeAttribute('style');
    heroFoot.removeAttribute('style');
    polarSection.removeAttribute('style');
    polarHeading.removeAttribute('style');
    polarMap.removeAttribute('style');
    polarPins.forEach((pin) => {
      pin.style.removeProperty('opacity');
      pin.removeAttribute('tabindex');
    });
    return;
  }
  const travel = Math.max(1, track.offsetHeight - window.innerHeight);
  const progress = clamp(-track.getBoundingClientRect().top / travel);
  const introExit = ease((progress - .04) / .16);
  const detailEnter = ease((progress - .20) / .12);
  const detailExit = ease((progress - .47) / .12);
  const detailOpacity = detailEnter * (1 - detailExit);
  const washEnter = ease((progress - .51) / .12);
  const mapEnter = ease((progress - .64) / .11);
  const pinsEnter = ease((progress - .73) / .09);
  const headingEnter = ease((progress - .84) / .09);

  intro.style.opacity = (1 - introExit).toFixed(3);
  intro.style.transform = `translate3d(0, ${(-110 * introExit).toFixed(1)}px, 0)`;
  intro.style.pointerEvents = introExit > .9 ? 'none' : 'auto';
  details.style.opacity = detailOpacity.toFixed(3);
  details.style.transform = `translate3d(0, ${(70 * (1 - detailEnter) - 80 * detailExit).toFixed(1)}px, 0)`;
  details.style.pointerEvents = detailOpacity > .9 ? 'auto' : 'none';
  colorWash.style.opacity = washEnter.toFixed(3);
  heroNav.style.opacity = (1 - washEnter).toFixed(3);
  heroNav.style.pointerEvents = washEnter > .9 ? 'none' : 'auto';
  heroFoot.style.opacity = (1 - washEnter).toFixed(3);
  polarSection.style.pointerEvents = pinsEnter > .9 ? 'auto' : 'none';
  polarMap.style.opacity = mapEnter.toFixed(3);
  polarMap.style.transform = `translate3d(0, ${(45 * (1 - mapEnter)).toFixed(1)}px, 0)`;
  polarPins.forEach((pin) => {
    pin.style.opacity = pinsEnter.toFixed(3);
    pin.tabIndex = pinsEnter > .9 ? 0 : -1;
  });
  polarHeading.style.opacity = headingEnter.toFixed(3);
  polarHeading.style.transform = `translate3d(0, ${(40 * (1 - headingEnter)).toFixed(1)}px, 0)`;
}

function requestUpdate() {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(updateStory);
}

window.addEventListener('scroll', requestUpdate, { passive: true });
window.addEventListener('resize', () => { layoutTeam(); requestUpdate(); });
reduceMotion.addEventListener('change', () => { layoutTeam(); requestUpdate(); });
document.fonts.ready.then(() => { layoutTeam(); requestUpdate(); });
layoutTeam();
requestUpdate();

const mapPins = [...document.querySelectorAll('.animal-pin')];
let openPin = null;
let pinSequence = 0;
const waitForPinMotion = (ms) => new Promise((resolve) => setTimeout(resolve, reduceMotion.matches ? 0 : ms));

function resetPin(pin) {
  const popup = document.getElementById(pin.getAttribute('aria-controls'));
  popup.hidden = true;
  popup.classList.remove('is-open', 'is-closing');
  pin.classList.remove('is-featured');
  pin.setAttribute('aria-expanded', 'false');
}

async function closePinPopup(restoreFocus = false) {
  if (!openPin) return;
  const pin = openPin;
  const popup = document.getElementById(pin.getAttribute('aria-controls'));
  const sequence = ++pinSequence;
  if (!popup.hidden) {
    popup.classList.remove('is-open');
    popup.classList.add('is-closing');
    await waitForPinMotion(240);
    if (sequence !== pinSequence) return;
  }
  popup.hidden = true;
  popup.classList.remove('is-closing');
  pin.classList.remove('is-featured');
  pin.setAttribute('aria-expanded', 'false');
  openPin = null;
  if (restoreFocus) pin.focus();
}

async function openPinPopup(pin) {
  if (openPin === pin) { closePinPopup(true); return; }
  const sequence = ++pinSequence;
  mapPins.forEach(resetPin);
  openPin = pin;
  pin.classList.add('is-featured');
  await waitForPinMotion(620);
  if (sequence !== pinSequence || openPin !== pin) return;
  const popup = document.getElementById(pin.getAttribute('aria-controls'));
  popup.hidden = false;
  popup.classList.add('is-open');
  pin.setAttribute('aria-expanded', 'true');
  popup.querySelector('.pin-popup-close').focus();
}

for (const pin of mapPins) {
  pin.addEventListener('click', () => openPinPopup(pin));
}

document.querySelectorAll('.pin-popup-close').forEach((button) => {
  button.addEventListener('click', () => closePinPopup(true));
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closePinPopup(true);
});
document.addEventListener('pointerdown', (event) => {
  if (openPin && !event.target.closest('.animal-pin, .pin-popup')) closePinPopup();
});
