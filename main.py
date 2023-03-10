import json
from binance import Client
import datetime

symbol = 'ETHUSDT'

now = datetime.datetime.now()
with open('secret.json', 'r') as file:
    secret_list = json.load(file)
client = Client(secret_list["api_key"], secret_list["api_secret"])

name_file = f'{symbol}-{str(now.date())}:{str(now.hour)}-{str(now.minute)}-{str(now.second)}'
print(name_file)

with open(f'{name_file}.json', 'w') as file1:
    json.dump({f"{symbol}": f"{str(now.date())}"}, file1, indent=4)
num_par = 0
while True:
    depth = client.get_orderbook_ticker(symbol=symbol)
    with open(f'{name_file}.json', 'r') as file:
        all_list = json.load(file)
    all_list[num_par] = depth
    all_list[num_par]['TIME_HOUR'] = datetime.datetime.now().hour
    all_list[num_par]['TIME_MINUTE'] = datetime.datetime.now().minute
    all_list[num_par]['TIME_SECOND'] = datetime.datetime.now().second
    for item in all_list:
        if 'TIME_HOUR' in all_list[item]:
            if all_list[item]['TIME_HOUR'] == datetime.datetime.now().hour - 1\
                    and all_list[item]['TIME_MINUTE'] == datetime.datetime.now().minute:
                if float(all_list[item]['bidPrice']) <= float(depth['bidPrice']) * 0.99:
                    print('в сравнении с ценой за прошедший час, цена выросла более чем на 1%')
                elif float(all_list[item]['bidPrice']) >= float(depth['bidPrice']) * 1.01:
                    print('в сравнении с ценой за прошедший час, цена упала более чем на 1%')
    with open(f'{name_file}.json', 'w') as file2:
        json.dump(all_list, file2, indent=4)
    num_par += 1

