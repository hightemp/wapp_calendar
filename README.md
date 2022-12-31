# wapp_calendar

Календарь.

- произносится каждый час
- календарь текущего года
    - дни подписанные по месяцам
- каледнарь с днями для меток за 3 года

![](./screenshots/2022-12-31_08-33.png)
![](./screenshots/2022-12-31_08-33_1.png)

## Запуск

```bash
wget https://github.com/hightemp/wapp_calendar/releases/latest/download/wapp_calendar.pyz
chmod a+x ./wapp_calendar.pyz
./wapp_calendar.pyz
```

## Упаковка

```bash
# https://docs.python.org/3/library/zipapp.html
python3 -m zipapp wapp_calendar -p "/usr/bin/env python3"
```