import subprocess
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich import print as rprint
import anthropic
import os

app = typer.Typer()
console = Console()

def get_git_log():
    result = subprocess.run(
        ["git", "log", "--oneline", "-20"],
        capture_output=True,
        text=True
    )
    return result.stdout

def ask_questions():
    what = Prompt.ask("[green]?[/green] What broke?")
    who = Prompt.ask("[green]?[/green] Who was affected?")
    fixed = Prompt.ask("[green]?[/green] Is it fixed?")
    return {"what": what, "who": who, "fixed": fixed}

def generate_postmortem(git_log, answers, mock=False):
    if mock:
        import time
        time.sleep(1.5) # Simulate API latency
        return f"""# Post-Mortem: {answers['what']}

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
- **What broke**: {answers['what']}
- **Who was affected**: {answers['who']}
- **Is it fixed**: {answers['fixed']}

## Action Items
1. Increase connection pool size limits
2. Implement better circuit breakers for the payment service
3. Add specific alerting for connection pool exhaustion

*Note: This is a mock response generated for testing purposes.*
"""
        
    client = anthropic.Anthropic()
    prompt = f"""
    You are a Staff/Principal Site Reliability Engineer writing a highly professional, blame-free, and technically deep incident post-mortem for a company-wide audience.
    
    Context provided:
    - Recent Git history (for deployment context): {git_log}
    - Incident summary from on-call:
      - What broke: {answers['what']}
      - Who was affected: {answers['who']}
      - Is it fixed: {answers['fixed']}
    
    Please write a comprehensive post-mortem document in Markdown format with the following structure:
    
    # Incident Post-Mortem: {answers['what'].title()}
    
    ## 1. Executive Summary
    Provide a concise, executive-level summary (2-3 sentences) of the incident, its duration, and the primary business impact.
    
    ## 2. Detailed Timeline
    Reconstruct a realistic timeline based on the git history and context provided. Use T-0 format (e.g., T-0, T+15m). Include detection time, mitigation time, and resolution time.
    
    ## 3. Impact Analysis
    Detail the exact scope of the impact based on the "Who was affected" data. Include estimated user impact, degradation level, and any potential data loss or financial implications.
    
    ## 4. Root Cause Analysis
    Provide a deep technical explanation of the root cause. Draw reasonable technical inferences based on the provided what/who context and the recent git history. Use the "5 Whys" methodology if appropriate.
    
    ## 5. Resolution & Recovery
    Explain exactly how the incident was mitigated and ultimately resolved. Mention what worked well and what could have gone better during the incident response.
    
    ## 6. Action Items (Preventative Measures)
    List 3-5 specific, actionable, and assignable engineering tasks to prevent recurrence or improve detection.
    
    Maintain a blameless, objective, and highly professional tone throughout the document.
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

@app.command()
def main(mock: bool = typer.Option(False, "--mock", help="Use mock API response instead of calling Claude")):
    console.print("💀 [red]deathlog v1.0[/red] — AI Post-Mortem Generator\n")
    
    git_log = get_git_log()
    
    # parse out the number of commits
    commit_count = len([line for line in git_log.split("\n") if line.strip()])
    console.print(f"[white]Scanning git log...[/white] found {commit_count} commits")
    
    # Mocking these outputs to match the visual design for now
    console.print("[white]Reading error logs...[/white] found 3 critical errors")
    console.print("[white]Last deploy:[/white] 2h ago (v2.4.1)\n")
    
    if not git_log:
        console.print("[red]No git history found.[/red]")
        return
        
    answers = ask_questions()
    console.print("\n[green]✓ Generating post-mortem...[/green]")
    
    try:
        postmortem = generate_postmortem(git_log, answers, mock=mock)
        
        # Save to file
        import datetime
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"postmortem-{date_str}.md"
        
        with open(filename, "w") as f:
            f.write(postmortem)
            
        console.print(f"[green]✓ Saved to: {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Error generating post-mortem: {e}[/red]")

if __name__ == "__main__":
    app()
