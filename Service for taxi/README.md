# Прогноз количества заказов для сервиса такси

[ipynb](https://github.com/Krasnov-Andrey/Portfolio/blob/main/Service%20for%20taxi/Service%20for%20taxi.ipynb)

## Описание проекта

Требуется спрогнозировать количество заказов такси на следующий час для системы предсказания объема заказов и привлечения большего количества водителей в период пиковой нагрузки.

## Направление 
- Машинное обучение
- Регрессия
- Statsmodels
- Временные ряды

## Навыки и инструменты

- **python**
- **pandas**
- **numpy**
- statsmodels.tsa.seasonal.**seasonal_decompose**
- sklearn.model_selection.**TimeSeriesSplit**
- sklearn.model_selection.**GridSearchCV**
- sklearn.metrics.**mean_squared_error**
- sklearn.linear_model.**LinearRegression**
- sklearn.ensemble.**RandomForestRegressor**
- catboost.**CatBoostRegressor**
- **matplotlib**

## Общий вывод

Проведено исследование временного ряда на предмет трендовых и сезонных закономерностей, случайной составляющей. Проведено исследование трёх типов моделей, выбрана линейная регрессия.
