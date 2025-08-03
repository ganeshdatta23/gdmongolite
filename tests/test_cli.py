from click.testing import CliRunner
from gdmongolite.cli import main

def test_cli_base():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "gdmongolite" in result.output
