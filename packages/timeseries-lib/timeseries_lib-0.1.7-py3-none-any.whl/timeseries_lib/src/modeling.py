from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from keras.src.layers import LayerNormalization, MultiHeadAttention

import numpy as np
import keras
from keras import Sequential, Model
from keras.src.layers import LSTM, Dense, Input, Bidirectional
from datetime import datetime

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeMixer
from neuralforecast.losses.pytorch import MAE, MSE, MAPE, RMSE, SMAPE, MASE
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def prepare_data_tm(df, date_col, target_col):
    """
    Сервисная функция. Преобразовывает данные для TimeMixer

    df: DataFrame с данными
    date_col: название столбца с датами
    target_col: название столбца с целевой переменной

    return: измененные данные
    """
    df = df.copy()
    df = df.reset_index()
    df.rename(columns={date_col: 'ds', target_col: 'y'}, inplace=True)
    df['unique_id'] = 'series'
    df = df.sort_values('ds')
    columns_to_keep = ['unique_id', 'ds', 'y']

    exog_cols = [col for col in df.columns if col not in ['unique_id', 'ds', 'y']]
    columns_to_keep.extend(exog_cols)

    df = df[columns_to_keep]

    return df

def ar_model(series, lags):
    """
    Создание и обучение авторегрессионной модели (AR)

    series: временной ряд
    lags: количество лагов (задержек)
    """

    model = ARIMA(series, order=(lags, 0, 0))
    model_fit = model.fit()

    return model_fit


def ma_model(series, lags):
    """
    Создание и обучение модели скользящего среднего (MA)

    series: временной ряд
    lags: количество лагов (задержек)
    """

    model = ARIMA(series, order=(0, 0, lags))
    model_fit = model.fit()

    return model_fit


def arima_model(series, order=(1, 1, 1)):
    """
    Создание и обучение модели ARIMA

    series: временной ряд
    order: параметры модели ARIMA (p, d, q)
    """

    model = ARIMA(series, order=order)
    model_fit = model.fit()

    return model_fit


def sarimax_model(series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
    """
    Создание и обучение модели SARIMA
    """
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit()
    return model_fit


def holt_winters_model(series, seasonal_periods, trend='add', seasonal='add'):
    """
    Создание и обучение модели Хольта-Винтерса

    series: временной ряд
    seasonal_periods: количество периодов сезонности
    trend: тип тренда (add или mul)
    seasonal: тип сезонности (add или mul)
    """

    model = ExponentialSmoothing(series, trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
    model_fit = model.fit()
    return model_fit


def lstm_model(series, n_steps, layer_config, n_features=1, epochs=10, batch_size=1):
    """
    Создание и обучение модели LSTM с динамической конфигурацией слоев, включая поддержку Bidirectional LSTM.

    series (np.array): Временной ряд в формате массива numpy.
    n_steps (int): Количество временных шагов для каждого входного образца.
    layer_config (list of dicts): Конфигурация слоев в виде списка словарей.
    n_features (int): Количество признаков на временной шаг (обычно 1 для одномерного временного ряда).
    epochs (int): Количество эпох обучения.
    batch_size (int): Размер батча при обучении.
    """

    X, y = [], []
    for i in range(len(series) - n_steps):
        X.append(series.iloc[i:i + n_steps].values)  # Используем .iloc и .values для извлечения данных
        y.append(series.iloc[i + n_steps])  # Используем .iloc для доступа к элементу по позиции
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    model = Sequential()
    first_layer = True  # Флаг для первого слоя

    for layer in layer_config:
        if layer['type'] == 'LSTM':
            if first_layer:  # Если это первый слой, задаем input_shape
                input_shape = (n_steps, n_features)
                first_layer = False  # Сброс флага после добавления первого слоя
            else:
                input_shape = None

            lstm_layer = LSTM(layer['units'], activation=layer.get('activation', 'relu'),
                              return_sequences=layer.get('return_sequences', True),
                              input_shape=input_shape)

            if layer.get('bidirectional', False):
                model.add(Bidirectional(lstm_layer))
            else:
                model.add(lstm_layer)
        elif layer['type'] == 'Dense':
            model.add(Dense(layer['units'], activation=layer.get('activation', 'relu')))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

    # Вычисление метрик
    y_pred = model.predict(X)
    errors = {}
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    errors['MSE'] = round(mse, 4)
    errors['MAE'] = round(mae, 4)
    errors['R²'] = round(r2, 4)

    # Сохранение модели в файл
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model.save(f'lstm_model_{timestamp}.h5')

    return model, errors


def timemixer_model(data, date_col, target_col, h=None, config=None):
    """
    Создает, обучает модель TimeMixer и выполняет прогнозирование.

    data: DataFrame с обучающими данными
    date_col:  название столбца с датами
    target_col:  название столбца с целевой переменной
    h: горизон планирования (по умолчанию половина обучающей выборки)
    config:  конфигурация модели (опционально)
    Все конфигурации модели можно посмотреть по ссылке: https://nixtlaverse.nixtla.io/neuralforecast/models.timemixer.html

    return: обученная модель
    """
    h = int(len(data) * 0.5) - 1

    default_config = {
        'h': h,
        'freq': 'D',
        'input_size': 2 * h,
        'n_series': 1,
        'loss': MAE(),
        'scaler_type': 'standard',
        'max_steps': 500,
        'learning_rate': 1e-3,
    }

    if config:
        default_config.update(config)

    train_df = prepare_data_tm(data, date_col, target_col)

    timemixer = TimeMixer(
        h=default_config['h'],
        input_size=default_config['input_size'],
        n_series=default_config['n_series'],
        loss=default_config['loss'],
        scaler_type=default_config['scaler_type'],
        max_steps=default_config['max_steps'],
        learning_rate=default_config['learning_rate']
    )

    nf = NeuralForecast(models=[timemixer], freq=default_config['freq'])
    nf.fit(df=train_df)

    return nf
