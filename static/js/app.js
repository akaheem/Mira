/* Mira -- progressive enhancement only.
 *
 * Everything in this file is layered on top of pages that already work. Every flow in
 * Mira is complete with JavaScript disabled; if this file fails to load, nothing breaks.
 * There is no framework here and no dependency to install.
 */
(function () {
  "use strict";

  /* -------------------------------------------------------------------------
   * Location switcher
   *
   * The switcher is a native <details> element and opens and closes on its own.
   * This only adds dismissal on outside-click and Escape.
   * ---------------------------------------------------------------------- */

  function closeOnOutsideClick() {
    var open = document.querySelectorAll("details.loc-switcher[open]");
    if (!open.length) return;

    Array.prototype.forEach.call(open, function (details) {
      function dismiss(event) {
        if (!details.contains(event.target)) {
          details.removeAttribute("open");
          teardown();
        }
      }

      function onKey(event) {
        if (event.key === "Escape") {
          details.removeAttribute("open");
          details.querySelector("summary").focus();
          teardown();
        }
      }

      function teardown() {
        document.removeEventListener("click", dismiss);
        document.removeEventListener("keydown", onKey);
      }

      document.addEventListener("click", dismiss);
      document.addEventListener("keydown", onKey);
    });
  }

  /* -------------------------------------------------------------------------
   * Journey sharing -- entirely client-side
   *
   * Design constraints, and why they are not negotiable:
   *
   *   1. No network request. The summary is assembled here, in the page, from
   *      values Mira is already displaying, and handed to the OS share sheet or
   *      the clipboard. It is never sent to Mira's server.
   *
   *   2. No share link. A short URL would be more convenient and would also mean
   *      every shared journey passes through a server that can log it -- which
   *      defeats the entire point. The cost is a longer message.
   *
   *   3. Nothing the student typed can reach this element. The summary is built
   *      only from route properties rendered by the server.
   *
   *   4. The button ships `hidden` in the HTML and is revealed here, so a browser
   *      without JavaScript shows no control that cannot work.
   * ---------------------------------------------------------------------- */

  function buildSummary(button) {
    var get = function (name) {
      return (button.getAttribute("data-share-" + name) || "").trim();
    };

    var lines = [];
    var to = get("to");
    var from = get("from");

    if (to) {
      lines.push("Going to " + to + (from ? " from " + from : "") + ".");
    }

    var modes = get("modes");
    if (modes) {
      lines.push(modes.charAt(0).toUpperCase() + modes.slice(1) + ".");
    }

    var detail = [];
    var duration = get("duration");
    if (duration && duration !== "unknown") {
      detail.push("about " + duration);
    }
    var walk = get("walk");
    if (walk && walk !== "0") {
      detail.push("about " + walk + " m walk at the end");
    }
    if (detail.length) {
      lines.push("Takes " + detail.join(", ") + ".");
    }

    var fare = get("fare");
    if (fare) {
      var fareNote = get("fare-note");
      lines.push("Fare: " + fare + (fareNote ? " (" + fareNote.toLowerCase() + ")" : "") + ".");
    } else {
      lines.push("Fare: not shown - confirm with the driver before travelling.");
    }

    var last = get("last");
    if (last) {
      lines.push("Last departure: " + last + ".");
    }
    if (get("dark")) {
      lines.push("Note: the last departure is after dark.");
    }

    lines.push("Fares and timings change - confirm before you travel.");
    return lines.join("\n");
  }

  function statusFor(button) {
    var foot = button.closest ? button.closest(".card-foot") : null;
    return (foot || document).querySelector("[data-share-status]");
  }

  function setStatus(button, message, isError) {
    var el = statusFor(button);
    if (!el) return;
    el.textContent = message;
    el.className = isError ? "meta meta-warn" : "meta";
  }

  /* Last resort: show the text in a selectable box. Some browsers expose neither
   * the share sheet nor the clipboard API outside a secure context, and a button
   * that silently does nothing is worse than one that hands you the text. */
  function manualCopy(button, text) {
    var existing = button.parentNode.querySelector("[data-share-manual]");
    if (existing) {
      existing.focus();
      existing.select();
      return;
    }

    var box = document.createElement("textarea");
    box.className = "share-manual";
    box.setAttribute("data-share-manual", "");
    box.setAttribute("readonly", "readonly");
    box.setAttribute("rows", "5");
    box.setAttribute("aria-label", "Journey summary to copy");
    box.value = text;
    button.parentNode.insertBefore(box, button.nextSibling);
    box.focus();
    box.select();
    setStatus(button, "Select and copy the text above.", false);
  }

  function copyToClipboard(button, text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () {
          setStatus(button, "Copied. Paste it to whoever you want to tell.", false);
        },
        function () {
          manualCopy(button, text);
        }
      );
      return;
    }
    manualCopy(button, text);
  }

  function share(button) {
    var text = buildSummary(button);

    if (navigator.share) {
      navigator.share({ text: text }).catch(function (error) {
        // The student dismissing the share sheet is a normal outcome, not a failure.
        if (error && error.name === "AbortError") return;
        copyToClipboard(button, text);
      });
      return;
    }

    copyToClipboard(button, text);
  }

  function wireSharing() {
    var buttons = document.querySelectorAll("[data-share-journey]");
    Array.prototype.forEach.call(buttons, function (button) {
      button.hidden = false;
      button.addEventListener("click", function () {
        share(button);
      });
    });
  }

  /* -------------------------------------------------------------------------
   * Time-of-day greeting
   *
   * Computed in the browser, not on the server, and that is the whole point.
   * The function runs in one region; the student may be eight timezones away.
   * A server-rendered "Good evening" is correct for whoever the server is
   * near and wrong for everyone else, which is a small untruth on the one
   * screen whose job is to establish that Mira does not say things it cannot
   * support.
   *
   * If this file does not load, the element stays empty and hidden, and the
   * heading underneath reads correctly on its own. Nothing is lost.
   * ---------------------------------------------------------------------- */

  function setGreeting() {
    var el = document.querySelector("[data-greeting]");
    if (!el) return;

    var hour = new Date().getHours();
    var greeting;

    if (hour >= 5 && hour < 12) {
      greeting = "Good morning.";
    } else if (hour >= 12 && hour < 18) {
      greeting = "Good afternoon.";
    } else {
      greeting = "Good evening.";
    }

    el.textContent = greeting;
  }

  document.addEventListener("DOMContentLoaded", function () {
    setGreeting();
    wireSharing();

    document.addEventListener("click", function (event) {
      var summary = event.target.closest && event.target.closest(".loc-summary");
      if (summary) {
        // Let the browser toggle first, then bind the dismissal handlers.
        window.setTimeout(closeOnOutsideClick, 0);
      }
    });
  });
})();
