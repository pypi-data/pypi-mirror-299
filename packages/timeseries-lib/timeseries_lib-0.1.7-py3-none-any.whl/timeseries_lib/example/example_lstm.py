import pandas as pd
from app.timeseries_lib import plot_time_series, lstm_model, load_model


data = pd.read_csv('COVID.csv', parse_dates=['date'])
data['released_percent'] = data['released'] / data['confirmed']
time_series = data.groupby('date')['released_percent'].sum()
print(time_series)

layer_config = [
    {'type': 'LSTM', 'units': 50, 'return_sequences': True, 'bidirectional': True},
    {'type': 'LSTM', 'units': 50, 'return_sequences': False},
    {'type': 'Dense', 'units': 1}
]
lstm_fit, errors = lstm_model(time_series, 10, layer_config, n_features=1, epochs=10, batch_size=1)
print(errors)

# lstm_fit_file = load_model('lstm_model_2024-09-15_21-57-45.h5', 'LSTM')
print(lstm_fit.summary())
