-- NutriSense AI SQLite schema
-- Used by src/database/connection.py

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    height_cm REAL,
    weight_kg REAL,
    goal TEXT,
    daily_calorie_goal INTEGER,
    email TEXT,
    password_hash TEXT,
    dietary_preference TEXT DEFAULT 'None',
    allergies TEXT DEFAULT '',
    medical_conditions TEXT DEFAULT '',
    activity_level TEXT DEFAULT 'Moderate',
    created_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_type TEXT,
    target_calories INTEGER,
    activity_level TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals(user_id);

CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_name TEXT NOT NULL,
    meal_type TEXT,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    confidence REAL,
    health_score INTEGER,
    image_name TEXT,
    analysis_date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_meals_user_date ON meals(user_id, analysis_date);

CREATE TABLE IF NOT EXISTS nutrition_foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT NOT NULL,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    category TEXT,
    serving_size TEXT,
    UNIQUE(food_name)
);

CREATE INDEX IF NOT EXISTS idx_nutrition_foods_name ON nutrition_foods(food_name);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_prefs_user_key ON user_preferences(user_id, key);


