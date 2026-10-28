# N-CODE GhostLog AI: Turning Forgotten Logs into Halloween Stories with Gemma

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26).*

## What I Built

I built **N-CODE GhostLog AI**, a local Halloween storytelling application powered by **Gemma 3 1B through Ollama**.

The idea is simple: what if an old computer's forgotten logs could tell a ghost story?

Users enter fictional terminal logs, choose an unsettling, melancholic, or playful mood, and decode a transmission. Gemma generates a title, a 110–190 word story, three clues, and a haunting final line. Users can download the result as Markdown.

The sample includes an archived session resuming after 13 years, a user called `nobody_here`, and a notification saying, “you forgot the light.”

These are creative prompts. GhostLog does not execute commands, scan a computer, or diagnose security incidents.

## Demo

![GhostLog displaying an actual Gemma-generated story](https://raw.githubusercontent.com/Deshan217/ncode-ghostlog-ai-hf26/75e92fc995cd924614391aa1981b234ac43a898a/docs/demo/ghostlog-real-gemma-output.png)

[Open the recorded browser walkthrough](https://github.com/Deshan217/ncode-ghostlog-ai-hf26/blob/75e92fc995cd924614391aa1981b234ac43a898a/docs/demo/ghostlog-real-ai-demo.webm) · [Direct video download](https://raw.githubusercontent.com/Deshan217/ncode-ghostlog-ai-hf26/75e92fc995cd924614391aa1981b234ac43a898a/docs/demo/ghostlog-real-ai-demo.webm).

The recording shows the real application calling local Gemma. The same browser test verifies the Markdown export and captures the mobile layout.

[Verified GitHub Actions run](https://github.com/Deshan217/ncode-ghostlog-ai-hf26/actions/runs/40669822794) · [Evidence and reproduction notes](https://github.com/Deshan217/ncode-ghostlog-ai-hf26/blob/75e92fc995cd924614391aa1981b234ac43a898a/docs/VERIFICATION.md)

This is a local application, rather than a publicly hosted AI service. Judges can reproduce it with Python 3.10+ and Ollama:

```bash
git clone https://github.com/Deshan217/ncode-ghostlog-ai-hf26.git
cd ncode-ghostlog-ai-hf26
ollama pull gemma3:1b
# Start ollama serve separately if Ollama is not already running.
python server.py
```

Then open `http://127.0.0.1:8766`. No app account or API key is required. Model downloads need internet access; generation uses the local Ollama endpoint.

## Code

[Source repository](https://github.com/Deshan217/ncode-ghostlog-ai-hf26) · [Verified application commit](https://github.com/Deshan217/ncode-ghostlog-ai-hf26/commit/c0027f889a12e66a58dfbf5b598864d4363cf945)

The application code is MIT licensed. Gemma's weights have their own terms.

## How I Built It

The application uses Python's standard library for the local HTTP server and HTML, CSS, and JavaScript for the interface. It needs no pip or npm packages to run. Node, Playwright, and Chrome are used by CI to record the demo.

The data flows from the browser to `/api/haunt`, through input validation, into Ollama's local `/api/generate` endpoint. Gemma produces JSON, the server validates it, and the interface renders the fields as text.

### A green test was not enough

The earlier workflow completed real inference, but its saved API result contained only **“A descent into a forgotten memory.”** That passed because the test checked only for a nonempty story and three clues.

It proved the model ran. It did not prove the storytelling requirement worked.

I strengthened the integration to pass an explicit JSON schema, require 110–190 story words, reject malformed or unfinished responses, and allow one validation retry. If both outputs fail, the app reports an error instead of inserting a canned story.

The updated verification checks the raw model response against the application output. The browser test independently generates a story, verifies the rendered narrative matches the API response, and checks the downloaded Markdown.

**Verified results on October 28, 2026:** 19 automated tests passed; actual API generation produced 149 story words and browser generation produced 155 words. Both used `gemma3:1b` and returned three clues. The evidence records the source commit, Ollama version, model digest, and raw generated text.

One stricter CI run returned an error; the subsequent evidence run passed with the same generation code. These are successful examples, not a measured reliability rate. Word counts and JSON checks also do not establish whether every story is creative or every clue is well grounded.

## Why Does Open Innovation Matter?

Gemma is the part that turns the fictional clues into a new narrative. Without the model, this application would be an input form with no story engine.

Running the open-weight model through Ollama means the text-generation request goes to the user's machine rather than a proprietary hosted language-model API. The prompt and validation code are available to inspect and change.

That makes the experiment easier to reproduce and adapt. It also keeps the project independent of a paid text-generation API.

GhostLog does not save input history. I still recommend fictional or fully redacted logs: local processing is not a reason to paste credentials or personal information. I have not measured performance across different hardware or formally tested an offline installation.

## Prize Categories

**Best Use of Gemma** — Gemma 3 1B generates the narrative, clues, title, and final line through the application's actual inference path.

## What's Next?

I would test more inputs and moods, evaluate how consistently clues connect to the supplied logs, and improve the experience on slower computers.

**Built by N-CODE STUDIO for Hacktoberfest 2026.**

*AI assistance was used for implementation, debugging, verification, and drafting this write-up.*

References: [Ollama structured-output documentation](https://docs.ollama.com/capabilities/structured-outputs). Two useful community discussions were [Ollama Structured Outputs in Practice — Getting Type-Safe JSON from Local LLMs with Pydantic](https://dev.to/jangwook_kim_e31e7291ad98/ollama-structured-outputs-in-practice-getting-type-safe-json-from-local-llms-with-pydantic-m38) by [@jangwook_kim_e31e7291ad98](https://dev.to/jangwook_kim_e31e7291ad98) and [Structured Output Gives You Syntax. It Doesn't Give You Semantics](https://dev.to/aiexplore369zoho/structured-output-gives-you-syntax-it-doesnt-give-you-semantics-3c13) by [@aiexplore369zoho](https://dev.to/aiexplore369zoho).
