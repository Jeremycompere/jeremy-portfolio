// Scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// Stagger children of gig grid
document.querySelectorAll('.gig-card, .rate-card').forEach((el, i) => {
  el.style.transitionDelay = (i * 0.07) + 's';
  el.classList.add('fade-up');
  observer.observe(el);
});

// Hide broken images gracefully (show placeholder bg instead)
document.querySelectorAll('.gig-media img, .hero-photo-frame img').forEach(img => {
  img.addEventListener('error', function() {
    this.classList.add('img-error');
  });
  // If already broken (cached error)
  if (img.complete && img.naturalWidth === 0) {
    img.classList.add('img-error');
  }
});

// ── VIDEO LIGHTBOX MODAL ──
(function () {
  const modal = document.getElementById('video-modal');
  if (!modal) return;
  const backdrop = modal.querySelector('.video-modal-backdrop');
  const closeBtn = modal.querySelector('.video-modal-close');
  const iframe = document.getElementById('video-modal-iframe');

  function openModal(src) {
    iframe.src = src;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    // Clear iframe after transition to stop playback
    setTimeout(function () { iframe.src = ''; }, 320);
  }

  // Play buttons trigger modal
  document.querySelectorAll('.gig-video-btn[data-video]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      openModal(btn.getAttribute('data-video'));
    });
  });

  // Close on X button
  closeBtn.addEventListener('click', closeModal);

  // Close on backdrop click
  backdrop.addEventListener('click', closeModal);

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
})();
