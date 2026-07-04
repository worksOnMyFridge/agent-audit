"""CLI argument handling and exit codes."""

from agent_audit.cli import main


def test_list_exits_zero(capsys):
    assert main(["--list"]) == 0
    assert "methodology" in capsys.readouterr().out


def test_audit_template_on_a_path(tmp_path, capsys):
    (tmp_path / "agent.py").write_text("x = 1\n")
    assert main([str(tmp_path)]) == 0
    assert "Template" in capsys.readouterr().out


def test_missing_path_exits_two(capsys):
    assert main([str("does-not-exist-xyz")]) == 2
    assert "not found" in capsys.readouterr().err


def test_no_args_prints_help_and_exits_one(capsys):
    assert main([]) == 1
    assert "usage" in capsys.readouterr().out.lower()
