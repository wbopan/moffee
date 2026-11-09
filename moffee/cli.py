from moffee import __version__
import click
import os
from moffee.builder import build, read_options
from livereload import Server
import tempfile


def run(md, output=None, live=False):
    """Process the markdown file to render slides."""
    if not os.path.exists(md):
        click.echo(f"Error: Markdown file '{md}' does not exist.", err=True)
        raise click.Abort()

    if not output:
        output = tempfile.mkdtemp()
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    options = read_options(md)
    base_template_dir = os.path.join(template_dir, "base")
    theme_template_dir = os.path.join(template_dir, options.theme)

    if not os.path.exists(theme_template_dir):
        click.echo(
            f"Error: Theme '{options.theme}' not found in templates directory.",
            err=True,
        )
        click.echo(f"Available themes: {', '.join(os.listdir(template_dir))}", err=True)
        raise click.Abort()

    def render_handler():
        """Re-read the theme from frontmatter on every (re)build so that
        changes to the ``theme`` option take effect in live mode without a restart."""
        current_options = read_options(md)
        current_theme_dir = os.path.join(template_dir, current_options.theme)
        if not os.path.exists(current_theme_dir):
            click.echo(
                f"Error: Theme '{current_options.theme}' not found in templates directory.",
                err=True,
            )
            try:
                available = ", ".join(os.listdir(template_dir))
            except OSError:
                available = "none"
            click.echo(f"Available themes: {available}", err=True)
            return
        build(
            document_path=md,
            output_dir=output,
            template_dir=base_template_dir,
            theme_dir=current_theme_dir,
        )

    render_handler()
    print(f"Generated html written to {os.path.join(output, 'index.html')}")
    if live:
        server = Server()
        server.watch(md, render_handler)
        server.watch(base_template_dir, render_handler)
        if theme_template_dir:
            server.watch(theme_template_dir, render_handler)
        server.serve(root=output)


@click.group(
    help="""
Render markdown file into slides.

This tool allows you to convert markdown files into HTML slides,
either generating them once or launching a live server to continuously
update the output as changes are made to the markdown file.
""",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(__version__, prog_name="moffee")
def cli():
    pass


@cli.command(
    help="""
Generate slides from a markdown file.

This command takes a markdown file as input and produces a set of slides
formatted as an HTML file. You can specify an output directory where the
HTML will be saved.

Example usage:

\b
  python moffee.py make example.md -o output/
"""
)
@click.argument("markdown", metavar="<markdown-file>")
@click.option(
    "-o",
    "--output",
    metavar="<output-path>",
    default=None,
    help="Output file path. If not specified, a temporary directory will be used.",
)
def make(markdown, output):
    """Generate slides from a markdown file."""
    run(markdown, output, live=False)


@cli.command(
    help="""
Launch live mode to update HTML outputs.

This command starts a live server that watches for changes to the specified
markdown file. As changes are made, the slides are automatically updated and
reflected in the browser.

Example usage:

\b
  python moffee.py live example.md
"""
)
@click.argument("markdown", metavar="<markdown-file>")
def live(markdown):
    """Launch live mode to update html outputs."""
    run(markdown, output=None, live=True)


if __name__ == "__main__":
    cli()
