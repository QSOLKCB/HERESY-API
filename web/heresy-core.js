(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.HeresyCore = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const INT32_MIN = -2147483648n;
  const INT32_MAX = 2147483647n;
  const LOST_KEY = "LOST-IN-.env.old.backup.final2";

  const OPERATIONS = Object.freeze({
    add: Object.freeze({ slug: "add", code: "ADD", method: "Add", field: "add", opcode: 1, symbol: "+" }),
    subtract: Object.freeze({ slug: "subtract", code: "SUB", method: "Subtract", field: "subtract", opcode: 2, symbol: "-" }),
    multiply: Object.freeze({ slug: "multiply", code: "MUL", method: "Multiply", field: "multiply", opcode: 3, symbol: "×" }),
    divide: Object.freeze({ slug: "divide", code: "DIV", method: "Divide", field: "divide", opcode: 4, symbol: "÷" }),
  });

  const STYLES = Object.freeze({
    "punch-card": Object.freeze({
      name: "Punch Card / Fixed Width",
      era: "1940s-1960s",
      punchline: "80 columns because storage used to arrive with furniture.",
      value: "A rigid physical record layout that operators and programs can agree on.",
      caveat: "Fixed width wastes space and becomes brittle when the record shape changes.",
      authenticated: false,
    }),
    "magnetic-tape": Object.freeze({
      name: "Magnetic Tape Record",
      era: "1950s-1980s",
      punchline: "Sequential access. Please rewind your microservice.",
      value: "Simple durable sequential records that are easy to append and batch.",
      caveat: "Random access and low-latency request/response are not the tape's hobbies.",
      authenticated: false,
    }),
    "raw-tcp": Object.freeze({
      name: "Raw TCP-style Frame",
      era: "1970s-1980s",
      punchline: "The documentation has become frighteningly short.",
      value: "Reliable ordered delivery plus explicit application message framing.",
      caveat: "TCP is a byte stream, not an API design. Versioning, auth, timeouts, and observability remain yours.",
      authenticated: false,
    }),
    udp: Object.freeze({
      name: "UDP-style Datagram",
      era: "1970s-1980s",
      punchline: "The packet can simply leave. No architecture review calendar invite required.",
      value: "Message boundaries and tiny application framing for freshness-first workloads.",
      caveat: "Delivery, ordering, retransmission, authentication, and congestion semantics may need to be supplied elsewhere.",
      authenticated: false,
    }),
    "ftp-batch": Object.freeze({
      name: "FTP / Batch File",
      era: "1970s-1990s",
      punchline: "Real-time, if tomorrow morning counts as a latency target.",
      value: "Inspectable, archivable, replayable, checksum-friendly asynchronous exchange.",
      caveat: "Plain FTP is unencrypted, and batch is the wrong tool when latency actually matters.",
      authenticated: false,
    }),
    rpc: Object.freeze({
      name: "RPC-ish Invocation",
      era: "1980s-1990s",
      punchline: "The network is a local function call until packet loss files an objection.",
      value: "Typed operation names and generated client/server calling conventions.",
      caveat: "Remote calls still fail in remote ways. Pretending otherwise creates exciting outages.",
      authenticated: false,
    }),
    corba: Object.freeze({
      name: "CORBA / IDL Theatre",
      era: "1990s",
      punchline: "The arithmetic has been referred to the Object Request Broker.",
      value: "Language-neutral interface contracts and distributed-object interoperability.",
      caveat: "This is deliberately GIOP-ish theatre. IDL is normally a build-time contract, not resent on every call.",
      authenticated: false,
    }),
    soap: Object.freeze({
      name: "SOAP-ish XML",
      era: "late 1990s-2000s",
      punchline: "The integer has entered the XML cathedral and acquired a namespace.",
      value: "Explicit envelopes, extensible headers, typed contracts, and enterprise tooling.",
      caveat: "The wider WS-* universe can add more ceremony in exchange for security, reliability, and governance.",
      authenticated: false,
    }),
    rest: Object.freeze({
      name: "REST-ish HTTP + JSON",
      era: "modern web",
      punchline: "Human-readable bureaucracy. Dave has lost the API key again.",
      value: "Ubiquitous HTTP tooling, intermediaries, debuggability, caches, and loose coupling.",
      caveat: "HTTP and JSON overhead can be disproportionate for tiny machine-to-machine messages.",
      authenticated: true,
    }),
    graphql: Object.freeze({
      name: "GraphQL-ish HTTP",
      era: "modern web",
      punchline: "Ask precisely for what you need after introducing yourself to the syntax tree.",
      value: "Client-selected response shape, schema introspection, and aggregation behind one endpoint.",
      caveat: "Query flexibility shifts complexity into schema design, resolvers, authorization, cost controls, and caching.",
      authenticated: true,
    }),
    "agent-tool": Object.freeze({
      name: "Agent Tool Call",
      era: "current AI stack",
      punchline: "Tiny arithmetic escorted by a schema, descriptions, arguments, and several responsible adults.",
      value: "Machine-readable affordances that let a model choose and call tools with validation.",
      caveat: "Tool schemas can consume substantial context repeatedly. Compact contracts and reuse matter at scale.",
      authenticated: true,
    }),
  });

  const STYLE_ORDER = Object.freeze([
    "punch-card",
    "magnetic-tape",
    "raw-tcp",
    "udp",
    "ftp-batch",
    "rpc",
    "corba",
    "soap",
    "rest",
    "graphql",
    "agent-tool",
  ]);

  function parseInt32(value, label) {
    const text = String(value).trim();
    if (!/^-?\d+$/.test(text)) {
      throw new Error(label + " must be a whole signed 32-bit integer.");
    }
    const parsed = BigInt(text);
    if (parsed < INT32_MIN || parsed > INT32_MAX) {
      throw new Error(label + " must be between -2147483648 and 2147483647.");
    }
    return parsed;
  }

  function greatestCommonDivisor(left, right) {
    let a = left < 0n ? -left : left;
    let b = right < 0n ? -right : right;
    while (b !== 0n) {
      const remainder = a % b;
      a = b;
      b = remainder;
    }
    return a;
  }

  function exactResult(left, right, operation) {
    if (operation.slug === "add") return (left + right).toString();
    if (operation.slug === "subtract") return (left - right).toString();
    if (operation.slug === "multiply") return (left * right).toString();
    if (right === 0n) throw new Error("Division by zero has been escalated to the architecture committee.");
    if (left % right === 0n) return (left / right).toString();
    let numerator = left;
    let denominator = right;
    if (denominator < 0n) {
      numerator = -numerator;
      denominator = -denominator;
    }
    const divisor = greatestCommonDivisor(numerator, denominator);
    numerator /= divisor;
    denominator /= divisor;
    return numerator.toString() + "/" + denominator.toString();
  }

  function asciiBytes(text) {
    const bytes = new Uint8Array(text.length);
    for (let index = 0; index < text.length; index += 1) {
      const code = text.charCodeAt(index);
      if (code > 127) throw new Error("Internal exhibit payload escaped ASCII containment.");
      bytes[index] = code;
    }
    return bytes;
  }

  function hex(bytes) {
    return Array.from(bytes, (value) => value.toString(16).padStart(2, "0")).join("");
  }

  function binaryMessage(operation, left, right) {
    const bytes = new Uint8Array(9);
    const view = new DataView(bytes.buffer);
    view.setUint8(0, operation.opcode);
    view.setInt32(1, Number(left), false);
    view.setInt32(5, Number(right), false);
    return bytes;
  }

  function tcpFrame(message) {
    const bytes = new Uint8Array(11);
    const view = new DataView(bytes.buffer);
    view.setUint16(0, message.length, false);
    bytes.set(message, 2);
    return bytes;
  }

  function signed11(value) {
    const sign = value < 0n ? "-" : "+";
    const digits = (value < 0n ? -value : value).toString().padStart(10, "0");
    return sign + digits;
  }

  function httpRequest(path, body) {
    return (
      "POST " + path + " HTTP/1.1\r\n" +
      "Host: example.invalid\r\n" +
      "Content-Type: application/json\r\n" +
      "Accept: application/json\r\n" +
      "X-Request-ID: 0042\r\n" +
      "X-API-Key: " + LOST_KEY + "\r\n" +
      "Content-Length: " + asciiBytes(body).length + "\r\n\r\n" +
      body
    );
  }

  function buildPayload(styleSlug, operation, left, right, intent) {
    const leftText = left.toString();
    const rightText = right.toString();
    const message = binaryMessage(operation, left, right);

    if (styleSlug === "punch-card") {
      return (operation.code.padEnd(8) + leftText.padStart(11) + rightText.padStart(11)).padEnd(80);
    }
    if (styleSlug === "magnetic-tape") {
      return operation.code + "|" + signed11(left) + "|" + signed11(right) + "\n";
    }
    if (styleSlug === "raw-tcp") return tcpFrame(message);
    if (styleSlug === "udp") return message;
    if (styleSlug === "ftp-batch") {
      return "HDR|JOB=0042|COUNT=1\n" + intent + "\nEOF|COUNT=1|CHECK=HUMAN-EYEBALL\n";
    }
    if (styleSlug === "rpc") {
      return "ArithmeticService." + operation.method + "(i32:" + leftText + ",i32:" + rightText + ")";
    }
    if (styleSlug === "corba") {
      return "GIOP-ISH|IDL:heresy/Arithmetic:1.0|operation=" + operation.field + "|a=" + leftText + "|b=" + rightText + "|request_id=0042";
    }
    if (styleSlug === "soap") {
      return "<?xml version=\"1.0\"?><soap:Envelope xmlns:soap=\"urn:soap\"><soap:Header><RequestId>0042</RequestId></soap:Header><soap:Body><" + operation.method + " xmlns=\"urn:heresy:arithmetic\"><a>" + leftText + "</a><b>" + rightText + "</b></" + operation.method + "></soap:Body></soap:Envelope>";
    }
    if (styleSlug === "rest") {
      const body = JSON.stringify({ operation: operation.field, arguments: { a: Number(left), b: Number(right) } });
      return httpRequest("/v1/arithmetic/" + operation.field, body);
    }
    if (styleSlug === "graphql") {
      const query = "mutation " + operation.method + "($a:Int!,$b:Int!){" + operation.field + "(a:$a,b:$b)}";
      const body = JSON.stringify({ query: query, variables: { a: Number(left), b: Number(right) } });
      return httpRequest("/graphql", body);
    }
    if (styleSlug === "agent-tool") {
      return JSON.stringify({
        authentication: { scheme: "api_key", status: "lost_again", last_known_location: ".env.old.backup.final2" },
        tool: {
          name: operation.field + "_two_integers",
          description: operation.method + " exactly two signed integers and return the mathematical result.",
          input_schema: {
            type: "object",
            properties: {
              a: { type: "integer", minimum: -2147483648, maximum: 2147483647 },
              b: { type: "integer", minimum: -2147483648, maximum: 2147483647 },
            },
            required: ["a", "b"],
            additionalProperties: false,
          },
        },
        arguments: { a: Number(left), b: Number(right) },
      });
    }
    throw new Error("Unknown interface style: " + styleSlug);
  }

  function evaluate(leftValue, rightValue, operationSlug, styleSlug) {
    const operation = OPERATIONS[operationSlug];
    const style = STYLES[styleSlug];
    if (!operation) throw new Error("Unknown arithmetic operation: " + operationSlug);
    if (!style) throw new Error("Unknown interface style: " + styleSlug);

    const left = parseInt32(leftValue, "Left operand");
    const right = parseInt32(rightValue, "Right operand");
    const result = exactResult(left, right, operation);
    const intent = operation.code + " " + left.toString() + " " + right.toString();
    const usefulBytes = asciiBytes(intent).length;
    const payload = buildPayload(styleSlug, operation, left, right, intent);
    const payloadBytes = typeof payload === "string" ? asciiBytes(payload).length : payload.length;
    const authenticated = style.authenticated;

    return Object.freeze({
      result: result,
      intent: intent,
      usefulBytes: usefulBytes,
      payloadBytes: payloadBytes,
      ceremonyBytes: payloadBytes - usefulBytes,
      estimatedTokens: Math.ceil(payloadBytes / 4),
      ceremonyRatio: payloadBytes / usefulBytes,
      payloadDisplay: typeof payload === "string" ? payload : "hex:" + hex(payload),
      styleName: style.name,
      era: style.era,
      punchline: style.punchline,
      valuePurchased: style.value,
      caveat: style.caveat,
      apiKeyStatus: authenticated ? "FOUND IN .env.old.backup.final2" : "NOT REQUIRED",
      authenticationStatus: authenticated ? "401" : "NOT APPLICABLE",
      remediation: authenticated ? "rewind tape" : "continue offending the abstraction layer",
    });
  }

  return Object.freeze({
    INT32_MIN: INT32_MIN,
    INT32_MAX: INT32_MAX,
    LOST_KEY: LOST_KEY,
    OPERATIONS: OPERATIONS,
    STYLES: STYLES,
    STYLE_ORDER: STYLE_ORDER,
    parseInt32: parseInt32,
    evaluate: evaluate,
  });
});
