from core.events import Signal
from core.components import BaseUtility, listen_to


class TestUtility(BaseUtility):
    @listen_to(Signal.TEST_SIGNAL)
    def handle_test(self, data: str):
        print(f"[Logger] Получен тестовый сигнал: {data}")
