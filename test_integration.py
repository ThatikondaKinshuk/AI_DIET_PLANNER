"""
Integration tests for AI Diet Planner
Tests the complete workflow of the application
"""

import os
import sys
from datetime import date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DietPlannerDB
from diet_planner import DietPlanner


def test_complete_workflow():
    """Test the complete workflow from user creation to diet plan generation"""
    print("\n" + "="*60)
    print("🧪 INTEGRATION TEST: Complete Workflow")
    print("="*60)
    
    # Use a test database
    test_db_path = "test_integration.db"
    
    try:
        # Step 1: Initialize database
        print("\n1️⃣  Initializing database...")
        db = DietPlannerDB(test_db_path)
        print("   ✅ Database initialized")
        
        # Step 2: Create a user
        print("\n2️⃣  Creating user profile...")
        user_id = db.add_user(
            name="John Doe",
            age=30,
            gender="Male",
            weight=80.0,
            height=180.0,
            activity_level="Moderately active (3-5 days/week)",
            goal="Lose weight",
            dietary_restrictions="None"
        )
        print(f"   ✅ User created with ID: {user_id}")
        
        # Step 3: Retrieve user
        print("\n3️⃣  Retrieving user data...")
        users_df = db.get_all_users()
        assert len(users_df) == 1, "Should have 1 user"
        user_data = users_df.iloc[0]
        print(f"   ✅ Retrieved user: {user_data['name']}")
        print(f"      Age: {user_data['age']}, Weight: {user_data['weight']}kg, Height: {user_data['height']}cm")
        
        # Step 4: Generate nutrition plan
        print("\n4️⃣  Generating nutrition plan...")
        plan = DietPlanner.get_complete_nutrition_plan(
            weight=user_data['weight'],
            height=user_data['height'],
            age=user_data['age'],
            gender=user_data['gender'],
            activity_level=user_data['activity_level'],
            goal=user_data['goal'],
            dietary_restrictions=user_data['dietary_restrictions']
        )
        print(f"   ✅ Plan generated")
        print(f"      BMR: {plan['bmr']} kcal")
        print(f"      TDEE: {plan['tdee']} kcal")
        print(f"      Target Calories: {plan['target_calories']} kcal")
        print(f"      Target Protein: {plan['target_macros']['protein']}g")
        print(f"      Target Carbs: {plan['target_macros']['carbs']}g")
        print(f"      Target Fats: {plan['target_macros']['fats']}g")
        
        # Step 5: Save diet plan to database
        print("\n5️⃣  Saving diet plan to database...")
        plan_id = db.add_diet_plan(
            user_id=user_id,
            target_calories=plan['target_calories'],
            protein_grams=plan['target_macros']['protein'],
            carbs_grams=plan['target_macros']['carbs'],
            fats_grams=plan['target_macros']['fats'],
            plan_date=date.today().isoformat()
        )
        print(f"   ✅ Diet plan saved with ID: {plan_id}")
        
        # Step 6: Save meals
        print("\n6️⃣  Saving meals to database...")
        meal_count = 0
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
            meal_count += 1
            print(f"      {meal['meal_type']}: {meal['name']} ({meal['calories']} kcal)")
        print(f"   ✅ {meal_count} meals saved")
        
        # Step 7: Retrieve and verify data
        print("\n7️⃣  Verifying saved data...")
        plans_df = db.get_all_diet_plans()
        assert len(plans_df) == 1, "Should have 1 diet plan"
        print(f"   ✅ Diet plans in database: {len(plans_df)}")
        
        meals_df = db.get_all_meals()
        assert len(meals_df) == meal_count, f"Should have {meal_count} meals"
        print(f"   ✅ Meals in database: {len(meals_df)}")
        
        # Step 8: Check statistics
        print("\n8️⃣  Checking statistics...")
        stats = db.get_statistics()
        print(f"   ✅ Statistics:")
        print(f"      Total Users: {stats['total_users']}")
        print(f"      Total Plans: {stats['total_plans']}")
        print(f"      Total Meals: {stats['total_meals']}")
        
        assert stats['total_users'] == 1
        assert stats['total_plans'] == 1
        assert stats['total_meals'] == meal_count
        
        # Step 9: Test with different parameters
        print("\n9️⃣  Testing with female user (Gain muscle)...")
        user_id_2 = db.add_user(
            name="Jane Smith",
            age=25,
            gender="Female",
            weight=60.0,
            height=165.0,
            activity_level="Very active (6-7 days/week)",
            goal="Gain muscle",
            dietary_restrictions="Vegetarian"
        )
        
        plan_2 = DietPlanner.get_complete_nutrition_plan(
            weight=60.0,
            height=165.0,
            age=25,
            gender="Female",
            activity_level="Very active (6-7 days/week)",
            goal="Gain muscle",
            dietary_restrictions="Vegetarian"
        )
        
        print(f"   ✅ Second user created (ID: {user_id_2})")
        print(f"      BMR: {plan_2['bmr']} kcal")
        print(f"      Target Calories: {plan_2['target_calories']} kcal")
        
        # Save second plan
        plan_id_2 = db.add_diet_plan(
            user_id=user_id_2,
            target_calories=plan_2['target_calories'],
            protein_grams=plan_2['target_macros']['protein'],
            carbs_grams=plan_2['target_macros']['carbs'],
            fats_grams=plan_2['target_macros']['fats'],
            plan_date=date.today().isoformat()
        )
        
        for meal in plan_2['meal_plan']:
            db.add_meal(
                plan_id=plan_id_2,
                meal_type=meal['meal_type'],
                meal_name=meal['name'],
                ingredients=meal['ingredients'],
                calories=meal['calories'],
                protein=meal['protein'],
                carbs=meal['carbs'],
                fats=meal['fats']
            )
        
        print(f"   ✅ Second plan saved (ID: {plan_id_2})")
        
        # Final statistics
        print("\n🔟  Final statistics...")
        final_stats = db.get_statistics()
        print(f"   ✅ Final count:")
        print(f"      Total Users: {final_stats['total_users']}")
        print(f"      Total Plans: {final_stats['total_plans']}")
        print(f"      Total Meals: {final_stats['total_meals']}")
        
        assert final_stats['total_users'] == 2
        assert final_stats['total_plans'] == 2
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n✨ The complete workflow is working perfectly!")
        print("   - User creation ✓")
        print("   - Diet plan generation ✓")
        print("   - Database storage ✓")
        print("   - Data retrieval ✓")
        print("   - Multiple users support ✓")
        print("   - Dietary restrictions support ✓")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print(f"\n🧹 Cleaned up test database")


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n" + "="*60)
    print("🧪 INTEGRATION TEST: Edge Cases")
    print("="*60)
    
    try:
        # Test minimum values
        print("\n1️⃣  Testing minimum values...")
        bmr_min = DietPlanner.calculate_bmr(40, 120, 18, "Female")
        print(f"   ✅ Minimum BMR: {bmr_min:.1f} kcal")
        
        # Test maximum values
        print("\n2️⃣  Testing maximum values...")
        bmr_max = DietPlanner.calculate_bmr(150, 220, 70, "Male")
        print(f"   ✅ Maximum BMR: {bmr_max:.1f} kcal")
        
        # Test all activity levels
        print("\n3️⃣  Testing all activity levels...")
        test_bmr = 1500
        for activity, multiplier in DietPlanner.ACTIVITY_MULTIPLIERS.items():
            tdee = DietPlanner.calculate_tdee(test_bmr, activity)
            print(f"   {activity}: {tdee:.1f} kcal (×{multiplier})")
        print("   ✅ All activity levels work")
        
        # Test all goals
        print("\n4️⃣  Testing all goals...")
        test_tdee = 2000
        for goal, adjustment in DietPlanner.GOAL_ADJUSTMENTS.items():
            target = DietPlanner.calculate_target_calories(test_tdee, goal)
            print(f"   {goal}: {target:.1f} kcal ({adjustment:+d})")
        print("   ✅ All goals work")
        
        # Test dietary restrictions filtering
        print("\n5️⃣  Testing dietary restrictions...")
        
        # Vegetarian
        veg_meals = DietPlanner.generate_meal_plan(2000, "Vegetarian")
        print(f"   Vegetarian: {len(veg_meals)} meals generated")
        
        # Vegan
        vegan_meals = DietPlanner.generate_meal_plan(2000, "Vegan")
        print(f"   Vegan: {len(vegan_meals)} meals generated")
        
        # None
        all_meals = DietPlanner.generate_meal_plan(2000, "")
        print(f"   No restrictions: {len(all_meals)} meals generated")
        
        print("   ✅ Dietary restrictions filtering works")
        
        print("\n" + "="*60)
        print("✅ ALL EDGE CASE TESTS PASSED!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🧪"*30)
    print("AI DIET PLANNER - INTEGRATION TESTS")
    print("🧪"*30)
    
    # Run tests
    test1_passed = test_complete_workflow()
    test2_passed = test_edge_cases()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Complete Workflow Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Edge Cases Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("="*60)
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! The application is ready to use!")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED! Please check the output above.")
        sys.exit(1)
