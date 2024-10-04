from enum import StrEnum


class Transmisions(StrEnum):
    AUTO = 'auto'
    MANUAL = 'manual'

    @staticmethod
    def map_value_from(value: str) -> 'Transmisions':
        value = value.lower()
        if value == 'manual' or value == 'manual_transmission':
            return Transmisions.MANUAL
        
        if value == 'automatic' or value == 'automatic_transmission':
            return Transmisions.AUTO
        
        raise ValueError(f'Invalid value: {value}')


class FuelTypes(StrEnum):
    PETROL = 'petrol'
    PETROL_CNG = 'petrol_cng'
    PETROL_LPG = 'petrol_lpg'
    DIESEL = 'diesel'
    ELECTRIC = 'electric'
    ETHANOL = 'ethanol'
    HYBRID = 'hybrid'
    HYBRID_PLUGIN = 'hybrid_plugin'
    HYDROGEN = 'hydrogen'

    @staticmethod
    def to_common(value: str) -> 'FuelTypes':
        value = value.lower().replace('-', '_')
        enum_value = FuelTypes.__members__.get(value.upper())

        if enum_value:
            return enum_value

        raise ValueError(f'Invalid value: {value}')
    