# hw9-personal-assistant-with-sqlalchemy-and-alembic

                                ***UA***

Це персональний помічник з інтерфейсом командного рядкаб версія 0.1.0.

Нижче наведені основні можливості "Асистента":

1. Зберігає контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
2. Виводить список контактів, у яких день народження через задану кількість днів від поточної дати;
3. Перевіряє правильність введеного номера телефону та email під час створення або редагування запису та повідомляє користувача у разі некоректного введення;
4. Здійснює пошук контактів з книги контактів;
5. Редагує та видаляє записи з книги контактів;
6. Зберігає нотатки з текстовою інформацією;
7. Проводить пошук за нотатками;
8. Редагує та видаляє нотатки;
9. Додає в нотатки "теги", ключові слова, що описують тему та предмет запису;
10. Здійснює пошук та сортування нотаток за ключовими словами (тегами);
11. Сортує файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).

Підтримуються наступні формати файлів для сортування:
зображення:'.jpeg', '.png', '.jpg', '.svg'
відео:'.avi', '.mp4', '.mov', '.mkv'
текстові:'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'
аудіо:'.mp3', '.ogg', '.wav', '.amr'
архівні:'.zip', '.gz', '.tar'

"Асистент" можна установити як пакет Python через команду pip install -e  з локації файлу setup.py.
Для запуску програми достатньо просто викликати команду "assistant" в командному рядку в будь-якому місці системи.

CLI Асистент має наступні функції: вітається з юзером, додавання запису до адресної книги, видалення запису, редагування запису, виведення контактів з адресної книги, виведення контактів з днями народження в задану кількість днів, додавання нотатки до записника, видалення нотатки, редагування нотатки, пошук нотатки, виведення нотатки, зміна тегу нотатки, виведення нотатки за тегом, пошук нотатки затегом, сортування файлів в папці за категоріями.
Також, в будь-який момент доступна команда "help" яка виводить список всіх доступних команд програми з коротким їх описом.

Программа створює файл 'assistant.db' в папці користувача, в якому зберігає всі контакти і нотатки 

Дякуємо за Ваш вибір нашого продукту. Бажаємо приємного користування!
_______________________________________________________________________________

                                ***ENG***

This is a personal assistant with the command line interface version 0.1.0. 

Here are some of the main features of the "Assistant":

1. Save contacts with name, address, date of birth, emails and phone numbers to the Addressbook;
2. Display the list of contacts which have birthday within a certain timeframe;
3. Check the entered email and phone number for validity during creation or editing the record and notifying the user in case of a problem;
4. Search contacts in the Addressbook;
5. Edit and remove records from Addressbook;
6. Save notes in text format;
7. Search the notes;
8. Edit and remove notes;
9. Add tags to the notes;
10. Search and sort the notes by tags;
11. Sort the files by categories(images, docs, videos, etc.) in a specified folder.

The following file formats are recognized:
images:'.jpeg', '.png', '.jpg', '.svg'
video:'.avi', '.mp4', '.mov', '.mkv'
documents:'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'
audio:'.mp3', '.ogg', '.wav', '.amr'
archive:'.zip', '.gz', '.tar'

The "Assistant" can be installed into your python as a package using the commant pip install -e from the setup.py file location.
To start the program, simply type command "assistant" in the console in any place of the system.

CLI Assistan has the following options: welcoming the user, add record to the addressbook, delete record, edit record, search for the Record, show the Records in Addressbook, show contacts with birthdays within a certain timeframe, add note to the notebook, delete note, edit note's text, find note, show note, change tag, show note by tag, find note by tag, sort files in a folder by categories.
Also, at any time you can use command "help" to see the list of all supported commands with their description.

The program creates a file 'assistant.db' in the user's folder, in which it stores all contacts and notes

Thanks for downloading and enjoy using the "Assistant" by PRDD.