import telebot
import telegaConstants
import vk
import json

global vkPassw
global vkLogin
vkPassw = ''
vkLogin = ''
global usName
global message
global referId

vkTeleBot = telebot.TeleBot(telegaConstants.teleToken)

print('vkTelegaBot запущен')
##########################################################################
@vkTeleBot.message_handler(commands=['vk'])
def vk_login(msg):
    if(authent(msg) == False):
        login = vkTeleBot.send_message(msg.chat.id, 'Введите логин вк' )
        vkTeleBot.register_next_step_handler(login , vk_pass)
    else:
        global vkPassw
        password = vkPassw
        vkPassw = password
      #  print('login : ' + vkLogin)
       # print('pass : ' + vkPassw)
        msgToPost = vkTeleBot.send_message(msg.chat.id, 'Что запостить?')
        vkTeleBot.register_next_step_handler(msgToPost, post_msg)


def authent(msg):
    global usName
    hiMyNameIs = str(msg.from_user.username)
    usName = hiMyNameIs
    global vkLogin
    global vkPassw
    if ((vkLogin != '') and (vkPassw != '') and (vkPassw == telegaConstants.dictUsers.get(hiMyNameIs))):
        return True
    else:
        return False


def vk_pass(msg):
    global vkLogin
    login = msg.text
    vkLogin = login
    passw = vkTeleBot.send_message(msg.chat.id, 'Введите пароль вк' )
    vkTeleBot.register_next_step_handler(passw, vk_auth)


def vk_auth(msg):
    global vkPassw
    password = msg.text
    vkPassw = password
   # print('login : ' + vkLogin)
   # print('pass : ' + vkPassw)
    msgToPost = vkTeleBot.send_message(msg.chat.id, 'Что запостить?')
    vkTeleBot.register_next_step_handler(msgToPost, post_msg)


def post_msg(msg):
    global usName
    try:
        msgToPost = msg.text
        session = vk.AuthSession(telegaConstants.app_id, vkLogin, vkPassw,
                                     scope='wall, messages')
        vk_api = vk.API(session)
        vkTeleBot.send_message(msg.chat.id, 'Соединяемся с ВК...')
        vkTeleBot.send_message(msg.chat.id, 'Авторизация завершена')

        vk_api.wall.post(message = msgToPost)
        vkTeleBot.send_message(msg.chat.id, 'Постим...')
        vkTeleBot.send_message(msg.chat.id, 'Готово! Ты запостил : ' + msgToPost)
        telegaConstants.dictUsers.update({usName:vkPassw})
        telegaConstants.dictLogins.update({vkLogin:vkPassw})

    except(vk.exceptions.VkAuthError, vk.exceptions.VkAPIError):
        vkTeleBot.send_message(msg.chat.id, 'Неверный логин-пароль... или произошла другая ошибка')
      #  print('логин : ' + vkLogin)
      #  print('пароль : ' + vkPassw)


@vkTeleBot.message_handler(commands=['offline'])
def setHideMe(msg):
    if authent(msg):
        session = vk.AuthSession(telegaConstants.app_id, vkLogin, vkPassw,
                                 scope='wall, messages')
        vk_api = vk.API(session)
        vk_api.account.setOffline()
        vkTeleBot.send_message(msg.chat.id, 'Алсо теперь ты оффлайн...')
    else:
        vkTeleBot.send_message(msg.chat.id, 'Вы не авторизованы...')

@vkTeleBot.message_handler(commands=['message'])
def sendMsg(msg):
    if authent(msg):
       sent = vkTeleBot.send_message(msg.chat.id, 'Напишите сообщение которое хотите отправить')
       vkTeleBot.register_next_step_handler(sent, nextStep)
    else:
        vkTeleBot.send_message(msg.chat.id, 'Вы не авторизованы...')
def nextStep(msg):
       global messag
       messag = msg.text
       sent = vkTeleBot.send_message(msg.chat.id, 'Напишите короткую ссылку того кому хотите отправить (.../username) ')
       vkTeleBot.register_next_step_handler(sent, nextStep2)
def nextStep2(msg):
    try:
        global referId
        referId = msg.text
        session = vk.AuthSession(telegaConstants.app_id, vkLogin, vkPassw,
                                     scope='wall, messages')
        vk_api = vk.API(session, v='5.62')
        usId = vk_api.users.get(user_ids = referId)
        #print(usId)
        usId = str(usId).replace(']','')
        usId = str(usId).replace('[','')
        usId = str(usId).replace("'",'"')
        print(usId)
        parsedUsId = json.loads(usId)
        #print(parsedUsId)
        print('id : ' + str(parsedUsId['id']))
        usId = str(parsedUsId['id'])
        vk_api.messages.send(user_id = usId, message = str(messag))
        vkTeleBot.send_message(msg.chat.id, 'Готово...')
    except(TypeError,vk.exceptions.VkAuthError, vk.exceptions.VkAPIError):
        print('TypeError')
        vkTeleBot.send_message(msg.chat.id, 'Что то пошло не так...')


vkTeleBot.polling(none_stop=True)