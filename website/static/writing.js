(function () {
  const track     = document.getElementById('shelfTrack');
  const prevBtn   = document.getElementById('prevBtn');
  const nextBtn   = document.getElementById('nextBtn');
  const dotsWrap  = document.getElementById('floorDots');
  const catLabel  = document.getElementById('categoryLabel');

  const sections  = Array.from(track.querySelectorAll('.shelf-section'));
  const total     = sections.length;
  let   current   = 0;

  sections.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'floor-dot';
    dot.setAttribute('aria-label', `Category ${i + 1}`);
    dot.addEventListener('click', () => goTo(i));
    dotsWrap.appendChild(dot);
  });

  function goTo(index) {
    current = Math.max(0, Math.min(total - 1, index));
    track.style.transform = `translateX(${-current * window.innerWidth}px)`;
    dotsWrap.querySelectorAll('.floor-dot').forEach((d, i) => {
      d.classList.toggle('active', i === current);
    });

    const name = sections[current].dataset.category;
    catLabel.classList.add('fading');
    setTimeout(() => {
      catLabel.textContent = name;
      catLabel.classList.remove('fading');
    }, 250);

    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === total - 1;
  }

  prevBtn.addEventListener('click', () => goTo(current - 1));
  nextBtn.addEventListener('click', () => goTo(current + 1));

  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft')  goTo(current - 1);
    if (e.key === 'ArrowRight') goTo(current + 1);
  });

  // Touch/swipe
  let tx = 0;
  document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) goTo(dx < 0 ? current + 1 : current - 1);
  }, { passive: true });

  window.addEventListener('resize', () => {
    const prev = track.style.transition;
    track.style.transition = 'none';
    track.style.transform  = `translateX(${-current * window.innerWidth}px)`;
    requestAnimationFrame(() => { track.style.transition = prev; });
  });

  goTo(0);

  const navToggle = document.getElementById('navToggle');
  const uiNav     = document.getElementById('uiNav');
  navToggle.addEventListener('click', () => uiNav.classList.toggle('open'));
})();
