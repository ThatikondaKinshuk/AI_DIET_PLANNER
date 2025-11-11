"""
Diet Planning Logic for AI Diet Planner
Calculates calories, macronutrients, and generates meal plans
"""

import random
from typing import Dict, List, Tuple
from datetime import datetime


class DietPlanner:
    """AI-powered diet planning engine"""
    
    # Activity level multipliers for BMR
    ACTIVITY_MULTIPLIERS = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Extremely active (physical job)": 1.9
    }
    
    # Goal adjustments (calories)
    GOAL_ADJUSTMENTS = {
        "Lose weight": -500,
        "Maintain weight": 0,
        "Gain muscle": 300
    }
    
    # Sample meal database with nutritional info
    MEAL_DATABASE = {
        "Breakfast": [
            {
                "name": "Oatmeal with Berries and Nuts",
                "ingredients": "1 cup oats, 1/2 cup mixed berries, 1 tbsp almonds, 1 tsp honey",
                "calories": 350,
                "protein": 12,
                "carbs": 55,
                "fats": 8
            },
            {
                "name": "Greek Yogurt Parfait",
                "ingredients": "1 cup Greek yogurt, 1/2 cup granola, 1/2 cup mixed berries",
                "calories": 320,
                "protein": 20,
                "carbs": 45,
                "fats": 6
            },
            {
                "name": "Scrambled Eggs with Whole Wheat Toast",
                "ingredients": "3 eggs, 2 slices whole wheat bread, 1 tsp butter, vegetables",
                "calories": 380,
                "protein": 25,
                "carbs": 35,
                "fats": 15
            },
            {
                "name": "Protein Smoothie Bowl",
                "ingredients": "1 banana, 1 scoop protein powder, 1/2 cup berries, toppings",
                "calories": 340,
                "protein": 28,
                "carbs": 48,
                "fats": 5
            },
            {
                "name": "Avocado Toast with Egg",
                "ingredients": "2 slices whole grain bread, 1/2 avocado, 2 eggs, seasonings",
                "calories": 420,
                "protein": 20,
                "carbs": 38,
                "fats": 22
            }
        ],
        "Lunch": [
            {
                "name": "Grilled Chicken Salad",
                "ingredients": "150g chicken breast, mixed greens, cherry tomatoes, olive oil dressing",
                "calories": 380,
                "protein": 40,
                "carbs": 15,
                "fats": 18
            },
            {
                "name": "Quinoa Buddha Bowl",
                "ingredients": "1 cup quinoa, chickpeas, roasted vegetables, tahini dressing",
                "calories": 450,
                "protein": 18,
                "carbs": 60,
                "fats": 15
            },
            {
                "name": "Turkey Sandwich with Side Salad",
                "ingredients": "Whole wheat bread, turkey breast, vegetables, side salad",
                "calories": 420,
                "protein": 32,
                "carbs": 45,
                "fats": 12
            },
            {
                "name": "Salmon with Sweet Potato",
                "ingredients": "150g salmon, 1 medium sweet potato, steamed broccoli",
                "calories": 480,
                "protein": 38,
                "carbs": 42,
                "fats": 18
            },
            {
                "name": "Chicken Stir-Fry with Brown Rice",
                "ingredients": "150g chicken, mixed vegetables, 1 cup brown rice, soy sauce",
                "calories": 520,
                "protein": 42,
                "carbs": 58,
                "fats": 12
            }
        ],
        "Dinner": [
            {
                "name": "Baked Salmon with Vegetables",
                "ingredients": "200g salmon, roasted vegetables, quinoa",
                "calories": 520,
                "protein": 45,
                "carbs": 35,
                "fats": 22
            },
            {
                "name": "Lean Beef Stir-Fry",
                "ingredients": "150g lean beef, mixed vegetables, brown rice",
                "calories": 480,
                "protein": 38,
                "carbs": 45,
                "fats": 16
            },
            {
                "name": "Grilled Chicken with Roasted Vegetables",
                "ingredients": "200g chicken breast, roasted vegetables, olive oil",
                "calories": 450,
                "protein": 48,
                "carbs": 25,
                "fats": 18
            },
            {
                "name": "Turkey Meatballs with Whole Wheat Pasta",
                "ingredients": "Turkey meatballs, whole wheat pasta, marinara sauce",
                "calories": 510,
                "protein": 40,
                "carbs": 52,
                "fats": 14
            },
            {
                "name": "Tofu and Vegetable Curry",
                "ingredients": "200g tofu, mixed vegetables, coconut milk, brown rice",
                "calories": 460,
                "protein": 22,
                "carbs": 55,
                "fats": 18
            }
        ],
        "Snacks": [
            {
                "name": "Apple with Almond Butter",
                "ingredients": "1 medium apple, 2 tbsp almond butter",
                "calories": 220,
                "protein": 6,
                "carbs": 28,
                "fats": 10
            },
            {
                "name": "Protein Shake",
                "ingredients": "1 scoop protein powder, 1 cup almond milk, 1 banana",
                "calories": 250,
                "protein": 25,
                "carbs": 32,
                "fats": 3
            },
            {
                "name": "Greek Yogurt with Honey",
                "ingredients": "1 cup Greek yogurt, 1 tbsp honey",
                "calories": 180,
                "protein": 18,
                "carbs": 24,
                "fats": 2
            },
            {
                "name": "Mixed Nuts and Berries",
                "ingredients": "1/4 cup mixed nuts, 1/2 cup berries",
                "calories": 200,
                "protein": 6,
                "carbs": 20,
                "fats": 12
            },
            {
                "name": "Hummus with Vegetables",
                "ingredients": "1/4 cup hummus, carrot and cucumber sticks",
                "calories": 150,
                "protein": 6,
                "carbs": 18,
                "fats": 7
            }
        ]
    }
    
    @staticmethod
    def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        weight in kg, height in cm
        """
        if gender.lower() == "male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        return bmr
    
    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        multiplier = DietPlanner.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
        return bmr * multiplier
    
    @staticmethod
    def calculate_target_calories(tdee: float, goal: str) -> float:
        """Calculate target calories based on goal"""
        adjustment = DietPlanner.GOAL_ADJUSTMENTS.get(goal, 0)
        return tdee + adjustment
    
    @staticmethod
    def calculate_macros(target_calories: float, goal: str) -> Dict[str, float]:
        """
        Calculate macronutrient distribution
        Returns grams of protein, carbs, and fats
        """
        if goal == "Lose weight":
            # Higher protein, moderate carbs, moderate fats
            protein_ratio = 0.35
            carbs_ratio = 0.35
            fats_ratio = 0.30
        elif goal == "Gain muscle":
            # High protein, higher carbs, moderate fats
            protein_ratio = 0.30
            carbs_ratio = 0.45
            fats_ratio = 0.25
        else:  # Maintain weight
            # Balanced macros
            protein_ratio = 0.30
            carbs_ratio = 0.40
            fats_ratio = 0.30
        
        # Convert calorie ratios to grams
        # Protein: 4 cal/g, Carbs: 4 cal/g, Fats: 9 cal/g
        protein_grams = (target_calories * protein_ratio) / 4
        carbs_grams = (target_calories * carbs_ratio) / 4
        fats_grams = (target_calories * fats_ratio) / 9
        
        return {
            "protein": round(protein_grams, 1),
            "carbs": round(carbs_grams, 1),
            "fats": round(fats_grams, 1)
        }
    
    @staticmethod
    def generate_meal_plan(target_calories: float, dietary_restrictions: str = "") -> List[Dict]:
        """
        Generate a daily meal plan
        Returns list of meals with nutritional information
        """
        meals = []
        total_calories = 0
        
        # Calorie distribution: Breakfast 25%, Lunch 35%, Dinner 30%, Snacks 10%
        target_breakfast = target_calories * 0.25
        target_lunch = target_calories * 0.35
        target_dinner = target_calories * 0.30
        target_snacks = target_calories * 0.10
        
        targets = {
            "Breakfast": target_breakfast,
            "Lunch": target_lunch,
            "Dinner": target_dinner,
            "Snacks": target_snacks
        }
        
        # Filter meals based on dietary restrictions
        dietary_lower = dietary_restrictions.lower()
        
        for meal_type, target in targets.items():
            available_meals = DietPlanner.MEAL_DATABASE[meal_type].copy()
            
            # Simple filtering based on dietary restrictions
            if "vegetarian" in dietary_lower or "vegan" in dietary_lower:
                available_meals = [
                    m for m in available_meals 
                    if not any(word in m["ingredients"].lower() 
                             for word in ["chicken", "beef", "turkey", "salmon", "egg"])
                ]
            
            if "vegan" in dietary_lower:
                available_meals = [
                    m for m in available_meals 
                    if not any(word in m["ingredients"].lower() 
                             for word in ["yogurt", "honey", "egg"])
                ]
            
            # If no meals available after filtering, use original list
            if not available_meals:
                available_meals = DietPlanner.MEAL_DATABASE[meal_type]
            
            # Select meal closest to target calories
            selected_meal = min(
                available_meals,
                key=lambda m: abs(m["calories"] - target)
            )
            
            meals.append({
                "meal_type": meal_type,
                **selected_meal
            })
            total_calories += selected_meal["calories"]
        
        return meals
    
    @staticmethod
    def get_complete_nutrition_plan(weight: float, height: float, age: int,
                                   gender: str, activity_level: str, goal: str,
                                   dietary_restrictions: str = "") -> Dict:
        """
        Get complete nutrition plan with calculations and meal suggestions
        """
        # Calculate BMR and TDEE
        bmr = DietPlanner.calculate_bmr(weight, height, age, gender)
        tdee = DietPlanner.calculate_tdee(bmr, activity_level)
        target_calories = DietPlanner.calculate_target_calories(tdee, goal)
        
        # Calculate macros
        macros = DietPlanner.calculate_macros(target_calories, goal)
        
        # Generate meal plan
        meal_plan = DietPlanner.generate_meal_plan(target_calories, dietary_restrictions)
        
        # Calculate actual totals from meal plan
        actual_calories = sum(meal["calories"] for meal in meal_plan)
        actual_protein = sum(meal["protein"] for meal in meal_plan)
        actual_carbs = sum(meal["carbs"] for meal in meal_plan)
        actual_fats = sum(meal["fats"] for meal in meal_plan)
        
        return {
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "target_calories": round(target_calories, 1),
            "target_macros": macros,
            "meal_plan": meal_plan,
            "actual_totals": {
                "calories": round(actual_calories, 1),
                "protein": round(actual_protein, 1),
                "carbs": round(actual_carbs, 1),
                "fats": round(actual_fats, 1)
            }
        }
