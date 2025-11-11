# 🥗 AI Diet Planner

An intelligent diet planning application that generates personalized meal plans based on your physical parameters, activity level, and fitness goals. Built with Streamlit and includes a comprehensive database to store and view all your data.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Personalized Calculations**: BMR, TDEE, and macronutrient calculations using scientifically-backed formulas
- **Smart Meal Planning**: AI-generated meal suggestions with detailed nutritional information
- **Database Integration**: SQLite database to store user profiles, diet plans, and meals
- **Interactive Dashboard**: View and analyze all your data with interactive charts
- **Export Data**: Download your data as CSV files
- **Dietary Restrictions**: Support for vegetarian, vegan, and other dietary preferences
- **Clean UI**: Beautiful, intuitive Streamlit interface

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ThatikondaKinshuk/AI_DIET_PLANNER.git
   cd AI_DIET_PLANNER
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running Locally

1. **Start the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

### Using the Application

1. **Create Your Profile**
   - Navigate to "Create Profile" in the sidebar
   - Enter your personal information (age, weight, height, gender)
   - Select your activity level and fitness goal
   - Optionally add dietary restrictions

2. **Generate Diet Plan**
   - Go to "Generate Diet Plan"
   - Select your profile from the dropdown
   - Click "Generate Diet Plan"
   - View your personalized meal plan with nutritional breakdown

3. **View Data**
   - Access the "View Data" page to see all stored information
   - View users, diet plans, and meals
   - Download data as CSV files
   - Analyze trends with interactive charts

## 🗄️ Database Schema

The application uses SQLite with three main tables:

### Users Table
- `id`: Primary key
- `name`: User's name
- `age`: Age in years
- `gender`: Male/Female
- `weight`: Weight in kg
- `height`: Height in cm
- `activity_level`: Physical activity level
- `goal`: Fitness goal (lose/maintain/gain)
- `dietary_restrictions`: Special dietary needs
- `created_at`: Timestamp

### Diet Plans Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `target_calories`: Daily calorie target
- `protein_grams`: Daily protein target
- `carbs_grams`: Daily carbs target
- `fats_grams`: Daily fats target
- `plan_date`: Date of plan creation
- `created_at`: Timestamp

### Meals Table
- `id`: Primary key
- `plan_id`: Foreign key to diet_plans
- `meal_type`: Breakfast/Lunch/Dinner/Snacks
- `meal_name`: Name of the meal
- `ingredients`: List of ingredients
- `calories`: Calorie content
- `protein`: Protein content (g)
- `carbs`: Carbohydrate content (g)
- `fats`: Fat content (g)

## 🔬 How It Works

### 1. BMR Calculation
Uses the **Mifflin-St Jeor Equation**:
- **Men**: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
- **Women**: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161

### 2. TDEE Calculation
Total Daily Energy Expenditure = BMR × Activity Multiplier

Activity Multipliers:
- Sedentary: 1.2
- Lightly active: 1.375
- Moderately active: 1.55
- Very active: 1.725
- Extremely active: 1.9

### 3. Target Calories
Based on your goal:
- **Lose weight**: TDEE - 500 calories
- **Maintain weight**: TDEE
- **Gain muscle**: TDEE + 300 calories

### 4. Macronutrient Distribution
Goal-specific macro ratios:
- **Lose weight**: 35% protein, 35% carbs, 30% fats
- **Maintain**: 30% protein, 40% carbs, 30% fats
- **Gain muscle**: 30% protein, 45% carbs, 25% fats

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.28.1
- **Database**: SQLite with direct SQL queries
- **Data Processing**: 
  - Pandas 2.1.1
  - NumPy 1.24.3
- **Visualization**: Plotly 5.17.0
- **ORM**: SQLAlchemy 2.0.21

## ☁️ Deployment

### Deploying to Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Sign up** at [Streamlit Cloud](https://streamlit.io/cloud)

3. **Deploy**:
   - Click "New app"
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

4. **Database Persistence**:
   - The SQLite database will persist during the session
   - For production use, consider using a cloud database (PostgreSQL, MySQL)

### Environment Variables (if needed)
- No environment variables required for basic functionality
- The database file will be created automatically

## 📁 Project Structure

```
AI_DIET_PLANNER/
├── app.py                 # Main Streamlit application
├── database.py            # Database operations and schema
├── diet_planner.py        # Diet planning logic and calculations
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── diet_planner.db       # SQLite database (created at runtime)
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more meal options
- Implement recipe API integration
- Add exercise tracking
- Create mobile-responsive design improvements
- Add multi-language support
- Implement meal planning for multiple days

## 📝 Notes & Disclaimers

- This application provides general nutrition guidance
- Always consult with healthcare professionals for medical advice
- Individual nutritional needs may vary
- Adjust plans based on your progress and how you feel
- The meal suggestions are examples and can be customized

## 🐛 Known Issues

- Database file is not included in git (by design)
- Large datasets may impact performance
- Mobile responsiveness could be improved

## 📧 Contact & Support

- **Issues**: Please report bugs via [GitHub Issues](https://github.com/ThatikondaKinshuk/AI_DIET_PLANNER/issues)
- **Repository**: [https://github.com/ThatikondaKinshuk/AI_DIET_PLANNER](https://github.com/ThatikondaKinshuk/AI_DIET_PLANNER)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Mifflin-St Jeor equation for BMR calculation
- Streamlit for the amazing framework
- Open source community for inspiration

---

**Made with ❤️ by the AI Diet Planner Team**

If you find this project useful, please give it a ⭐!
