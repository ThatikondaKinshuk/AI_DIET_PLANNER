"""
Sample Data Generator for AI Diet Planner
Run this script to populate the database with sample data for demonstration
"""

from database import DietPlannerDB
from diet_planner import DietPlanner
from datetime import date, timedelta
import random


def generate_sample_data():
    """Generate sample users and diet plans for demonstration"""
    
    print("\n" + "="*60)
    print("🎲 GENERATING SAMPLE DATA FOR AI DIET PLANNER")
    print("="*60)
    
    # Initialize database
    db = DietPlannerDB()
    
    # Sample users with diverse profiles
    sample_users = [
        {
            "name": "John Smith",
            "age": 30,
            "gender": "Male",
            "weight": 80.0,
            "height": 178.0,
            "activity_level": "Moderately active (3-5 days/week)",
            "goal": "Lose weight",
            "dietary_restrictions": "None"
        },
        {
            "name": "Emma Johnson",
            "age": 25,
            "gender": "Female",
            "weight": 62.0,
            "height": 165.0,
            "activity_level": "Very active (6-7 days/week)",
            "goal": "Gain muscle",
            "dietary_restrictions": "Vegetarian"
        },
        {
            "name": "Michael Brown",
            "age": 35,
            "gender": "Male",
            "weight": 95.0,
            "height": 185.0,
            "activity_level": "Lightly active (1-3 days/week)",
            "goal": "Lose weight",
            "dietary_restrictions": "None"
        },
        {
            "name": "Sarah Davis",
            "age": 28,
            "gender": "Female",
            "weight": 55.0,
            "height": 160.0,
            "activity_level": "Sedentary (little or no exercise)",
            "goal": "Maintain weight",
            "dietary_restrictions": "Vegan"
        },
        {
            "name": "David Wilson",
            "age": 40,
            "gender": "Male",
            "weight": 75.0,
            "height": 175.0,
            "activity_level": "Moderately active (3-5 days/week)",
            "goal": "Maintain weight",
            "dietary_restrictions": "None"
        }
    ]
    
    print(f"\n📝 Creating {len(sample_users)} sample users...")
    
    created_users = []
    for idx, user_data in enumerate(sample_users, 1):
        user_id = db.add_user(**user_data)
        created_users.append((user_id, user_data))
        print(f"   {idx}. {user_data['name']} (ID: {user_id}) - {user_data['goal']}")
    
    print(f"   ✅ {len(created_users)} users created")
    
    # Generate diet plans for each user
    print(f"\n🍽️  Generating diet plans...")
    
    total_plans = 0
    total_meals = 0
    
    for user_id, user_data in created_users:
        # Generate 1-3 plans per user (different dates)
        num_plans = random.randint(1, 3)
        
        for plan_num in range(num_plans):
            # Calculate plan date (today minus some days)
            days_ago = plan_num * 7  # Weekly plans
            plan_date = (date.today() - timedelta(days=days_ago)).isoformat()
            
            # Generate nutrition plan
            plan = DietPlanner.get_complete_nutrition_plan(
                weight=user_data['weight'],
                height=user_data['height'],
                age=user_data['age'],
                gender=user_data['gender'],
                activity_level=user_data['activity_level'],
                goal=user_data['goal'],
                dietary_restrictions=user_data['dietary_restrictions']
            )
            
            # Save diet plan
            plan_id = db.add_diet_plan(
                user_id=user_id,
                target_calories=plan['target_calories'],
                protein_grams=plan['target_macros']['protein'],
                carbs_grams=plan['target_macros']['carbs'],
                fats_grams=plan['target_macros']['fats'],
                plan_date=plan_date
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
                total_meals += 1
            
            total_plans += 1
            print(f"   Plan {total_plans} created for {user_data['name']} ({plan_date})")
    
    print(f"   ✅ {total_plans} diet plans created")
    print(f"   ✅ {total_meals} meals added")
    
    # Display final statistics
    print("\n📊 Database Statistics:")
    stats = db.get_statistics()
    print(f"   👥 Total Users: {stats['total_users']}")
    print(f"   📋 Total Diet Plans: {stats['total_plans']}")
    print(f"   🍽️  Total Meals: {stats['total_meals']}")
    
    print("\n" + "="*60)
    print("✅ SAMPLE DATA GENERATION COMPLETE!")
    print("="*60)
    print("\n💡 You can now run the Streamlit app to view the sample data:")
    print("   streamlit run app.py")
    print("\n📈 Navigate to 'View Data' to see all the generated information!")
    

if __name__ == "__main__":
    try:
        generate_sample_data()
    except Exception as e:
        print(f"\n❌ Error generating sample data: {e}")
        import traceback
        traceback.print_exc()
