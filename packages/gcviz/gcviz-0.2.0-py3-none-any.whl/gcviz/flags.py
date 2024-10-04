from enum import StrEnum


class Flags(StrEnum):
    REMOVE_POLLUTION = "Remove pollution"
    ONLY_BASELINE = "Only baseline"


def get_flags_from_checklist(checklist: list[str]) -> list[Flags]:
    return [Flags(flag_str) for flag_str in checklist]
