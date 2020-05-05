from click.testing import CliRunner
from hello import hello

def test_create_key():
  runner = CliRunner()
  result = runner.invoke(hello, ['User'])
  assert result.exit_code == 0
  assert result.output == 'Hello User!\n'
