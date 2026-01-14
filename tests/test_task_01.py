import sys
import io
from task_01 import EmailNotifier, SMSNotifier, PushNotifier, notify_all

def test_notify_all():
    inputs = ["Привет!"]
    expected_outputs = [
        "[Email] Отправка: Привет!",
        "[SMS] Отправка: Привет!",
        "[Push] Отправка: Привет!"
    ]

    # Перехватываем stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()

    try:
        notifiers = [EmailNotifier(), SMSNotifier(), PushNotifier()]
        notify_all(notifiers, "Привет!")
        output = captured_output.getvalue().strip().split('\n')
        assert output == expected_outputs, f"Ожидалось {expected_outputs}, получено {output}"
        print("OK")
    finally:
        sys.stdout = old_stdout

if __name__ == "__main__":
    test_notify_all()