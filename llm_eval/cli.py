import click
from .runner import run_suite, compare_suites
from .reporter import print_report, print_compare_report, save_json


@click.group()
def cli():
    """llm-eval-bench — evaluate LLM prompt outputs against test suites."""
    pass


@cli.command()
@click.option("--suite", "-s", required=True, help="Path to your test suite YAML/JSON file")
@click.option("--model", "-m", default=None, help="Model to use (overrides suite file)")
@click.option("--api-key", envvar="LLM_API_KEY", default=None, help="API key (or set LLM_API_KEY env var)")
@click.option("--judge-model", default=None, help="Model to use as LLM judge (defaults to main model)")
@click.option("--judge-api-key", envvar="JUDGE_API_KEY", default=None, help="API key for judge model")
@click.option("--output", "-o", default=None, help="Save results to a JSON file")
def run(suite, model, api_key, judge_model, judge_api_key, output):
    """Run a test suite against an LLM."""
    try:
        report = run_suite(
            suite_path=suite,
            model=model,
            api_key=api_key,
            judge_model=judge_model,
            judge_api_key=judge_api_key,
        )
        print_report(report)
        if output:
            save_json(report, output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command()
@click.option("--suite", "-s", required=True, help="Path to your test suite YAML/JSON file")
@click.option("--baseline", required=True, help="Baseline model name")
@click.option("--candidate", required=True, help="Candidate model name")
@click.option("--baseline-api-key", envvar="BASELINE_API_KEY", default=None)
@click.option("--candidate-api-key", envvar="CANDIDATE_API_KEY", default=None)
@click.option("--output", "-o", default=None, help="Save comparison results to a JSON file")
def compare(suite, baseline, candidate, baseline_api_key, candidate_api_key, output):
    """Compare two models on the same test suite."""
    try:
        report = compare_suites(
            suite_path=suite,
            baseline_model=baseline,
            candidate_model=candidate,
            baseline_api_key=baseline_api_key,
            candidate_api_key=candidate_api_key,
        )
        print_compare_report(report)
        if output:
            save_json(report, output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
if __name__ == "__main__":
    cli()