# kontenjanci-public

[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/no-ragrets.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)

Public version of Telegram bot "İTÜ Kontenjan İzlemcisi". (This repo doesn't include the bot token)
https://telegram.me/ITUKontenjanBot

## How does it work?

Istanbul Technical University updates its course information page every 15 minutes. Scraper, which is available
in scraper.py, scrapes the webpage and adds a CRN(Unique course number) to a list if (course capacity > enrollment).

Then, in application.py, we have the application which uses the Scraper every 15 minutes and saves the list in a file
called available_courses.txt. To do that, I am using a library called schedule.

Finally, we have bot.py which is a Telegram bot. User is able to add course numbers s/he wants and then start the "watch" which
notifies the user when the course number s/he follows is added to available_courses.txt. To do that, I have used python-telegram-bot library.

