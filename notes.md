# Формат запроса
## Простой поиск

Для запроса

`обл. Нижегородская, г. Выкса, рп. Досчатое, пл. Советская, д. 1`

с поиском только по разделу "Мой дом" ссылка выглядит следующим образом:

`https://www.reformagkh.ru/search/houses?query=обл.+Нижегородская%2C+г.+Выкса%2C+рп.+Досчатое%2C+пл.+Советская%2C+д.+1&mh=on`

## Расширенный поиск

В случае заполнения формы расширенного поиска следующими сведениями:

* **Регион:** Нижегородская (обл)
* **Населённый пункт:** Выкса (г), Досчатое (рп)
* **Улица:** Советская (пл)
* **Номер дома:** 1
* **Раздел "Мой Дом":** ☑

клиент передаёт на сервер следующую информацию:

region=%D0%9D%D0%B8%D0%B6%D0%B5%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%28%D0%BE%D0%B1%D0%BB%29&region-guid=88cd27e2-6a8a-4421-9718-719a28a0a088&district=&district-guid=&settlement=%D0%92%D1%8B%D0%BA%D1%81%D0%B0+%28%D0%B3%29%2C+%D0%94%D0%BE%D1%81%D1%87%D0%B0%D1%82%D0%BE%D0%B5+%28%D1%80%D0%BF%29&settlement-guid=db90fa56-d1ef-4ff5-9c83-6323a13fb03a&street=%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F+%28%D0%BF%D0%BB%29&street-guid=40a338e8-81f5-4e9d-aa46-13fca3bbfb90&house=1&house-guid=d40b6416-fe68-b6f1-50fe-b2bd3ab2fcbe&op=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8&sections%5Ball%5D=0&sections%5Bhouses%5D=0&sections%5Bhouses%5D=1&sections%5Balarm%5D=0&sections%5Bunder_construction%5D=0&sections%5Bcompleted%5D=0&sections%5Boverhaul%5D=0

или:

```
region: Нижегородская (обл)
region-guid: 88cd27e2-6a8a-4421-9718-719a28a0a088
district:
district-guid:
settlement: Выкса (г), Досчатое (рп)
settlement-guid: db90fa56-d1ef-4ff5-9c83-6323a13fb03a
street: Советская (пл)
street-guid: 40a338e8-81f5-4e9d-aa46-13fca3bbfb90
house: 1
house-guid: d40b6416-fe68-b6f1-50fe-b2bd3ab2fcbe
op: Найти
sections[all]: 0
sections[houses]: 0
sections[houses]: 1
sections[alarm]: 0
sections[under_construction]: 0
sections[completed]: 0
sections[overhaul]: 0
```

# Результаты поиска

На странице с результатами поиска содержится ссылка на страницу интерующего дома:

```html
<a href="/myhouse/profile/view/6502713">обл. Нижегородская, г. Выкса, рп. Досчатое, пл. Советская, д. 1</a>
```

# Страница дома

Искомая информация размещена на странице дома в html коде.

"Общие сведения" и "Конструктивные элементы дома" загружаются сразу одной страницей.

## Общие сведения
### Год ввода в эксплуатацию
```html
<tr class="left">
    <td><b></b><span>Год ввода дома в эксплуатацию</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>1940</span></td>
</tr>
```
### Количество этажей
```html
<td colspan="2" class="colspan">
    <b></b><span class="title">Количество этажей:</span>
    <table class="col_list">
        <tbody>
        <tr class="left">
            <td><span>наибольшее, ед.</span></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td><span>Не заполнено</span></td>
        </tr>
        <tr class="left">
            <td><span>наименьшее, ед.</span></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td><span>Не заполнено</span></td>
        </tr>
        </tbody>
    </table>
</td>
```
### Последнее изменение анкеты
```html
<tr class="left">
    <td><span>Последнее изменение анкеты</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span class="black_text">
                            22.05.2015
                 в
                20:42
                    </span></td>
</tr>
```
### Серия и тип постройки
```html
<tr class="left">
    <td><b></b><span>Серия, тип постройки здания</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>Не заполнено</span></td>
</tr>
```
#### Для другого дома
```html
<tr class="left">
    <td><b></b><span>Серия, тип постройки здания</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>137</span></td>
</tr>
```
**Судя по всему, серия и тип постройки это одно и то же**
### Тип дома
```html
<tr class="left">
    <td><b></b><span>Тип дома</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>Многоквартирный дом</span></td>
</tr>
```
### Дом признан аварийным
```html
<tr class="left">
    <td><b></b><span>Дом признан аварийным</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>Да</span></td>
</tr>
```
### Кадастровый номер
```html
<tr>
    <th style="text-align:center">Кадастровый номер</th>
</tr>
</thead>
<tbody>
                                            <tr>
            <td style="padding: 10px;">Нет данных</td>
        </tr>
                                    </tbody>
```
## Конструктивные элементы дома
### Тип перекрытий
```html
<tr class="left">
    <td><b></b><span>Тип перекрытий</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>
         Не заполнено
    </span></td>
</tr>
```
### Материал несущих стен
```html
<tr class="left">
    <td><b></b><span>Материал несущих стен</span></td>
    <td></td>
</tr>
<tr>
    <td></td>
    <td><span>
         Не заполнено
    </span></td>
</tr>
```
