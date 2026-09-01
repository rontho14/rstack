---
name: debug
description: Use when the user asks to diagnose incorrect runtime behavior, trace a value or request across components, or investigate why a running system is not behaving as expected.
---

# Debug

Don't guess → 2–3 hypotheses → instrument → reproduce → read logs → fix → verify → strip probes.

Use when a **running** system is wrong (value, branch, hop, payload). Compile/test failures are not this skill.

## Capture (pick the layer that holds the evidence)

| Layer | Default | Fallback |
|-------|---------|----------|
| Java orch | `log.info` / existing logback stdout | — |
| MFE BFF | existing `serviceLogger` / process stdout | — |
| Browser | POST to ingest (below) | Log on the BFF hop of the same request instead |

Prefer process stdout. Do **not** start ingest unless the fact you need exists only in the browser. Do not ask the user to copy console output.

Ingest (browser only):

```bash
python3 .cursor/skills/debug/ingest.py &
curl -s -X POST http://127.0.0.1:8787/session -d '{"name":"short-slug"}'
```

Save `session_id`. Logs: `.debug/debug-$SESSION_ID.log`.

## Loop

1. **Hypotheses** — 2–3, testable, different layers if the bug could be UI *or* BFF *or* orch. Not five guesses in the same function.
2. **Instrument** — wrap in `#region debug` / `#endregion`. Tag `hypothesisId`. 3–8 points: entry, branch, outbound payload, inbound result.
3. **Reproduce** — clear the log/stdout, give exact steps (URL, button, cupom, API). User runs them.
4. **Analyze** — each hypothesis: CONFIRMED / REJECTED / INCONCLUSIVE. All inconclusive → new probes, don't fix.
5. **Fix** — only on CONFIRMED. Keep probes. Tag verify logs `runId=post-fix`.
6. **Verify** — user reproduces; before/after in logs. Then delete every `#region debug`.

## Probes

**Java (slf4j):**

```java
// #region debug
log.info("debug H1 {} payloadHash={}", hypothesis, hash);
// #endregion
```

**MFE BFF:** same idea on the existing logger (`module`, `hop`, `correlationId` if present).

**Browser:**

```js
// #region debug
const SESSION_ID = 'REPLACE'
const debugLog = (msg, data, hypothesisId) => {
  const body = JSON.stringify({ sessionId: SESSION_ID, msg, data, hypothesisId })
  if (!navigator.sendBeacon?.('http://127.0.0.1:8787/log', body)) {
    fetch('http://127.0.0.1:8787/log', { method: 'POST', body }).catch(() => {})
  }
}
// #endregion
```

If the browser POST is blocked (CSP/mixed content), don't fight it — log the same data on the BFF.

## Rules

- No fix without a log line that confirms the cause.
- Don't strip probes before a post-fix log proves it.
- Don't cluster all probes on the UI when orch/Feign could be the source.
