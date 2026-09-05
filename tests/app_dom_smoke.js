"use strict";

const assert = require("assert");
const core = require("../web/heresy-core.js");

function element(initial) {
  return {
    value: initial && Object.prototype.hasOwnProperty.call(initial, "value") ? initial.value : "",
    textContent: initial && Object.prototype.hasOwnProperty.call(initial, "textContent") ? initial.textContent : "",
    hidden: initial && Object.prototype.hasOwnProperty.call(initial, "hidden") ? initial.hidden : false,
    listeners: {},
    children: [],
    addEventListener(type, handler) {
      this.listeners[type] = handler;
    },
    appendChild(child) {
      this.children.push(child);
      if (!this.value && child.value) {
        this.value = child.value;
      }
    },
  };
}

const ids = [
  "calculator-form",
  "style",
  "error",
  "result",
  "intent",
  "style-name",
  "era",
  "useful-bytes",
  "payload-bytes",
  "tokens",
  "ceremony-ratio",
  "ceremony-bytes",
  "payload",
  "punchline",
  "value-purchased",
  "caveat",
  "api-key-status",
  "auth-status",
  "remediation",
  "left",
  "right",
  "operation",
];

const elements = Object.fromEntries(ids.map((id) => [id, element()]));
elements.left.value = "2";
elements.right.value = "2";
elements.operation.value = "add";
elements.error.hidden = true;

const documentStub = {
  getElementById(id) {
    return elements[id];
  },
  createElement() {
    return element();
  },
};

global.window = { HeresyCore: core };
global.document = documentStub;

require("../web/app.js");

assert.strictEqual(elements.result.textContent, "4");
assert.strictEqual(elements.intent.textContent, "ADD 2 2");
assert.ok(elements.payload.textContent.length > 0);
assert.strictEqual(elements.error.hidden, true);

// Force a failed calculation after a successful one.
elements.operation.value = "divide";
elements.right.value = "0";
elements.right.listeners.change();

assert.strictEqual(elements.error.hidden, false);
assert.match(elements.error.textContent, /architecture committee/);

for (const id of [
  "result",
  "intent",
  "style-name",
  "era",
  "useful-bytes",
  "payload-bytes",
  "tokens",
  "ceremony-ratio",
  "ceremony-bytes",
  "payload",
  "punchline",
  "value-purchased",
  "caveat",
  "api-key-status",
  "auth-status",
  "remediation",
]) {
  assert.strictEqual(elements[id].textContent, "", id + " retained stale output");
}

console.log("HERESY DOM adapter: failed calculations clear stale museum output.");
