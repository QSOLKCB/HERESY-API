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

// Loading the app stages the defaults but does not execute arithmetic.
assert.strictEqual(elements.result.textContent, "");
assert.strictEqual(elements.intent.textContent, "");
assert.strictEqual(elements.payload.textContent, "");
assert.strictEqual(elements.error.hidden, true);

for (const id of ["left", "right", "operation", "style"]) {
  assert.strictEqual(elements[id].listeners.change, undefined, id + " unexpectedly recalculates on change");
}

// Changing staged input must not execute until the enterprise commit is submitted.
elements.left.value = "9";
elements.right.value = "4";
elements.operation.value = "multiply";
assert.strictEqual(elements.result.textContent, "");

let prevented = false;
elements["calculator-form"].listeners.submit({
  preventDefault() {
    prevented = true;
  },
});
assert.strictEqual(prevented, true);
assert.strictEqual(elements.result.textContent, "36");
assert.strictEqual(elements.intent.textContent, "MUL 9 4");
assert.ok(elements.payload.textContent.length > 0);
assert.strictEqual(elements.error.hidden, true);

// Force a failed calculation after a successful one, again only through submit.
elements.operation.value = "divide";
elements.right.value = "0";
elements["calculator-form"].listeners.submit({ preventDefault() {} });

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

console.log("HERESY DOM adapter: arithmetic executes only after enterprise commit approval.");
