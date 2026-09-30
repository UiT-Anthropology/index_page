const track = document.querySelector('.story-track');
const intro = document.querySelector('.story-intro');
const details = document.querySelector('.story-details');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

const clamp = (value) => Math.min(1, Math.max(0, value));
const ease = (value) => {
  const t = clamp(value);
  return t * t * (3 - 2 * t);
};

let scheduled = false;
function updateStory() {
  scheduled = false;
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
window.addEventListener('resize', requestUpdate);
reduceMotion.addEventListener('change', requestUpdate);
requestUpdate();
