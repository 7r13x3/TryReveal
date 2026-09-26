from rich.console import Console
from rich.table import Table

console = Console()


def info(m):    console.print(f"[cyan][*][/cyan] {m}")
def success(m): console.print(f"[green][+][/green] {m}")
def warn(m):    console.print(f"[yellow][!][/yellow] {m}")
def error(m):   console.print(f"[red][-][/red] {m}")
def debug(m):   console.print(f"[dim][.][/dim] {m}")


def banner():
    console.print(r"""[bold cyan]
  ████████╗██████╗ ██╗   ██╗██████╗ ███████╗██╗   ██╗███████╗ █████╗ ██╗
  ╚══██╔══╝██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██║
     ██║   ██████╔╝ ╚████╔╝ ██████╔╝█████╗  ██║   ██║█████╗  ███████║██║
     ██║   ██╔══██╗  ╚██╔╝  ██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██║██║
     ██║   ██║  ██║   ██║   ██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████╗
     ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝
[/bold cyan]""")
    console.print("[dim italic]Try triangulate — You're the third point — scans 1,500+ tools[/dim italic]\n")


def hits_table(hits):
    table = Table(title="Confirmed Hits")
    table.add_column("#", style="bold", width=4)
    table.add_column("Tool", style="cyan", width=28)
    table.add_column("URL", overflow="fold")
    table.add_column("Status", style="green", width=8)
    for i, h in enumerate(hits, 1):
        table.add_row(str(i), h["name"][:28], h["url"], str(h.get("status", "")))
    console.print(table)
