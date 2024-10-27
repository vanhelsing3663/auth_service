from pathlib import Path

from pydantic import BaseModel, PostgresDsn, TypeAdapter, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    """Настройки Uvicorn для запуска сервиса.

    Arguments:
        host (str): IP, который слушает uvicorn (IP в желаемом интерфейсе / 0.0.0.0).

        port (int): Port, который слушает uvicorn.

        workers (int = None): Число Uvicorn Workers.

        reload (bool = False): Reload Uvicorn для src изменений (debug).
    """

    host: str
    port: int
    workers: int = None
    reload: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR
    public_key_path: Path = BASE_DIR
    algorithm: str = "RS256"  # Для приаватного и пубилчного ключа
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class DatabaseConfig(BaseModel):
    """Конфиг для бд.

    Attributes:
        host (str): адрес доступа к сервису БД.

        port (int): порт на котором осуществляется взаимодействие с суервисом БД.

        name (str): название базы данных в сервисе.

        username (str): имя пользователя от лица которого осуществляется взаимодействие.

        password (str): пароль пользователя.

        scheme (str): `dialect+driver`, по умолчанию: `postgresql+asyncpg`.

        echo_sqlalchemy (bool): вывод информации об sql запросах осуществляемых ORM, по умолчанию: `False`.

        echo_pool (bool): по умолчанию `False`.
        https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.echo_pool.

        pool_size (int): количество соединений, которые нужно держать открытыми в пуле соединений,
        по умолчанию `50`.
        https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_size.

        max_overflow (int): по умолчанию `10`.
        https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.max_overflow.
    """

    host: str
    port: int
    name: str
    username: str
    password: str

    scheme: str = "postgresql+asyncpg"
    echo_sqlalchemy: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        """Получение URL для соединения с БД.

        Включает в себя валидацию введенных данных при помощи класса `PostgresDsn` из `pydantic`.

        Returns:
            PostgresDsn: класс провалидировавший ссылку на БД, дополнительно нужно преобразовать
            к `str` для использования.
        """
        url = MultiHostUrl.build(
            scheme=self.scheme,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )
        db_url = TypeAdapter(PostgresDsn).validate_python(url)
        return db_url


class Settings(BaseSettings):
    """Основной класс настроек, содержащий конфигурации.

    Класс настроек создается при помощи `model_config` являеющегося
    реализацией `SettingsConfigDict`. В нем заданы парметры:
        - `extra` - игнорирует сторонние переменные в файле настроек (`.env`).
        - `env_file` - задает приоритет для файлов настроек. Например
    `env_file=(".env", ".env.prod")` сперва он будет искать файл `.env.prod`,
    после `.env`. Позволяет при помощи файлов задавать среду production.
        - `case_sensitive` - чувствительность к регистру переменных.
        - `env_nested_delimiter` - основной параметр, позволяющий разбивать один
        большой класс настроек на малые подклассы, отвечающие за определенную
        для них часть.

    **Важное замечание**:
    Переменная может быть задана в окружении, НЕ ОБЯЗАТЕЛЬНО задается в `.env`.
    ```sh
    export DB__ECHO_SQLALCHEMY=True
    ```
    Тоже будет работать!


    ### Как задать имя переменной

    В файле `.env` указывается название в специальном формате. Например
    пусть разделитель (значение `env_nested_delimiter`) будет "__" и мы хотим задать
    поле в классе конфигурации для БД (DatabaseConfig). Для этого нужно записать
    переменную по следующему шаболону - `<поле_хранящие_бд_конфиг><разделитель><параметр_настройки>

    Для настройки:
    ```py
    class DatabaseConfig(BaseModel):
        ...
        echo_sqlalchemy: bool = False
        ...

    class Settings(BaseSettings):
        ...
        db: DatabaseConfig
        ...
    ```

    Мы должны записать следующим образом переменную в файле `.env`:

    `DB__ECHO_SQLALCHEMY=True`

    Тогда класс настроек сможет определить к какому конифгу относится запись и изменит переменную.


    Ознкаомится с работой `BaseSettings`:
    https://docs.pydantic.dev/latest/concepts/pydantic_settings/

    Attributes:
        tg (TGConfig): класс конфигурации для Telegram бота.
        run (RunConfig): класс конфигурации для запуска сервиса.
        logging (LoggingConfig): класс конфигурации логирования сервисва.
        db (DatabaseConfig): класс конфигурации по работу с Базой Данных.
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=(".env", ".env.prod"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    run: RunConfig
    db: DatabaseConfig
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
