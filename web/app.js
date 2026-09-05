(function () {
  "use strict";

  const core = window.HeresyCore;
  const form = document.getElementById("calculator-form");
  const styleSelect = document.getElementById("style");
  const error = document.getElementById("error");

  const fields = {
    result: document.getElementById("result"),
    intent: document.getElementById("intent"),
    styleName: document.getElementById("style-name"),
    era: document.getElementById("era"),
    usefulBytes: document.getElementById("useful-bytes"),
    payloadBytes: document.getElementById("payload-bytes"),
    tokens: document.getElementById("tokens"),
    ceremonyRatio: document.getElementById("ceremony-ratio"),
    ceremonyBytes: document.getElementById("ceremony-bytes"),
    payload: document.getElementById("payload"),
    punchline: document.getElementById("punchline"),
    valuePurchased: document.getElementById("value-purchased"),
    caveat: document.getElementById("caveat"),
    apiKeyStatus: document.getElementById("api-key-status"),
    authStatus: document.getElementById("auth-status"),
    remediation: document.getElementById("remediation"),
  };

  function populateStyles() {
    core.STYLE_ORDER.forEach(function (slug) {
      const style = core.STYLES[slug];
      const option = document.createElement("option");
      option.value = slug;
      option.textContent = style.era + " · " + style.name;
      styleSelect.appendChild(option);
    });
  }

  function clearReport() {
    Object.keys(fields).forEach(function (name) {
      fields[name].textContent = "";
    });
  }

  function render(report) {
    fields.result.textContent = report.result;
    fields.intent.textContent = report.intent;
    fields.styleName.textContent = report.styleName;
    fields.era.textContent = report.era;
    fields.usefulBytes.textContent = String(report.usefulBytes);
    fields.payloadBytes.textContent = String(report.payloadBytes);
    fields.tokens.textContent = String(report.estimatedTokens);
    fields.ceremonyRatio.textContent = report.ceremonyRatio.toFixed(2) + "×";
    fields.ceremonyBytes.textContent = (report.ceremonyBytes >= 0 ? "+" : "") + report.ceremonyBytes + " ceremony bytes";
    fields.payload.textContent = report.payloadDisplay;
    fields.punchline.textContent = report.punchline;
    fields.valuePurchased.textContent = report.valuePurchased;
    fields.caveat.textContent = report.caveat;
    fields.apiKeyStatus.textContent = report.apiKeyStatus;
    fields.authStatus.textContent = report.authenticationStatus;
    fields.remediation.textContent = report.remediation;
  }

  function calculate() {
    error.hidden = true;
    error.textContent = "";
    try {
      const report = core.evaluate(
        document.getElementById("left").value,
        document.getElementById("right").value,
        document.getElementById("operation").value,
        styleSelect.value
      );
      render(report);
    } catch (problem) {
      clearReport();
      error.textContent = problem instanceof Error ? problem.message : String(problem);
      error.hidden = false;
    }
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    calculate();
  });

  ["left", "right", "operation", "style"].forEach(function (id) {
    document.getElementById(id).addEventListener("change", calculate);
  });

  populateStyles();
  calculate();
})();
