## API demo
https://www.loom.com/share/55fa80ba8c234675bcdb7cc1ccc38033

## UI Mockup
https://miro.com/app/board/uXjVIkLdpME=/?share_link_id=132606136343

## Core functionality explanation
This function currently serves as our reliable gateway for fetching core weather data, like temperature, conditions, and humidity, directly from the OpenWeatherMap API. It's designed with built-in retries and robust error handling to ensure that information is gathered consistently, even with network quirks or API limits. Looking ahead, this established pattern of securely acquiring external data will be vital as I explore integrating specialized datasets. Specifically, I'm working on how to adapt this logic to pull accurate pollen information from projects like the Google Pollen API, which integrates seamlessly with the Google Maps platform.

The only real blocker I have right now is the dataset I'm acquiring from Ambee. There's been a lot of back-and-forth communication about getting the specific pollen data I need to build my machine learning models and integrate them with the data from the API. Once I have that—hopefully this week—I’ll be able to hit the ground running with the core logic and features. After that, I’ll focus on designing the charts, refining the models, and finalizing the UI layout. It’s going to be a tight timeline, but I’m confident the wait will be worth it.