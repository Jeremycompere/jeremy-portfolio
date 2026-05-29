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
