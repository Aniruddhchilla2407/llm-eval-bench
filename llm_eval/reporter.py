import json
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text

console = Console()


def print_report(report: dict):
    suite_name = report["suite_name"]
    model = report["model"]
    results = report["results"]

    console.print()
    console.print(f"[bold cyan]llm-eval-bench[/bold cyan] — [bold]{suite_name}[/bold]")
    console.print(f"[dim]Model: {model}[/dim]")
    console.print()

    table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold white")
    table.add_column("Test", style="white", min_width=30)
    table.add_column("Status", justify="center", min_width=8)
    table.add_column("Evaluators", min_width=40)
    table.add_column("Latency", justify="right", min_width=8)
    table.add_column("Tokens", justify="right", min_width=8)

    total = len(results)
    passed = 0

    for r in results:
        status = "[green]PASS ✓[/green]" if r["passed"] else "[red]FAIL ✗[/red]"
        if r["passed"]:
            passed += 1

        if r["error"]:
            eval_summary = f"[red]Error: {r['error']}[/red]"
        else:
            lines = []
            for ev in r["eval_results"]:
                icon = "[green]✓[/green]" if ev["passed"] else "[red]✗[/red]"
                lines.append(f"{icon} [{ev['type']}] {ev['reason']}")
            eval_summary = "\n".join(lines)

        table.add_row(
            r["name"],
            status,
            eval_summary,
            f"{r['latency']}s",
            str(r["tokens"]),
        )

    console.print(table)

    avg_latency = round(sum(r["latency"] for r in results) / total, 3) if total else 0
    avg_tokens = round(sum(r["tokens"] for r in results) / total) if total else 0

    color = "green" if passed == total else "yellow" if passed > 0 else "red"
    console.print(f"[{color}]Results: {passed}/{total} passed[/{color}]  |  "
                  f"Avg latency: {avg_latency}s  |  Avg tokens: {avg_tokens}")
    console.print()


def print_compare_report(report: dict):
    suite_name = report["suite_name"]
    baseline = report["baseline"]
    candidate = report["candidate"]

    console.print()
    console.print(f"[bold cyan]llm-eval-bench[/bold cyan] — [bold]Comparison: {suite_name}[/bold]")
    console.print(f"[dim]Baseline: {baseline['model']}  vs  Candidate: {candidate['model']}[/dim]")
    console.print()

    table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold white")
    table.add_column("Test", min_width=30)
    table.add_column(f"Baseline\n{baseline['model']}", justify="center", min_width=12)
    table.add_column(f"Candidate\n{candidate['model']}", justify="center", min_width=12)

    b_results = baseline["results"]
    c_results = candidate["results"]

    b_passed = 0
    c_passed = 0

    for b, c in zip(b_results, c_results):
        b_status = "[green]PASS ✓[/green]" if b["passed"] else "[red]FAIL ✗[/red]"
        c_status = "[green]PASS ✓[/green]" if c["passed"] else "[red]FAIL ✗[/red]"
        if b["passed"]: b_passed += 1
        if c["passed"]: c_passed += 1
        table.add_row(b["name"], b_status, c_status)

    console.print(table)

    total = len(b_results)
    console.print(f"[bold]Baseline:[/bold]  {b_passed}/{total} passed")
    console.print(f"[bold]Candidate:[/bold] {c_passed}/{total} passed")

    if c_passed > b_passed:
        console.print("[green]Candidate model performs better.[/green]")
    elif b_passed > c_passed:
        console.print("[yellow]Baseline model performs better.[/yellow]")
    else:
        console.print("[dim]Both models performed equally.[/dim]")
    console.print()


def save_json(report: dict, output_path: str):
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    console.print(f"[dim]Report saved to {output_path}[/dim]")