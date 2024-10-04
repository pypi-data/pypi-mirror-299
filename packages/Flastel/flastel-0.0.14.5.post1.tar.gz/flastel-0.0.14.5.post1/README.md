
## Installation

```bash
  pip install flastel
```
    

# Flastel
Flastel is a new module for creating a Telegram bot.    
    You will be able to create several bots on your site by setting them up on your hosting.    
    The "polling" mode is also supported.   
    With the "webhook" method, you don't need multi-mode support.
    You no longer need to create a background specifically for the bot.     
    This module supports weak hosting, which allows you to save money. 



## Usage/Examples

```
from Flastel import TelegramPollingBot
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = "bot_token"
bot = TelegramPollingBot(bot_token)

@bot.command(commands=["/start"], caps_ignore=False)
async def start_command(message):
    chat_id = message.chat_id
    from_user_name = message.from_user.all_name
    await bot.send_message(chat_id, f"Привіт, {from_user_name}! Це стартова команда.", parse_mode="HTML")
    
@bot.command_with_params(commands=["/start"], params=["play", "say", "pay"])
async def start_command_with_params(message, params):
    chat_id = message.chat_id
    from_user_name = message.from_user.all_name
    await bot.send_message(chat_id, f"Привіт, {from_user_name}! Це стартова команда з параметрами {params}.")

@bot.messages_text(messages_txt=["Hello"],  caps_ignore=True)
async def message_handler(message):
    chat_id = message.chat_id
    from_user_name = message.from_user.all_name
    await bot.send_message(chat_id, f"Привіт, {from_user_name}! Дякую за таку привітність.")

@bot.command(commands=["/donate"], caps_ignore=False)
async def donate_command(message):
    user_id = message.chat_id
    title = 'На розвиток модуля'
    description = 'Ня, насправді ці кошти підуть на каву розробнику ʕ•́ᴥ•̀ʔっ'
    payload = 'new_donate'
    currency = 'XTR'
    prices = ['Donates', 10]
    await bot.send_pay(user_id, title, description, payload, currency, prices, in_support=False)

@bot.pay_pre(currency="XTR", prices=[10, 20])
async def handle_xtr_payment(query_data):
    await bot.ok_pay(query_data)

@bot.successful_payment(currency="XTR", prices=[10, 20])
async def handle_successful_xtr_payment(payment_data):
    chat_id = payment_data.chat_id
    await bot.send_message(chat_id,
                f"""Дякую за кружечку кави, тепер на у мене на одну кружку більше!
              （っ＾▿＾）\nᕙ(^▿^-ᕙ) {payment_data.total_amount}{payment_data.currency}""")

if __name__ == "__main__":
    asyncio.run(bot.run_polling())
```


## Links
[Telegram Chat](https://t.me/Flastele)     
[PyPI](https://pypi.org/project/Flastel/)   
[Wiki](https://github.com/DepyXa/Flastel/wiki)


## Support

For support, email gosdepyxa@gmail.com.

