/* ================================================================
   RADIANCE OVERSEAS — Master JavaScript v2.0
   ================================================================ */
(function() {
  'use strict';

  /* ── NAVBAR ─────────────────────────────────────────────────── */
  function initNav() {
    const nav = document.querySelector('.site-nav');
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.nav-menu');

    // Scroll sticky effect
    window.addEventListener('scroll', function() {
      if (nav) nav.classList.toggle('scrolled', window.scrollY > 40);
    });

    // Mobile toggle
    if (toggle && menu) {
      toggle.addEventListener('click', function() {
        toggle.classList.toggle('open');
        menu.classList.toggle('open');
      });

      // Mobile dropdown
      document.querySelectorAll('.nav-menu > li').forEach(function(li) {
        const dd = li.querySelector('.nav-dropdown');
        if (dd && window.innerWidth <= 768) {
          li.addEventListener('click', function(e) {
            if (e.target.closest('a') && !e.target.closest('.nav-dropdown')) {
              e.preventDefault();
              li.classList.toggle('open');
            }
          });
        }
      });
    }

    // Close menu on outside click
    document.addEventListener('click', function(e) {
      if (menu && !e.target.closest('.site-nav')) {
        menu.classList.remove('open');
        if (toggle) toggle.classList.remove('open');
      }
    });
  }

  /* ── HERO SLIDER ─────────────────────────────────────────────── */
  function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.hero-dot');
    if (!slides.length) return;

    let current = 0;
    let timer;

    function goTo(n) {
      slides[current].classList.remove('active');
      if (dots[current]) dots[current].classList.remove('active');
      current = (n + slides.length) % slides.length;
      slides[current].classList.add('active');
      if (dots[current]) dots[current].classList.add('active');
    }

    function autoplay() {
      timer = setInterval(function() { goTo(current + 1); }, 5500);
    }

    // Nav buttons
    const prevBtn = document.querySelector('.hero-btn-prev');
    const nextBtn = document.querySelector('.hero-btn-next');
    if (prevBtn) prevBtn.addEventListener('click', function() { clearInterval(timer); goTo(current - 1); autoplay(); });
    if (nextBtn) nextBtn.addEventListener('click', function() { clearInterval(timer); goTo(current + 1); autoplay(); });

    // Dots
    dots.forEach(function(dot, i) {
      dot.addEventListener('click', function() { clearInterval(timer); goTo(i); autoplay(); });
    });

    // Touch swipe
    let touchStartX = 0;
    const heroEl = document.querySelector('.hero-slider');
    if (heroEl) {
      heroEl.addEventListener('touchstart', function(e) { touchStartX = e.touches[0].clientX; });
      heroEl.addEventListener('touchend', function(e) {
        const diff = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 50) { clearInterval(timer); goTo(diff > 0 ? current + 1 : current - 1); autoplay(); }
      });
    }

    goTo(0);
    autoplay();
  }

  /* ── SCROLL REVEAL ───────────────────────────────────────────── */
  function initScrollReveal() {
    const elements = document.querySelectorAll('.anim-fade-up');
    if (!elements.length) return;

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    elements.forEach(function(el) { observer.observe(el); });
  }

  /* ── COUNTER ANIMATION ───────────────────────────────────────── */
  function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-count'));
          const duration = 2000;
          const step = target / (duration / 16);
          let current = 0;
          const timer = setInterval(function() {
            current += step;
            if (current >= target) { current = target; clearInterval(timer); }
            el.textContent = Math.floor(current).toLocaleString();
          }, 16);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(function(el) { observer.observe(el); });
  }

  /* ── FAQ ACCORDION ───────────────────────────────────────────── */
  function initFaq() {
    document.querySelectorAll('.faq-q').forEach(function(q) {
      q.addEventListener('click', function() {
        const isOpen = this.classList.contains('open');
        // Close all
        document.querySelectorAll('.faq-q').forEach(function(x) {
          x.classList.remove('open');
          const a = x.nextElementSibling;
          if (a) { a.style.display = 'none'; }
        });
        // Open clicked (if it was closed)
        if (!isOpen) {
          this.classList.add('open');
          const a = this.nextElementSibling;
          if (a) { a.style.display = 'block'; }
        }
      });
    });
  }

  /* ── GRADE TABS ──────────────────────────────────────────────── */
  function initGradeTabs() {
    document.querySelectorAll('.grade-tab').forEach(function(tab) {
      tab.addEventListener('click', function() {
        const group = this.closest('.grade-tabs-wrap');
        if (!group) return;
        group.querySelectorAll('.grade-tab').forEach(function(t) { t.classList.remove('active'); });
        group.querySelectorAll('.grade-panel').forEach(function(p) { p.style.display = 'none'; });
        this.classList.add('active');
        const panel = document.getElementById(this.dataset.panel);
        if (panel) panel.style.display = 'block';
      });
    });
  }

  /* ── GALLERY FILTER ──────────────────────────────────────────── */
  function initGallery() {
    const filters = document.querySelectorAll('.filter-btn');
    const items = document.querySelectorAll('.gallery-item');
    if (!filters.length) return;

    filters.forEach(function(btn) {
      btn.addEventListener('click', function() {
        filters.forEach(function(b) { b.classList.remove('active'); });
        this.classList.add('active');
        const cat = this.dataset.filter;
        items.forEach(function(item) {
          if (cat === 'all' || item.dataset.cat === cat) {
            item.style.display = '';
            item.style.animation = 'scaleIn .35s ease both';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });

    // Lightbox
    items.forEach(function(item) {
      item.addEventListener('click', function() {
        const src = this.querySelector('img').src;
        const caption = this.dataset.caption || '';
        openLightbox(src, caption);
      });
    });
  }

  function escapeHtml(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  function openLightbox(src, caption) {
    var safeSrc = escapeHtml(src);
    var safeCaption = caption ? escapeHtml(caption) : '';
    var lb = document.createElement('div');
    lb.id = 'lightbox';
    lb.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:99999;display:flex;align-items:center;justify-content:center;flex-direction:column;';

    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = 'position:absolute;top:20px;right:24px;background:none;border:none;color:#fff;font-size:36px;cursor:pointer;line-height:1;';
    closeBtn.addEventListener('click', function() { lb.remove(); });

    var img = document.createElement('img');
    img.src = safeSrc;
    img.style.cssText = 'max-width:90vw;max-height:80vh;border-radius:8px;box-shadow:0 8px 40px rgba(0,0,0,.5);';

    lb.appendChild(closeBtn);
    lb.appendChild(img);

    if (safeCaption) {
      var p = document.createElement('p');
      p.style.cssText = 'color:rgba(255,255,255,.7);margin-top:14px;font-size:14px;';
      p.textContent = caption;
      lb.appendChild(p);
    }

    lb.addEventListener('click', function(e) { if (e.target === lb) lb.remove(); });
    document.body.appendChild(lb);
    document.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', esc); } });
  }

  /* ── CONTACT FORM ────────────────────────────────────────────── */
  function initContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const origText = btn.textContent;
      btn.textContent = 'Sending...';
      btn.disabled = true;

      const data = {
        from_name: form.querySelector('#name') ? form.querySelector('#name').value : '',
        user_email: form.querySelector('#email') ? form.querySelector('#email').value : '',
        phone: form.querySelector('#phone') ? form.querySelector('#phone').value : '',
        subject: form.querySelector('#subject') ? form.querySelector('#subject').value : '',
        message: form.querySelector('#message') ? form.querySelector('#message').value : '',
        to_email: 'aagosh@radianceoverseas.com'
      };

      // EmailJS send
      if (window.emailjs) {
        emailjs.send('service_4tenaxt', 'template_radiance', data)
          .then(function() {
            showFormSuccess();
            form.reset();
          })
          .catch(function() { showFormError(); })
          .finally(function() { btn.textContent = origText; btn.disabled = false; });
      } else {
        // Fallback: open mailto
        window.location = `mailto:info@radianceoverseas.com?subject=${encodeURIComponent(data.subject)}&body=${encodeURIComponent(data.message)}`;
        btn.textContent = origText; btn.disabled = false;
      }
    });
  }

  function showFormSuccess() {
    const msg = document.getElementById('form-success');
    if (msg) { msg.style.display = 'block'; setTimeout(function() { msg.style.display = 'none'; }, 5000); }
  }
  function showFormError() {
    alert('Message could not be sent. Please email us directly at info@radianceoverseas.com');
  }

  /* ── BLOG LOADER ─────────────────────────────────────────────── */
  function loadBlogPosts() {
    const container = document.getElementById('blog-posts-container');
    if (!container) return;

    fetch('https://www.radianceoverseas.com/blogs/wp-json/wp/v2/posts?per_page=6&_embed')
      .then(function(r) { return r.json(); })
      .then(function(posts) {
        container.innerHTML = '';
        posts.forEach(function(post) {
          var title = post.title.rendered.replace(/<[^>]*>/g, '');
          var link = post.link;
          var excerpt = post.excerpt.rendered.replace(/<[^>]*>/g, '').substring(0, 200) + '\u2026';
          var date = new Date(post.date).toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' });
          var img = (post._embedded && post._embedded['wp:featuredmedia'] && post._embedded['wp:featuredmedia'][0])
            ? post._embedded['wp:featuredmedia'][0].source_url
            : 'https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?w=600&q=80';

          var card = document.createElement('div');
          card.className = 'blog-card anim-fade-up';

          var imgDiv = document.createElement('div');
          imgDiv.className = 'blog-card-img';
          var imgEl = document.createElement('img');
          imgEl.src = img;
          imgEl.alt = title;
          imgEl.loading = 'lazy';
          imgDiv.appendChild(imgEl);

          var body = document.createElement('div');
          body.className = 'blog-card-body';

          var meta = document.createElement('div');
          meta.className = 'blog-card-meta';
          var tag = document.createElement('span');
          tag.className = 'blog-card-tag';
          tag.textContent = 'Organic';
          var dateSpan = document.createElement('span');
          dateSpan.textContent = '\uD83D\uDCC5 ' + date;
          meta.appendChild(tag);
          meta.appendChild(dateSpan);

          var h3 = document.createElement('h3');
          h3.textContent = title;
          var p = document.createElement('p');
          p.textContent = excerpt;
          var a = document.createElement('a');
          a.href = link;
          a.target = '_blank';
          a.rel = 'noopener';
          a.className = 'read-more';
          a.textContent = 'Read More ';
          var arrow = document.createElement('span');
          arrow.textContent = '\u2192';
          a.appendChild(arrow);

          body.appendChild(meta);
          body.appendChild(h3);
          body.appendChild(p);
          body.appendChild(a);
          card.appendChild(imgDiv);
          card.appendChild(body);
          container.appendChild(card);
        });
        initScrollReveal();
      })
      .catch(function() {
        // Keep the static fallback cards already in HTML — don't wipe them
        console.log('Blog API unavailable — using static cards');
      });
  }

  /* ── INIT ────────────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', function() {
    initNav();
    initHeroSlider();
    initScrollReveal();
    initCounters();
    initFaq();
    initGradeTabs();
    initGallery();
    initContactForm();
    loadBlogPosts();
  });

})();
