const track = document.querySelector('.story-track');
const intro = document.querySelector('.story-intro');
const details = document.querySelector('.story-details');
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
    return;
  }
  const travel = Math.max(1, track.offsetHeight - window.innerHeight);
  const progress = clamp(-track.getBoundingClientRect().top / travel);
  const introExit = ease((progress - .07) / .28);
  const detailEnter = ease((progress - .34) / .22);
  const detailExit = ease((progress - .80) / .17);
  const detailOpacity = detailEnter * (1 - detailExit);

  intro.style.opacity = (1 - introExit).toFixed(3);
  intro.style.transform = `translate3d(0, ${(-110 * introExit).toFixed(1)}px, 0)`;
  intro.style.pointerEvents = introExit > .9 ? 'none' : 'auto';
  details.style.opacity = detailOpacity.toFixed(3);
  details.style.transform = `translate3d(0, ${(70 * (1 - detailEnter) - 80 * detailExit).toFixed(1)}px, 0)`;
  details.style.pointerEvents = detailOpacity > .9 ? 'auto' : 'none';
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

const mapWrap = document.querySelector('.polar-map-wrap');
const mapPins = [...document.querySelectorAll('.animal-pin')];
let openPin = null;

function placePinPopup(pin, popup) {
  const mapRect = mapWrap.getBoundingClientRect();
  const pinRect = pin.getBoundingClientRect();
  const x = pinRect.left + pinRect.width / 2 - mapRect.left;
  const y = pinRect.top + pinRect.height / 2 - mapRect.top;
  const gap = 24;
  const width = popup.offsetWidth;
  const height = popup.offsetHeight;
  const left = Math.max(8, Math.min(x - width / 2, mapRect.width - width - 8));
  const top = pinRect.top - height - gap >= 12 ? y - height - gap : y + gap;

  popup.style.left = `${left}px`;
  popup.style.top = `${top}px`;
  popup.style.setProperty('--origin-x', `${x - left}px`);
  popup.style.setProperty('--origin-y', `${y - top}px`);
}

function closePinPopup(restoreFocus = false) {
  if (!openPin) return;
  const pin = openPin;
  const popup = document.getElementById(pin.getAttribute('aria-controls'));
  popup.hidden = true;
  popup.classList.remove('is-open');
  pin.setAttribute('aria-expanded', 'false');
  openPin = null;
  if (restoreFocus) pin.focus();
}

for (const pin of mapPins) {
  pin.addEventListener('click', () => {
    if (openPin === pin) { closePinPopup(true); return; }
    closePinPopup();
    const popup = document.getElementById(pin.getAttribute('aria-controls'));
    popup.hidden = false;
    placePinPopup(pin, popup);
    popup.classList.remove('is-open');
    void popup.offsetWidth;
    popup.classList.add('is-open');
    pin.setAttribute('aria-expanded', 'true');
    openPin = pin;
    popup.querySelector('.pin-popup-close').focus();
  });
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
window.addEventListener('resize', () => {
  if (openPin) placePinPopup(openPin, document.getElementById(openPin.getAttribute('aria-controls')));
});
