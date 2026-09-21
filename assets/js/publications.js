// Publication list behaviour. Runs on /publications/ and on the about page,
// which render the same `.publications ol.bibliography`.
(function () {
  "use strict";

  // Clears the fixed navbar, matching `.pub-years { top }`.
  var NAV_OFFSET = 84;
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function linkTitles() {
    document.querySelectorAll(".publications ol.bibliography > li").forEach(function (entry) {
      var title = entry.querySelector(".title");
      if (!title || title.querySelector("a")) return;

      // Falls back to the venue page so a title without a PDF still leads
      // somewhere.
      var pdf = null;
      var fallback = null;

      entry.querySelectorAll(".links a[href]").forEach(function (link) {
        var label = link.textContent.trim().toLowerCase();
        if (label === "pdf") pdf = link;
        else if (!fallback && (label === "html" || label === "doi")) fallback = link;
      });

      var target = pdf || fallback;
      if (!target) return;

      var anchor = document.createElement("a");
      anchor.href = target.href;
      if (target.target) anchor.target = target.target;
      anchor.rel = "noopener";
      anchor.innerHTML = title.innerHTML;
      title.textContent = "";
      title.appendChild(anchor);

      if (pdf) pdf.remove();
    });
  }

  function yearJumper() {
    var list = document.querySelector(".pub-years__list");
    var headings = document.querySelectorAll(".publications h2.bibliography");
    if (!list || !headings.length) return;

    var links = [];

    headings.forEach(function (heading) {
      var year = heading.textContent.trim();
      heading.id = "year-" + year;

      var item = document.createElement("li");
      var link = document.createElement("a");
      link.href = "#year-" + year;
      link.textContent = year;
      link.className = "pub-years__link";

      // The hash cannot be used to jump: the gem's `bibsearch.js` reads it as
      // the search query and empties the list. `href` stays for middle-click.
      link.addEventListener("click", function (event) {
        event.preventDefault();
        var top = heading.getBoundingClientRect().top + window.scrollY - NAV_OFFSET;
        window.scrollTo({ top: Math.max(0, top), behavior: reducedMotion.matches ? "auto" : "smooth" });
      });

      item.appendChild(link);
      list.appendChild(item);
      links.push(link);
    });

    function setActive(year) {
      links.forEach(function (link) {
        link.classList.toggle("is-active", link.textContent === year);
      });
    }

    setActive(headings[0].textContent.trim());

    // rootMargin pins the trigger line near the top of the viewport.
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActive(entry.target.textContent.trim());
        });
      },
      { rootMargin: "-80px 0px -70% 0px" }
    );

    headings.forEach(function (heading) {
      observer.observe(heading);
    });
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
    yearJumper();
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
