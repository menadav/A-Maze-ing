from typing import Any, Dict


def read_config(path: str) -> Dict[str, str]:
    config = {}
    try:
        with open(path) as file:
            check = [
                "WIDTH", "HEIGHT", "ENTRY", "EXIT",
                "ALGORITHM", "SOLVER", "OUTPUT_FILE",
                "PERFECT", "SEED"
                ]
            checking = set()
            for line in file:
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                elif "=" not in line:
                    raise ValueError("no config, txt not found")
                key, value = map(str.strip, line.split("=", 1))
                if key in (check):
                    if key in (checking):
                        raise ValueError(f"Duplicate key found: {key} ")
                    checking.add(key)
                    config[key] = value
                else:
                    raise ValueError(f"Unknown key: {key} ")
    except FileNotFoundError:
        raise FileNotFoundError(f"File {path} not found")
    return config


def parse_value(key: str, value: str) -> Any:
    if key in ("WIDTH", "HEIGHT"):
        return int(value)
    if key in ("ENTRY", "EXIT"):
        return tuple(map(int, value.split(",")))
    if key == "SEED":
        return int(value) if value.strip() else None
    if key == "PERFECT":
        v = value.strip().lower()
        if v in ("true", "yes", "y", "t", "1"):
            return True
        if v in ("false", "no", "n", "f", "0"):
            return False
        raise ValueError(f"Invalid boolean for PERFECT: '{value}'")
    if key == "ALGORITHM":
        v = value.strip().lower()
        if v in ("prim", "dfs"):
            return v
        raise ValueError(f"Invalid ALGORITHM: '{value}' (use prim or dfs)")
    if key == "SOLVER":
        v = value.strip().lower()
        if v in ("bfs", "dfs"):
            return v
        raise ValueError(f"Invalid SOLVER: '{value}' (use bfs or dfs)")
    return value


def parse_config(config: Dict[str, str]) -> Dict[str, Any]:
    parsed = {}

    for key, value in config.items():
        try:
            parsed[key.lower()] = parse_value(key, value)
        except Exception as e:
            raise ValueError(f"Error in {key}: {value} → {e}")

    required = [
        "width", "height", "entry", "exit",
        "output_file", "perfect"
    ]
    for r in required:
        if r not in parsed:
            raise ValueError(f"Missing required config key: {r.upper()} ")

    return parsed
