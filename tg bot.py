from fake_useragent import UserAgent
import requests
import json
import telebot
from telebot import types
from secret import TOKEN

ua = UserAgent()
def collect_data():
    response = requests.get(
        url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap',
        headers={'user-agent': f'{ua.random}'}
    )

    with open('result.json', 'w') as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

def tg_bot():
    bot = telebot.TeleBot(TOKEN)
    @bot.message_handler(commands=['start'])
    def start(message):
        done_text = '<b>Thanks for using CoinMarketCap BOT</b>\n<i>To start: write "/info" or click on the <b>🧙🏻Information</b> button.</i>'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        best5 = types.KeyboardButton('🧙🏻Information')
        info = types.KeyboardButton('🧙🏻TOP 5')
        list = types.KeyboardButton('🧙🏻List')
        markup.add(best5, info, list)
        bot.send_photo(message.chat.id, 'https://s2.coinmarketcap.com/static/cloud/img/news/placeholder1-new.jpg', caption=f'{done_text}', reply_markup=markup, parse_mode='html')


    @bot.message_handler(commands=['top5'])
    def top5(message):
        done_text = str()
        with open('result.json') as file:
            data = json.load(file)

        for i in range(5):
            token = data['data']['cryptoCurrencyList'][i]['name']

            if round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], 4) == 0:
                res = '{:.8f}'.format(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'])
                price = res

            elif int(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price']) == 0:
                for j in range(2, 5, 2):
                    if round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], j) == 0:
                        continue
                    else:
                        price = round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], j)
                        break
            else:
                price = round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], 2)

            link_name = data['data']['cryptoCurrencyList'][i]['slug']
            link = f'https://coinmarketcap.com/currencies/{link_name}'
            done_text += f'\n🟢Name: <b>{token}</b>\n💹Price <b>{price}$</b>\n📂Link: <b>{link}</b>\n'
        bot.send_message(message.chat.id, f'{done_text}', disable_web_page_preview=True, parse_mode='html')


    @bot.message_handler(commands=['info'])
    def info(message):
        done_text = '<b>To check the first five CMC tokens:</b> write /top5 or click 🧙🏻TOP-5 button\n\n<b>To check your token:</b> write its name\n\n<b>To check the entire list of tracked tokens:</b> write /list or click 🧙🏻List button'
        bot.send_message(message.chat.id, f'{done_text}', parse_mode='html')


    @bot.message_handler(commands=['list'])
    def list(message):
        done_text = '<b>List of all tracked coins:</b>'
        with open('result.json') as file:
            data = json.load(file)
        done_list = []
        d_list = str()
        for i in range(100):
            hneed = data['data']['cryptoCurrencyList'][i]['name']
            done_list.append(hneed)
        for i in range(99):
            d_list += f'{done_list[i]}, '
            if i != 0 and i % 3 == 0:
                d_list += '\n'
        d_list += f'{done_list[99]}.'
        bot.send_message(message.chat.id,f'🧙🏻{done_text}\n\n{d_list}', parse_mode='html')


    @bot.message_handler(content_types='text')
    def user_text(message):

        with open('result.json') as file:
            data = json.load(file)

        for i in range(100):
            msg = message.text
            dta = data['data']['cryptoCurrencyList'][i]['name']
            if msg.upper().lower() == dta.upper().lower():
                tname = data['data']['cryptoCurrencyList'][i]['name']
                lname = data['data']['cryptoCurrencyList'][i]['slug']
                link = f'https://coinmarketcap.com/currencies/{lname}'
                if round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], 4) == 0:
                    res = '{:.8f}'.format(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'])
                    price = res

                elif int(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price']) == 0:
                    for j in range(2, 5, 2):
                        if round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], j) == 0:
                            continue
                        else:
                            price = round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], j)
                            break
                else:
                    price = round(data['data']['cryptoCurrencyList'][i]['quotes'][2]['price'], 2)
                bot.send_message(message.chat.id, f'🟢Name: <b>{tname}</b>\n<b>💹Price: {price}$</b>\n<b>📂Link: {link}</b>',disable_web_page_preview=True ,parse_mode='html')
            else:
                continue

        if message.text == '🧙🏻TOP 5':
            top5(message)
        elif message.text == '🧙🏻Information':
            info(message)
        elif message.text == '🧙🏻List':
            list(message)


    bot.polling(non_stop=True)

def main():
    collect_data()
    tg_bot()

if __name__ == '__main__':
    main()
