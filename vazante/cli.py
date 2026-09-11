"""Command-line entry point. Subcommands grow as each pipeline stage is built."""
from __future__ import annotations

from pathlib import Path

import typer

app = typer.Typer(help="VAZANTE desk tooling — detection, Oracle, buyer boxes, economics.", no_args_is_help=True)
cvm_app = typer.Typer(help="CVM bulk layer (open data).", no_args_is_help=True)
app.add_typer(cvm_app, name="cvm")


@app.command()
def status() -> None:
    """Environment report: Python, packages, data dirs."""
    from vazante.env import report

    report()


@app.command("max-bid")
def max_bid_cmd(
    locked: float = typer.Option(..., "--L", help="Locked onward proceeds, FIRM only, R$m"),
    costs: float = typer.Option(0.578, "--C", help="Non-purchase costs, R$m"),
    tax_rate: float = typer.Option(0.371, "--t", help="Tax rate on the spread"),
    cover: float = typer.Option(1.20, help="Cover ratio, tax inside the basis"),
) -> None:
    """One-trade arithmetic: the maximum firm seller bid under the 1.20× rule. MODEL, not a bid."""
    from vazante.economics.reference_book import Trade

    for k, v in Trade(L=locked, C=costs, t=tax_rate, cover=cover).as_dict().items():
        print(f"{k:24s} {v:10.4f}")


@cvm_app.command("months")
def cvm_months(last: int = 12) -> None:
    """Months the CVM has published (newest last)."""
    from vazante.cvm.download import list_available_months

    for m in list_available_months()[-last:]:
        print(m)


@cvm_app.command("fetch")
def cvm_fetch(months: int = 24, end: str | None = None, force: bool = False) -> None:
    """Fetch the last N informe months as dated snapshots into data/raw/cvm/inf_mensal/."""
    from vazante.cvm.download import fetch_informe_range

    for p in fetch_informe_range(months_back=months, end=end, force=force):
        print(p)


@cvm_app.command("meta")
def cvm_meta(force: bool = False) -> None:
    """Fetch the CVM data dictionary."""
    from vazante.cvm.download import fetch_meta

    print(fetch_meta(force=force))


@cvm_app.command("cad-fi")
def cvm_cad_fi(force: bool = False) -> None:
    """Fetch today's cadastro snapshot."""
    from vazante.cvm.download import fetch_cad_fi

    print(fetch_cad_fi(force=force))


@cvm_app.command("headers")
def cvm_headers(zip_path: Path) -> None:
    """Header row of every CSV member of an informe ZIP (input to the mapping freeze)."""
    from vazante.cvm.download import informe_headers

    for name, cols in informe_headers(zip_path).items():
        print(f"## {name} ({len(cols)} columns)")
        for i, c in enumerate(cols, 1):
            print(f"  {i:3d}  {c}")


if __name__ == "__main__":
    app()
