from core.events import bus, Signal


def listen_to(signal: Signal):
    def decorator(func):
        func._signal_to_listen = signal
        return func

    return decorator


class BaseUtility:
    def __init__(self):
        self._subscribed_methods = []

        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if hasattr(method, "_signal_to_listen"):
                signal = method._signal_to_listen
                bus.subscribe(signal, method)
                self._subscribed_methods.append((signal, method))

    def destroy(self):
        for signal, method in self._subscribed_methods:
            bus.unsubscribe(signal, method)
        self._subscribed_methods.clear()
