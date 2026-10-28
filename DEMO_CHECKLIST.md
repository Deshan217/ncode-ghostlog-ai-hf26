# Demo and submission checklist

- Use only the synthetic sample logs included in the app; no personal logs or credentials.
- Confirm the GitHub Actions run linked in `docs/VERIFICATION.md` is successful at the stated source commit.
- Inspect `real-gemma-story.json`: model name, Ollama version, model digest, completed response, 110–190 story words, and three clues.
- Inspect `browser-gemma-story.json`: this is a separate actual generation initiated by the UI.
- Watch the recorded video and open the desktop and mobile screenshots.
- Open the exported Markdown and confirm it contains the generated story.
- The public video and screenshots are under `docs/demo/`; the original CI artifact is linked for provenance.
- Review `DEV_SUBMISSION_DRAFT.md` using the official Week 4 template. Required tags: `devchallenge`, `hf26challenge`.
- Enter Best Use of Gemma based on the actual application inference. Claim other categories only for meaningful uses you can demonstrate.
- The application runs locally; it has no hosted inference URL and needs no app login.
- Review the article and publish it on DEV before the official deadline. A repository upload or saved DEV draft does not submit an entry.
- Official cutoff: October 31, 2026, 11:59 PM PDT, which is November 1, 2026, 12:29 PM in Sri Lanka.

Rules: https://dev.to/page/hacktoberfest-week4-2026-10-26-contest-rules
