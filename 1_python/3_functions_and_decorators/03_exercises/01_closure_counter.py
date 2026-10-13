"""Упражнение: замыкание-счётчик без утечки состояния наружу."""


def make_counter():
    # TODO: реализуйте фабрику счётчика.
    # make_counter() должна вернуть функцию increment(), которая при каждом вызове
    # увеличивает внутренний счётчик на 1 и возвращает новое значение.
    # Состояние счётчика не должно быть доступно снаружи иначе, чем через increment().
    raise NotImplementedError


if __name__ == "__main__":
    counter_a = make_counter()
    counter_b = make_counter()

    assert counter_a() == 1
    assert counter_a() == 2
    assert counter_a() == 3

    # Второй счётчик должен иметь независимое состояние.
    assert counter_b() == 1
    assert counter_a() == 4

    print("PASS")
