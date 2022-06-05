# API protocols

To install and run app use:

```bash
poetry install
poetry run uvicorn app.main:app
```

URLS:

- `localhost:8000/` - html page for websockets demonstration
- `localhost:8000/docs` - swagger for REST demonstration
- `localhost:8000/jrpc/docs` - swagger for JSON RPC demonstration
- `localhost:8000/graphql` - for graphql demonstration

## Rest

`REST` (Representational state transfer) – это стиль архитектуры программного обеспечения для распределенных систем, таких как World Wide Web, который, как правило, используется для построения веб-служб. Термин REST был введен в 2000 году Роем Филдингом, одним из авторов HTTP-протокола. Системы, поддерживающие REST, называются RESTful-системами.

Также стоит упомянуть такой инструмент как `Swagger` а точнее `OpenAPI`. `The OpenAPI Specification` (с англ. — «спецификация OpenAPI»; изначально известная как Swagger Specification) — формализованная спецификация и экосистема множества инструментов, предоставляющая интерфейс между front-end системами, кодом библиотек низкого уровня и коммерческими решениями в виде API. Вместе с тем, cпецификация построена таким образом, что не зависит от языков программирования, и удобна в использовании как человеком, так и машиной.

`Swagger` позволяет нам иметь интерактивную документацию наших API методов, и поддерживать контракт между клиентом и сервером в релевантном состоянии.

Выглядит примерно так:

```json
{
        "openapi": "3.0.2",
        "info": {
            "title": "FastAPI",
            "version": "0.1.0"
        },
        "paths": {
            "/hello": {
                "get": {
                    "summary": "Hello",
                    "operationId": "hello_hello_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response Hello Hello Get",
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
```

### Links

- [wikipedia Rest](https://ru.wikipedia.org/wiki/REST)
- [Синхронизируем понимание REST](https://dou.ua/lenta/articles/rest-conception/)
- [Які є конвенції в REST API та для чого їх дотримуватись](https://dou.ua/forums/topic/34550/)

---

## JSON RPC

JSON-RPC — это облегченный протокол удаленного вызова процедур (`RPC` remote procedure call) без сохранения состояния. В первую очередь эта спецификация определяет несколько структур данных и правила их обработки. Он не зависит от транспорта в том смысле, что концепции могут использоваться в одном и том же процессе, через сокеты, через http или во многих различных средах передачи сообщений.

Протокол позволяет клиенту вызывать непосредсвенно методы на сервере, и получать ответ, или ошибку, коды ошибок мы определяем сами и никак не ограничены статус кодами как в REST, здесь это две разные сущности.

Протокол позволяет делать Batch операции, т.е. мы можем передать серверу несколько вызовов за один запрос.

**Single call:**

```json
// Request -->
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "get_user",
  "params": {
    "id": 123
  }
}

// <-- Response
{
  "jsonrpc": "2.0",
  "error": {
    "code": 6000,
    "message": "User doesn't exist",
    "data": {
      "user_id": 123
    }
  },
  "id": 0
}
```

**Call with error:**

```json
// Request -->
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "get_user",
  "params": {
    "id": 123
  }
}

// <-- Response
{
  "jsonrpc": "2.0",
  "error": {
    "code": 6000,
    "message": "User doesn't exist",
    "data": {
      "user_id": 123
    }
  },
  "id": 0
}
```

**Batch call:**

```json
// Request -->
[
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "echo",
    "params": {
      "data": "hello"
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "echo",
    "params": {
      "data": "hello again"
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "echo",
    "params": {
      "data": "HELLO AGAIN!!!!!!"
    }
  },
  {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "nosuchmethod",
    "params": {
      "data": "dummy"
    }
  }
]

// <-- Response
[
  {
    "jsonrpc": "2.0",
    "result": "hello",
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "result": "hello again",
    "id": 2
  },
  {
    "jsonrpc": "2.0",
    "result": "HELLO AGAIN!!!!!!",
    "id": 3
  },
  {
    "jsonrpc": "2.0",
    "error": {
      "code": -32601,
      "message": "Method not found"
    },
    "id": 4
  }
]    
```

### Links

- [jsonrpc spec](https://www.jsonrpc.org/specification)
- [REST? Возьмите тупой JSON-RPC](https://habr.com/ru/post/441854/)
- [JSON-RPC? Возьмите хитрый REST](https://habr.com/ru/post/476576/)

---

## Websockets

`WebSocket` — протокол связи поверх TCP-соединения, предназначенный для обмена сообщениями между браузером и веб-сервером в режиме реального времени.
Порой нам не нужно вернуть какую-то информацию клиенту сразу, а только тогда когда она появится например, и тогда мы можем опрашивать сервер с некоторой периодичностью пока сервер не вернет нам запрошеный ресурс, но это создает дополнительную нагрузку на сервер. Вебсокеты решают эту проблемму, они обеспечивают двунаправленную свзяь между клиентом и сервисом.

### Links

- [Асинхронный веб, или Что такое веб-сокеты](https://tproger.ru/translations/what-are-web-sockets/)
- [mozilla WebSockets](https://developer.mozilla.org/ru/docs/Web/API/WebSockets_API)

---

## GraphQl

GraphQL — это язык запросов данных и манипулирования ими с открытым исходным кодом для API, а также среда выполнения для выполнения запросов с существующими данными. GraphQL был разработан Facebook внутри компании в 2012 году, а затем публично выпущен в 2015 году. 7 ноября 2018 года проект GraphQL был перенесен из Facebook во вновь созданный GraphQL Foundation, организованный некоммерческой организацией Linux Foundation.
Он обеспечивает подход к разработке веб-API и сравнивается с REST и другими архитектурами веб-сервисов. Это позволяет клиентам определять структуру требуемых данных, и такая же структура данных возвращается с сервера, что предотвращает возврат чрезмерно больших объемов данных. Но это влияет на то, насколько эффективным может быть веб-кеширование результатов запроса. Гибкость и богатство языка запросов также усложняют работу, что может быть нецелесообразно для простых API. Несмотря на название, GraphQL не обеспечивает того разнообразия операций с графами, которое можно было бы найти в полноценной графовой базе данных, такой как Neo4j, или даже в диалектах SQL, поддерживающих транзитивное замыкание.

**Example:**

```graphql
mutation CreateUser1 {
  createUser(firstName: "Lu", lastName: "Ling", age: 32) {
    id
    lastName
  }
}

mutation CreateUser2 {
  createUser(firstName: "Bob", lastName: "Bobston", phone: "9719263") {
    id
    lastName
  }
}

query ListUsers {
  users {
    id
    firstName
    lastName
    age
  }
}

query GetUser {
  user(id: 1) {
    firstName
    lastName
    age
    phone
  }
}

mutation UpdateUserAge {
  updateUser(id: 1, age: 22) {
    id
    age
    phone
  }
}

mutation UpdateUserPhone {
  updateUser(id: 1, phone: "123213") {
    id
    age
    phone
  }
}

mutation DeleteUser {
  deleteUser(id: 1) {
    ok
    message
  }
}
```

- [GraphQl docs](https://graphql.org/)
- [Введение в GraphQL](https://dou.ua/lenta/articles/working-with-qraphql/)
- [Что же такое этот GraphQL?](https://habr.com/ru/post/326986/)

---

## GRPC

`gRPC` (Remote Procedure Calls) — это система удалённого вызова процедур (RPC) с открытым исходным кодом, первоначально разработанная в Google в 2015 году. В качестве транспорта используется HTTP/2, в качестве языка описания интерфейса — Protocol Buffers. gRPC предоставляет такие функции как аутентификация, двунаправленная потоковая передача и управление потоком, блокирующие или неблокирующие привязки, а также отмена и тайм-ауты. Генерирует кроссплатформенные привязки клиента и сервера для многих языков. Чаще всего используется для подключения служб в микросервисном стиле архитектуры и подключения мобильных устройств и браузерных клиентов к серверным службам.

Сложное использование HTTP/2 в gRPC делает невозможным реализацию клиента gRPC в браузере - вместо этого требуется прокси.

**TODO:** add some examples

- [GRPC docs](https://grpc.io/)
- [wikipedia GRPC](https://ru.wikipedia.org/wiki/GRPC)
- [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview)

---
