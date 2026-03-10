<div align="center">
  <h1>💀 deathlog</h1>
  
  <p><b>AI Post-Mortem Generator</b></p>
  <p>Generate post-mortems from git history in 30 seconds.</p>
</div>

## What does it do?
`deathlog` reads your recent git commit history, asks you 3 quick questions about an incident, and uses Claude 3.5 Sonnet to automatically generate a detailed Markdown post-mortem document.

Stop wasting time writing post-mortems manually when you can automate 90% of the work.

## Installation

```bash
pip install deathlog
```

## Usage

You'll need an Anthropic API key to use the tool.

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Navigate to any git project folder where an incident occurred and run:

```bash
deathlog
```

It will ask you three questions:
1. What broke?
2. Who was affected?
3. Is it fixed?

And then generate a `postmortem-YYYY-MM-DD.md` file in the current directory!

### Testing without an API Key
If you just want to test the CLI flow without an API key, use the `--mock` flag:
```bash
deathlog --mock
```

## Example Output

```markdown
# Post-Mortem: Payment service timed out

## Summary
The payment service timed out affecting approximately 200 users for 45 minutes. The issue has been identified and resolved.

## Timeline
- **T-0**: Incident began
- **T+15**: Alerts fired
- **T+30**: Root cause identified
- **T+45**: Fix deployed and service restored

## Root Cause
Connection pool exhaustion to the primary database replica under unexpected load spikes.

## Impact
- **What broke**: Payment service timed out
- **Who was affected**: Approx 200 users, 45 mins
- **Is it fixed**: yes

## Action Items
1. Increase connection pool size limits
2. Implement better circuit breakers for the payment service
3. Add specific alerting for connection pool exhaustion
```
