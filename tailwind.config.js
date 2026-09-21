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
        // Warm rather than clinical. A support tool that looks like a government form
        // gets used less, and this one is competing with not being opened at all.
        ink: "#241C22",
        quiet: "#5A5560",
        plum: {
          50: "#FBF5F8",
          100: "#F5E6EC",
          200: "#E8C9D6",
          400: "#A85C7E",
          600: "#8A3A61",
          700: "#6D2B4C",
          800: "#4E1E36",
        },
        sand: {
          50: "#FDFAF7",
          100: "#FAF6F2",
          200: "#F1E9E1",
          300: "#E3D6C9",
        },
        // Status colours. Each pairing below is checked for contrast on its own tint.
        //
        // Three provenance states need three tones that are distinguishable from each
        // other, and none of them may be the ONLY signal -- each is paired with a glyph
        // (check / diamond / bang) and a word, because colour alone fails roughly 1 in 12
        // men and fails completely in forced-colours mode.
        moss: { 100: "#E3F1E9", 700: "#2F6B4F" },   // verified
        iris: { 100: "#E9EAF6", 700: "#3E4275" },   // illustrative -- neutral, not a warning
        amber: { 100: "#FBEFD9", 700: "#8A5A12" },  // not yet verified, and stale
        brick: { 100: "#FBE7E4", 700: "#8C2F22" },  // urgent
      },
      fontFamily: {
        // System stack on purpose. A webfont is 30-100KB on a connection where the
        // student is already waiting; the platform font costs nothing and reads well.
        sans: [
          "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto",
          "Helvetica Neue", "Arial", "sans-serif",
        ],
      },
      maxWidth: { content: "44rem" },
    },
  },
  plugins: [],
};
