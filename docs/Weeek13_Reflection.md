## API demo
https://www.loom.com/share/55fa80ba8c234675bcdb7cc1ccc38033

## Core functinality explanation
This function currently serves as our reliable gateway for fetching core weather data, like temperature, conditions, and humidity, directly from the OpenWeatherMap API. It's designed with built-in retries and robust error handling to ensure that information is gathered consistently, even with network quirks or API limits. Looking ahead, this established pattern of securely acquiring external data will be vital as I explore integrating specialized datasets. Specifically, I'm working on how to adapt this logic to pull accurate pollen information from projects like the Pollen API, which integrates seamlessly with the Google Maps platform.