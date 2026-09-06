  // sticky nav shadow
  const navEl = document.getElementById('siteNav');
  window.addEventListener('scroll', () => {
    navEl.classList.toggle('scrolled', window.scrollY > 8);
  }, { passive:true });

  // mobile menu
  const hbBtn = document.getElementById('hamburgerBtn');
  const mMenu = document.getElementById('mobileMenu');
  hbBtn.addEventListener('click', () => {
    mMenu.classList.toggle('open');
  });
  mMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mMenu.classList.remove('open')));

  // hero entrance
  requestAnimationFrame(() => {
    setTimeout(() => document.getElementById('heroContent').classList.add('in'), 80);
  });

  // rotating headline phrase (Snappy-style)
  const heroPhraseEl = document.getElementById('heroPhrase');
  const phrases = ['source it.', 'customize it.', 'package it.', 'deliver it.'];
  let phraseIdx = 0;
  if (heroPhraseEl) {
    setInterval(() => {
      heroPhraseEl.classList.add('fade');
      setTimeout(() => {
        phraseIdx = (phraseIdx + 1) % phrases.length;
        heroPhraseEl.textContent = phrases[phraseIdx];
        heroPhraseEl.classList.remove('fade');
      }, 320);
    }, 2600);
  }

  // rotating AI gift-finder search suggestions
  const gfInput = document.getElementById('giftSearchInput');
  const gfRow = document.getElementById('gfSearchRow');
  const gfPrompts = [
    'Try: “500 customized kits for an upcoming event”',
    'Try: “Onboarding kit for my new employees”',
    'Try: “Suggest some gift hampers for this Diwali”',
    'Try: “Corporate gifts under ₹1,000 per person”',
    'Try: “Wellness kit for a team celebration”',
    'Try: “Festive hampers for 200 clients”'
  ];
  let gfIdx = 0;
  if (gfInput && gfRow) {
    setInterval(() => {
      gfRow.classList.add('fade');
      setTimeout(() => {
        gfIdx = (gfIdx + 1) % gfPrompts.length;
        gfInput.setAttribute('placeholder', gfPrompts[gfIdx]);
        gfRow.classList.remove('fade');
      }, 200);
    }, 1300);
  }

  // scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll('.reveal, .reveal-stag').forEach(el => io.observe(el));
