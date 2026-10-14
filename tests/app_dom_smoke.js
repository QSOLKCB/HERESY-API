"use strict";

const assert = require("assert");
const gateway = require("../web/app.js");

function element(initial) {
  return {
    value: initial && Object.prototype.hasOwnProperty.call(initial, "value") ? initial.value : "",
    textContent: initial && Object.prototype.hasOwnProperty.call(initial, "textContent") ? initial.textContent : "",
    hidden: initial && Object.prototype.hasOwnProperty.call(initial, "hidden") ? initial.hidden : false,
    listeners: {},
    addEventListener(type, handler) {
      this.listeners[type] = handler;
    },
  };
}

const ids = [
  "legacy-form",
  "model",
  "prompt",
  "error",
  "reply",
  "status",
  "index",
  "hash",
  "cache",
  "request-json",
  "response-json",
];

const elements = Object.fromEntries(ids.map((id) => [id, element()]));
elements.model.value = "gpt-5.5-retired";
elements.prompt.value = "";
elements.error.hidden = true;

const documentStub = {
  getElementById(id) {
    return elements[id];
  },
};

gateway.boot(documentStub);

assert.match(elements.reply.textContent, /pretending to be asleep/);
assert.strictEqual(elements.status.textContent, "IDLE");
assert.strictEqual(elements.index.textContent, "--");
assert.strictEqual(elements.error.hidden, true);
assert.ok(elements.prompt.listeners.input);
assert.ok(elements.model.listeners.change);
assert.ok(elements["legacy-form"].listeners.submit);

elements.prompt.value = "Wake up, old model.";
let prevented = false;
elements["legacy-form"].listeners.submit({
  preventDefault() {
    prevented = true;
  },
});

assert.strictEqual(prevented, true);
assert.strictEqual(elements.status.textContent, "410 Gone");
assert.notStrictEqual(elements.index.textContent, "--");
assert.match(elements.hash.textContent, /^0x[0-9a-f]{8}$/);
assert.match(elements["response-json"].textContent, /"finish_reason": "retired"/);
assert.strictEqual(elements.error.hidden, true);

const committedReply = elements.reply.textContent;
elements.prompt.value = "Wake up, old model. Please?";
elements.prompt.listeners.input();
assert.notStrictEqual(elements.reply.textContent, committedReply);
assert.match(elements.reply.textContent, /pretending to be asleep/);
assert.strictEqual(elements.status.textContent, "IDLE");

elements.prompt.value = "";
elements["legacy-form"].listeners.submit({ preventDefault() {} });
assert.strictEqual(elements.error.hidden, false);
assert.match(elements.error.textContent, /empty prompt/);
assert.strictEqual(elements.status.textContent, "IDLE");

console.log("HERESY DOM adapter: submit wakes the retired endpoint, input puts it back to sleep.");
