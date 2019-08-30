# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_token import TOKEN # This file is not going to be uploaded to public Github
from datetime import datetime
import requests, re, scraper, logging

followed_crns = list()
chat_id = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def follow(bot, update, args):
    
    """
    Adds crns to the followed_crns list.

    """    
    global followed_crns, chat_id
    chat_id = update.message.chat_id
    
    for arg in args:
        followed_crns.append(str(arg))
        bot.send_message(chat_id = chat_id, text = str(arg) + " listeye başarıyla eklendi.")
        
    followed_crns = list(set(followed_crns)) # Remove duplicate entries
        
def unfollow(bot, update, args):
    
    """
    Removes crns from the followed_crns list.
    
    """   
    global followed_crns, chat_id
    chat_id = update.message.chat_id    
    
    for arg in args:
        try:
            followed_crns.remove(str(arg))
            bot.send_message(chat_id = chat_id, text = str(arg) + " artık takip edilmiyor.")
        except ValueError:
            bot.send_message(chat_id = chat_id, text = str(arg) + " takip edilenler arasında değil.")
            
def follow_reset(bot, update):
    
    """
    Resets the followed list.
    """
    
    global followed_crns, chat_id
    chat_id = update.message.chat_id
    
    followed_crns = list()
    bot.send_message(chat_id = chat_id, text = "Takip edilenler sıfırlandı.")
    
def show_followed(bot, update):
    
    """
    Shows the contents of the followed list.
    """
    
    global followed_crns, chat_id
    chat_id = update.message.chat_id
    
    if len(followed_crns) == 0:
        bot.send_message(chat_id = chat_id, text = "Gösterilecek bir şey yok.")
        
    for crn in followed_crns:
        bot.send_message(chat_id = chat_id, text = crn + "\t")
        
def show_help(bot, update):
    
    """
    Shows commands.
    """
    
    chat_id = update.message.chat_id
    text = """
/crntakip: Yeni CRNleri takip et.\n
/crnbirak: CRNyi takipten çıkar.\n
/sifirla: Bütün CRNleri takipten çıkar.\n
/izlemebasla: Uyarı sistemini başlat.\n
/goster: Takip edilen bütün CRNleri göster.\n
/yardim: Bu metni gör.\n
    \n    
Örnek Kullanım: /crntakip 7811 8931 yazarak bu iki CRN'yi takibe alabilirsiniz.\n
Yer boşaldığında uyarı gelmesi için /izlemebasla komutuyla izlemi başlatmanız gerekir.
    """
    bot.send_message(chat_id, text)
    
def check_crn(bot, job):
    
    """
    For every CRN in followed_crns list, check if there is any available space.
    """
    
    available = list()
    global followed_crns, chat_id
    
    with open("available_courses.txt") as txt_file:
        available = txt_file.read().lstrip("['").rstrip("']").split("', '")
        
    for crn in followed_crns:
        if (crn in available):
            bot.send_message(chat_id = job.context, text = crn + " kodlu derste boş yer var!")
    
def start(bot, update):
    
    """
    First message the user sees.
    """
    chat_id = update.message.chat_id
    text = "İTÜ Kontenjanlarını takip etmene yardımcı olmak için buradayım."
    bot.send_message(chat_id, text)
    show_help(bot, update)

    
def watch(bot, update, job_queue):

    """
    Start watching if there is any available space in the system.
    """    
    
    chat_id = update.message.chat_id
    t1 = datetime.now()  
    t2 = datetime(t1.year, t1.month, t1.day, t1.hour, 15, 20)
    t3 = datetime(t1.year, t1.month, t1.day, t1.hour, 30, 20)
    t4 = datetime(t1.year, t1.month, t1.day, t1.hour, 45, 20)
    t5 = datetime(t1.year, t1.month, t1.day, t1.hour + 1, 00, 20)
    first_run = min(abs(t2 - t1), abs(t3 - t1), abs(t4 - t1), abs(t5 - t1))
    job = job_queue.run_repeating(check_crn, 900, (t1 + first_run), context = chat_id)
    
    bot.send_message(chat_id = chat_id, text = "İzleme başlandı.")
    
#def unwatch(bot, update, job_queue):
#
#    """
#    Start watching if there is any available space in the system.
#    """    
#    
#    chat_id = update.message.chat_id    
#    bot.send_message(chat_id = chat_id, text = "İzlem bırakıldı.")
    
def main():
    updater = Updater(token=TOKEN)
    
    dispatcher = updater.dispatcher
    
    job_q = updater.job_queue
    
    handler_list = [CommandHandler("start", start),
                    CommandHandler("crntakip", follow, pass_args=True),
                    CommandHandler("crnbirak", unfollow, pass_args=True),
                    CommandHandler("sifirla", follow_reset),
                    CommandHandler("goster", show_followed),
                    CommandHandler("izlemebasla", watch, pass_job_queue=True),
                    CommandHandler("yardim", show_help)]
                    
    for handler in handler_list:
        dispatcher.add_handler(handler)
        

    updater.start_polling()
    updater.idle()
    
main()
