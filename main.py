import services

if __name__ == '__main__':
    # Inserts the up to date list of Mutual Funds symbols to DB
    services.insert_mutual_funds_symbols()

    # Inserts the up to date list of Stock symbols to DB
    services.insert_stock_etf_symbols()

    #Updates the mutual funds and stock values
    services.update_current_value()
