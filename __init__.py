from __future__ import annotations

import functools
import logging
from pathlib import Path

_BUNDLED_DIR = Path(__file__).parent
_log = logging.getLogger(__name__)


@functools.lru_cache(maxsize=32)
def load_prompt(name: str, *, project: str = "kernel") -> str:
    if not name or "/" in name or "\\" in name or name in (".", ".."):
        raise ValueError(f"Invalid prompt name: {name}")
    if not project or "/" in project or "\\" in project or project in (".", ".."):
        raise ValueError(f"Invalid project name: {project}")

    bundled = _BUNDLED_DIR / project / f"{name}.md"
    if not bundled.is_file():
        raise FileNotFoundError(f"bundled prompt not found: {bundled}")
    parts = [bundled.read_text(encoding="utf-8").strip()]

    from patchpilot.config import get_prompts_dirs

    seen: set[Path] = set()
    for d in get_prompts_dirs():
        resolved = d.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        for candidate in (d / project / f"{name}.md", d / f"{name}.md"):
            if candidate.is_file():
                try:
                    text = candidate.read_text(encoding="utf-8").strip()
                except (OSError, UnicodeDecodeError):
                    _log.warning("failed to read external prompt %s", candidate)
                    continue
                if text:
                    parts.append(text)
                    break

    return "\n\n".join(parts)


@functools.lru_cache(maxsize=64)
def load_external_prompt(name: str, *, project: str = "kernel") -> str:
    if not name or "/" in name or "\\" in name or name in (".", ".."):
        raise ValueError(f"Invalid prompt name: {name}")
    if not project or "/" in project or "\\" in project or project in (".", ".."):
        raise ValueError(f"Invalid project name: {project}")

    from patchpilot.config import get_prompts_dirs

    seen: set[Path] = set()
    for d in get_prompts_dirs():
        resolved = d.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        for candidate in (d / project / f"{name}.md", d / f"{name}.md"):
            if candidate.is_file():
                try:
                    text = candidate.read_text(encoding="utf-8").strip()
                except (OSError, UnicodeDecodeError):
                    _log.warning("failed to read external prompt %s", candidate)
                    continue
                if text:
                    return text
    return ""


@functools.lru_cache(maxsize=32)
def load_shared_prompt(name: str) -> str:
    if not name or "/" in name or "\\" in name or name in (".", ".."):
        raise ValueError(f"Invalid prompt name: {name}")
    path = _BUNDLED_DIR / "shared" / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(f"shared prompt not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def bust_cache() -> None:
    load_prompt.cache_clear()
    load_external_prompt.cache_clear()
    load_shared_prompt.cache_clear()
