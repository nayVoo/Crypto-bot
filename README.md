# Crypto-bot

# ENG.

This Python bot is designed for monitoring cryptocurrency prices on the Binance exchange and executing trading operations in the testnet mode. Let's go through the key elements of the code:

Used Libraries:

The code utilizes various libraries, such as aiohttp, asyncio, threading, websockets, pandas, and binance. These libraries provide tools for network operations, asynchronous task execution, data processing, and interaction with the Binance API.
Authentication:

The bot uses API keys for authentication on the Binance testnet. The keys are stored in environment variables and loaded using the dotenv library.
Loading Tokens:

The bot loads the list of tokens and contracts available on the Binance exchange using the corresponding API methods.
Token Sorting:

The sort_token function sorts the list of tokens, excluding those listed in the delete_list.
Fetching Candlestick Data:

The get_klines function retrieves candlestick data (price charts) for each token in the list and creates a DataFrame with information on high, low, open, close prices, and dates.
Connecting to the Data Stream:

The socket_connect function establishes a connection to the Binance data stream, subscribes to the candlestick stream for each token, and asynchronously processes incoming data.
Data Comparison and Analysis:

The compare_price_tokens function compares the current price with previous extremes and, based on certain conditions, makes decisions about buying or selling a coin.
Launching the Main Function:

The main function, main, is launched to asynchronously connect to the data stream.
Bot Execution:

At the end of the code, the condition if __name__ == '__main__': is used to run the bot by calling asyncio.run(main()).
Note that the code interacts with real data sources and the Binance testnet. If considering using this code in live trading conditions, caution and additional testing are advised. Additionally, it's important to adhere to ethical standards and legal requirements when developing and deploying trading bots.


# RUS.

Этот бот написан на Python и предназначен для мониторинга цен на криптовалютные активы на бирже Binance, а также для выполнения торговых операций в режиме тестовой площадки (testnet). Давайте рассмотрим ключевые элементы кода:

Используемые библиотеки:

Код использует различные библиотеки, такие как aiohttp, asyncio, threading, websockets, pandas и binance. Эти библиотеки предоставляют инструменты для работы с сетью, выполнения асинхронных задач, обработки данных и взаимодействия с API биржи Binance.
Аутентификация:

Бот использует API-ключи для аутентификации на тестовой площадке Binance. Ключи хранятся в переменных окружения и загружаются с использованием библиотеки dotenv.
Загрузка токенов:

Бот загружает список токенов и контрактов, доступных на бирже Binance, с использованием соответствующих методов API.
Сортировка токенов:

Функция sort_token выполняет сортировку списка токенов, исключая те, которые находятся в списке delete_list.
Получение данных свечей:

Функция get_klines получает свечи (курсовую графику) для каждого токена в списке и формирует датафрейм с данными по высоким, низким, открытым ценам и датам.
Подключение к потоку данных:

Функция socket_connect устанавливает соединение с потоком данных биржи Binance, подписывается на поток свечей для каждого токена и асинхронно обрабатывает поступающие данные.
Сравнение и анализ данных:

Функция compare_price_tokens сравнивает текущую цену с предыдущими экстремумами и, в зависимости от условий, принимает решение о покупке или продаже монеты.
Запуск основной функции:

Основная функция main запускает асинхронное подключение к потоку данных.
Запуск бота:

В конце кода используется условие if __name__ == '__main__':, чтобы запустить бот, вызвав функцию asyncio.run(main()).
Обратите внимание, что код обращается к реальным источникам данных и тестовой площадке Binance, поэтому использование этого кода в реальных торговых условиях требует осторожности и дополнительного тестирования.
