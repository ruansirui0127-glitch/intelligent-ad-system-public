"""Audit the repository before publishing or sharing it.

The script is intentionally conservative. It flags files and text patterns that
need human review before a public push.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BLOCKED_PATH_PATTERNS = [
    re.compile(r"(^|/)\.env($|\.)"),
    re.compile(r"(^|/)config/private/"),
    re.compile(r"(^|/)runtime/private/"),
    re.compile(r"(^|/)secrets?/"),
    re.compile(r"(^|/)private/"),
    re.compile(r"(^|/)outputs?/"),
    re.compile(r"(^|/)exports?/"),
    re.compile(r"(^|/)downloads?/"),
    re.compile(r"(^|/)screenshots?/"),
    re.compile(r"(^|/)raw-captures?/"),
    re.compile(r"(^|/)data/raw/.*[^/]$"),
]

ALLOWED_TRACKED_PATHS = {
    "config/examples/.env.example",
    "config/examples/meta.env.example",
    "config/examples/tokens.example.json",
    "data/raw/.gitkeep",
}

BLOCKED_EXTENSIONS = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".crt",
    ".cer",
    ".xlsx",
    ".xls",
    ".csv",
    ".tsv",
    ".zip",
    ".7z",
    ".rar",
    ".pdf",
    ".docx",
}

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"gho_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"Bearer [A-Za-z0-9._-]{20,}"),
    re.compile(r"(?i)(access_token|refresh_token|client_secret|app_secret|api_key)\s*[:=]\s*['\"][A-Za-z0-9._-]{16,}['\"]"),
]

REVIEW_TERMS = [
    "真实广告账户",
    "真实广告数据",
    "后台截图",
    "原始导出",
    "客户资料",
    "身份证",
    "银行卡",
    "合同",
    "报价",
    "营收",
    "利润",
    "成本线",
    "内部策略",
]

ALLOW_REVIEW_FILES = {
    "README.md",
    "SECURITY.md",
    "AGENTS.md",
    ".github/pull_request_template.md",
    "docs/publication-checklist.md",
    "docs/planning/README.md",
    "docs/planning/business-profile.md",
    "docs/meta-conversion-goals.md",
    "docs/project-foundation.md",
    "scripts/publication_audit.py",
}


def git_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def is_text_file(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(4096)
    except OSError:
        return False
    if b"\0" in chunk:
        return False
    try:
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def scan() -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []

    for rel in git_files():
        path = ROOT / rel
        normalized = rel.replace(os.sep, "/")
        suffix = path.suffix.lower()

        if normalized not in ALLOWED_TRACKED_PATHS and any(
            pattern.search(normalized) for pattern in BLOCKED_PATH_PATTERNS
        ):
            blockers.append(f"blocked path: {rel}")

        if suffix in BLOCKED_EXTENSIONS:
            blockers.append(f"blocked file type: {rel}")

        if not path.is_file() or not is_text_file(path):
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                blockers.append(f"secret-like text: {rel} / {pattern.pattern}")

        if rel not in ALLOW_REVIEW_FILES:
            for term in REVIEW_TERMS:
                if term in text:
                    warnings.append(f"review business-sensitive term: {rel} / {term}")

    return blockers, warnings


def main() -> int:
    blockers, warnings = scan()

    if warnings:
        print("Review warnings:")
        for item in warnings:
            print(f"  - {item}")

    if blockers:
        print("Publication blockers:")
        for item in blockers:
            print(f"  - {item}")
        return 1

    print("Publication audit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
