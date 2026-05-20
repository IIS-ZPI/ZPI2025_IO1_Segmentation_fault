from src.utils.exchange_rates import get_exchange_rates

if __name__ == "__main__":
    print(get_exchange_rates("EUR", "2026-03-30", "2026-04-10"))
