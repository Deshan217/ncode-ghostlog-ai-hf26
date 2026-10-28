# N-CODE GhostLog AI: A Haunted Terminal That Tells Stories with Local Gemma

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26).*

## What I Built

I built **N-CODE GhostLog AI**, a local-first Halloween storytelling application that transforms fictional or redacted terminal logs into an original mystery using the **open-weight Gemma 3 1B model** through Ollama.

Users provide imaginary logs, choose a mood, and request a decoded transmission: a story title, narrative, three connected clues, and an eerie final line. This is creative fiction, not a security scanner or evidence of paranormal activity. Input commands are never executed.

## Demo

**Source:** https://github.com/Deshan217/ncode-ghostlog-ai-hf26

**Verified model test and recorded video:** [INSERT SUCCESSFUL NEW GITHUB ACTIONS RUN URL AND ARTIFACT AFTER VERIFICATION]

**Publicly viewable video:** [ADD VIDEO URL AFTER UPLOADING A REAL RECORDING]

To run locally, install Ollama, pull `gemma3:1b`, run `python server.py`, and open `http://127.0.0.1:8766`. This is not a publicly hosted application.

## Code

https://github.com/Deshan217/ncode-ghostlog-ai-hf26

The MIT-licensed repository contains the Python server, Ollama integration, responsive browser UI, automated tests and a GitHub Actions workflow.

## How I Built It

1. The user provides fictional computer logs and chooses a tone.
2. A local Python web server validates the input and sends a structured prompt to Ollama.
3. The open-weight Gemma 3 1B model generates an original narrative with three clues.
4. The server validates model output before rendering in the browser. Missing inference returns an error, never fake output.
5. The user downloads a Markdown version of the story.

The server listens only on localhost, restricts origins and input size, and renders generated content safely through DOM text nodes.

**Verified real test results:** [ADD ACTUAL WORKFLOW RUN ID, MODEL OUTPUT, VIDEO AND SCREENSHOT.]

## Why Does Open Innovation Matter?

A locally runnable open-weight model makes the storytelling experience inspectable, customizable, and operable without a proprietary text-generation API. The prompts and validation code are public. While this project source is MIT licensed, the model weights have their own terms.

## Ghost in the Machine

A fictional computer remembers obsolete sessions, mysterious file playback, and forgotten messages. GhostLog uses those eerie hints to create stories about the histories machines seem to hold.

## What's Next?

I would add more moods and language options, optional local story history, keyboard accessibility improvements and improved model-response validation.

**Built by N-CODE STUDIO for Hacktoberfest 2026.**

---

Before publishing: replace placeholders with actual evidence. Use official Week 4 template and required `devchallenge` / `hf26challenge` tags. Do not claim fully hosted AI. Deadline October 31, 2026, 11:59 PM PDT.
