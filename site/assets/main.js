// shihabarch.tech — interactions (reveal on scroll, stat count-up). No dependencies.
(function () {
  // mark JS as available — .reveal is only hidden when this runs (no-JS browsers see everything)
  document.documentElement.classList.add("js");
  // reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // count-up for numeric stats
  function countUp(el) {
    const target = parseInt(el.dataset.count, 10);
    if (isNaN(target)) return;
    const dur = 1300, t0 = performance.now();
    const fmt = new Intl.NumberFormat("en-US");
    function frame(t) {
      const p = Math.min((t - t0) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt.format(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  const statIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { countUp(e.target); statIO.unobserve(e.target); } });
  }, { threshold: 0.4 });
  document.querySelectorAll("[data-count]").forEach((el) => statIO.observe(el));
})();
