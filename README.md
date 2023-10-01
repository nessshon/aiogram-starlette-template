<h1 align="center">🤖 Aiogram-Starlette Template</h1>

## Features

- [Aiogram 3x](https://github.com/aiogram/aiogram/) as Telegram Bot API
- [FastAPI](https://github.com/tiangolo/fastapi/) for separate API Routes
- [Starlette-Admin](https://github.com/jowilf/starlette-admin/) as web Admin Panel
- [Telegram Login Widget](https://core.telegram.org/widgets/login/) for admin authorization

## Screenshots

<img src="https://telegra.ph//file/550fe083f6eaa36c3f64b.jpg" width="50%"><img src="https://telegra.ph//file/20cf7d8a48597177e4f9b.jpg" width="50%">
<img src="https://telegra.ph//file/95075ad356b3b139b928a.jpg" width="50%"><img src="https://telegra.ph//file/77b0e2ca4c075c68fc30b.jpg" width="50%">

## Installation

1. Clone this [template](https://github.com/nessshon/aiogram-starlette-template):

    ```bash
    git clone https://github.com/nessshon/aiogram-starlette-template
    ```

2. Go to the project folder:

    ```bash
    cd aiogram-starlette-template
    ```

3. Create environment variables file:

    ```bash
    cp .env.example .env
    ```

4. Configure [environment variables](#environment-variables-reference) file:

    ```bash
    nano .env
    ```

5. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

6. Run app:

    ```bash
    python -m app
    ```

### Environment variables reference

| Variable            | Type | Description                                                 | Example             |
|---------------------|------|-------------------------------------------------------------|---------------------|
| BOT_TOKEN           | str  | Bot token, get it from [@BotFather](https://t.me/BotFather) | 123456:qweRTY       | 
| BOT_USERNAME        | str  | The username of the bot                                     | same_bot            |
| BOT_DEV_ID          | int  | User ID of the bot developer                                | 123456789           |
| BOT_ADMIN_ID        | int  | User ID of the bot administrator                            | 123456789           |
| APP_HOST            | str  | The host address where the app is running                   | localhost           |
| APP_PORT            | int  | The port number on which the app is listening               | 8000                |
| APP_DEBUG           | bool | Set this variable to enable or disable debugging            | False               |
| ADMIN_BASE_URL      | str  | The base URL for the admin panel routes                     | /admin              |
| ADMIN_TEMPLATES_DIR | str  | The directory path for the admin panel templates            | {}/admin/templates  |
| ADMIN_STATICS_DIR   | str  | The directory path for the admin panel static files         | {}/admin/statics    |
| ADMIN_LANGUAGES     | list | The supported languages for the admin panel                 | en,ru               |
| ADMIN_TITLE         | str  | The title of the admin panel                                | Admin Panel         |
| WEBHOOK_SECRET      | str  | Secret key for securing the webhook                         | qwerty12345         |
| WEBHOOK_DOMAIN      | str  | The domain of the webhook                                   | https://example.com |
| WEBHOOK_PATH        | str  | The path of the webhook                                     | /bot                |
| REDIS_HOST          | str  | The hostname or IP address of the Redis server              | localhost           |
| REDIS_PORT          | int  | The port number on which the Redis server is running        | 6379                |
| REDIS_DB            | int  | The Redis database number                                   | 1                   |
| DB_HOST             | str  | The hostname or IP address of the database server           | localhost           |
| DB_PORT             | int  | The port number on which the database server is running     | 3306                |
| DB_USERNAME         | str  | The username for accessing the database                     | user                |
| DB_PASSWORD         | str  | The password for accessing the database                     | password            |
| DB_DATABASE         | str  | The name of the database                                    | dbname              |
