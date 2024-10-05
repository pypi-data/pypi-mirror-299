from enum import StrEnum


class PriceCurrency(StrEnum):
    PLN = 'PLN'

    @staticmethod
    def map_value_from(value: str) -> 'PriceCurrency':
        value = value.upper()
        if value == 'PLN':
            return PriceCurrency.PLN

        raise ValueError(f'Invalid value: {value}')