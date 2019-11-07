# Сервер для развертывания предсказательных моделей

## Структура базовых файлов

- `ch_pat_service.py` - рабочая версия сервиса и базовое (отладочное) приложение №1 на "чистом" [flask](https://flask.palletsprojects.com/)
- `ch_pat_dash_app.py` - базовое (отладочное) приложение №2 с использованием [dash](https://plot.ly/dash/)
- `ch_pat_model.py`, `model_basics.py` - базовый класс и пример реализации предсказательной модели
- `ch_pat_models_management.py` - функции управления моделями
- `ch_pat_param_schema.py` - схема для валидации параметров на [marshmallow](https://marshmallow.readthedocs.io/)
- `params_list.csv` - список параметров
- `templates`, `static/css` - папки с файлами для рендеринга базового приложения №1
- `models` - папка с дампами обученных моделей

## Встраивание моделей

1) Внесение новой модели делается в отдельной ветке с pull request'ом по готовности.
1) Каждая модель описывается в файле `model_<специфичное имя>.py`, наследуясь от класса `ChPatModel` (`ch_pat_model.py`). При необходимости вспомогательные файлы, касающиеся этой модели, можно сохранить в отдельной папке (не в корне).
1) Для тестирования моделей в файле могут быть реализованы функции в файлах `test_<специфичное имя>.py` (можно использовать [pytest](https://docs.pytest.org/))
1) Обученная и настроенная модель сохраняется в pickle-файл с расширением `.pkl` в папке `models` с использованием метода `store_model`.
1) Необходимые входные параметры вносятся в таблицу в `params_list.csv` и в схему для валидации `ch_pat_param_schema.py`.

## Запуск приложения

### Основной рабочий вариант запуска (№1)

Приложение запускается из файла `ch_pat_service.py` командой:
```bash
python ch_pat_service.py
```
Становятся доступны следующие сервисы (адрес по умолчанию - http://127.0.0.1:5000/):
- `/ch_pat_service` - основная рабочая точка входа сервиса, используемая для интеграции (выход - json)
- `/ch_pat_service_ui` - точка входа сервиса, выдающая "читаемый" html
- `/` - отладочный интерфейс, формируемый по параметрам из `params_list.csv` для вызова сервиса `/ch_pat_service_ui`

### Отладочный/исследовательский вариант запуска (№2)

Приложение на dash запускается из файла `ch_pat_dash_app.py` командой:
```bash
python ch_pat_dash_app.py
```
По умолчанию приложение доступно по адресу http://127.0.0.1:8050/. 

### Дополнительные опции запуск на сервере

Запуск скриптом на bash (на сервере ДМ скрипт `~/run_ch_service.sh`):
```bash
export FLASK_APP=~/chronic-patient-model-service/ch_pat_service.py
cd ~/chronic-patient-model-service
flask run --host=0.0.0.0 &
```

Снятие фоновых процессов flask (на сервере ДМ скрипт `~/kill_ch_server.sh`):
```bash
killall flask
```
