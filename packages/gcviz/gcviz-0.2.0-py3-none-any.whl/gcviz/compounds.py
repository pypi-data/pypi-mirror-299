from functools import lru_cache
from dash import html


@lru_cache()
def compounds_beautify(
    compound: str, as_dash: bool = False
) -> str | list[html.Sub | str]:
    """Beautify the compound name.


    Parameters
    ----------

    compound : str
        The compound name.

    as_dash : bool
        If True, return a list of html components, otherwise a string.

    """

    compound = compound.lower()

    # Function that generate the proper output (html or string)
    # based on the as_dash parameter
    def sub(text: str) -> html.Sub | str:
        if as_dash:
            return html.Sub(text)
        else:
            return f"<sub>{text}</sub>"

    def join(*args) -> str | list[html.Sub | str]:
        if as_dash:
            return args
        else:
            return "".join(args)

    # Well known compounds for which no rule can be applied
    match compound:
        case "ccl4":
            return join("CCl", sub("4"))
        case "ch2cl2":
            return join("CH", sub("2"), "Cl", sub("2"))
        case "ch3br":
            return join("CH", sub("3"), "Br")
        case "so2f2":
            return join("SO", sub("2"), "F", sub("2"))
        case "ch3ccl3":
            return join("CH", sub("3"), "CCl", sub("3"))
        case "ch3cl":
            return join("CH", sub("3"), "Cl")
        case "chcl3":
            return join("CHCl", sub("3"))
        case "n2o":
            return join("N", sub("2"), "O")
        case "co" | "pce" | "tce":
            return compound.upper()

    # Compounds of type ABC-123
    if compound.startswith(("cfc-", "hcfc-", "hfc-", "hfo-", "h-", "pfc-")):
        # Only the beggining is upper case
        start, *end = compound.split("-")
        return f"{start.upper()}-{'-'.join(end)}"

    elif compound[-1].isdigit():
        # Formula with last letter as a number (eg. CO2, NH4, SF6, ...)
        return join(f"{compound[:-1].upper()}", sub(compound[-1]))
    else:
        # Will work for many compounds given by there chemical name (eg. methane, ethane, ...)
        return compound.capitalize()
