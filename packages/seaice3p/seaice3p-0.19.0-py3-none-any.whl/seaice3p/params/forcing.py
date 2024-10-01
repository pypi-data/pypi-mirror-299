from pathlib import Path
from dataclasses import dataclass
from serde import serde, coerce
import numpy as np
from .dimensional import (
    DimensionalParams,
    DimensionalConstantForcing,
    DimensionalBRW09Forcing,
    DimensionalYearlyForcing,
    DimensionalRadForcing,
    DimensionalRobinForcing,
    DimensionalSWForcing,
    DimensionalConstantSWForcing,
    DimensionalOilHeating,
    DimensionalBackgroundOilHeating,
    DimensionalLWForcing,
    DimensionalConstantLWForcing,
    DimensionalTurbulentFlux,
    DimensionalConstantTurbulentFlux,
)


def _filter_missing_values(air_temp, days):
    """Filter out missing values are recorded as 9999"""
    is_missing = np.abs(air_temp) > 100
    return air_temp[~is_missing], days[~is_missing]


@serde(type_check=coerce)
@dataclass(frozen=True)
class BaseOceanForcing:
    """Not to be used directly but provides parameters for fixed ocean properties:
    gas saturation, temperature and bulk salinity to other forcing configuration
    classes
    """

    ocean_temp: float = 0.1
    ocean_bulk_salinity: float = 0
    ocean_gas_sat: float = 1.0


@serde(type_check=coerce)
@dataclass(frozen=True)
class ConstantForcing(BaseOceanForcing):
    """Constant temperature forcing"""

    constant_top_temperature: float = -1.5


@serde(type_check=coerce)
@dataclass(frozen=True)
class YearlyForcing(BaseOceanForcing):
    """Yearly sinusoidal temperature forcing"""

    offset: float = -1.0
    amplitude: float = 0.75
    period: float = 4.0


@serde(type_check=coerce)
class BRW09Forcing:
    """Surface and ocean temperature data loaded from thermistor temperature record
    during the Barrow 2009 field study.
    """

    ocean_bulk_salinity: float = 0
    ocean_gas_sat: float = 1.0
    Barrow_top_temperature_data_choice: str = "air"

    def __post_init__(self):
        """populate class attributes with barrow dimensional air temperature
        and time in days (with missing values filtered out).

        Note the metadata explaining how to use the barrow temperature data is also
        in seaice3p/forcing_data. The indices corresponding to days and air temp are
        hard coded in as class variables.
        """
        DATA_INDICES = {
            "time": 0,
            "air": 8,
            "bottom_snow": 18,
            "top_ice": 19,
            "ocean": 43,
        }
        data = np.genfromtxt(
            Path(__file__).parent.parent / "forcing_data/BRW09.txt", delimiter="\t"
        )
        top_temp_index = DATA_INDICES[self.Barrow_top_temperature_data_choice]
        ocean_temp_index = DATA_INDICES["ocean"]
        time_index = DATA_INDICES["time"]

        barrow_top_temp = data[:, top_temp_index]
        barrow_days = data[:, time_index] - data[0, time_index]
        barrow_top_temp, barrow_days = _filter_missing_values(
            barrow_top_temp, barrow_days
        )

        barrow_bottom_temp = data[:, ocean_temp_index]
        barrow_ocean_days = data[:, time_index] - data[0, time_index]
        barrow_bottom_temp, barrow_ocean_days = _filter_missing_values(
            barrow_bottom_temp, barrow_ocean_days
        )

        self.barrow_top_temp = barrow_top_temp
        self.barrow_bottom_temp = barrow_bottom_temp
        self.barrow_ocean_days = barrow_ocean_days
        self.barrow_days = barrow_days


@serde(type_check=coerce)
@dataclass(frozen=True)
class RadForcing(BaseOceanForcing):
    """Forcing parameters for radiative transfer simulation with oil drops

    we have not implemented the non-dimensionalisation for these parameters yet
    and so we just pass the dimensional values directly to the simulation"""

    SW_forcing: DimensionalSWForcing = DimensionalConstantSWForcing()
    LW_forcing: DimensionalLWForcing = DimensionalConstantLWForcing()
    turbulent_flux: DimensionalTurbulentFlux = DimensionalConstantTurbulentFlux()
    oil_heating: DimensionalOilHeating = DimensionalBackgroundOilHeating()


@serde(type_check=coerce)
@dataclass(frozen=True)
class RobinForcing(BaseOceanForcing):
    """Dimensionless forcing parameters for Robin boundary condition"""

    biot: float = 12
    restoring_temperature: float = -1.3


ForcingConfig = (
    ConstantForcing | YearlyForcing | BRW09Forcing | RadForcing | RobinForcing
)


def get_dimensionless_forcing_config(
    dimensional_params: DimensionalParams,
) -> ForcingConfig:
    ocean_temp = (
        dimensional_params.water_params.ocean_temperature
        - dimensional_params.water_params.ocean_freezing_temperature
    ) / dimensional_params.water_params.temperature_difference
    ocean_bulk_salinity = 0
    ocean_gas_sat = dimensional_params.gas_params.ocean_saturation_state
    match dimensional_params.forcing_config:
        case DimensionalConstantForcing():
            top_temp = (
                dimensional_params.forcing_config.constant_top_temperature
                - dimensional_params.water_params.ocean_freezing_temperature
            ) / dimensional_params.water_params.temperature_difference
            return ConstantForcing(
                ocean_temp=ocean_temp,
                ocean_bulk_salinity=ocean_bulk_salinity,
                ocean_gas_sat=ocean_gas_sat,
                constant_top_temperature=top_temp,
            )
        case DimensionalYearlyForcing():
            return YearlyForcing(
                ocean_temp=ocean_temp,
                ocean_bulk_salinity=ocean_bulk_salinity,
                ocean_gas_sat=ocean_gas_sat,
                offset=dimensional_params.forcing_config.offset,
                amplitude=dimensional_params.forcing_config.amplitude,
                period=dimensional_params.forcing_config.period,
            )
        case DimensionalBRW09Forcing():
            return BRW09Forcing(
                ocean_bulk_salinity=ocean_bulk_salinity,
                ocean_gas_sat=ocean_gas_sat,
                Barrow_top_temperature_data_choice=dimensional_params.forcing_config.Barrow_top_temperature_data_choice,
            )
        case DimensionalRadForcing():
            return RadForcing(
                ocean_temp=ocean_temp,
                ocean_bulk_salinity=ocean_bulk_salinity,
                ocean_gas_sat=ocean_gas_sat,
                SW_forcing=dimensional_params.forcing_config.SW_forcing,
                LW_forcing=dimensional_params.forcing_config.LW_forcing,
                turbulent_flux=dimensional_params.forcing_config.turbulent_flux,
                oil_heating=dimensional_params.forcing_config.oil_heating,
            )
        case DimensionalRobinForcing():
            restoring_temperature = (
                dimensional_params.forcing_config.restoring_temperature
                - dimensional_params.water_params.ocean_freezing_temperature
            ) / dimensional_params.water_params.temperature_difference
            biot = (
                dimensional_params.lengthscale
                * dimensional_params.forcing_config.heat_transfer_coefficient
                / dimensional_params.water_params.liquid_thermal_conductivity
            )
            return RobinForcing(
                ocean_temp=ocean_temp,
                ocean_bulk_salinity=ocean_bulk_salinity,
                ocean_gas_sat=ocean_gas_sat,
                biot=biot,
                restoring_temperature=restoring_temperature,
            )
        case _:
            raise NotImplementedError
