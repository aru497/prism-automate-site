// Shared "I'm Interested / Start a project" popup form.
// Auto-wires any link to #interest or #contact (and any [data-interest] element)
// to open a modal, so no page needs an inline fill-in form. Progressive
// enhancement: with JS the modal opens; without it, the link still resolves.
//
// Submit path: POSTs the fields to Formspree (https://formspree.io), which
// emails every submission straight to your inbox and logs it in a dashboard —
// no mail client needed. If the request fails (or the form ID below is still
// the placeholder) it falls back to a pre-filled mailto so a lead is never lost.
//
// SETUP (one time): create a free form at https://formspree.io, then paste its
// ID below. The ID is the last part of the endpoint it gives you —
// e.g. for https://formspree.io/f/mqkzabcd the ID is "mqkzabcd".
(function () {
  var FORMSPREE_ID = 'YOUR_FORM_ID';            // <-- paste your Formspree form ID here
  var CC = 'arun@prismscale.com';               // second recipient (add in Formspree dashboard too)
  var ENDPOINT = 'https://formspree.io/f/' + FORMSPREE_ID;
  var MAILTO = 'dharam@prismscale.com,' + CC;   // fallback only

  var css =
    '.pi-overlay{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;padding:1.25rem;background:rgba(5,4,8,.82);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);opacity:0;visibility:hidden;transition:opacity .28s cubic-bezier(.16,1,.3,1),visibility 0s linear .28s;}' +
    '.pi-overlay.open{opacity:1;visibility:visible;transition-delay:0s;}' +
    '.pi-card{width:100%;max-width:500px;max-height:92vh;overflow-y:auto;background:#0d0a15;border:1px solid rgba(255,255,255,.14);color:#f1f0f6;padding:clamp(1.5rem,4vw,2.4rem);transform:translateY(12px);transition:transform .28s cubic-bezier(.16,1,.3,1);font:400 1rem/1.5 "Familjen Grotesk","Helvetica Neue",Arial,sans-serif;}' +
    '.pi-overlay.open .pi-card{transform:none;}' +
    '.pi-head{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;}' +
    '.pi-head h3{margin:0;font-family:"Hanken Grotesk","Familjen Grotesk",sans-serif;font-weight:200;font-size:1.9rem;line-height:1.03;letter-spacing:-.02em;}' +
    '.pi-close{background:none;border:0;color:rgba(255,255,255,.6);font-size:1.6rem;line-height:1;cursor:pointer;padding:.1rem .3rem;}' +
    '.pi-close:hover{color:#f1f0f6;}' +
    '.pi-sub{margin:.6rem 0 1.4rem;color:rgba(255,255,255,.62);font-size:.97rem;line-height:1.5;}' +
    '.pi-field{display:grid;gap:.4rem;margin-bottom:.9rem;}' +
    '.pi-field label{font-size:.72rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6);}' +
    '.pi-field input,.pi-field textarea{width:100%;font:inherit;color:#f1f0f6;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.32);padding:.85rem .9rem;border-radius:0;}' +
    '.pi-field input::placeholder,.pi-field textarea::placeholder{color:rgba(255,255,255,.4);}' +
    '.pi-field input:focus,.pi-field textarea:focus{outline:none;border-color:#a89ef1;background:rgba(168,158,241,.08);}' +
    '.pi-field textarea{resize:vertical;min-height:96px;}' +
    '.pi-row{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;}' +
    '@media(max-width:560px){.pi-row{grid-template-columns:1fr;}}' +
    '.pi-submit{margin-top:.3rem;width:100%;background:#d9a86a;color:#16121f;border:1px solid #d9a86a;padding:1rem;font:600 1rem/1 "Familjen Grotesk",sans-serif;cursor:pointer;}' +
    '.pi-submit:hover{background:#e7bd86;}' +
    '.pi-note{margin:.7rem 0 0;font-size:.88rem;color:rgba(255,255,255,.6);min-height:1.1em;}';
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var overlay = document.createElement('div');
  overlay.className = 'pi-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Contact form');
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML =
    '<div class="pi-card">' +
      '<div class="pi-head"><h3>Let’s talk.</h3>' +
      '<button type="button" class="pi-close" aria-label="Close">×</button></div>' +
      '<p class="pi-sub">Tell us what you’re trying to build or fix. A real person replies within one business day — no deck required.</p>' +
      '<form class="pi-form" novalidate>' +
        '<div class="pi-row">' +
          '<div class="pi-field"><label for="pi-name">Name</label><input id="pi-name" name="name" type="text" autocomplete="name" required></div>' +
          '<div class="pi-field"><label for="pi-email">Work email</label><input id="pi-email" name="email" type="email" autocomplete="email" required></div>' +
        '</div>' +
        '<div class="pi-field"><label for="pi-company">Company</label><input id="pi-company" name="company" type="text" autocomplete="organization"></div>' +
        '<div class="pi-field"><label for="pi-msg">What should Claude take off your plate?</label><textarea id="pi-msg" name="message"></textarea></div>' +
        '<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">' +
        '<button type="submit" class="pi-submit">I’m Interested →</button>' +
        '<p class="pi-note" role="status" aria-live="polite"></p>' +
      '</form>' +
    '</div>';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    document.body.appendChild(overlay);
    var note = overlay.querySelector('.pi-note');
    var form = overlay.querySelector('.pi-form');
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      overlay.classList.add('open');
      overlay.setAttribute('aria-hidden', 'false');
      document.documentElement.style.overflow = 'hidden';
      if (window.__lenis) window.__lenis.stop();
      var f = overlay.querySelector('#pi-name');
      if (f) setTimeout(function () { f.focus(); }, 60);
    }
    function close() {
      overlay.classList.remove('open');
      overlay.setAttribute('aria-hidden', 'true');
      document.documentElement.style.overflow = '';
      if (window.__lenis) window.__lenis.start();
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    overlay.querySelector('.pi-close').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) close();
    });

    // Wire every interest / contact trigger to the popup (capture phase so it
    // beats any page-level smooth-scroll handler on the same link).
    var triggers = document.querySelectorAll('a[href$="#interest"], a[href$="#contact"], [data-interest]');
    triggers.forEach(function (t) {
      t.addEventListener('click', function (e) { e.preventDefault(); open(); }, true);
    });

    function mailtoFallback(name, payload) {
      var body = 'Name: ' + payload.name + '\nEmail: ' + payload.email +
        '\nCompany: ' + payload.company + '\n\n' + payload.message;
      location.href = 'mailto:' + MAILTO + '?subject=' +
        encodeURIComponent('Enquiry from ' + name) + '&body=' + encodeURIComponent(body);
    }

    var submitting = false;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (submitting) return;
      if (form._honey && form._honey.value) return;          // bot trap
      var name = form.name.value.trim(), email = form.email.value.trim();
      if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        note.textContent = 'Add your name and a valid work email and we’re good to go.';
        note.style.color = '#a89ef1';
        return;
      }
      var payload = {
        name: name,
        email: email,                                  // Formspree uses this as reply-to
        company: form.company.value.trim(),
        message: form.message.value.trim(),
        _subject: 'New enquiry from ' + name + ' — prismautomate.com',
        _cc: CC
      };

      // Not configured yet → skip the network round-trip, go straight to email.
      if (FORMSPREE_ID === 'YOUR_FORM_ID') {
        mailtoFallback(name, payload);
        note.textContent = 'Opening your email app to send — one moment.';
        return;
      }

      var btn = form.querySelector('.pi-submit');
      var label = btn.textContent;
      submitting = true; btn.disabled = true; btn.textContent = 'Sending…';
      note.style.color = ''; note.textContent = '';

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }, function () { return { ok: r.ok, data: {} }; }); })
        .then(function (res) {
          if (res.ok && (!res.data || !res.data.errors)) {
            form.reset();
            note.textContent = 'Got it — thank you. A real person replies within one business day.';
          } else {
            // Endpoint issue — don't lose the lead.
            mailtoFallback(name, payload);
            note.textContent = 'Finishing in your email app — just hit send.';
          }
        })
        .catch(function () {
          mailtoFallback(name, payload);
          note.textContent = 'Finishing in your email app — just hit send.';
        })
        .finally(function () {
          submitting = false; btn.disabled = false; btn.textContent = label;
        });
    });
  });
})();
