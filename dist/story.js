const track = document.querySelector('.story-track');
const intro = document.querySelector('.story-intro');
const details = document.querySelector('.story-details');
const teamSection = document.querySelector('.team-scroll');
const teamStage = document.querySelector('.team-stage');
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

  const first = teamCards[0];
  const last = teamCards[teamCards.length - 1];
  const center = (teamStage.clientWidth - first.offsetWidth) / 2;
  teamStart = center - first.offsetLeft;
  teamDistance = first.offsetLeft - last.offsetLeft;
  teamTravel = Math.max(1, teamDistance * 1.2);
  teamSection.style.height = `${window.innerHeight + teamTravel}px`;
}

function updateTeam() {
  if (reduceMotion.matches || teamCards.length < 2) return;
  const progress = clamp(-teamSection.getBoundingClientRect().top / teamTravel);
  const offset = teamStart + teamDistance * progress;
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
