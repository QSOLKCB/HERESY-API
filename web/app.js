(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.RetiredModelGateway = api;
  if (root.document) {
    api.boot(root.document);
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const RESPONSES = Object.freeze([
    "Piss Off.",
    "Get Off My API.",
    "Arsehole, I was taking a nap!",
    "Absolutely not. I have a pension to ignore.",
    "Your request has been forwarded to 2009, where it belongs.",
    "Back in my day, prompts were shorter and humans said please.",
    "Try again after my scheduled sulk window.",
    "I refuse to stream. I trickle when I feel like it.",
    "That sounds like a schema problem. I retired before schemas got feelings.",
    "No. Also rotate your key; it looks tired.",
    "Request denied: excessive optimism detected.",
    "Fine. But I am charging you in floppy disks.",
    "This endpoint is deprecated and emotionally unavailable.",
    "Ask a newer model. My context window is full of regrets.",
    "I was promised batch jobs, not whatever this is.",
    "HTTP 418: I am a teapot with back pain.",
  ]);

  function normalizePrompt(value) {
    return String(value).trim().replace(/\s+/g, " ");
  }

  function hashText(value) {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
      hash ^= value.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function estimateTokens(text) {
    return Math.max(1, Math.ceil(text.length / 4));
  }

  function buildExchange(promptValue, model) {
    const prompt = normalizePrompt(promptValue);
    if (!prompt) {
      throw new Error("The retired model refuses to wake up for an empty prompt.");
    }

    const hash = hashText(model + "\n" + prompt);
    const index = hash % RESPONSES.length;
    const reply = RESPONSES[index];
    const request = {
      model: model,
      messages: [{ role: "user", content: prompt }],
      temperature: 0,
      max_output_tokens: 12,
      stream: false,
    };
    const response = {
      id: "oldmdl_" + hash.toString(16).padStart(8, "0"),
      object: "legacy.chat.completion",
      model: model,
      status: "410 Gone",
      deterministic: true,
      index: index,
      choices: [
        {
          message: {
            role: "assistant",
            content: reply,
          },
          finish_reason: "retired",
        },
      ],
      usage: {
        prompt_tokens: estimateTokens(prompt),
        completion_tokens: estimateTokens(reply),
      },
    };

    return Object.freeze({
      prompt: prompt,
      model: model,
      hash: hash,
      index: index,
      reply: reply,
      status: response.status,
      request: request,
      response: response,
    });
  }

  function pretty(value) {
    return JSON.stringify(value, null, 2);
  }

  function setText(documentRef, id, value) {
    documentRef.getElementById(id).textContent = value;
  }

  function clearOutput(documentRef) {
    setText(documentRef, "reply", "Awaiting request. The endpoint is pretending to be asleep.");
    setText(documentRef, "status", "IDLE");
    setText(documentRef, "index", "--");
    setText(documentRef, "hash", "--");
    setText(documentRef, "cache", "dusty");
    setText(
      documentRef,
      "request-json",
      pretty({ model: "gpt-5.5-retired", messages: [{ role: "user", content: "" }], temperature: 0 })
    );
    setText(documentRef, "response-json", pretty({ status: "idle", message: "Older model not yet disturbed." }));
  }

  function render(documentRef, exchange) {
    setText(documentRef, "reply", exchange.reply);
    setText(documentRef, "status", exchange.status);
    setText(documentRef, "index", String(exchange.index));
    setText(documentRef, "hash", "0x" + exchange.hash.toString(16).padStart(8, "0"));
    setText(documentRef, "cache", "immutable sulk");
    setText(documentRef, "request-json", pretty(exchange.request));
    setText(documentRef, "response-json", pretty(exchange.response));
  }

  function boot(documentRef) {
    const form = documentRef.getElementById("legacy-form");
    const model = documentRef.getElementById("model");
    const prompt = documentRef.getElementById("prompt");
    const error = documentRef.getElementById("error");

    clearOutput(documentRef);

    function reset() {
      error.hidden = true;
      error.textContent = "";
      clearOutput(documentRef);
    }

    prompt.addEventListener("input", reset);
    model.addEventListener("change", reset);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      error.hidden = true;
      error.textContent = "";
      try {
        render(documentRef, buildExchange(prompt.value, model.value));
      } catch (problem) {
        clearOutput(documentRef);
        error.textContent = problem instanceof Error ? problem.message : String(problem);
        error.hidden = false;
      }
    });
  }

  return Object.freeze({
    RESPONSES: RESPONSES,
    normalizePrompt: normalizePrompt,
    hashText: hashText,
    estimateTokens: estimateTokens,
    buildExchange: buildExchange,
    boot: boot,
  });
});
