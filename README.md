# Преобразование Хафа для кругов известного радиуса 

## Установка и запуск 
* Клонировать репозиторий к себе на устройство
* (все?)

## Поиск окружностей заданного радиуса на изображении

1) Добавьте изображение, на котором хотите найти окружности, в папку ```images```
2) В терминале перейдите в основную папку и запустите следующюю команду. 

```
poetry run hough_circle_transform <name_of_your_image.jpg> <radius>
```
Первым параметром укажите имя изображения (в примере это ```coins.jpg```), вторым - радиус искомой окружности (в примере - ```80```).

Пример запуска:

<image src="readme_pictures/1.jpg">

Результаты сохранятся в папку ```results```, в подпапку с именем вашего изображения. (Никакие папки создавать не надо, оно сделается само). 

Пример результата работы алгоритма (была просто картинка с монетками, алгоритм наримовал окружности радиуса 60, которые нашел): 

<image src="readme_pictures/result_60.jpg">

Сам алгоритм лежит в файле ``` src/hypermodern_python/console.py ```

## Запуск тестов 

Тесты прописаны в файле ``` tests/test_console.py```
* Чтобы их запустить из термиала (из основной папки), введите следующую команду: 

```
poetry run pytest 
```
Пример запуска:

<image src="readme_pictures/2.jpg">

Тесты запускаются, используя изображения ```1.jpg``` ```2.jpg``` и ```3.jpg``` из папки ```images```, поэтому если вдруг их там нет (по какой-то причине), то тесты проходиться, очевидно, не будут.
Результаты работы алгоритма на тестовых изображениях лежат все в той же папке ```results```.

* Если хотите посмотреть, какую часть основного кода алгоритма покрывают тесты, запустите ту же команду с опцией ```--cov```

```
poetry run pytest --cov
```
Пример:

<image src="readme_pictures/3.jpg">

Здесь требуемое покрытие кода установлено на 50% (это можно настроить в файле ```pyproject.toml```, раздел ```[tool.coverage.report]```, параметр ```fail_under```)


