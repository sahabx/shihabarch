// Shihab's Architecture — interactions (nav toggle, reveal, count-up, interactive canvas background).
// No dependencies.
(function () {
  document.documentElement.classList.add("js");

  // mobile nav
  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".nav-toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  // reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  // count-up for numeric stats
  function countUp(el) {
    var target = parseInt(el.dataset.count, 10);
    if (isNaN(target)) return;
    var dur = 1300, t0 = performance.now();
    var fmt = new Intl.NumberFormat("en-US");
    function frame(t) {
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt.format(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  var statIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { countUp(e.target); statIO.unobserve(e.target); }
    });
  }, { threshold: 0.4 });
  document.querySelectorAll("[data-count]").forEach(function (el) { statIO.observe(el); });

  initArtifact();

  function initArtifact() {
    var canvas = document.getElementById("arch-canvas");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var w = 0, h = 0, dpr = 1, nodes = [], raf = null;
    var pointer = { x: -1e4, y: -1e4, active: false };
    var palette = ["77,163,255", "139,92,246", "192,132,252", "52,211,153"];

    // Position the canvas to sit exactly behind the first section of the page
    // (the hero on the landing, otherwise the page header), below the sticky nav.
    function layoutCanvas() {
      var sec = document.querySelector("main .hero, main .cs-head, main .page-head");
      if (!sec) return;
      var r = sec.getBoundingClientRect();
      canvas.style.top = Math.round(r.top + window.scrollY) + "px";
      canvas.style.height = Math.round(r.height) + "px";
    }

    function resize() {
      layoutCanvas();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      var rect = canvas.getBoundingClientRect();
      w = Math.max(1, rect.width);
      h = Math.max(1, rect.height);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    }

    function seed() {
      var count = Math.max(42, Math.min(95, Math.round((w * h) / 15000)));
      nodes = [];
      for (var i = 0; i < count; i++) {
        var core = i % 11 === 0;
        nodes.push({
          x: Math.random() * w,
          y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          r: core ? 2.2 + Math.random() * 1.4 : 0.7 + Math.random() * 1.3,
          c: palette[Math.floor(Math.random() * palette.length)],
          core: core,
          ph: Math.random() * Math.PI * 2
        });
      }
    }

    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      var parallax = window.scrollY * 0.35;
      var i, j, a, b;

      // edges between close nodes
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j];
          var dx = a.x - b.x;
          var dy = (a.y + parallax) - (b.y + parallax);
          var d2 = dx * dx + dy * dy;
          if (d2 < 130 * 130) {
            var alpha = (1 - Math.sqrt(d2) / 130) * 0.45;
            ctx.strokeStyle = "rgba(77,163,255," + alpha.toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y + parallax);
            ctx.lineTo(b.x, b.y + parallax);
            ctx.stroke();
          }
        }
      }

      // pointer links
      if (pointer.active) {
        for (i = 0; i < nodes.length; i++) {
          a = nodes[i];
          var pdx = pointer.x - a.x;
          var pdy = pointer.y - (a.y + parallax);
          var pd = Math.hypot(pdx, pdy);
          if (pd < 140) {
            ctx.strokeStyle = "rgba(139,92,246," + ((1 - pd / 140) * 0.7).toFixed(3) + ")";
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y + parallax);
            ctx.lineTo(pointer.x, pointer.y);
            ctx.stroke();
          }
        }
      }

      // nodes
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        var pulse = a.core ? (0.6 + 0.4 * Math.sin(t / 320 + a.ph)) : 1;
        ctx.fillStyle = "rgba(" + a.c + "," + ((a.core ? 0.9 : 0.75) * pulse).toFixed(3) + ")";
        ctx.shadowColor = "rgba(" + a.c + ",0.8)";
        ctx.shadowBlur = a.core ? 12 : 6;
        ctx.beginPath();
        ctx.arc(a.x, a.y + parallax, a.r * (a.core ? 1.15 : 1) * pulse, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // move
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > w) a.vx *= -1;
        if (a.y < 0 || a.y > h) a.vy *= -1;
        if (pointer.active) {
          var rx = a.x - pointer.x;
          var ry = (a.y + parallax) - pointer.y;
          var rd = Math.hypot(rx, ry);
          if (rd < 110 && rd > 0.01) {
            var f = ((110 - rd) / 110) * 1.6;
            a.x += (rx / rd) * f;
            a.y += (ry / rd) * f;
          }
        }
        a.x = Math.max(0, Math.min(w, a.x));
        a.y = Math.max(0, Math.min(h, a.y));
      }
      raf = requestAnimationFrame(frame);
    }

    function frame(t) { draw(t); }

    function drawStatic() {
      ctx.clearRect(0, 0, w, h);
      var parallax = window.scrollY * 0.35;
      var i, j, a, b;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j];
          var dx = a.x - b.x;
          var dy = (a.y + parallax) - (b.y + parallax);
          var d2 = dx * dx + dy * dy;
          if (d2 < 130 * 130) {
            var alpha = (1 - Math.sqrt(d2) / 130) * 0.45;
            ctx.strokeStyle = "rgba(77,163,255," + alpha.toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y + parallax);
            ctx.lineTo(b.x, b.y + parallax);
            ctx.stroke();
          }
        }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        ctx.fillStyle = "rgba(" + a.c + ",0.8)";
        ctx.shadowColor = "rgba(" + a.c + ",0.8)";
        ctx.shadowBlur = a.core ? 12 : 6;
        ctx.beginPath();
        ctx.arc(a.x, a.y + parallax, a.r, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    function start() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
      if (reduce) { drawStatic(); return; }
      raf = requestAnimationFrame(frame);
    }

    function updatePointer(e) {
      var rect = canvas.getBoundingClientRect();
      var y = e.clientY - rect.top;
      if (e.clientY < rect.top || e.clientY > rect.bottom) {
        pointer.active = false;
        pointer.x = -1e4; pointer.y = -1e4;
        return;
      }
      pointer.x = e.clientX - rect.left;
      pointer.y = y;
      pointer.active = true;
    }

    window.addEventListener("pointermove", updatePointer);
    window.addEventListener("pointerdown", updatePointer);
    window.addEventListener("pointerup", function () { pointer.active = false; });

    resize();
    start();

    var resizeTimer;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () { resize(); start(); }, 120);
    });
    // Re-measure once fonts/first paint settle so the height matches the section exactly.
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { resize(); start(); });
    }
    window.addEventListener("load", function () { resize(); start(); });
  }
})();