# 🚀 Quick Start Guide

Get started with AI Diet Planner in 5 minutes!

## Step 1: Installation

```bash
# Clone the repository
git clone https://github.com/ThatikondaKinshuk/AI_DIET_PLANNER.git
cd AI_DIET_PLANNER

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 3: Create Your First Profile

1. Click on **"👤 Create Profile"** in the sidebar
2. Fill in your information:
   - Name
   - Age
   - Gender
   - Weight (kg)
   - Height (cm)
   - Activity Level
   - Goal (Lose/Maintain/Gain)
   - Dietary Restrictions (optional)
3. Click **"Create Profile"**

## Step 4: Generate Your Diet Plan

1. Click on **"📊 Generate Diet Plan"** in the sidebar
2. Select your profile from the dropdown
3. Click **"Generate Diet Plan"**
4. View your personalized meal plan with:
   - BMR and TDEE calculations
   - Target calories and macros
   - Daily meal suggestions
   - Nutritional breakdown

## Step 5: View Your Data

1. Click on **"📈 View Data"** in the sidebar
2. Explore different tabs:
   - **Users**: All user profiles
   - **Diet Plans**: All generated plans
   - **Meals**: All meal suggestions
   - **Statistics**: Overview and analytics
3. Download data as CSV files

## 🎯 Quick Tips

- **Multiple Users**: Create profiles for family members
- **Track Progress**: Generate new plans regularly
- **Export Data**: Download CSV files for external analysis
- **Dietary Restrictions**: Enter "vegetarian", "vegan", or specific allergies
- **Adjust Goals**: Create new profiles as your goals change

## 🔧 Troubleshooting

### App won't start?
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Try running with Python directly
python -m streamlit run app.py
```

### Database errors?
- The app creates `diet_planner.db` automatically
- Delete the database file to start fresh

### Import errors?
- Make sure you're in the correct directory
- Verify Python version is 3.8 or higher

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize meal options in `diet_planner.py`
- Deploy to Streamlit Cloud for online access

## 🎉 You're Ready!

Start planning your perfect diet today! 🥗
