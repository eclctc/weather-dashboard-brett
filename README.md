## 🌤️ Overview
This is a simple Tkinter application that serves as a weather dashboard, providing real-time weather information and forecasts for cities around the world. Users can search for a city to view current weather conditions and a multi-day forecast.

## ✨ Features
- City Search: Users can search for weather information by entering a city name.
- Toggle between Dark and Light Mode.
- Current Weather Display: Shows current temperature, humidity, and general weather conditions.

## 🏢 Structure
├── README.md
├── config.py
├── controllers
|   | 
│   └── weather_controller.py
├── docs
│   ├── System Design.pdf
│   └── Week11_Reflection.md
├── features
|   | 
│   ├── graph_logic.py
│   ├── prediction_logic.py
│   └── weather_logger.py
├── main.py
├── models
│   |
│   └── weather_model.py
├── requirments.txt
├── screenshots
├── tests
|   |
│   └── test_persistece.py
├── views
│   │ 
│   └── weather_view.py
└── weather_log.csv

13 directories, 21 files

## 🚀 Getting Started
Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for API calls
- Code editor (VS Code, Sublime Text, etc.) for development

## 🛠️ Technologies Used
- Python: For dynamic content updates, fetching data from a weather API, and handling user interactions.
- Tkinter: For UI and visuals representations of data
- Weather API: Utilizes a third-party weather API (OpenWeatherMap) to retrieve real-time weather data.
- Local Storage: Persistent data storage for search history

## 🎯 Usage
To use the Weather Dashboard:
1. Clone the repository:
    git clone https://github.com/eclctc/weather-dashboard-brett.git
2. Navigate to the project directory:
    cd weather-dashboard-brett
3. Run the program:
    python main.py
4. Enter your OpenWeatherMap API key into the .env file
5. Enter a city: Type the name of a city into the search bar and press "Get Weather" to view its weather information.

## 🤝 Contributing
This project was developed as a capstone project for JTC Tech Pathways Summer '25. While primarily for educational purposes, contributions and suggestions are welcome:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 🙏 Acknowledgments
- JTC Tech Pathways Summer '25: For providing the learning opportunity and project framework
- Weather API Provider: For reliable weather data services
- Open Source Community: For tools and libraries that made this project possible
- Instructors and Mentors: For guidance and support throughout the development process