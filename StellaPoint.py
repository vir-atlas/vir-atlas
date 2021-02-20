# @author Marisa Loraas
# 2/20/2021
# @brief: StellaPoint object: creates an object for every point the STELLA records, so that you can access any attribute
# that stella outputs for any point of record. Each attribute in the __init__ parameters are the attributes given out
# by stella that can be seen in the stella_data_column_header.xlsx (besides the columns with "mark" in them because I
# deemed them not important for these attributes, but they are commented out


class StellaPoint:
    def __init__(self, batch, day, timestamp, decimal_hour,  surface_temp_units, surface_temp, surface_temp_error_bar,
                 air_temp_units, air_temp, air_temp_error_bar, relative_humidity_units, relative_humidity,
                 relative_humidity_error_bar, air_pressure_units, air_pressure_hpa, air_pressure_error_bar,
                 altitude_units, altitude_m_uncal, altitude_error_bar,  vs_waveband_units, vs_power_units,
                 visible_spectrum_error_bar, vs_waveband_450, vs_power_450, vs_waveband_500, vs_power_500,
                 vs_waveband_550, vs_power_550, vs_waveband_570, vs_power_570, vs_waveband_600, vs_power_600,
                 vs_waveband_650, vs_power_650, nir_waveband_units, nir_power_units, nir_spectrum_error_bar,
                 nir_waveband_610, nir_power_610, nir_waveband_680, nir_power_680, nir_waveband_730, nir_power_730,
                 nir_waveband_760, nir_power_760, nir_waveband_810,
                 nir_power_810, nir_waveband_860, nir_power_860):
        self.batch = batch
        self.day = day
        self.timestamp = timestamp
        #  self.dhm = decimal_hours_mark
        self.dh = decimal_hour
        #  self.stm = surface_temp_mark
        self.surface_temp_units = surface_temp_units
        self.surface_temp = surface_temp
        self.st_error_bar = surface_temp_error_bar
        # self.atm = air_temp_mark
        self.air_temp_units = air_temp_units
        self.air_temp = air_temp
        self.at_error_bar = air_temp_error_bar
    #   self.rhm = relative_humidity_mark
        self.rel_humid_units = relative_humidity_units
        self.rel_humid = relative_humidity
        self.rh_error_bar = relative_humidity_error_bar
    #   self.apm = air_pressure_mark
        self.air_pressure_units = air_pressure_units
        self.air_pressure_hpa = air_pressure_hpa
        self.ap_error_bar = air_pressure_error_bar
    #    self.altitude_mark = altitude_mark
        self.altitude_units = altitude_units
        self.altitude_m_uncal = altitude_m_uncal
        self.altitude_error_bar = altitude_error_bar
    #   self.vs_mark = visible_spectrum_mark
        self.vs_waveband_units = vs_waveband_units
        self.vs_power_units = vs_power_units
        self.vs_error_bar = visible_spectrum_error_bar
        self.vs_waveband_450 = vs_waveband_450  # <-- check
        self.vs_power_450 = vs_power_450
        self.vs_waveband_500 = vs_waveband_500  # <-- check
        self.vs_power_500 = vs_power_500
        self.vs_waveband_550 = vs_waveband_550  # <-- check
        self.vs_power_550 = vs_power_550
        self.vs_waveband_570 = vs_waveband_570
        self.vs_power_570 = vs_power_570
        self.vs_waveband_600 = vs_waveband_600 # <-- check
        self.vs_power_600 = vs_power_600
        self.vs_waveband_650 = vs_waveband_650
        self.vs_power_650 = vs_power_650
        # self.nir_spectrum_mark = nir_spectrum_mark
        self.nir_waveband_units = nir_waveband_units
        self.nir_power_units = nir_power_units
        self.nir_spectrum_error_bar = nir_spectrum_error_bar
        self.nir_waveband_610 = nir_waveband_610  # <--Check
        self.nir_power_610 = nir_power_610
        self.nir_waveband_680 = nir_waveband_680  # <--Check
        self.nir_power_680 = nir_power_680
        self.nir_waveband_730 = nir_waveband_730  # <-- Check
        self.nir_power_730 = nir_power_730
        self.nir_waveband_760 = nir_waveband_760  # <--Check
        self.nir_power_760 = nir_power_760
        self.nir_waveband_810 = nir_waveband_810  # <--Check
        self.nir_power_810 = nir_power_810
        self.nir_waveband_860 = nir_waveband_860  # <-- check
        self.nir_power_860 = nir_power_860
