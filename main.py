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

def generate_postmortem(git_log, answers):
    client = anthropic.Anthropic()
    prompt = f"""
    You are a senior engineer writing a post-mortem.
    Git history: {git_log}
    Incident: What broke: {answers['what']}, Who was affected: {answers['who']}, Is it fixed: {answers['fixed']}
    
    Write a post-mortem with these sections:
    1. Summary (2 sentences)
    2. Timeline
    3. Root Cause
    4. Impact
    5. Action Items
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
def main():
    console.print("💀 [red]deathlog v1.0[/red] — AI Post-Mortem Generator\n")
    
    console.print("[white]Scanning git log...[/white]")
    git_log = get_git_log()
    if not git_log:
        console.print("[red]No git history found.[/red]")
        return
        
    answers = ask_questions()
    console.print("\n[green]✓ Generating post-mortem...[/green]")
    
    try:
        postmortem = generate_postmortem(git_log, answers)
        
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
