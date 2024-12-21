import requests
from django.core.cache import cache
from django.http import JsonResponse

def get_weather_data(city, api_key="543c25cec64dd334bf1d766c48691a33"):

    # 设置缓存
    cache_key = 'weather_data_{city}'
    weather = cache.get(cache_key)

    if weather is None: # 缓存中没有weather数据
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={api_key}&city={city}&extensions=base"
        try:
            response = requests.get(url)
            data = response.json()

            if data["status"] == "1" and 'lives' in data:
                weather_data = data["lives"][0]
                weather = {
                    "city": weather_data["city"],
                    "weather": weather_data["weather"],
                    "temperature": f"{weather_data['temperature']}°C",
                    "winddirection": weather_data["winddirection"],
                    "windpower": f"{weather_data['windpower']}级",
                    "humidity": f"{weather_data['humidity']}%"
                }
                cache.set(cache_key, weather, timeout=3600) # 一小时缓存
                print(f"Request URL: {url}")
                print(f"API Response: {data}")
                return weather
            else:
                return {"error": "天气数据获取失败"}
        except Exception as e:
            return {"error": f"请求错误: {e}"}
    return weather
