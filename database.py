"""
Database module for AI Diet Planner
Handles all database operations including user profiles, diet plans, and meals
"""

import sqlite3
from datetime import datetime
import pandas as pd
from typing import Optional, List, Dict, Any


class DietPlannerDB:
    """Database manager for the AI Diet Planner application"""
    
    def __init__(self, db_path: str = "diet_planner.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                activity_level TEXT NOT NULL,
                goal TEXT NOT NULL,
                dietary_restrictions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Diet plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diet_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                target_calories REAL NOT NULL,
                protein_grams REAL NOT NULL,
                carbs_grams REAL NOT NULL,
                fats_grams REAL NOT NULL,
                plan_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Meals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                meal_type TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fats REAL NOT NULL,
                FOREIGN KEY (plan_id) REFERENCES diet_plans (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_user(self, name: str, age: int, gender: str, weight: float, 
                 height: float, activity_level: str, goal: str, 
                 dietary_restrictions: str = "") -> int:
        """Add a new user to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (name, age, gender, weight, height, 
                             activity_level, goal, dietary_restrictions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, gender, weight, height, activity_level, goal, 
              dietary_restrictions))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def add_diet_plan(self, user_id: int, target_calories: float, 
                     protein_grams: float, carbs_grams: float, 
                     fats_grams: float, plan_date: str) -> int:
        """Add a new diet plan to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO diet_plans (user_id, target_calories, protein_grams,
                                   carbs_grams, fats_grams, plan_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, target_calories, protein_grams, carbs_grams, 
              fats_grams, plan_date))
        
        plan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return plan_id
    
    def add_meal(self, plan_id: int, meal_type: str, meal_name: str,
                ingredients: str, calories: float, protein: float,
                carbs: float, fats: float):
        """Add a meal to a diet plan"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO meals (plan_id, meal_type, meal_name, ingredients,
                             calories, protein, carbs, fats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (plan_id, meal_type, meal_name, ingredients, calories, 
              protein, carbs, fats))
        
        conn.commit()
        conn.close()
    
    def get_all_users(self) -> pd.DataFrame:
        """Get all users as a DataFrame"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM users ORDER BY created_at DESC", conn)
        conn.close()
        return df
    
    def get_all_diet_plans(self) -> pd.DataFrame:
        """Get all diet plans with user information"""
        conn = self.get_connection()
        query = """
            SELECT 
                dp.id,
                u.name as user_name,
                dp.target_calories,
                dp.protein_grams,
                dp.carbs_grams,
                dp.fats_grams,
                dp.plan_date,
                dp.created_at
            FROM diet_plans dp
            JOIN users u ON dp.user_id = u.id
            ORDER BY dp.created_at DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_all_meals(self) -> pd.DataFrame:
        """Get all meals with plan information"""
        conn = self.get_connection()
        query = """
            SELECT 
                m.id,
                u.name as user_name,
                m.meal_type,
                m.meal_name,
                m.ingredients,
                m.calories,
                m.protein,
                m.carbs,
                m.fats
            FROM meals m
            JOIN diet_plans dp ON m.plan_id = dp.id
            JOIN users u ON dp.user_id = u.id
            ORDER BY m.id DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_user_diet_plans(self, user_id: int) -> pd.DataFrame:
        """Get all diet plans for a specific user"""
        conn = self.get_connection()
        query = """
            SELECT * FROM diet_plans 
            WHERE user_id = ?
            ORDER BY created_at DESC
        """
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        return df
    
    def get_plan_meals(self, plan_id: int) -> pd.DataFrame:
        """Get all meals for a specific diet plan"""
        conn = self.get_connection()
        query = """
            SELECT * FROM meals 
            WHERE plan_id = ?
            ORDER BY meal_type
        """
        df = pd.read_sql_query(query, conn, params=(plan_id,))
        conn.close()
        return df
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = cursor.fetchone()[0]
        
        # Total diet plans
        cursor.execute("SELECT COUNT(*) FROM diet_plans")
        stats['total_plans'] = cursor.fetchone()[0]
        
        # Total meals
        cursor.execute("SELECT COUNT(*) FROM meals")
        stats['total_meals'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
