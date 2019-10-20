## Приложение API

Перед началом работы с API. Необходимо получить токен. Для этого нужно перейти по урлу ниже и авторизоваться или отправить запрос: 

#### Получение токена
```
POST /api/v1/token/login
{
    "email": "text@mail.com",
    "password": "pass"
}

200 OK
{
    "auth_token": "be9828c21f006606bf683524d67c6ed94669"
}
```

Затем прикладывать этот токен к запросу в заголовке: 
"Authorization: Token be9828c21f006606bf683524d67c6ed94669"

---
### Реализованный функционал
Для редактирования магазина, необходимо являться администратором магазина.
Для создания магазина и получения статуса администратора обратитесь к администратора ресурса.

#### Сигнал на обновление прайса
```
POST /api/v1/partner/update
{
    "url": "https://partner-site.ru/files/price.yaml",
}

200 OK
{
    'Status': True
}
```


#### Получить статус получения заказов
```
GET /api/v1/partner/state
{}

200 OK
{
    "state": "on",
}
```


#### Включить/выключить заказы по id магазина
```
POST /api/v1/partner/state/1
{
    "state": "off",
}

200 OK
{
    "shop_id": 1,
    "state": "on"
}
```


#### Включить/выключить заказы всех магазинов пользователя
```
POST /api/v1/partner/state/
{
    "state": "on",
}

200 OK
{
{
    "Shops": [
        {
            "name": "Связной",
            "state": "on"
        },
        {
            "name": "Евросеть",
            "state": "on"
        }
    ]
}
```

#### Получить список заказов
```
GET /api/v1/partner/order

200 OK
{
    "orders": [
        {
            "id": 1,
            "create_date": "2019-10-20T16:07:59.517307Z"
        },
        {
            "id": 2,
            "create_date": "2018-11-20T16:07:59.517307Z"
        },
    ]
}
```


#### Получить состав заказа
```
GET /api/v1/partner/order/1/

200 OK
{
    "order": {
        "id": 1,
        "create_date": "2019-10-20T16:07:59.517307Z",
        "comment": "text",
        "status": "Новый",
        "cart": {
            "items": [
                {
                    "productinfo": {
                        "product": {
                            "name": "Смартфон Apple iPhone XR 256GB (черный)"
                        },
                        "price": 65000
                    },
                    "quantity": 1,
                    "item_total": "65000.00"
                }
            ],
            "cart_total": "65000.00"
        },
        "address": "Самовывоз"
    }
}
```

