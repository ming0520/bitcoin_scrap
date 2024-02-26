# ScrapperE

ScrapperE is a Django project for web scraping.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Anaconda.
* You have a `<Windows/Linux/Mac>` machine. State which OS is supported/required.

## Installing ScrapperE

To install ScrapperE, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/ming0520/bitcoin_scrap.git
    ```

2. Navigate to the project directory:
    ```
    cd scrapperE
    ```

3. Create a conda environment:
    ```
    conda env create -f environment.yml
    ```

4. Activate the conda environment:
    ```
    conda activate "your_environment_name"
    ```

5. Configure the database in `scrapperE\scrapperE\settings.py`:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
Please replace `'your_database_name'`, `'your_username'`, and `'your_password'` with your actual database name, username, and password respectively.


## Using ScrapperE

To use ScrapperE, follow these steps

1. Load the database data:
    ```
    python manage.py loaddata database_dump.json
    ```

2. Apply migrations:
    ```
    python manage.py migrate
    ```

3. Run the server:
    ```
    python manage.py runserver
    ```

## Dump Database data to database_dump.json
```
set PYTHONIOENCODING=utf-8
python manage.py dumpdata > database_dump.json
```

## Navigate to Views

For more details about the views, please refer to [Views Readme](scrapperE/scrap/ViewsReadme.md)


## Data Sources

### Bitcoin
1. [Bitstamp OHLC](https://www.bitstamp.net/market/tradeview/)

### Reddit Communities

1. [CryptoCurrency Trading](https://www.reddit.com/r/CryptoCurrencyTrading/)
2. [Bitcoin - A Peer to Peer Electronic Cash System](https://www.reddit.com/r/btc/)
3. [Bitcoin for Beginners](https://www.reddit.com/r/BitcoinBeginners/)
4. [Bitcoin - The Currency of the Internet](https://www.reddit.com/r/Bitcoin/)

## Contact

If you want to contact me you can reach me at `<your_email@address.com>`.

## License

This project uses the following license: `<license_name>`.