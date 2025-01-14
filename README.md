# Робот Яндекс доставщик на Bluetooth управлении

Идея была взята из статьи на хабре https://habr.com/ru/articles/809953/

## Ровер

Изначально идёт с инерционным двитателем.
Ровер на озон - https://ozon.ru/t/woxBn6P
Цена: 1900р

## Мозги
В качестве мозков был взят модуль xiao esp32-c6
На aliexpress https://sl.aliexpress.ru/p?key=7TFhG4b
Можно взять на ozon примерно за ту же цену, я брал на ozon.
Цена: 600-700р 

## Двигатели
Я пытался найти с редуктором которые будут достаточно мощные при малом токе
Взял вот такие https://sl.aliexpress.ru/p?key=NLFhGTx
Stage3 242rpm
Цена: 800р (за 2 шт) + доставка 280р

## Батарейка
Как в статье.
Аккумуляторная батарейка 042030 (30x20x4 мм)
Цена: 250р

## Контроллер моторов
MX1508 модуль драйвера https://ozon.ru/t/rNKN8pA
Цена: 200р

## Проводки, припой, паяльник

Уже были, брал давно вот такие, очень рекомендую https://ozon.ru/t/n1xzQPe
Паяльник pine64
Припой - какой-то дефолт с озона.

## Разработка прошивки

Я решил разрабатываться на python, поэтому шить в контроллер будем micropython.
XIAO esp32-c6 нужно шить micropython-ом с сайта разработчика https://wiki.seeedstudio.com/xiao_esp32c6_micropython/

Шить нужно как описано вот тут https://micropython.org/download/esp32c6/

В коде ничего сложного, труднее всего было уложить в голове про BLE

Закидываем прошивку на устройство
```
mpremote cp ble_server_main.py :main.py
```
Или запускаем прямо с компа
```
mpremote run ble_server_main.py
```

mpremote поставить по инструкции https://docs.micropython.org/en/latest/reference/mpremote.html

## Разработка приложения

Выбрал опцию для людей которым плохо при виде java (и kotlin тоже)
Есть прекрасный визуальный мышевозильный сервис для сборки приложений https://ai2.appinventor.mit.edu
Как можно понять, он достаточно мощный, потому-что я смог там собрать приложение для работы с BLE (Bluetooth Low Energy).
Проект приложения так же приложил в исходный код.

## Питонячие тонкости...

typeshed: https://micropython-stubs.readthedocs.io/en/main/11_install_stubs.html

```
uv venv .venv
uv pip install -r requirements-dev.txt
```
