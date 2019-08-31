# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_token import TOKEN # This file is not going to be uploaded to public Github
from datetime import datetime
import requests, re, scraper, logging, os, time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Below, we have job2 which is a remnant of the past. Now that we check if the
# data is old, we don't need a second check mechanism.

def is_data_old():
    
    """
    Checks the last modification of the available_courses file, returns
    False if it is modified in less than two minutes ago, returns True
    if it is older.
    """
    
    time_m_struct = time.localtime(os.path.getmtime("available_courses.txt"))
    dt = datetime.fromtimestamp(time.mktime(time_m_struct))
    time_passed = (datetime.now() - dt).seconds
    if (time_passed > 120):
        return True
    else:
        return False

def follow(bot, update, args, chat_data):
    
    """
    Adds crns to the followed_crns list.
    """
    
    if "follow" not in chat_data:
        followed_crns = list()
        chat_data["follow"] = followed_crns
        
    followed_crns = chat_data["follow"]
    chat_id = update.message.chat_id
    
    for arg in args:
        followed_crns.append(str(arg))
        bot.send_message(chat_id = chat_id, text = str(arg) + " listeye başarıyla eklendi.")
    
    followed_crns = list(set(followed_crns)) # Remove duplicate entries
    
    chat_data["follow"] = followed_crns
        
def unfollow(bot, update, args, chat_data):
    
    """
    Removes crns from the followed_crns list.
    
    """   
    if "follow" not in chat_data:
        followed_crns = list()
        chat_data["follow"] = followed_crns
        
    followed_crns = chat_data["follow"]
    chat_id = update.message.chat_id    
    
    for arg in args:
        try:
            followed_crns.remove(str(arg))
            bot.send_message(chat_id = chat_id, text = str(arg) + " artık takip edilmiyor.")
        except ValueError:
            bot.send_message(chat_id = chat_id, text = str(arg) + " takip edilenler arasında değil.")
      
    chat_data["follow"] = followed_crns
    
def follow_reset(bot, update, chat_data):
    
    """
    Resets the followed list.
    """
    
    if "follow" not in chat_data:
        followed_crns = list()
        chat_data["follow"] = followed_crns
        
    followed_crns = chat_data["follow"]
    
    chat_id = update.message.chat_id
    
    followed_crns = list()
    bot.send_message(chat_id = chat_id, text = "Takip edilenler sıfırlandı.")
    chat_data["follow"] = followed_crns
    
def show_followed(bot, update, chat_data):
    
    """
    Shows the contents of the followed list.
    """
    
    if "follow" not in chat_data:
        followed_crns = list()
        chat_data["follow"] = followed_crns
        
    followed_crns = chat_data["follow"]
    chat_id = update.message.chat_id
    
    if len(followed_crns) == 0:
        bot.send_message(chat_id = chat_id, text = "Gösterilecek bir şey yok.")
        
    for crn in followed_crns:
        bot.send_message(chat_id = chat_id, text = crn + "\t")
    
    chat_data["follow"] = followed_crns
        
def show_help(bot, update):
    
    """
    Shows commands.
    """
    
    chat_id = update.message.chat_id
    text = """
/crntakip: Yeni CRNleri takip et.\n
/crnbirak: CRNyi takipten çıkar.\n
/sifirla: Bütün CRNleri takipten çıkar.\n
/izlembaslat: Uyarı sistemini başlat.\n
/izlemdurdur: Uyarı sistemini durdur.\n
/goster: Takip edilen bütün CRNleri göster.\n
/yardim: Bu metni gör.\n
    \n    
Örnek Kullanım: /crntakip 7811 8931 yazarak bu iki CRN'yi takibe alabilirsiniz.\n
Yer boşaldığında uyarı gelmesi için /izlembaslat komutuyla izlemi başlatmanız gerekir.
    """
    bot.send_message(chat_id, text)
    
def check_crn(bot, job):
    
    """
    For every CRN in followed_crns list, check if there is any available space.
    """
    
    available = list()
    
    counter = 0    
    while is_data_old():
        time.sleep(10)
        counter += 1
        if (counter > 12):
            bot.send_message(chat_id = job.context[0], text = "Sistemde bir sıkıntı var.")
            return
        
    with open("available_courses.txt") as txt_file:
        available = txt_file.read().lstrip("['").rstrip("']").split("', '")
    
    try:
        for crn in job.context[1]["follow"]:
            if (crn in available):
                bot.send_message(chat_id = job.context[0], text = crn + " kodlu derste boş yer var!")
    except:
        print("wut")
    
def start(bot, update):
    
    """
    First message the user sees.
    """
    chat_id = update.message.chat_id
    text = "İTÜ Kontenjanlarını takip etmene yardımcı olmak için buradayım."
    bot.send_message(chat_id, text)
    show_help(bot, update)

    
def watch(bot, update, job_queue, chat_data):

    """
    Start watching and notify if there is any available seats in the system.
    """    
    
    chat_id = update.message.chat_id
    
    if "job1" in chat_data:
        bot.send_message(chat_id = chat_id, text = "İzlem zaten başlatılmış.")
    else:
        t1 = datetime.now()  
        
        t2 = datetime(t1.year, t1.month, t1.day, t1.hour, 15, 20)
        t3 = datetime(t1.year, t1.month, t1.day, t1.hour, 30, 20)
        t4 = datetime(t1.year, t1.month, t1.day, t1.hour, 45, 20)
        t5 = datetime(t1.year, t1.month, t1.day, t1.hour + 1, 00, 20)
        
        update_times = [t2, t3, t4, t5]
        find_min = list()
        
        for t in update_times:
            difference = t - t1
            if difference.days >= 0:
                find_min.append(difference)
        
        first_run = min(find_min)
        #t6 = datetime(t1.year, t1.month, t1.day, t1.hour, t1.minute + 1, t1.second)
        #one_minute = t6 - t1
        
        job1 = job_queue.run_repeating(check_crn, 900, (t1 + first_run), context = [chat_id, chat_data]) # First check
        # job2 = job_queue.run_repeating(check_crn, 900, (t1 + first_run + one_minute), context = [chat_id, chat_data]) # Check again after 1 minute
        
        chat_data["job1"] = job1
        # chat_data["job2"] = job2    
        
        bot.send_message(chat_id = chat_id, text = "İzleme başlandı.")
    
def unwatch(bot, update, job_queue, chat_data):

    """
    Kill watching processes.
    """    
    
    chat_id = update.message.chat_id
    
    if "job1" not in chat_data:
        bot.send_message(chat_id = chat_id, text = "İzlem zaten aktif değil.")
    else:
        job1 = chat_data["job1"]
        #job2 = chat_data["job2"]
        job1.schedule_removal()
        #job2.schedule_removal()
        del chat_data["job1"]
        #del chat_data["job2"]
        bot.send_message(chat_id = chat_id, text = "İzlem bırakıldı.")
    
def main():
    updater = Updater(token=TOKEN)
    
    dispatcher = updater.dispatcher
    
    job_q = updater.job_queue
    
    handler_list = [CommandHandler("start", start),
                    CommandHandler("crntakip", follow, pass_args=True, pass_chat_data=True),
                    CommandHandler("crnbirak", unfollow, pass_args=True, pass_chat_data=True),
                    CommandHandler("sifirla", follow_reset, pass_chat_data=True),
                    CommandHandler("goster", show_followed, pass_chat_data=True),
                    CommandHandler("izlembaslat", watch, pass_job_queue=True, pass_chat_data=True),
                    CommandHandler("izlemdurdur", unwatch, pass_job_queue=True, pass_chat_data=True),
                    CommandHandler("yardim", show_help)]
                    
    for handler in handler_list:
        dispatcher.add_handler(handler)
        
    updater.start_polling()
    updater.idle()
    
main()
