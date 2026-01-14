
---

## 📄 2. `task_01.py` — пример решения (Задание 1)

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class EmailNotifier(Notifier):
    def send(self, message: str):
        print(f"[Email] Отправка: {message}")

class SMSNotifier(Notifier):
    def send(self, message: str):
        print(f"[SMS] Отправка: {message}")

class PushNotifier(Notifier):
    def send(self, message: str):
        print(f"[Push] Отправка: {message}")

def notify_all(notifiers, message):
    for notifier in notifiers:
        notifier.send(message)