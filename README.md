#Преобразование Хафа для кругов известного радиуса 

##Установка и запуск 
* Клонировать репозиторий к себе на устройство
* (все?)

## Поиск окружностей заданного радиуса на изображении

1) Добавьте изображение, на котором хотите найти окружности, в папку ```images```
2) В терминале перейдите в основную папку и запустите следующюю команду. 

```
poetry run hough_circle_transform coins.jpg 60

```
Первым параметром укажите имя изображения, вторым - радиус искомой окружности.

Пример запуска:

<image src="readme_pictures/1.jpg">

Результаты сохранятся в папку ```results```, в подпапку с именем вашего изображения. (Никакие папки создавать не надо, оно сделается само). 

Пример результата работы алгоритма: 

<image src="readme_pictures/result_60.jpg">


