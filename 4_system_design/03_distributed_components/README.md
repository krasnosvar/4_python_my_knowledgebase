# Тема 03. Компоненты распределённой системы (Distributed Components)

## Зачем этот раздел

Инфраструктурные компоненты, которые связывают уже выделенные сервисы в единую систему: API Gateway, выбор БД под конкретный сервис (полиглот-персистентность), роль брокеров сообщений на уровне архитектуры, алгоритмы балансировки нагрузки, health checks и service discovery. Теория подкреплена runnable-примерами на чистом Python и упражнениями в формате сценариев системного дизайна.

**Уже знакомы с темой?** → [CHEATSHEET.md](./CHEATSHEET.md) — роль API Gateway, SQL vs NoSQL, алгоритмы балансировки, liveness vs readiness.

## Что нужно знать заранее

- Темы [01_architecture_styles](../01_architecture_styles/) и [02_performance_and_scaling](../02_performance_and_scaling/).
- Брокеры сообщений и SQL на уровне [2_data_and_messaging](../../2_data_and_messaging/), HTTP — на уровне [3_web_frameworks](../../3_web_frameworks/).

## Структура раздела

*   **[01_theory/](./01_theory/)** — теория, разбитая по подтемам:
    *   [01_api_gateway.md](./01_theory/01_api_gateway.md) — роль API Gateway, cross-cutting concerns, риск «толстого» шлюза, отличие от BFF.
    *   [02_databases_in_distributed_systems.md](./01_theory/02_databases_in_distributed_systems.md) — SQL vs NoSQL, когда что, полиглот-персистентность, согласованность между БД разных сервисов.
    *   [03_message_brokers_role.md](./01_theory/03_message_brokers_role.md) — роль брокера сообщений как компонента архитектуры: развязка, буферизация, асинхронность (без механики конкретных брокеров).
    *   [04_load_balancing.md](./01_theory/04_load_balancing.md) — алгоритмы балансировки: Round Robin, Weighted Round Robin, Least Connections, Least Response Time, IP Hash, Power of Two Choices.
    *   [05_health_checks_and_discovery.md](./01_theory/05_health_checks_and_discovery.md) — liveness vs readiness, client-side и server-side service discovery, реестр сервисов.
    *   [06_use_cases.md](./01_theory/06_use_cases.md) — практические применения: типичная сборка запроса, частые ошибки, мини-чеклист.
*   **[02_examples/](./02_examples/)** — runnable-примеры на чистом Python (без внешних зависимостей, детерминированные, завершаются сами):
    *   [01_load_balancer_algorithms](./02_examples/01_load_balancer_algorithms/main.py) — Round Robin против Least Connections на неоднородной по длительности нагрузке.
    *   [02_service_registry_health_checks](./02_examples/02_service_registry_health_checks/main.py) — реестр сервисов с heartbeat: зависший инстанс исключается из пула здоровых, восстановившийся — возвращается.
    *   [03_api_gateway_routing](./02_examples/03_api_gateway_routing/main.py) — минимальный шлюз: маршрутизация, аутентификация на периметре, rate limiting, без бизнес-логики внутри сервисов.
*   **[03_exercises/](./03_exercises/)** — сценарии системного дизайна (не код): описание ситуации и вопросы для письменного разбора.
    *   [01_design_the_gateway](./03_exercises/01_design_the_gateway.md) — определить границы ответственности API Gateway для конкретной системы.
    *   [02_pick_the_database](./03_exercises/02_pick_the_database.md) — подобрать БД под несколько сервисов с разным профилем нагрузки.
    *   [03_load_balancing_strategy](./03_exercises/03_load_balancing_strategy.md) — выбрать алгоритм балансировки под конкретный профиль трафика.
    *   [04_service_discovery_failure](./03_exercises/04_service_discovery_failure.md) — разобрать реальный отказ через призму health checks и discovery.
*   **[04_exercises_answers/](./04_exercises_answers/)** — разобранные рассуждения по тем же сценариям.

## Как проходить

1. Прочитайте теорию по подтемам в [01_theory/](./01_theory/), начиная с [01_api_gateway.md](./01_theory/01_api_gateway.md).
2. Запустите и изучите примеры из `02_examples/`:
   ```bash
   python3 ./02_examples/01_load_balancer_algorithms/main.py
   python3 ./02_examples/02_service_registry_health_checks/main.py
   python3 ./02_examples/03_api_gateway_routing/main.py
   ```
3. Проработайте сценарии в `03_exercises/` письменно, прежде чем заглядывать в разбор.
4. Сверьте свои рассуждения с [04_exercises_answers/](./04_exercises_answers/).

## Когда двигаться дальше

Когда можете определить границы ответственности API Gateway, подобрать БД и алгоритм балансировки под профиль нагрузки и объяснить разницу между liveness и readiness — переходите к [04_case_studies](../04_case_studies/).
