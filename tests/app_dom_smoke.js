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

// Staged edits may invalidate an old report, but must never calculate a new one.
assert.ok(elements.left.listeners.input);
assert.ok(elements.right.listeners.input);
assert.ok(elements.operation.listeners.change);
assert.ok(elements.style.listeners.change);

elements.left.value = "9";
elements.left.listeners.input();
elements.right.value = "4";
elements.right.listeners.input();
elements.operation.value = "multiply";
elements.operation.listeners.change();
assert.strictEqual(elements.result.textContent, "");
assert.strictEqual(elements.intent.textContent, "");

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

// Native browser validation may block submit. Input invalidation must still remove
// the previously committed report before the browser refuses the request.
elements.right.value = "";
elements.right.listeners.input();
assert.strictEqual(elements.result.textContent, "");
assert.strictEqual(elements.intent.textContent, "");
assert.strictEqual(elements.payload.textContent, "");
assert.strictEqual(elements.error.hidden, true);

// Restore a valid staged request and commit it again.
elements.right.value = "4";
elements.right.listeners.input();
elements.operation.value = "multiply";
elements.operation.listeners.change();
elements["calculator-form"].listeners.submit({ preventDefault() {} });
assert.strictEqual(elements.result.textContent, "36");

// Force a calculation failure after a successful one, through submit.
elements.operation.value = "divide";
elements.operation.listeners.change();
elements.right.value = "0";
elements.right.listeners.input();
assert.strictEqual(elements.result.textContent, "");
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

console.log("HERESY DOM adapter: staged edits invalidate reports; only commit executes arithmetic.");
