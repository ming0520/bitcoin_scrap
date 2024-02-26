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
    git clone https://github.com/yourusername/scrapperE.git
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
    conda activate your_environment_name
    ```

## Using ScrapperE

To use ScrapperE, follow these steps - dont use this first:

1. Load the database data:
    ```
    python manage.py loaddata dumps/data.json
    ```

2. Apply migrations:
    ```
    python manage.py migrate
    ```

3. Run the server:
    ```
    python manage.py runserver
    ```

## Data Sources

### Bitcoin
1. Bitcoin price OHLC: [bitstamp.net/market/tradeview/](https://www.bitstamp.net/market/tradeview/)

### Reddit Communities

1. [CryptoCurrency Trading](https://www.reddit.com/r/CryptoCurrencyTrading/)
2. [Bitcoin - A Peer to Peer Electronic Cash System](https://www.reddit.com/r/btc/)
3. [Bitcoin for Beginners](https://www.reddit.com/r/BitcoinBeginners/)
4. [Bitcoin - The Currency of the Internet](https://www.reddit.com/r/Bitcoin/)

## Contact

If you want to contact me you can reach me at `<your_email@address.com>`.

## License

This project uses the following license: `<license_name>`.