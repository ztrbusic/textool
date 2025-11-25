from pathlib import Path
import json
import typer

app = typer.Typer()

# @app.callback()
# def main():
#     """
#     textool — multi-command CLI.
#     """
#     pass

@app.command(name="pii", help="Personal identifiable information detection tool")
def pii(
	input: Path = typer.Argument(
		help="pii help text placeholder",
		show_default=False,
		),
	out: Path = typer.Option(
		Path("out/pii.jsonl"),
		"--out", "-o",
		help="Destination for JSONL report containing PII detection results."
		)
):
	if not input.exists():
		typer.echo(f"Error: input path not found: {input}")
		raise typer.Exit(code=1)
	# if input.suffix.lower() != ".pdf":
	# 	typer.echo("Unsupported file type (only PDFs allowed for now.)")
	# 	raise typer.Exit(code=1)

	typer.echo(f"Scanning {input} - will write to {out}")

	from textool.extractors import pii_extractor
	result = pii_extractor.scan_pii(input)
	out.parent.mkdir(parents=True, exist_ok=True)
	if out.suffix.lower() not in [".json", ".jsonl"]:
		out = out.with_suffix(".json")
	with out.open ("a", encoding="utf-8") as f:
		f.write(json.dumps(result, ensure_ascii=False) + "\n")



@app.command(name="meta", help="Metadata extraction tool")
def meta(
	input: Path = typer.Argument(
		help="meta help text placeholder",
		show_default=False,
		),
	out: Path = typer.Option(
		Path("out/meta.jsonl"),
		"--out", "-o",
		help="Destination for JSONL report containing metadata detection results."
		)
):
    if not input.exists():
    	typer.echo(f"Error: input path not found: {input}")
    	raise typer.Exit(code=1)
    if not input.suffix.lower == ".pdf":
    	typer.echo("Unsupported file type (only PDFs allowed for now.)")
    	raise typer.Exit(code=1)
    typer.echo(f"Scanning {input} - will write to {out}")