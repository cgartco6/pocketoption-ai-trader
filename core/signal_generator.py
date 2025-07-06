# Modified data ingestion in signal_generator.py
def get_market_data():
    """Memory-optimized data loader"""
    return pd.read_csv(
        'prices.csv',
        usecols=['timestamp','symbol','bid','ask'],
        dtype={'bid':'float32','ask':'float32'}  # Reduced precision
    )
