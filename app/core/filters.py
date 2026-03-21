from fastapi import HTTPException


ROLE_MAP = {
    "all": [1, 2, 3, 4, 5, 6],
    "tank": [1],
    "fighter": [2],
    "ass": [3],
    "mage": [4],
    "mm": [5],
    "supp": [6],
}

LANE_MAP = {
    "all": [1, 2, 3, 4, 5],
    "exp": [1],
    "mid": [2],
    "roam": [3],
    "jungle": [4],
    "gold": [5],
}


def parse_multi(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def validate_and_map_multi(
    selected_raw: str,
    mapping: dict[str, list[int]],
    default: list[int],
    field_name: str,
) -> list[int]:
    selected = parse_multi(selected_raw)

    if not selected:
        return default

    invalid = [item for item in selected if item not in mapping]
    if invalid:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid {field_name}: {', '.join(invalid)}. Allowed: {', '.join(mapping.keys())}",
        )

    if "all" in selected:
        return default

    result = set()
    for item in selected:
        result.update(mapping[item])

    return list(result)