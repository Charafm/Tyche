from core.utils import hello

def test_hello(capsys):
    hello()
    captured = capsys.readouterr()
    assert "Hello" in captured.out
