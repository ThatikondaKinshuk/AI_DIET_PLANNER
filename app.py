"""
AI Diet Planner - Streamlit Application
A comprehensive diet planning application with database integration
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
from database import DietPlannerDB
from diet_planner import DietPlanner

# Page configuration
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def init_db():
    return DietPlannerDB()

db = init_db()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🥗 AI Diet Planner")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "👤 Create Profile", "📊 Generate Diet Plan", "📈 View Data", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 This app helps you create personalized diet plans based on your goals and preferences.")


# Home Page
if page == "🏠 Home":
    st.markdown('<div class="main-header">🥗 AI Diet Planner</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to Your Personalized Diet Planning Assistant!
    
    This application helps you create customized diet plans based on:
    - Your physical parameters (age, weight, height)
    - Activity level
    - Fitness goals
    - Dietary restrictions
    
    #### 🎯 Features:
    - **Personalized Calculations**: BMR, TDEE, and macro calculations
    - **Smart Meal Planning**: AI-generated meal suggestions
    - **Database Integration**: Store and view all your data
    - **Visual Analytics**: Track your nutrition with interactive charts
    - **Easy to Use**: Simple, intuitive interface
    """)
    
    # Display statistics
    stats = db.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Total Users", stats['total_users'])
    with col2:
        st.metric("📋 Diet Plans Created", stats['total_plans'])
    with col3:
        st.metric("🍽️ Total Meals", stats['total_meals'])
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate through the application!")


# Create Profile Page
elif page == "👤 Create Profile":
    st.header("👤 Create Your Profile")
    st.markdown("Please provide your information to get started with personalized diet planning.")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name*", placeholder="Enter your name")
            age = st.number_input("Age*", min_value=10, max_value=100, value=25)
            gender = st.selectbox("Gender*", ["Male", "Female"])
            weight = st.number_input("Weight (kg)*", min_value=30.0, max_value=300.0, value=70.0, step=0.5)
        
        with col2:
            height = st.number_input("Height (cm)*", min_value=100.0, max_value=250.0, value=170.0, step=0.5)
            activity_level = st.selectbox(
                "Activity Level*",
                list(DietPlanner.ACTIVITY_MULTIPLIERS.keys())
            )
            goal = st.selectbox(
                "Goal*",
                list(DietPlanner.GOAL_ADJUSTMENTS.keys())
            )
            dietary_restrictions = st.text_input(
                "Dietary Restrictions",
                placeholder="e.g., vegetarian, vegan, gluten-free"
            )
        
        submit_button = st.form_submit_button("Create Profile", use_container_width=True)
        
        if submit_button:
            if not name:
                st.error("Please enter your name!")
            else:
                try:
                    # Add user to database
                    user_id = db.add_user(
                        name=name,
                        age=age,
                        gender=gender,
                        weight=weight,
                        height=height,
                        activity_level=activity_level,
                        goal=goal,
                        dietary_restrictions=dietary_restrictions
                    )
                    
                    st.success(f"✅ Profile created successfully! User ID: {user_id}")
                    st.balloons()
                    
                    # Show preview
                    st.markdown("### Profile Summary:")
                    profile_data = {
                        "Name": name,
                        "Age": age,
                        "Gender": gender,
                        "Weight": f"{weight} kg",
                        "Height": f"{height} cm",
                        "Activity Level": activity_level,
                        "Goal": goal,
                        "Dietary Restrictions": dietary_restrictions or "None"
                    }
                    
                    for key, value in profile_data.items():
                        st.write(f"**{key}:** {value}")
                    
                    st.info("💡 Now go to 'Generate Diet Plan' to create your personalized meal plan!")
                    
                except Exception as e:
                    st.error(f"Error creating profile: {str(e)}")


# Generate Diet Plan Page
elif page == "📊 Generate Diet Plan":
    st.header("📊 Generate Your Diet Plan")
    
    # Get all users
    users_df = db.get_all_users()
    
    if users_df.empty:
        st.warning("⚠️ No users found. Please create a profile first!")
        st.info("👈 Go to 'Create Profile' in the sidebar to get started.")
    else:
        # User selection
        user_names = users_df['name'].tolist()
        user_ids = users_df['id'].tolist()
        user_dict = dict(zip(user_names, user_ids))
        
        selected_name = st.selectbox("Select User Profile", user_names)
        selected_user_id = user_dict[selected_name]
        
        # Get user data
        user_data = users_df[users_df['id'] == selected_user_id].iloc[0]
        
        # Display user info
        st.markdown("### Selected Profile:")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Age", f"{user_data['age']} years")
        col2.metric("Weight", f"{user_data['weight']} kg")
        col3.metric("Height", f"{user_data['height']} cm")
        col4.metric("Goal", user_data['goal'])
        
        st.markdown("---")
        
        # Generate plan button
        if st.button("🎯 Generate Diet Plan", use_container_width=True):
            with st.spinner("Generating your personalized diet plan..."):
                try:
                    # Get complete nutrition plan
                    plan = DietPlanner.get_complete_nutrition_plan(
                        weight=user_data['weight'],
                        height=user_data['height'],
                        age=user_data['age'],
                        gender=user_data['gender'],
                        activity_level=user_data['activity_level'],
                        goal=user_data['goal'],
                        dietary_restrictions=user_data['dietary_restrictions']
                    )
                    
                    # Save to database
                    plan_id = db.add_diet_plan(
                        user_id=selected_user_id,
                        target_calories=plan['target_calories'],
                        protein_grams=plan['target_macros']['protein'],
                        carbs_grams=plan['target_macros']['carbs'],
                        fats_grams=plan['target_macros']['fats'],
                        plan_date=date.today().isoformat()
                    )
                    
                    # Save meals
                    for meal in plan['meal_plan']:
                        db.add_meal(
                            plan_id=plan_id,
                            meal_type=meal['meal_type'],
                            meal_name=meal['name'],
                            ingredients=meal['ingredients'],
                            calories=meal['calories'],
                            protein=meal['protein'],
                            carbs=meal['carbs'],
                            fats=meal['fats']
                        )
                    
                    st.success("✅ Diet plan generated successfully!")
                    
                    # Display results
                    st.markdown("### 📊 Nutritional Calculations")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("BMR (Basal Metabolic Rate)", f"{plan['bmr']} kcal")
                    col2.metric("TDEE (Total Daily Energy)", f"{plan['tdee']} kcal")
                    col3.metric("Target Calories", f"{plan['target_calories']} kcal")
                    
                    st.markdown("### 🎯 Target Macronutrients")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Protein", f"{plan['target_macros']['protein']} g")
                    col2.metric("Carbs", f"{plan['target_macros']['carbs']} g")
                    col3.metric("Fats", f"{plan['target_macros']['fats']} g")
                    
                    # Macronutrient pie chart
                    st.markdown("### 📈 Macronutrient Distribution")
                    
                    macros_data = {
                        'Nutrient': ['Protein', 'Carbs', 'Fats'],
                        'Grams': [
                            plan['actual_totals']['protein'],
                            plan['actual_totals']['carbs'],
                            plan['actual_totals']['fats']
                        ]
                    }
                    
                    fig = px.pie(
                        macros_data,
                        values='Grams',
                        names='Nutrient',
                        title='Daily Macronutrient Distribution',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFE66D']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Meal plan
                    st.markdown("### 🍽️ Your Daily Meal Plan")
                    
                    for meal in plan['meal_plan']:
                        with st.expander(f"**{meal['meal_type']}** - {meal['name']} ({meal['calories']} kcal)"):
                            st.write(f"**Ingredients:** {meal['ingredients']}")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Calories", f"{meal['calories']} kcal")
                            col2.metric("Protein", f"{meal['protein']} g")
                            col3.metric("Carbs", f"{meal['carbs']} g")
                            col4.metric("Fats", f"{meal['fats']} g")
                    
                    # Actual totals
                    st.markdown("### 📝 Daily Totals")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Calories", f"{plan['actual_totals']['calories']} kcal")
                    col2.metric("Total Protein", f"{plan['actual_totals']['protein']} g")
                    col3.metric("Total Carbs", f"{plan['actual_totals']['carbs']} g")
                    col4.metric("Total Fats", f"{plan['actual_totals']['fats']} g")
                    
                except Exception as e:
                    st.error(f"Error generating diet plan: {str(e)}")


# View Data Page
elif page == "📈 View Data":
    st.header("📈 Database View & Analytics")
    
    # Tabs for different data views
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📋 Diet Plans", "🍽️ Meals", "📊 Statistics"])
    
    with tab1:
        st.subheader("All Users")
        users_df = db.get_all_users()
        
        if users_df.empty:
            st.info("No users in the database yet.")
        else:
            st.dataframe(users_df, use_container_width=True)
            st.download_button(
                label="📥 Download Users Data",
                data=users_df.to_csv(index=False),
                file_name=f"users_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with tab2:
        st.subheader("All Diet Plans")
        plans_df = db.get_all_diet_plans()
        
        if plans_df.empty:
            st.info("No diet plans in the database yet.")
        else:
            st.dataframe(plans_df, use_container_width=True)
            st.download_button(
                label="📥 Download Diet Plans Data",
                data=plans_df.to_csv(index=False),
                file_name=f"diet_plans_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Visualizations
            if len(plans_df) > 0:
                st.markdown("### 📊 Diet Plans Analytics")
                
                # Average calories by user
                fig = px.bar(
                    plans_df,
                    x='user_name',
                    y='target_calories',
                    title='Target Calories by User',
                    labels={'target_calories': 'Calories', 'user_name': 'User'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("All Meals")
        meals_df = db.get_all_meals()
        
        if meals_df.empty:
            st.info("No meals in the database yet.")
        else:
            st.dataframe(meals_df, use_container_width=True)
            st.download_button(
                label="📥 Download Meals Data",
                data=meals_df.to_csv(index=False),
                file_name=f"meals_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Meal type distribution
            if len(meals_df) > 0:
                st.markdown("### 🍽️ Meals Analytics")
                
                meal_type_counts = meals_df['meal_type'].value_counts()
                fig = px.pie(
                    values=meal_type_counts.values,
                    names=meal_type_counts.index,
                    title='Distribution of Meal Types'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Database Statistics")
        stats = db.get_statistics()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Users", stats['total_users'])
        col2.metric("📋 Total Diet Plans", stats['total_plans'])
        col3.metric("🍽️ Total Meals", stats['total_meals'])
        
        # Additional analytics
        if stats['total_plans'] > 0:
            plans_df = db.get_all_diet_plans()
            
            st.markdown("### 📈 Nutritional Trends")
            
            # Average macros
            avg_protein = plans_df['protein_grams'].mean()
            avg_carbs = plans_df['carbs_grams'].mean()
            avg_fats = plans_df['fats_grams'].mean()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Protein", f"{avg_protein:.1f} g")
            col2.metric("Avg Carbs", f"{avg_carbs:.1f} g")
            col3.metric("Avg Fats", f"{avg_fats:.1f} g")


# About Page
elif page == "ℹ️ About":
    st.header("ℹ️ About AI Diet Planner")
    
    st.markdown("""
    ### 🎯 Purpose
    
    The AI Diet Planner is a comprehensive web application designed to help individuals 
    create personalized diet plans based on their unique characteristics and goals.
    
    ### ⚙️ How It Works
    
    1. **Profile Creation**: Enter your physical parameters, activity level, and goals
    2. **Calculation Engine**: Uses scientifically-backed formulas (Mifflin-St Jeor) to calculate:
       - BMR (Basal Metabolic Rate)
       - TDEE (Total Daily Energy Expenditure)
       - Target calories based on your goal
       - Optimal macronutrient distribution
    3. **Meal Generation**: AI-powered meal suggestions tailored to your needs
    4. **Database Storage**: All data is stored in a SQLite database for easy access and analysis
    
    ### 🔬 Scientific Basis
    
    - **BMR Calculation**: Mifflin-St Jeor Equation
    - **Activity Multipliers**: Evidence-based TDEE calculations
    - **Macro Distribution**: Goal-specific ratios optimized for different objectives
    
    ### 🛠️ Technology Stack
    
    - **Frontend**: Streamlit
    - **Database**: SQLite with SQLAlchemy
    - **Visualization**: Plotly
    - **Data Processing**: Pandas, NumPy
    
    ### 📊 Features
    
    - ✅ Personalized calorie and macro calculations
    - ✅ Smart meal plan generation
    - ✅ Database integration for data persistence
    - ✅ Interactive data visualization
    - ✅ Export data as CSV
    - ✅ Dietary restriction support
    - ✅ Clean, intuitive interface
    
    ### 📝 Notes
    
    - This app provides general nutrition guidance
    - Always consult healthcare professionals for medical advice
    - Individual results may vary
    - Adjust plans based on your progress and how you feel
    
    ### 🔗 Database Schema
    
    The application uses three main tables:
    - **Users**: Stores user profiles
    - **Diet Plans**: Stores generated diet plans with calorie and macro targets
    - **Meals**: Stores individual meals with detailed nutritional information
    
    ### 📧 Support
    
    For questions or feedback, please reach out through the repository.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: November 2024
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ using Streamlit | 🥗 AI Diet Planner © 2024</p>
    </div>
    """,
    unsafe_allow_html=True
)
