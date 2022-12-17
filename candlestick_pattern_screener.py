
import talib

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
data['Morning Star'] = morning_star
data['Engulfing'] = engulfing
engulfing_days = data[data['Engulfing'] != 0]

print(engulfing_days)
