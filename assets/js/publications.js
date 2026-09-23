// Publication list behaviour. Runs on /publications/ and on the about page,
// which render the same `.publications ol.bibliography`.
(function () {
  "use strict";

  // Clears the fixed navbar, matching tocbot's `headingsOffset`.
  var NAV_OFFSET = 84;
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function linkTitles() {
    document.querySelectorAll(".publications ol.bibliography > li").forEach(function (entry) {
      var title = entry.querySelector(".title");
      if (!title || title.querySelector("a")) return;

      // The title goes to the paper's page, DOI first: it is the permanent one.
      // The PDF keeps its own button unless it is all the entry has.
      var doi = null;
      var html = null;
      var pdf = null;

      entry.querySelectorAll(".links a[href]").forEach(function (link) {
        var label = link.textContent.trim().toLowerCase();
        if (label === "doi") doi = link;
        else if (label === "html") html = link;
        else if (label === "pdf") pdf = link;
      });

      var target = doi || html || pdf;
      if (!target) return;

      var anchor = document.createElement("a");
      anchor.href = target.href;
      if (target.target) anchor.target = target.target;
      anchor.rel = "noopener";
      anchor.innerHTML = title.innerHTML;
      title.textContent = "";
      title.appendChild(anchor);

      // The button the title just took would say the same thing twice.
      target.remove();
    });
  }

  // The gem's `common.js` marks every `.publications h2` `data-toc-skip`, so the
  // year headings never reach tocbot. On this page they are the only headings
  // and they are exactly what the sidebar is for, so un-skip and rebuild.
  function yearSidebar() {
    var sidebar = document.querySelector("#toc-sidebar");
    if (!sidebar || !window.tocbot) return;

    var headings = document.querySelectorAll(".publications h2");
    if (!headings.length) return;

    headings.forEach(function (heading) {
      heading.removeAttribute("data-toc-skip");
      if (!heading.id) heading.id = "year-" + heading.textContent.trim();
    });

    if (typeof window.tocbot.destroy === "function") window.tocbot.destroy();
    window.tocbot.init({
      tocSelector: "#toc-sidebar",
      contentSelector: '[role="main"]',
      headingSelector: "h2, h3",
      ignoreSelector: "[data-toc-skip]",
      hasInnerContainers: true,
      orderedList: false,
      activeLinkClass: "is-active-link",
      scrollSmooth: true,
      scrollSmoothOffset: -80,
      headingsOffset: 80,
    });

    var label = document.createElement("p");
    label.className = "pub-years__label";
    label.textContent = "years";
    sidebar.insertBefore(label, sidebar.firstChild);

    // A link click must not reach the URL hash: the gem's `bibsearch.js` reads
    // it as the search query and empties the list. Capture phase, so tocbot's
    // own handler never runs.
    sidebar.addEventListener(
      "click",
      function (event) {
        var link = event.target.closest(".toc-link");
        if (!link) return;
        var heading = document.getElementById(decodeURIComponent((link.getAttribute("href") || "").slice(1)));
        if (!heading) return;

        event.preventDefault();
        event.stopPropagation();
        var top = heading.getBoundingClientRect().top + window.scrollY - NAV_OFFSET;
        window.scrollTo({ top: Math.max(0, top), behavior: reducedMotion.matches ? "auto" : "smooth" });
      },
      true
    );
  }

  // One height for every card. Each year is its own `ol`, so a grid cannot
  // reach across them. Scoped to `.pub-layout`: about's entries are not boxed.
  function evenCards() {
    var cards = document.querySelectorAll(".pub-layout .publications ol.bibliography > li");
    if (!cards.length) return;

    cards.forEach(function (card) {
      card.style.minHeight = "";
    });

    var tallest = 0;
    cards.forEach(function (card) {
      tallest = Math.max(tallest, card.getBoundingClientRect().height);
    });

    cards.forEach(function (card) {
      card.style.minHeight = Math.ceil(tallest) + "px";
    });
  }

  function init() {
    linkTitles();
    yearSidebar();
    evenCards();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Images land after first paint and titles rewrap on resize.
  window.addEventListener("load", evenCards);

  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(evenCards, 150);
  });
})();
