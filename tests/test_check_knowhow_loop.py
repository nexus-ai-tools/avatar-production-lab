"""tools/check_knowhow_loop.py の単体テスト。本物の気づき帳とスキルの形式も点検する。

正本: nexus-ai-2045/nexus-ai-skills の shared/skills/knowhow-feedback-loop/scripts/test_check_knowhow_loop.py（写し）。
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_knowhow_loop", ROOT / "tools/check_knowhow_loop.py")
ck = importlib.util.module_from_spec(spec)
sys.modules["check_knowhow_loop"] = ck  # dataclass が自分のモジュールを引けるように
spec.loader.exec_module(ck)

HEAD = "| ID | 記録日 | 段・作業 | 気づき | 根拠 | 反映先 | 状態 | 反映 |\n|---|---|---|---|---|---|---|---|\n"
TODAY = dt.date(2026, 11, 7)


def ledger(rows: str) -> ck.Report:
    r = ck.Report()
    ck.check_ledger(HEAD + rows, TODAY, r)
    return r


def test_本物の気づき帳とスキルに形式の誤りが無い():
    # 日付に左右されない所（形式）だけを見る。期限切れは --strict の運用で検知する
    r = ck.run(TODAY)
    assert r.errors == []


def test_期限内の未反映は待ちに入る():
    r = ledger("| K001 | 2026-11-01 | 9 物理 | 横髪を分ける | 動画 | 定石カード/09 | 未反映 | |\n")
    assert r.errors == [] and r.overdue == [] and len(r.pending) == 1


def test_14日を超えた未反映は期限切れ():
    r = ledger("| K001 | 2026-10-20 | 9 物理 | 横髪を分ける | 動画 | 定石カード/09 | 未反映 | |\n")
    assert len(r.overdue) == 1 and "18日目" in r.overdue[0]


def test_反映済みは反映の列が要る():
    r = ledger("| K001 | 2026-11-01 | 道具 | 何か | 根拠 | skill:x | 反映済み | |\n")
    assert any("反映済みなのに" in e for e in r.errors)


def test_見送りは理由が要る():
    r = ledger("| K001 | 2026-11-01 | 道具 | 何か | 根拠 | skill:x | 見送り | |\n")
    assert any("理由が空" in e for e in r.errors)


def test_IDの重複と状態の誤りを出す():
    r = ledger(
        "| K001 | 2026-11-01 | a | b | c | d | 反映済み | PR#1 |\n"
        "| K001 | 2026-11-01 | a | b | c | d | 済み | |\n"
    )
    assert any("重複" in e for e in r.errors)
    assert any("状態は" in e for e in r.errors)


def test_列の数の誤りを出す():
    r = ledger("| K001 | 2026-11-01 | a | b |\n")
    assert any("列の数" in e for e in r.errors)


def test_スキルの名前違いとリンク切れと古さ(tmp_path, monkeypatch):
    d = tmp_path / ".claude/skills/foo"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(
        "---\nname: bar\ndescription: 試し\n---\n\n見直し: 2026-01-01\n\n[無い](../../../nai.md)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(ck, "REPO", tmp_path)
    r = ck.Report()
    ck.check_skill(d / "SKILL.md", TODAY, r)
    assert any("フォルダ名" in e for e in r.errors)
    assert any("リンク切れ" in e for e in r.errors)
    assert len(r.stale) == 1


def test_strictは期限切れで失敗(tmp_path, monkeypatch, capsys):
    led = tmp_path / "気づき帳.md"
    led.write_text(HEAD + "| K001 | 2026-10-01 | a | b | c | d | 未反映 | |\n", encoding="utf-8")
    monkeypatch.setattr(ck, "LEDGER", led)
    monkeypatch.setattr(ck, "SKILLS", tmp_path / "なし")
    assert ck.main(["--today", "2026-11-07"]) == 0
    assert ck.main(["--today", "2026-11-07", "--strict"]) == 1
    assert "期限切れ" in capsys.readouterr().out


def test_気づき帳は1つだけ置く(tmp_path, monkeypatch):
    monkeypatch.setattr(ck, "REPO", tmp_path)
    r = ck.run(TODAY, skills=tmp_path / "なし")
    assert any("1つだけ" in e for e in r.errors)
    for sub in ("docs/a/改善ループ", "docs/b/改善ループ"):
        (tmp_path / sub).mkdir(parents=True)
        (tmp_path / sub / "気づき帳.md").write_text(HEAD, encoding="utf-8")
    r = ck.run(TODAY, skills=tmp_path / "なし")
    assert any("docs/a" in e and "docs/b" in e for e in r.errors)


def test_空の気づき帳は通る(tmp_path, monkeypatch):
    (tmp_path / "docs/改善ループ").mkdir(parents=True)
    (tmp_path / "docs/改善ループ/気づき帳.md").write_text(HEAD, encoding="utf-8")
    monkeypatch.setattr(ck, "REPO", tmp_path)
    assert ck.run(TODAY).errors == []
