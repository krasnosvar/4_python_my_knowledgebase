"""Упражнение: замыкание-счётчик без утечки состояния наружу."""


def make_counter():
    # TODO: реализуйте фабрику счётчика.
    # make_counter() должна вернуть функцию increment(), которая при каждом вызове
    # увеличивает внутренний счётчик на 1 и возвращает новое значение.
    # Состояние счётчика не должно быть доступно снаружи иначе, чем через increment().
    raise NotImplementedError


if __name__ == "__main__":
    checks_passed = 0
    total_checks = 5

    counter_a = make_counter()
    counter_b = make_counter()

    assert counter_a() == 1
    checks_passed += 1
    assert counter_a() == 2
    checks_passed += 1
    assert counter_a() == 3
    checks_passed += 1

    # Второй счётчик должен иметь независимое состояние.
    assert counter_b() == 1
    checks_passed += 1
    assert counter_a() == 4
    checks_passed += 1

    print(f"\n{checks_passed}/{total_checks} проверок пройдено")
