# kontenjanci-public
Public version of Telegram bot "İTÜ Kontenjan İzlemcisi". (This repo doesn't include the bot token)
https://telegram.me/ITUKontenjanBot

## How does it work?

Istanbul Technical University updates its course information page every 15 minutes. Scraper, which is available
in scraper.py, scrapes the webpage and adds a CRN(Unique course number) to a list if (course capacity > enrollment).

Then, in application.py, we have the application which uses the Scraper every 15 minutes and saves the list in a file
called available_courses.txt. To do that, I am using a library called schedule.

Finally, we have bot.py which is a Telegram bot. User is able to add course numbers s/he wants and then start the "watch" which
notifies the user when the course number s/he follows is added to available_courses.txt. To do that, I have used python-telegram-bot library.

## Future Development Plans

1. Sometimes it takes a long time for scraper to scrape every course so bot checks the file again after a minute to make sure user didn't miss an
important update. But I am going to use "os.path.getmtime(path)" and wait if the file's (last modified date is > 1 minute). This way, I do not
have to check the file twice and am sure it is up to date. <b>Done</b>

2. Browser headers can be added to scraper so it looks more legit. <b>Done</b>

3. Scraper checks the available course codes everytime, I might just use another file to hold course codes and update it
manually(by running the scraper function which updates the course codes) if necessary. <b>Done</b>
