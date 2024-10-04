import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print
from costctl import removeCelluloid,jvm_reports,heap_dump
# from cost-cli.module2 import function2
console = Console()

@click.group(invoke_without_command=True, context_settings=dict(help_option_names=[]))
@click.pass_context
@click.option('--help', '-h', is_flag=True, expose_value=False, is_eager=True, callback=lambda ctx, param, value: ctx.invoke(print_help) if value else None, help='Show this message and exit.')
def cli(ctx):
    """Cost CLI"""
    if ctx.invoked_subcommand is None:
        print_help()
    pass

@click.command()
def removemanifest():
    """Run application to remove files from application manifests"""
    removeCelluloid.main()

@click.command()
@click.option('-d', '--directory', required=True, type=click.Path(), help='Directory path for JVM report.')
@click.option('-n', '--namespace', required=False, multiple=True, help='List of namespaces for JVM report.')
def jvmreport(directory,namespace):
    """Generate JVM report"""
    jvm_reports.main(directory, namespace)

@click.command()
def heapdump():
    """Generate Heap Dump"""
    heap_dump.main()

@click.command()
@click.pass_context
def print_help(ctx):
    image_text = Text("""
 $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$$$\ 
$$  __$$\ $$  __$$\ $$  __$$\\__$$  __|
$$ /  \__|$$ /  $$ |$$ /  \__|  $$ |   
$$ |      $$ |  $$ |\$$$$$$\    $$ |   
$$ |      $$ |  $$ | \____$$\   $$ |   
$$ |  $$\ $$ |  $$ |$$\   $$ |  $$ |   
\$$$$$$  | $$$$$$  |\$$$$$$  |  $$ |   
 \______/  \______/  \______/   \__|
""", justify="center", style="bold red")

    help_text = Text("""
Cost CLI

Usage:
  costctl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  removemanifest  Run application to remove files from application manifests
  jvmreport       Generate JVM report
  heapdump        Generate Heap Dump

Run 'costctl COMMAND --help' for more information on a command.
""", style="bold blue")

    console.print(image_text)
    console.print(Panel.fit(help_text, title="[bold blue]Help[/bold blue]", border_style="bold blue"))


cli.add_command(removemanifest)
cli.add_command(jvmreport)
cli.add_command(heapdump)
# cli.add_command(print_help)

if __name__ == '__main__':
    cli() 