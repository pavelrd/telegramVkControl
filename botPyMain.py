import telebot
import constants
import datetime
import random
import requests
import json
import time

myBot = telebot.TeleBot(constants.token)
print('bot-сервер запущен')

@myBot.message_handler(commands=['start'])
def start(message):
            sent = myBot.send_message(message.chat.id, 'Привет, {name}! '.format(name = str(message.from_user.username)))
            myBot.send_message(message.chat.id, 'Кстати мне можно писать что угодно, я смогу ответить, но учтите, что все еще я бот в процессе разработки!')
            myBot.send_message(message.chat.id,
                               'Теперь я научился показывать погоду! Спросите меня что-нибудь о ней! Например: "На улице холодно?"')
            constants.name.append(str(message.from_user.username))
            print(constants.name[len(constants.name)-1] + ' использует бот')

@myBot.message_handler(commands = ['stop'])
def stop(message):
        myBot.send_message(message.chat.id, 'До свидания, {name}!'.format(name = constants.name[len(constants.name)-1]))
        print('{name} закончил использование бота!'.format(name = constants.name[len(constants.name)-1]))

@myBot.message_handler(commands = ['description'])
def description(msg):
    myBot.send_message(msg.chat.id, 'Отправьте мне /start или /stop чтобы начать диалог или просто поговорите со мной :) Или ты че команды не умеешь смотреть')
    myBot.send_message(msg.chat.id, 'Кстати мне можно писать что угодно, я смогу ответить, но учтите, что все еще я бот в процессе разработки!')
    myBot.send_message(msg.chat.id, 'Теперь я научился показывать погоду! Спросите меня что-нибудь о ней! Например: "На улице холодно?"')

@myBot.message_handler(commands = ['schedule'])
def sendSchedule(msg):
    myBot.send_photo(msg.chat.id, photo=constants.url)

@myBot.message_handler(commands = ['week'])
def dispWeek(msg):

    week = datetime.datetime.utcnow().isocalendar()[1]
    studyWeek = week - datetime.datetime(2017, 9 , 1).isocalendar()[1] + 1

    myBot.send_message(msg.chat.id,'сейчас ' + str(week) + ' неделя года и ' + str(studyWeek) + ' учебная неделя')
    if isWeekEven(studyWeek) == True:
        print('Знаменатель')
        myBot.send_message(msg.chat.id,'Знаменатель')
    elif isWeekEven(studyWeek) == False:
        print('Числитель')
        myBot.send_message(msg.chat.id,'Числитель')
    if(17 - studyWeek) > 0:
        myBot.send_message(msg.chat.id,'до сессии осталось {weeksLeft} недель(-и)!'.format(weeksLeft = (17-studyWeek)))
    else:
        myBot.send_message(msg.chat.id,'че пацаны сессия')

    print('week : '+ str(week))
    print('studyweek : '+ str(studyWeek))

@myBot.message_handler(commands = ['userlist'])
def dispUserList(message):
    myBot.send_message(message.chat.id, str(constants.name))
    print(constants.name)

@myBot.message_handler(commands=['weather'])
def showWeather(message):
    try:
        print('Пользователь ' + str(message.from_user.username) + ' запросил погоду')
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Moscow,ru&units=metric&APPID=2f63cb4d02e27e9b67128d8982fd7d43')
        json_str = response.content
        dataList = parseJson(json_str)
        constants.dataList = dataList
        myBot.send_message(message.chat.id,'Сейчас в городе Москва {temp}°, {description}'.format(temp=dataList[2], description=constants.dictWeather.get(dataList[0],'')))
    except TypeError:
        print('TypeError occured')
        myBot.send_message(message.chat.id, 'Что-то пошло не так! Попробуй запросить погоду позже...')


@myBot.message_handler(content_types = ['text'])
def listenAndReply(message):
    try:
       # if(str(message.text).__contains__('@')== False):
           # if(str(message.text).__contains__(vkPassw) == False):
               # print(str(message.text))
                if(str(message.text).__contains__('лучший технический вуз')):
                    myBot.send_message(message.chat.id, 'МГТУ ИМЕНИ НИКОЛАЯ ЭРНЕСТОВИЧА БАУМАНА')
                elif(str(message.text).__contains__('Привет') or str(message.text).__contains__('привет') or (str(message.text).__contains__('Йоу'))):
                    myBot.send_message(message.chat.id, constants.sayHi[random.randint(0, 1)])
                elif(str(message.text).__contains__('time')):
                    myBot.send_message(message.chat.id, 'ITS TIME TO STOOOOP')
                elif(str(message.text).__contains__('асписани')): #РасписаниЕ
                    sendSchedule(message)
                elif (str(message.text).__contains__('огод')):  #ПогодА
                    showWeather(message)
                    if constants.dataList[2] > 24:
                        myBot.send_message(message.chat.id, 'Жарко')
                    elif constants.dataList[2] > 20 and constants.dataList[2] < 24:
                        myBot.send_message(message.chat.id, 'Тепло')
                    elif constants.dataList[2] < 20 and constants.dataList[2] > 10:
                        myBot.send_message(message.chat.id, 'Прохладно')
                    elif constants.dataList[2] < 0:
                        myBot.send_message(message.chat.id, 'Мороз')
                    else: myBot.send_message(message.chat.id, 'Холодновато')
                elif (str(message.text).__contains__('можешь')):
                    description(message)
                elif (str(message.text).__contains__('холодно')):
                    showWeather(message)
                    if constants.dataList[2] > 24:
                        myBot.send_message(message.chat.id, 'Жарко')
                    elif constants.dataList[2] > 20 and constants.dataList[2] < 24:
                        myBot.send_message(message.chat.id, 'Тепло')
                    elif constants.dataList[2] < 20 and constants.dataList[2] > 10:
                        myBot.send_message(message.chat.id, 'Прохладно')
                    elif constants.dataList[2] < 0:
                        myBot.send_message(message.chat.id, 'Мороз')
                    else: myBot.send_message(message.chat.id, 'Холодновато')
                elif (str(message.text).__contains__('арко')):
                    showWeather(message)
                    if constants.dataList[2] > 24:
                        myBot.send_message(message.chat.id, 'Жарко')
                    elif constants.dataList[2] > 20 and constants.dataList[2] < 24:
                        myBot.send_message(message.chat.id, 'Тепло')
                    elif constants.dataList[2] < 20 and constants.dataList[2] > 10:
                        myBot.send_message(message.chat.id, 'Прохладно')
                    elif constants.dataList[2] < 0:
                        myBot.send_message(message.chat.id, 'Мороз')
                    else: myBot.send_message(message.chat.id, 'Холодновато')
                elif (str(message.text).__contains__('сколько градус')):
                    showWeather(message)
                elif (str(message.text).__contains__('емператур')):
                    showWeather(message)
                elif (str(message.text).__contains__('Холодно')):
                    showWeather(message)
                    if constants.dataList[2] > 24:
                        myBot.send_message(message.chat.id, 'Жарко')
                    elif constants.dataList[2] > 20 and constants.dataList[2] < 24:
                        myBot.send_message(message.chat.id, 'Тепло')
                    elif constants.dataList[2] < 20 and constants.dataList[2] > 10:
                        myBot.send_message(message.chat.id, 'Прохладно')
                    elif constants.dataList[2] < 0:
                        myBot.send_message(message.chat.id, 'Мороз')
                    else: myBot.send_message(message.chat.id, 'Холодновато')
                elif (str(message.text).__contains__('пары')):
                    sendSchedule(message)
                elif (str(message.text).__contains__('учимся')):
                    sendSchedule(message)
                elif(str(message.text).__contains__('зонт')) or (str(message.text).__contains__('Зонт')):
                    if str(constants.dataList[0]).__contains__('rain') or str(constants.dataList[0]).__contains__('drizzle') or str(constants.dataList[0]).__contains__('shower'):
                            print('Дождливо')
                            myBot.send_message(message.chat.id,'на улице пригодится зонтик \U00002614')
                    else: myBot.send_message(message.chat.id,'пока на улице зонтик не пригодится \U00002614')
               # else:
                  #  myBot.send_message(message.chat.id, constants.sayHi[random.randint(2, len(constants.sayHi) - 1)])
    except(TypeError):
        myBot.send_message(message.chat.id, 'ошибка')
        print('TypeError')

def isWeekEven(week):
    if (week % 2) == 0:
        return True
        print('{EvWeek} is even'.format(EvWeek = week))
    else:
        return False
        print('{EvWeek} is not even'.format(EvWeek=week))

def parseJson(jsonStr):
    try:
        json_str = jsonStr
        print(jsonStr)
        parsed_str = json.loads(json_str.decode('utf-8'))
        print(parsed_str['weather'])

        substr = str(parsed_str['weather']).replace('[','')
        substr = substr.replace(']','')
        substr = substr.replace("'",'"')
        print(substr)
        parsed_substr = json.loads(substr)
        print('id : ' + str(parsed_substr['id']))
        identif = int(parsed_substr['id'])
        print(identif)
        print('description : ' + str(parsed_substr['description']))
        description = str(parsed_substr['description'])
        print(description)

        substr = str(parsed_str['main']).replace('[','')
        substr = substr.replace(']','')
        substr = substr.replace("'",'"')
        parsed_substr = json.loads(substr)
        print('temp : ' + str(parsed_substr['temp']))
        temp = float( parsed_substr['temp'])
        print(temp)
        return [identif, description ,temp]
    except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, TypeError, json.JSONDecodeError,TypeError):
        print('Error occurred')
while True:
    try:
        myBot.polling(none_stop=False)
    except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, json.JSONDecodeError, TypeError, requests.exceptions.ReadTimeout):
        print('Error occurred')
    time.sleep(1)
