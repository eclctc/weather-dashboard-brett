## 🌤️ Overview
The app combines real-time weather data with specialized pollen monitoring, allowing users to search weather conditions for any city while offering detailed pollen analytics specifically for Atlanta, GA. The seven-day historical pollen trends cover three types of pollen data, giving users insight into recent patterns that could affect their health.

## ✨ Features
- City Search: Users can search for weather information by entering a city name.
- Toggle between Dark and Light Mode.
- View seven day historical trends for three types of pollen data in Atlanta, GA
- Provides health recommendations, risk scores and real time pollen and weather information
- Predictions based on two years of hisorical pollen information based off historical precipitation, temperatures, wind speed and pollen counts

## 🏢 Structure
```
├── README.md
├── controllers
|   | 
│   └── weather_controller.py
├── data
|   | 
│   └── atlanta_historical_weather_data.csv
│   └── merged_pollen_weather_data.csv
│   └── pollen_atlanta_23_24.csv
│   └── team_weather_data.csv
│   └── weather_atlanta_23_24.csv
├── docs
|   |
│   ├── System Design.pdf
│   └── Week11_Reflection.md
│   └── Week13_Reflection.md
│   └── Week14_reflection.md
│   └── Week15_reflection.md
├── features
|   | 
│   ├── team_feature.py
│   ├── prediction_logic.py
│   └── weather_logger.py
├── models
│   |
│   └── weather_model.py
│   └── pollen_model.py
├── tests
|   |
│   └── test_persistece.py
│   └── test_pollen_api.py
│   └── test_weather_api.py
│   └── test_weather_view_chart.py
├── views
│   │ 
│   └── dashboard_view.py
│   └── prediction_view.py
│   └── search_view.py
│   └── team_view.py
├── requirments.txt
├── screenshots
├── app.py

```

## 🚀 Getting Started
Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API calls
- Code editor (VS Code, Sublime Text, etc.) for development and testing

## 🛠️ Technologies Used
- Python: For dynamic content updates, fetching data from a multiple APIs, prediction logic, graphs and handling user interactions.
- Tkinter: For UI and visuals representations of data
- Weather API: Utilizes a third-party weather API (OpenWeatherMap) to retrieve real-time weather data.
- Google Pollen API: Utilizes a third-party weather API (Google) to retrieve real-time pollen data.
- Local Storage: Persistent data storage for search history

## 🎯 Usage
To use the Weather Dashboard:
1. Clone the repository:
    git clone https://github.com/eclctc/weather-dashboard-brett.git
2. Navigate to the project directory:
    cd weather-dashboard-brett
3. Run pip install requirements.txt **Note:** if you're using a Mac and a virtual environment in VS Code, you may have issues with Tkinter. If you do run into issues, try downloading [Anaconda](https://www.anaconda.com/download), installing it globally and then selecting Conda as your python interpreter in VS Code.
4. Enter your [OpenWeatherMap API](https://openweathermap.org/) key into the .env file and save
5. Enter your [Google Pollen API](https://developers.google.com/maps/documentation/pollen/overview) key into the .env file and save
6. Run the program:
    python app.py

## 🤝 Contributing
This project was developed as a capstone project for JTC Tech Pathways Summer '25. While primarily for educational purposes, contributions and suggestions are welcome:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 🙏 Acknowledgments
- [JTC Tech Pathways Summer '25:](https://centerforjustice.columbia.edu/justicethroughcode) For providing the learning opportunity and project framework
- [Open Weather API Provider:](https://openweathermap.org/) For reliable weather data services
- [Google Pollen API Provider:](https://developers.google.com/maps/documentation/pollen) For reliable pollen data services
- [Ambee:](https://www.getambee.com/) For providing historical pollen data for Atlanta, GA to handle machine learning predictions
- Open Source Community: For tools and libraries that made this project possible
- Instructors and Mentors: For guidance and support throughout the development process