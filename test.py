# @dp.message_handler(commands=['start'])
# async def welcome(message: types.Message):
#     try:
#         p2p.reject(bill_id=new_bill.bill_id)
#     except:
#         pass
#     await message.answer('Вы хотите приобрести арбуз?\nДля приобретения пропишите /buywatermelon')


# @dp.message_handler(commands=['buywatermelon'])
# async def buy(message: types.Message):
#     global bill
#     price = 1 #Цена которая будет запрашиваться у пользователя
#     lifetime = 7 #Время действия ссылки
#     comment = 'Оплата заказа' #Комментарий к платежу, может быть абсолютно любым
#     bill = p2p.bill(amount=price, lifetime=lifetime, comment=comment) #Создаем счет
#     link_oplata = bill.pay_url #Получаем ссылку на оплату из нашего счета
#     await message.answer(f'Приветствуем!\nАрбуз стоит: {price} рублей\nСчет действителен 7 минут\nДля оплаты нажмите на данное слово: {link_oplata}')
#     x = threading.Thread(target=functionoplata, args=(message,)) #Target - данный параметр принимает переменную, а в нашем варианте функцию которая будет проверять оплату. Args - аргументы, допустим для отправки сообщения.
#     x.start() #Запуск потока

# async def functionoplata(message: types.Message): #Функция, ее можно создавать даже не асинхронной - ведь эта функция выполняется в потоке для пользователя.
#     oplata_time = datetime.datetime.now() #Получаем текущее время
#     datetime_delta = oplata_time + timedelta(minutes=7) #Получаем разницу между датами.
#     while True: #Создание цикла
#         status = p2p.check(bill_id=bill.bill_id).status #Проверка статуса оплаты
#         if status == 'PAID': #Проверка, на то - дошла ли оплата до бота. Вслучае положительного ответа, он выполняет данный if.
#             await message.answer('Оплата дошла до нас! Ауе')
#             break #Завершение цикла
#         elif datetime.datetime.now() > datetime_delta: #Делаем проверку, на время оплаты. То есть в случае неоплаты в течении 7-ми минут, цикл прекращается.
#             await message.answer('мужик, ты че не оплатил')
#             break #Завершение цикла
#     time.sleep(0.1) #Спим некое время, чтобы бот не крашнулся.
