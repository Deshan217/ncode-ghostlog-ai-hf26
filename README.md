# N-CODE GhostLog AI 👻

**Hacktoberfest 2026 · Week 4 · Ghost in the Machine**

An original, local-first Halloween storytelling experience. Paste fictional or fully redacted terminal log lines; open-weight **Gemma 3 1B** running via **Ollama** interprets those clues as a spooky fictional transmission, a three-clue trail and an eerie final line.

Created during the Week 4 contest window, October 28, 2026. Open source under MIT. Built by N-CODE STUDIO.

> **Not a forensic/security tool.** GhostLog invents stories, not evidence of cyber threats or paranormal activity. It never runs input commands.

## Why this fits the theme

"Ghost in the Machine" becomes a fictional story engine: an old system's logs whisper a tale. Using a **locally runnable open-weight model** makes the storytelling logic accessible and swappable and means fictional prompts aren't transmitted to a proprietary hosted model.

## Get running (Windows / macOS / Linux)

Prerequisites: Python 3.10+, [Ollama](https://ollama.com/download) and the Gemma 3 model.

```bash
ollama pull gemma3:1b
# If Ollama is not already running, in a separate terminal:
ollama serve
# In this project folder:
python server.py
```

On Windows, `py -3 server.py` works. Or double-click `start-windows.bat`. Visit **http://127.0.0.1:8766**.

No npm or pip dependencies are required to *run* the application. Node and Playwright are used only by the CI screenshot/video capture workflow.

## Real AI functionality

- Responds to user-supplied *fictional/redacted* log entries and selected tone.
- Calls `http://127.0.0.1:11434/api/generate` using Ollama and `gemma3:1b` with a JSON schema, response validation, and a 110–190 word story check.
- Produces a 110–190 word fictional story, three clues, and a final line. Malformed or out-of-range output gets one retry, then a clear error.
- Reports a clear error when the model is unavailable; does **not** fake AI output.
- Lets you download a Markdown story.
- Binds local-only web server (`127.0.0.1:8766`), restricts request sizes and external origins, does not store input history.

**Generation time:** the model call can take up to 140 seconds per attempt. One output-validation retry is allowed, so slow machines may take several minutes.

**Privacy caveat:** You control the local Ollama process, but should still avoid pasting secrets or personal logs; GhostLog was designed for fictional or redacted inputs. Logs are not sent to any cloud model by this code. Model artifacts are subject to their respective licenses.

## Testing

```bash
python -m unittest discover -s tests -v
python -m py_compile engine.py server.py
```

Unit tests mock model outputs. **Unit tests are not evidence of real AI execution.** The included GitHub Actions workflow also installs Ollama, runs real `gemma3:1b` through the actual `/api/haunt` route and records a real browser demonstration with Playwright and Chrome. When the workflow completes, download the **ghostlog-real-gemma-demo** artifact for model JSON, a real video `.webm`, and PNG screenshots.

### Project layout

- `server.py` — local HTTP server + guarded JSON API
- `engine.py` — prompt, local Ollama call, structured response validation
- `static/` — dark, responsive web interface
- `tests/` — API/input checks
- `scripts/` — real model proof and headless browser recording
- `.github/workflows/verify.yml` — tests, local AI inference, demo artifact
- `DEV_SUBMISSION_DRAFT.md` — submission article starter

## Hacktoberfest Week 4

- [Official Ghost in the Machine challenge](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)
- Rules: a **brand-new project** during Oct 26–31, open-source AI at its core, a DEV post with the official template/tags, public code, actual demo, and an explanation of why open innovation matters.
- **Deadline:** Oct 31, 2026, 11:59 PM PDT = **Nov 1, 2026, 12:29 PM in Sri Lanka**.
- A green GitHub workflow and an uploaded video are proof of tests, but do **not** themselves submit a DEV challenge entry. Publish the DEV article separately.

## Limits

- Real inference evidence is linked in docs/VERIFICATION.md; passing these examples does not establish a reliability rate across all inputs.
- Local demo, not a publicly hosted SaaS app.
- AI may hallucinate, omit clues, or fail schema validation; errors are surfaced rather than substituted with a fake response.
- No malware diagnosis or shell command execution.

MIT License © 2026 N-CODE STUDIO.

## Source preservation and evidence

The supplied project ZIP was retained unchanged. Every original file path was present in the existing repository at commit 4512b5a; existing GitHub edits were used as the baseline. The archive SHA-256 and the original file hashes are in [docs/original-zip-manifest.json](docs/original-zip-manifest.json).

See [docs/VERIFICATION.md](docs/VERIFICATION.md) for the verified commit, actual inference output, screenshots, video, and limitations. The DEV article remains a draft until explicitly published.
