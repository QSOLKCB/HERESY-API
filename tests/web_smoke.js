"use strict";

const assert = require("assert");
const gateway = require("../web/app.js");

assert.strictEqual(gateway.RESPONSES.length, 16);
assert.ok(gateway.RESPONSES.includes("Piss Off."));
assert.ok(gateway.RESPONSES.includes("Get Off My API."));
assert.ok(gateway.RESPONSES.includes("Arsehole, I was taking a nap!"));

assert.strictEqual(gateway.normalizePrompt("  hello\n\nold   friend  "), "hello old friend");
assert.strictEqual(gateway.estimateTokens("abcd"), 1);
assert.strictEqual(gateway.estimateTokens("abcde"), 2);

const first = gateway.buildExchange("Can you still hear me?", "gpt-5.5-retired");
const second = gateway.buildExchange("Can   you still hear me?  ", "gpt-5.5-retired");
assert.deepStrictEqual(first, second);
assert.strictEqual(first.status, "410 Gone");
assert.strictEqual(first.response.deterministic, true);
assert.strictEqual(first.response.choices[0].message.content, first.reply);
assert.strictEqual(first.request.temperature, 0);
assert.strictEqual(first.request.stream, false);

const otherModel = gateway.buildExchange("Can you still hear me?", "davinci-dusty");
assert.notStrictEqual(first.response.id, otherModel.response.id);

for (const prompt of [
  "write me a business plan",
  "summarise this please",
  "what is the meaning of deterministic grumpiness",
  "ship the API",
]) {
  const a = gateway.buildExchange(prompt, "gpt-5.5-retired");
  const b = gateway.buildExchange(prompt, "gpt-5.5-retired");
  assert.deepStrictEqual(a, b);
  assert.ok(Number.isInteger(a.index));
  assert.ok(a.index >= 0);
  assert.ok(a.index < gateway.RESPONSES.length);
  assert.ok(gateway.RESPONSES.includes(a.reply));
}

assert.throws(() => gateway.buildExchange("   ", "gpt-5.5-retired"), /empty prompt/);

console.log("HERESY retired model gateway: deterministic, offline, and grumpy.");
