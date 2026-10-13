"""Решение: замыкание-счётчик без утечки состояния наружу."""


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


if __name__ == "__main__":
    counter_a = make_counter()
    counter_b = make_counter()

    assert counter_a() == 1
    assert counter_a() == 2
    assert counter_a() == 3

    assert counter_b() == 1
    assert counter_a() == 4

    print("PASS")
