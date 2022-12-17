
cursor.execute(""
CREATE TABLE IF NOT EXISTS stock_price (
id INTEGER PRIMARY KEY,
stock_id INTEGER,
date NOT NULL,
open NOT NULL,
high NOT NULL,
Low NOT NULL,
close NOT NULL,
volume NOT NULL,
sma_20, sma_50,
rsi_14,
FOREIGN KEY (stock_id) REFERENCES stock (id)



for bar in barsets [symbol]:
	stock_id = stock_dict[symbol]
	if len(recent_closes) >= 50 and current_date = bar.t.date(): 
		sma_20 = tulipy.sma(numpy.array(recent_closes), period=20) [-1] 
		sma_50 = tulipy.sma(numpy.array(recent_closes), period=50) [-1] 
		rsi_14 = tulipy.rsi(numpy.array(recent_closes), period=14) [-1]
	else:
		sma_20, sma_50, rsi_14 = None, None, None
		
	cursor.execute('''INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_20, sma_50, | VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
	(stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))
connection.commit()		

