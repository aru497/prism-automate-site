// Prism Automate: smooth scrolling (Lenis), nav state, mobile menu, hero ring tilt,
// strategy-session form mailto fallback.
// Scroll reveals are pure CSS (animation-timeline: view()) so content never gates on JS.

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const nav = document.querySelector('.nav');
const toggle = document.querySelector('.nav-toggle');

const closeMenu = () => {
  nav.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
};

// Framer-style inertia scrolling. Skipped under reduced motion; native scroll remains.
let lenis = null;
if (!reduceMotion && typeof Lenis !== 'undefined') {
  document.documentElement.classList.add('inertia-scroll');
  lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1 });
  const raf = time => {
    lenis.raf(time);
    requestAnimationFrame(raf);
  };
  requestAnimationFrame(raf);
}

// Anchor navigation: route through Lenis when active so in-page jumps share the same feel.
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id.length <= 1) return;
    const target = document.querySelector(id);
    if (!target) return;
    closeMenu();
    if (lenis) {
      e.preventDefault();
      lenis.scrollTo(target, { offset: -84, duration: 1.4 });
    }
  });
});

// Hero eyebrow typewriter: cycles the positioning lines. Static under reduced motion.
const typeText = document.getElementById('type-text');
if (typeText && !reduceMotion) {
  const PHRASES = [
    'AI Automation Company',
    'Anthropic Claude Partner',
    'Agentic Platforms That Ship',
    'Event Tech and Virtual Try-On'
  ];
  // starts fully typed (matches the static markup), so the first move is a delete
  let phrase = 0, chars = PHRASES[0].length, deleting = true;
  const step = () => {
    const current = PHRASES[phrase];
    if (deleting) {
      chars--;
      if (chars === 0) {
        deleting = false;
        phrase = (phrase + 1) % PHRASES.length;
      }
    } else {
      chars++;
    }
    typeText.textContent = PHRASES[phrase].slice(0, chars);
    let delay = deleting ? 28 : 52;
    if (!deleting && chars === current.length) {
      deleting = true;
      delay = 2200; // hold the finished line
    }
    setTimeout(step, delay);
  };
  setTimeout(step, 2400);
}

// Ring videos: freeze under reduced motion; footer ring only loads/plays when near view.
if (reduceMotion) {
  document.querySelectorAll('video').forEach(v => {
    v.removeAttribute('autoplay');
    v.pause();
  });
} else {
  const wmRing = document.querySelector('.wm-ring');
  if (wmRing) {
    new IntersectionObserver(([entry], io) => {
      if (entry.isIntersecting) {
        wmRing.play().catch(() => {});
        io.disconnect();
      }
    }, { rootMargin: '300px' }).observe(wmRing);
  }
}

// Nav background: sentinel-based, no scroll listener.
const sentinel = document.getElementById('top-sentinel');
new IntersectionObserver(([entry]) => {
  nav.classList.toggle('is-scrolled', !entry.isIntersecting);
}).observe(sentinel);

// Mobile menu.
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(open));
});

// Hero ring tilt: pointer-driven target, critically damped spring toward it.
// Applies to the <video> itself: transforming a wrapper would isolate the blend
// group and expose the video rectangle. Decorative only: gated behind fine
// pointer + motion preference.
const shell = document.querySelector('.hero-ring video');
const shellHit = document.querySelector('.hero-ring');
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
if (shell && finePointer && !reduceMotion) {
  const MAX_DEG = 6;
  const K = 170, C = 26; // stiffness + critical damping (2 * sqrt(K))
  let tx = 0, ty = 0;          // target rotation
  let x = 0, y = 0, vx = 0, vy = 0; // spring state
  let raf = null, last = 0;

  const tick = now => {
    const dt = Math.min((now - last) / 1000, 1 / 30);
    last = now;
    vx += ((tx - x) * K - vx * C) * dt;
    vy += ((ty - y) * K - vy * C) * dt;
    x += vx * dt;
    y += vy * dt;
    shell.style.transform = `perspective(1100px) rotateX(${y.toFixed(3)}deg) rotateY(${x.toFixed(3)}deg)`;
    const settled = Math.abs(tx - x) < 0.01 && Math.abs(ty - y) < 0.01 &&
                    Math.abs(vx) < 0.01 && Math.abs(vy) < 0.01;
    if (settled && tx === 0 && ty === 0) {
      shell.style.transform = '';
      shell.style.willChange = '';
      raf = null;
      return;
    }
    raf = requestAnimationFrame(tick);
  };
  const wake = () => {
    if (raf === null) {
      shell.style.willChange = 'transform';
      last = performance.now();
      raf = requestAnimationFrame(tick);
    }
  };
  shellHit.addEventListener('pointermove', e => {
    const r = shellHit.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 2 * MAX_DEG;
    ty = -((e.clientY - r.top) / r.height - 0.5) * 2 * MAX_DEG;
    wake();
  });
  shellHit.addEventListener('pointerleave', () => { tx = 0; ty = 0; wake(); });
}

// TODO: replace mailto with a real backend endpoint + confirmed inbox.
const form = document.getElementById('demo-form');
const note = document.getElementById('form-note');
form.addEventListener('submit', e => {
  e.preventDefault();
  const name = form.name.value.trim();
  const email = form.email.value.trim();
  if (!name || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    note.textContent = 'Please add your name and a valid work email.';
    note.style.color = 'var(--lav)';
    return;
  }
  const body = [
    `Name: ${name}`,
    `Email: ${email}`,
    `Company/project: ${form.company.value.trim()}`,
    '',
    form.message.value.trim()
  ].join('\n');
  const subject = encodeURIComponent(`Strategy session request: ${name}`);
  window.location.href = `mailto:hello@prismscale.com?subject=${subject}&body=${encodeURIComponent(body)}`;
  note.textContent = 'Your email draft is ready to send. We reply within one business day.';
  note.style.color = '';
});
