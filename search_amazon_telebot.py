import os
import telebot
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get('6162457611:AAHMDK5z-eLg1lTirbH7QIM5DSWOt4zBufk')
bot = telebot.TeleBot('6162457611:AAHMDK5z-eLg1lTirbH7QIM5DSWOt4zBufk')

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello, How are you doing?")

@bot.message_handler (content_types = ['text'])
def after_text (message):
     url = f'https://www.amazon.ae/s?k={message.text}'
     response = requests.get(url)
     content  = response.content
     soup = BeautifulSoup(content, 'html.parser')
     full_items = soup.find_all('div', {'class': 'a-section a-spacing-base'})
     result_item = []
     
     for item in full_items:
        try:
             item_image = item.find('img', {'data-image-latency':"s-product-image"}).attrs.get('src')
             item_model = item.find('span', {'class':"a-size-base-plus a-color-base a-text-normal"}).text
             item_price = item.find('span', {'class':"a-offscreen"}).text
             item_star = item.find('span', {'class':'a-icon-alt'}).text
        except:
             item_star = '0.0 out of 5 starts'
             item_image = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Fvector-art%2F500564-add-to-cart-icon-design&psig=AOvVaw2PEXgMBRZGAjFRqD66KyH7&ust=1681988012619000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCNCKnuHjtf4CFQAAAAAdAAAAABAh'
             item_model = ' '
             item_price = ' '

        item_link_last = item.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).attrs.get('href')
        item_full_link = 'https://www.amazon.ae/'+item_link_last
        item_full = {
             'item_model' : item_model,
             'item_image' : item_image,
             'item_price' : item_price,
             'item_star' : item_star,
             'item_link' : item_full_link
             }
        result_item.append(item_full)
    
     for i in range(5):
         item_image = result_item[i]['item_image']
         item_model = result_item[i]['item_model']
         item_price = result_item[i]['item_price']
         item_star  = result_item[i]['item_star']
         item_link  = result_item[i]['item_link']
         full_detail = "-->Model: "+item_model + "\n-->Price: " + item_price + "\n-->Star: "+ item_star + "\n-->Link: "+item_link
         bot.send_photo(message.chat.id, photo=item_image, caption=full_detail, reply_markup=None)

bot.polling(none_stop = True, interval = 0)