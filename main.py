import services
import my_logger

logger = my_logger.config_logger(__name__)

if __name__ == '__main__':
    try:
        logger.info("Daily investment sync started")
        # Inserts the up to date list of Mutual Funds symbols to DB
        services.insert_mutual_funds_symbols()

        # Inserts the up to date list of Stock symbols to DB
        services.insert_stock_etf_symbols()

        #Updates the mutual funds and stock values
        services.update_current_value()

        logger.info("Daily investment sync completed successfully")

    except Exception:
        logger.exception("Daily investment sync failed")
        raise
