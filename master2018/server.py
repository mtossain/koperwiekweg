import rpyc
import os

class WeatherService(rpyc.Service):

    # Class variables to be accessed from outside
    temperature = 0
    pressure = 0
    humidity = 0
    rain = 0
    rain_rate = 0
    wind_speed = 0
    wind_dir_str = ''
    wind_dir_angle = 0
    uv_index = 0
    light_intensity = 0

    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def get_all(self): # this is an exposed method
        return self.temperature,self.pressure,self.humidity,self.rain,self.rain_rate,self.wind_speed,self.wind_dir_str,self.wind_dir_angle,self.uv_index,self.light_intensity

    def update_sensor_2018(self,in_temperature,in_pressure,in_humidity,in_uv_index,in_light_intensity): # this is an exposed method
        self.temperature = in_temperature
        self.pressure = in_pressure
        self.humidity = in_humidity
        self.uv_index = in_uv_index
        self.light_intensity = in_light_intensity
        pass
    
    def update_sensor_rain(self,in_rain,in_rain_rate): # this is an exposed method
        self.rain = in_rain
        self.rain_rate = in_rain_rate
        pass

    def update_sensor_wind(self,in_wind_speed,in_wind_dir_str,in_wind_dir_angle): # this is an exposed method
        self.wind_speed = in_wind_speed
        self.wind_dir_str = in_wind_dir_str
        self.wind_dir_angle = in_wind_dir_angle
        pass

if __name__ == "__main__":

    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(WeatherService(), port=18861,protocol_config={"allow_public_attrs": True})
    print('[OK] Waiting for connection...')
    t.start()
