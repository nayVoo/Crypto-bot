import aiohttp
import asyncio
import threading
import websockets
import pandas as pd
from datetime import datetime
from binance.client import Client
import unicorn_binance_websocket_api
import json

import os
from dotenv import load_dotenv

load_dotenv()


test_api_key = os.getenv('test_api_key')
test_api_secret = os.getenv('test_api_secret')





start = datetime.now()
client = Client(test_api_key, test_api_secret, testnet=True) #testnet = fake trade platform

token_list = []
futures_list = []
sort_list = ['BTC', 'ETH', 'ETHBTC', 'LTCBTC', 'BNBBTC', 'BTCUSDT', 'ETHUSDT', 'TRXBTC', 'XRPBTC', 'BNBUSDT',
	'LTCUSDT','LTCBNB', 'XRPUSDT', 'XRPBNB', 'TRXBNB', 'TRXUSDT', 'NEOBTC', 'QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH',
	'GASBTC', 'BNBETH', 'LRCBTC', 'LRCETH', 'QTUMBTC', 'ZRXBTC', 'KNCBTC', 'FUNETH', 'NEOETH', 'IOTABTC', 'IOTAETH',
	'LINKBTC', 'LINKETH', 'XVGETH', 'MTLBTC', 'EOSBTC', 'SNTBTC', 'ETCETH', 'ETCBTC', 'ZECBTC', 'ZECETH', 'BNTBTC',
	'ASTBTC', 'DASHBTC', 'DASHETH', 'OAXBTC', 'REQBTC', 'VIBBTC', 'TRXETH', 'POWRBTC', 'POWRETH', 'XRPETH', 'ENJBTC']

df_columns = [] # Для столпцов в удобном для меня виде
extremum_dict = {} #Для списка highc, lowc, highf, lowf, openc, UTC, сюда довольное быстро производиться запись
volume_dict = {} # Для токенов


#Список токенов
def get_sort_token():
	global token_list
	spot_info = client.get_exchange_info()
	spot_list = [symbol['symbol'] for symbol in spot_info['symbols'] if symbol.get('permissions', [])[0] == 'SPOT']
	token_list.extend(spot_list)
	#print(token_list)
	#Сюда кидаю монеты и они сортируються, потом сделать так что бы ещё и delete_lsit кидался в дальнейшем
	to_sort = [x for x in token_list if x in sort_list]
	token_list = to_sort
	return token_list




#Список фючерсов
def get_futures():
	global futures_list
	contact_info = client.futures_exchange_info()
	contact_list = [contract['symbol'] for contract in contact_info['symbols'] if contract.get('contractType', None) == 'PERPETUAL'] 
	futures_list.extend(contact_list)



#Получаем свечи и их значения
#def get_klines(symbol_list):
#	global df_columns
#	global extremum_dict
#	global volume_dict
#	df = pd.DataFrame(columns=symbol_list, index=['highc', 'lowc', 'highf', 'lowf', 'openc', 'UTC'])
#	print(df)
#
#	for symbol in symbol_list:
#		klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=5)
#		try:
#			openc = float(klines[-1][1])
#			highc = float(klines[-1][2])
#			lowc = float(klines[-1][3])
#			highf = float(klines[0][2])
#			lowf = float(klines[0][3])
#			UTC = formatted_time = datetime.utcfromtimestamp(float(klines[-1][0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
#		except Exception as ex: print(f'Exception in get_klines: {ex}')
#		df.loc['highc', symbol] = highc # Цена верхней свечи сейчас
#		df.loc['lowc', symbol] = lowc # Цена нижней свечи сейчас
#		df.loc['highf', symbol] = highf # Цена верхней нижней свечи
#		df.loc['lowf', symbol] = lowf # Цена первой нижней свечи
#		df.loc['openc', symbol] = openc # Цена текущего открытия
#		df.loc['UTC', symbol] = UTC # Время открытия
#		volume_dict[symbol] = symbol
#
#
#	df = df.T #строки в столбцы or столбцы в строки
#	df_columns = df
#	df_dict = df.to_dict()
#	print('data dicttt----------------------------')
#	for symbol, value_dict in df_dict.items():
#		for key in value_dict.keys(): #symbol - назва столбца (highc,lowc,countc...), в value_dict дохера инфы поэтому ещё один цикл
#			extremum_dict[key] = {
#			'highc': df_dict['highc'][key], 'lowc': df_dict['lowc'][key], 
#			'highf': df_dict['highf'][key], 'lowf': df_dict['lowf'][key], 
#			'openc': df_dict['openc'][key], 'UTC': df_dict['UTC'][key],
#			}
#
#	print(extremum_dict)
#
		##		ASYNC VERSION OF KLINES			##
async def get_klines(symbol_list):
    global df_columns
    global extremum_dict
    global volume_dict

    # Construct DataFrame without await
    df = pd.DataFrame(columns=symbol_list, index=['highc', 'lowc', 'highf', 'lowf', 'openc', 'UTC'])
    print(df)

    for symbol in symbol_list:
        klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=5)
        try:
            openc = float(klines[-1][1])
            highc = float(klines[-1][2])
            lowc = float(klines[-1][3])
            highf = float(klines[0][2])
            lowf = float(klines[0][3])
            timestamp = float(klines[-1][0]) / 1000
            UTC = formatted_time = datetime.utcfromtimestamp(float(klines[-1][0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as ex:
            print(f'Exception in get_klines: {ex}')

        df.loc['highc', symbol] = highc
        df.loc['lowc', symbol] = lowc
        df.loc['highf', symbol] = highf
        df.loc['lowf', symbol] = lowf
        df.loc['openc', symbol] = openc
        df.loc['UTC', symbol] = UTC
        volume_dict[symbol] = symbol

    df = df.T  # строки в столбцы or столбцы в строки
    df_columns = df
    df_dict = df.to_dict()
    print(df)
    print('data dicttt----------------------------')
    for symbol, value_dict in df_dict.items():
        for key in value_dict.keys():
            extremum_dict[key] = {
                'highc': df_dict['highc'][key], 'lowc': df_dict['lowc'][key],
                'highf': df_dict['highf'][key], 'lowf': df_dict['lowf'][key],
                'openc': df_dict['openc'][key], 'UTC': df_dict['UTC'][key],
            }

    #print(extremum_dict)





async def socket_connect(symbol_list):
	global volume_dict
	url = 'wss://stream.binance.com:9443/stream?streams='
	async with websockets.connect(url, ping_interval=None) as bwebsocket: # подключаемся к бинансу по url
		message = { # и задаём запрос
		'method': 'SUBSCRIBE',
		'params': [f'{symbol.lower()}@kline_1d' for symbol in symbol_list], #просто преврашаем монеты в нижний регистр
		'id': 1
		}
		#print(message)
		await bwebsocket.send(json.dumps(message)) #отправляем запрос в виде Json
		data = json.loads(await bwebsocket.recv()) #ждём инфо от серва и декодируем
		#print('Data: ',data)
		count = 0
		async for sock in bwebsocket: #опять ждём инфо и проходимся по каждому елементу
			data = json.loads(sock)

			stream = data.get('stream', None) # Свеча
			symbol = data.get('data', {}).get('k', {}).get('s', None) # Монета


			open_price = float(data.get('data', {}).get('k', {}).get('o', None)) # Цена открытия
			close_price = float(data.get('data', {}).get('k', {}).get('c', None)) # Цена закрытия

			high_price = float(data.get('data', {}).get('k', {}).get('h', None)) # Цена найбольшей
			low_price = float(data.get('data', {}).get('k', {}).get('l', None)) # Цена найменьшей

			volume = float(data.get('data', {}).get('k', {}).get('q', None)) #Обьем

			open_or_close = data.get('data', {}).get('k', {}).get('x', None) # Открыта или закрыта

			#print('DATA:', data)
			#print('Stream: ', stream)
			#print('Symbol: ', symbol)
			#print('Open: ', open_price)
			#print('Close: ', close_price)
			#print('Highest: ', high_price)
			#print('Lowest: ', low_price)
			#print('Open or close: ', open_or_close)
			count += 1
			if open_or_close == False or volume_dict[symbol] == None:
				volume_dict[symbol] = volume
				compare_price_tokens(close_price,symbol,volume)#symbol, open_price, close_price, high_price, low_price, volume)
			if count == 3:
				break

#ВОТ ТУТ МНЕ НУЖНО СДЕЛАТЬ ПИЗДЕЦ СЛОЖНЫЕ ВЫЧИСЛЕНИЯ для покупки и продажи
def compare_price_tokens(price, symbol, volume):#(symbol, open_price, close_price, high_price, low_price, volume):
	global volume_dict

	#НУЖНО ДОБАВИТЬ НЕСКОЛЬКО HIGH, LOW И ПО ИНДЕКСАМ РАССПРЕДЕЛИТЬ НА HIGH_1, HIGH_2... И ЧТО БЫ ОНО ОРИЕНТИРОВАЛОСЬ НА ПРЕД


	top = 2 # сколько раз обьем должен привысить себя что бы мы вошли
	money = 20000 # бюджет
	stoploss = 0.5 # пол процента
	
	stop = 1 - stoploss/100
	stoplong = 1 + stoploss/100

	high = extremum_dict[symbol]['highc']
	low = extremum_dict[symbol]['lowc']
	try: delta_volume = int(volume/volume_dict[symbol]) # разница между текущим обьемом и предыдущим
	except: delta_volume = 0

	if (price <= (1.005 * high) and price > high) and delta_volume >= top: # Если цена уже вошла в низкий диапазон то покупаем
		print(f'found situation on {symbol}. High is {high}')
		orders(price, symbol)
	elif (price >= (0.995 * low) and price < low) and delta_volume >= top: # Если же наоборот поднялась в диапазон то продажа монеты
		print('for futures trading')
		print(symbol, high)
	if price >= 1.005 * high or price <= low * 0.995: # Если же держиться на среднем уровне то ничего
		pass
		print('delete extremum and add new')
#ПРОВЕЛ ТЕСТ, ОШИБОК НЕТУ


get_sort_token()
asyncio.run(get_klines(token_list))


async def main():
    await socket_connect(token_list)
if __name__ == '__main__':
    asyncio.run(main())
