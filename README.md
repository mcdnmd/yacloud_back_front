# Item book
Backend и frontend для демонстрации работы YandexCloud

[Линк на фронт](https://itembook.website.yandexcloud.net/)

## Команды
Для взаимодействия с YandexCloud созданы шорткаты в `Makefile` все
команды небходимо выполнять в корне проекта

Например, посмотреть актуальные gateways можно так:
```bash
make show-gateway
```

Обновить настройки api-gateway:
```bash
make update-gateway
```

Обновить front:
```bash
make deploy-front
```

Обновить back:
```bash
make deploy-back
```

## Back
Весь бекенд реализован на `FastApi`. Работа с бд происходит через паттерн репозиторий. Попытался написать абстрактную
заготовку, в `backend/common/repository.py` с помощью которой можно масштабировать сущности в БД.
