"""制作ノウハウの改善ループ（気づき帳とスキル）を点検する。

正本: nexus-ai-2045/nexus-ai-skills の shared/skills/knowhow-feedback-loop/scripts/check_knowhow_loop.py。
各リポジトリの tools/check_knowhow_loop.py はこの写し。直すときは正本を直してから写す（写しだけ変えない）。

点検すること:
    1. 気づき帳（docs/**/改善ループ/気づき帳.md、リポジトリに1つ）の形式
       - 表の列の数、ID の形（K+3桁）と重複、記録日の形、状態の値
       - 反映済みなのに「反映」の列が空、見送りなのに理由が空
    2. 未反映の放置: 記録日から EXPIRE_DAYS 日を超えたものを「期限切れ」として出す
    3. スキル（.claude/skills/*/SKILL.md。無いリポジトリでは飛ばす）
       - 先頭の name が置き場のフォルダ名と一致し、description がある
       - 「見直し: YYYY-MM-DD」の行がある。STALE_DAYS 日を超えたら警告
       - 相対リンクの行き先が実在する

使い方:
    python3 tools/check_knowhow_loop.py            # 一覧を出す。形式の誤りがあれば終了コード1
    python3 tools/check_knowhow_loop.py --strict   # 期限切れ・古いスキルがあっても終了コード1
    python3 tools/check_knowhow_loop.py --today 2026-11-30  # 日付を指定して試す

期限の日数を変えるときは、理由を気づき帳に1行書いてから変える（決まりを黙って緩めない）。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
LEDGER: Path | None = None  # None ならリポジトリの docs/**/改善ループ/気づき帳.md を探す
SKILLS: Path | None = None  # None なら REPO/.claude/skills
LEDGER_GLOB = "docs/**/改善ループ/気づき帳.md"

EXPIRE_DAYS = 14  # 未反映をこの日数より長く放置しない
STALE_DAYS = 60  # スキルの見直しの間隔

COLUMNS = ["ID", "記録日", "段・作業", "気づき", "根拠", "反映先", "状態", "反映"]
STATES = {"未反映", "反映済み", "見送り"}
ID_RE = re.compile(r"^K\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REVIEW_RE = re.compile(r"^見直し:\s*(\d{4}-\d{2}-\d{2})\s*$", re.M)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)  # 形式の誤り（常に失敗）
    overdue: list[str] = field(default_factory=list)  # 期限切れの未反映
    stale: list[str] = field(default_factory=list)  # 見直しが古いスキル
    pending: list[str] = field(default_factory=list)  # 期限内の未反映


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def check_ledger(text: str, today: dt.date, report: Report) -> None:
    lines = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    if not lines:
        report.errors.append("気づき帳: 表が見つからない")
        return
    header = split_row(lines[0])
    if header != COLUMNS:
        report.errors.append(f"気づき帳: 見出しの列が違う（期待: {' | '.join(COLUMNS)}）")
        return
    seen: set[str] = set()
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            report.errors.append(f"気づき帳: 列の数が{len(cells)}（{len(COLUMNS)}のはず）: {line[:40]}")
            continue
        row = dict(zip(COLUMNS, cells))
        kid = row["ID"]
        if not ID_RE.match(kid):
            report.errors.append(f"気づき帳: ID の形が違う（K+3桁）: {kid}")
        if kid in seen:
            report.errors.append(f"気づき帳: ID が重複: {kid}")
        seen.add(kid)
        if not DATE_RE.match(row["記録日"]):
            report.errors.append(f"{kid}: 記録日の形が違う（YYYY-MM-DD）: {row['記録日']}")
            continue
        try:
            recorded = dt.date.fromisoformat(row["記録日"])
        except ValueError:
            report.errors.append(f"{kid}: 記録日が日付として読めない: {row['記録日']}")
            continue
        for col in ("気づき", "根拠", "反映先"):
            if not row[col]:
                report.errors.append(f"{kid}: 「{col}」が空")
        state = row["状態"]
        if state not in STATES:
            report.errors.append(f"{kid}: 状態は {'・'.join(sorted(STATES))} のどれか: {state}")
        elif state == "反映済み" and not row["反映"]:
            report.errors.append(f"{kid}: 反映済みなのに「反映」の列（PR番号か既存の場所）が空")
        elif state == "見送り" and not row["反映"]:
            report.errors.append(f"{kid}: 見送りなのに理由が空")
        elif state == "未反映":
            age = (today - recorded).days
            msg = f"{kid}（{age}日目）→ {row['反映先']}: {row['気づき']}"
            (report.overdue if age > EXPIRE_DAYS else report.pending).append(msg)


def check_skill(path: Path, today: dt.date, report: Report) -> None:
    rel = path.relative_to(REPO)
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        report.errors.append(f"{rel}: 先頭の --- で囲んだ name・description が無い")
        return
    front = dict(
        (k.strip(), v.strip()) for k, v in (ln.split(":", 1) for ln in m.group(1).splitlines() if ":" in ln)
    )
    if front.get("name") != path.parent.name:
        report.errors.append(f"{rel}: name（{front.get('name')}）がフォルダ名（{path.parent.name}）と違う")
    if not front.get("description"):
        report.errors.append(f"{rel}: description が空")
    rv = REVIEW_RE.search(text)
    if not rv:
        report.errors.append(f"{rel}: 「見直し: YYYY-MM-DD」の行が無い")
    else:
        age = (today - dt.date.fromisoformat(rv.group(1))).days
        if age > STALE_DAYS:
            report.stale.append(f"{rel}: 見直しから{age}日")
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        dest = (path.parent / target.split("#", 1)[0]).resolve()
        if not dest.exists():
            report.errors.append(f"{rel}: リンク切れ: {target}")


def find_ledger(repo: Path, report: Report) -> Path | None:
    hits = sorted(repo.glob(LEDGER_GLOB))
    if len(hits) != 1:
        found = "、".join(str(h.relative_to(repo)) for h in hits) or "なし"
        report.errors.append(f"気づき帳は {LEDGER_GLOB} に1つだけ置く（見つかったもの: {found}）")
        return None
    return hits[0]


def run(today: dt.date, ledger: Path | None = None, skills: Path | None = None) -> Report:
    report = Report()
    ledger = ledger or LEDGER or find_ledger(REPO, report)
    skills = skills or SKILLS or REPO / ".claude/skills"
    if ledger is not None:
        if ledger.exists():
            check_ledger(ledger.read_text(encoding="utf-8"), today, report)
        else:
            report.errors.append(f"気づき帳が無い: {ledger}")
    for path in sorted(skills.glob("*/SKILL.md")):
        check_skill(path, today, report)
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="制作ノウハウの改善ループ（気づき帳とスキル）を点検する")
    ap.add_argument("--strict", action="store_true", help="期限切れ・古いスキルがあっても終了コード1にする")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=dt.datetime.now(ZoneInfo("Asia/Tokyo")).date(), help="今日の日付（既定は日本時間の今日。試す時だけ指定）")
    args = ap.parse_args(argv)
    r = run(args.today)
    sections = [
        ("形式の誤り", r.errors),
        (f"期限切れ（未反映のまま{EXPIRE_DAYS}日超え）", r.overdue),
        (f"見直しが古いスキル（{STALE_DAYS}日超え）", r.stale),
        ("期限内の未反映", r.pending),
    ]
    for title, items in sections:
        print(f"## {title}: {len(items)}件")
        for item in items:
            print(f"- {item}")
    failed = bool(r.errors) or (args.strict and bool(r.overdue or r.stale))
    print("結果: " + ("NG" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
