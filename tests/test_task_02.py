import sys
import io

# Подменяем stdin на "7\n3"
sys.stdin = io.StringIO("7\n3")
old_stdout = sys.stdout
sys.stdout = out = io.StringIO()

try:
    import task_02  # студентский файл
    output = out.getvalue().strip().split('\n')
    expected = [
        "Гав! Я животное! Мой размер: 7",
        "Мяу! Я животное! Мой размер: 3"
    ]
    assert output == expected, f"Ожидалось {expected}, получено {output}"
    print("OK")
finally:
    sys.stdout = old_stdout