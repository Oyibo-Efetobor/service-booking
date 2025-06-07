import openpyxl
import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

async def send_broadcast(token: str, mode: int, message: str = '', excel_path: str = 'bot_users.xlsx'):
    if not os.path.exists(excel_path):
        print('No bot_users.xlsx file found.')
        return
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    bot = Bot(token=token)
    for row in ws.iter_rows(min_row=2, values_only=True):
        chat_id = row[0]
        try:
            if mode == 1:
                with open('online.png', 'rb') as img:
                    await bot.send_photo(chat_id=chat_id, photo=img, caption='BROADCAST: Chapel Booking Bot is ONLINE ✅')
                print(f"Online image sent to {chat_id}")
            elif mode == 2:
                with open('offline.png', 'rb') as img:
                    await bot.send_photo(chat_id=chat_id, photo=img, caption='BROADCAST: Chapel Booking Bot is OFFLINE ❌')
                print(f"Offline image sent to {chat_id}")
            elif mode == 3:
                await bot.send_message(chat_id=chat_id, text=f"BROADCAST MESSAGE FROM EFETOBOR.DEV🚨: \n\n{message}")
                print(f"Text message sent to {chat_id}")
        except Exception as e:
            print(f"Failed to send to {chat_id}: {e}")

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print('TELEGRAM_BOT_TOKEN not found in .env file.')
        exit(1)
    print('What do you want to broadcast?')
    print('1. Online image')
    print('2. Offline image')
    print('3. Text message')
    mode = input('Enter 1, 2, or 3: ').strip()
    if mode == '1':
        asyncio.run(send_broadcast(token, 1))
    elif mode == '2':
        asyncio.run(send_broadcast(token, 2))
    elif mode == '3':
        msg = input('Enter the broadcast message: ').strip()
        asyncio.run(send_broadcast(token, 3, msg))
    else:
        print('Invalid input. Exiting.')
