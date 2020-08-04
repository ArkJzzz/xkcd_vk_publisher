## xkcd_vk_publisher

Публикация комиксов [xkcd](https://xkcd.com/) на стену группы [ВКонтакте](https://vk.com/)


### Подготовка


Создайте [группу Вконтакте](https://vk.com/groups?tab=admin), в которую будете выкладывать комиксы.

Создайте приложение Вконтакте на [странице для разработчиков](https://vk.com/apps?act=manage). В качестве типа приложения следует указать `standalone` — это подходящий тип для приложений, которые просто запускаются на компьютере.

Получите `client_id` созданного приложения. Если нажать на кнопку "Редактировать" для нового приложения, в адресной строке вы увидите его `client_id`.

Получите ключ доступа пользователя. Ключ можно получить вручную с помощью [Implicit Flow](https://vk.com/dev/implicit_flow_user).

Пример запроса:
```
https://oauth.vk.com/authorize?client_id=<VK_APP_CLIENT_ID>&display=page&scope=photos,wall,offline,groups&response_type=token&v=5.120&state=autorization_complete
```

Ключ доступа к API `access_token` будет передан в URL-фрагменте ссылки:
```
https://oauth.vk.com/blank.html#access_token=<YOUR_ACCESS_TOKEN>&expires_in=0&user_id=<USER_ID>&state=autorization_complete
```


### Установка

- Клонируйте репозиторий:
```bash
git clone https://github.com/ArkJzzz/xkcd_vk_publisher.git
```

- Создайте файл `.env` и поместите в него токены ВКонтакте:
```
VK_CLUB_ID=<id_группы_ВКонтакте>
VK_USER_ID=<id_администратора_группы>
VK_APP_ACCESS_TOKEN=<ключ_доступа_приложения_ВКонтакте>
```

- Установить зависимости:
```bash
pip3 install -r requirements.txt
```

### Запуск

```bash
python3 main.py

```

**Примерный вывод в терминал:**

```
(xkcd-env) arkjzzz@arkjzzz:~/xkcd$ python main.py 
download_picture:19 - https://imgs.xkcd.com/comics/six_months.png
download_picture:29 - comics_image.png
main.py:48 - comics_image.png
main.py:115 - Адрес сервера получен
main.py:118 - Изображение загружено на сервер
main.py:123 - Изображение сохранено на сервере
main.py:127 - Опубликована запись 11, "Six Months" 
But then she does that thing with her tongue and I remember why I left you.
(xkcd-env) arkjzzz@arkjzzz:~/xkcd$
```

**Результат работы скрипта:**

![](xkcd.gif)
