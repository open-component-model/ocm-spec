// @ts-check

"use strict";

// Custom markdownlint rule: enforce the American spelling "artifact".
//
// The OCM specification standardized on the spelling "artifact" (see
// open-component-model/ocm-spec PR #40, "refactor: use artifact instead of
// artefact everywhere"). The British spelling "artefact" occasionally creeps
// back in (e.g. new label conventions, example YAML like `ociArtefact`), which
// breaks terminology consistency and, worse, produces wire-format identifiers
// that differ only by spelling.
//
// This rule fails linting whenever "artefact"/"Artefact" (in any casing) is
// used, and points the author at the correct spelling.

const artefactRegex = /artefact/gi;

module.exports = {
  names: ["OCM001", "no-artefact-spelling"],
  description:
    'Use the spelling "artifact" instead of "artefact" (OCM spec convention)',
  information: new URL(
    "https://github.com/open-component-model/ocm-spec/pull/40"
  ),
  tags: ["spelling", "terminology", "ocm"],
  parser: "none",
  function: function noArtefactSpelling(params, onError) {
    for (const [lineIndex, line] of params.lines.entries()) {
      let match;
      // Reset lastIndex because the regex is stateful (global flag).
      artefactRegex.lastIndex = 0;
      while ((match = artefactRegex.exec(line)) !== null) {
        const found = match[0];
        // Preserve the original casing when suggesting the fix.
        const replacement = found
          .replace(/artefact/g, "artifact")
          .replace(/Artefact/g, "Artifact")
          .replace(/ARTEFACT/g, "ARTIFACT");
        onError({
          lineNumber: lineIndex + 1,
          detail: `Found "${found}"; use "${replacement}" instead.`,
          context: line.trim().slice(0, 100),
          range: [match.index + 1, found.length],
          fixInfo: {
            editColumn: match.index + 1,
            deleteCount: found.length,
            insertText: replacement,
          },
        });
      }
    }
  },
};
