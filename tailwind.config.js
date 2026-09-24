/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/js/**/*.js"],

  // Tailwind only emits a class it can find as a literal string in `content`. Three
  // classes in _macros.html are built by interpolation instead, so the scanner sees
  // `chip-` and `prov-note-` and never the finished name:
  //
  //     class="chip chip-{{ record.provenance_state }}"
  //     class="prov-note prov-note-{{ record.provenance_state }}"
  //     class="chip-mark chip-mark-{{ condition.provenance }}"
  //
  // Without this list those three families compile to nothing, and the failure is quiet:
  // the markup is correct, the page renders, and the provenance chips -- the one visual
  // element this whole product is built around -- come out unstyled. Two of the three
  // states happen to appear literally in about.html, which is exactly what would make the
  // gap hard to notice in a spot check.
  //
  // If a state is ever added to PROVENANCE_STATES, add its classes here too.
  safelist: [
    "chip-verified", "chip-illustrative", "chip-unverified",
    "prov-note-verified", "prov-note-illustrative", "prov-note-unverified",
    "chip-mark-verified", "chip-mark-illustrative", "chip-mark-unverified",
  ],

  theme: {
    extend: {
      colors: {
        // -- Surfaces ------------------------------------------------------------------
        // Warm off-white rather than pure white everywhere. Pure white at full-screen
        // brightness is harsh on a phone held up on a bus, and this app is read in
        // exactly those conditions.
        //
        // The scales are named for what they ARE, not for a hue that used to be there.
        // The previous palette called the surface scale `sand` and the brand scale
        // `plum`; redefining those hexes under the old names would have left `plum-700`
        // resolving to a teal, which is a name that lies to the next person to read it.
        ink: "#1A1D1C",     // body text. Near-black, faintly green so it sits with the teal
        quiet: "#515A57",   // secondary text. 6.7:1 on paper-100
        paper: {
          50: "#FFFFFF",    // soft white -- resource, help and process cards
          100: "#F7F8F5",   // warm off-white -- the page itself
          200: "#EDEFE9",   // inset fills, hairline rules
          300: "#DCE0D8",   // borders
        },

        // -- Brand ---------------------------------------------------------------------
        // Deep teal. It carries trust without the clinical coldness of navy, which is the
        // specific failure this palette exists to avoid: a support tool that looks like a
        // government form gets opened less, and this one is already competing with not
        // being opened at all.
        teal: {
          50: "#EDF4F5",
          100: "#D6E6E9",
          200: "#AECED4",
          400: "#5F94A0",   // decorative marks only, never text on a light surface
          600: "#1A6273",   // links, focus. 6.8:1 on paper-50
          700: "#124E5A",   // THE primary. 9.2:1 against white, both directions
          800: "#0C3A44",   // pressed/hover
        },

        // Mist aqua. Informational and supportive surfaces -- the blocks that are telling
        // you something rather than asking you to do something.
        aqua: {
          50: "#F2F9F8",
          100: "#E7F4F2",
          200: "#CCE6E2",
          700: "#1D5B54",   // 6.9:1 on aqua-100
        },

        // Soft coral. Used where the interface needs to be *noticed*: an urgent notice, a
        // stale-data warning. Deliberately sparse -- if every card is coral, none is.
        // coral-400 is a surface/accent tone only; it is ~2:1 on white and must never
        // carry text.
        coral: {
          100: "#FBE9E7",
          200: "#F4CBC5",
          400: "#E89A91",
          700: "#8E3A2E",   // 6.4:1 on coral-100
        },

        // Lavender. Decorative only -- quiet fills behind supportive copy, never a status
        // and never a call to action.
        lavender: {
          100: "#EFEDFA",
          200: "#DCD9F4",
          700: "#3E3A6B",
        },

        // -- Status --------------------------------------------------------------------
        // Three provenance states need three tones that are distinguishable from each
        // other, and none of them may be the ONLY signal -- each is paired with a glyph
        // (check / diamond / bang) and a word, because colour alone fails roughly 1 in 12
        // men and fails completely in forced-colours mode.
        //
        // Verified is green rather than teal on purpose. If the trust marker were the same
        // hue as every button on the page, "this is verified" would stop reading as a
        // distinct claim and start reading as chrome.
        moss: { 100: "#E4F1E8", 700: "#2C6247" },   // verified.   6.1:1
        iris: { 100: "#EAECF7", 700: "#3C4173" },   // illustrative -- neutral, not a warning. 8.1:1
        amber: { 100: "#FAF0DA", 700: "#805312" },  // not yet verified, and stale. 5.9:1

        // Each pairing above is checked for contrast on its own tint; see
        // `verify_contrast.py` for the arithmetic rather than trusting these comments.
      },

      fontFamily: {
        // Self-hosted, latin subset, woff2 only, declared in static/css/input.css.
        //
        // This REVERSES an earlier decision to ship no webfont at all, on the grounds that
        // 30-100KB is a real cost on a connection where the student is already waiting.
        // That cost was real; it was accepted deliberately, because the owner's design
        // direction needs an editorial serif for hierarchy and a screen-tuned sans for
        // body text, and no system stack provides both across Windows, macOS, Android and
        // iOS. The bill is 95KB for the whole type system -- Inter is one variable file
        // covering 100-900, and DM Serif Display's italic is only fetched on the one page
        // that uses it.
        //
        // The rule that survives: nothing is fetched from a third-party CDN. A font
        // request to fonts.googleapis.com would leak the reader's IP and the page they
        // are on to a third party, on a product whose entire argument is that it does not
        // do things like that quietly.
        sans: [
          "Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto",
          "Helvetica Neue", "Arial", "sans-serif",
        ],
        display: [
          "DM Serif Display", "Georgia", "Cambria", "Times New Roman", "serif",
        ],
      },

      maxWidth: { content: "44rem" },

      // Spacious, not pill-shaped. 24px is generous enough to read as "card" rather than
      // "box" at phone width without the corners eating the first character of a line.
      borderRadius: { card: "1.5rem" },
    },
  },

  plugins: [],
};
