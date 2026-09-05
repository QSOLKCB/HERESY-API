"use strict";

const assert = require("assert");
const core = require("../web/heresy-core.js");

assert.strictEqual(core.STYLE_ORDER.length, 11);
assert.deepStrictEqual(Object.keys(core.OPERATIONS), ["add", "subtract", "multiply", "divide"]);

const punch = core.evaluate("2", "2", "add", "punch-card");
assert.strictEqual(punch.result, "4");
assert.strictEqual(punch.intent, "ADD 2 2");
assert.strictEqual(punch.usefulBytes, 7);
assert.strictEqual(punch.payloadBytes, 80);

const udp = core.evaluate("2", "2", "add", "udp");
const tcp = core.evaluate("2", "2", "add", "raw-tcp");
assert.strictEqual(udp.payloadBytes, 9);
assert.strictEqual(tcp.payloadBytes, 11);
assert.ok(udp.payloadDisplay.startsWith("hex:01"));
assert.ok(tcp.payloadDisplay.startsWith("hex:0009"));

const rest = core.evaluate("17", "-3", "subtract", "rest");
assert.strictEqual(rest.result, "20");
assert.strictEqual(rest.authenticationStatus, "401");
assert.strictEqual(rest.apiKeyStatus, "FOUND IN .env.old.backup.final2");
assert.ok(rest.payloadDisplay.includes("X-API-Key: LOST-IN-.env.old.backup.final2"));

const agent = core.evaluate("2147483647", "-2147483648", "add", "agent-tool");
const agentPayload = JSON.parse(agent.payloadDisplay);
for (const name of ["a", "b"]) {
  assert.strictEqual(agentPayload.tool.input_schema.properties[name].minimum, -2147483648);
  assert.strictEqual(agentPayload.tool.input_schema.properties[name].maximum, 2147483647);
}

assert.strictEqual(core.evaluate("6", "3", "divide", "rpc").result, "2");
assert.strictEqual(core.evaluate("1", "3", "divide", "rpc").result, "1/3");
assert.strictEqual(core.evaluate("-1", "-3", "divide", "rpc").result, "1/3");
assert.throws(() => core.evaluate("1", "0", "divide", "rpc"), /architecture committee/);
assert.throws(() => core.parseInt32("2147483648", "operand"), /between/);
assert.throws(() => core.parseInt32("3.14", "operand"), /whole/);

for (const style of core.STYLE_ORDER) {
  const first = core.evaluate("9", "4", "multiply", style);
  const second = core.evaluate("9", "4", "multiply", style);
  assert.deepStrictEqual(first, second);
  assert.ok(first.payloadBytes > 0);
  assert.ok(first.estimatedTokens > 0);
  assert.ok(first.punchline.length > 0);
  assert.ok(first.valuePurchased.length > 0);
  assert.ok(first.caveat.length > 0);
}

console.log("HERESY web core: deterministic, offline, and still needlessly ceremonial.");
