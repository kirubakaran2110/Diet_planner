import streamlit as st
import pandas as pd
from datetime import date

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="💪",
    layout="centered"
)

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------
def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calorie_estimate(goal):
    if goal == "Muscle Gain":
        return 2200
    elif goal == "Weight Loss":
        return 1800
    else:
        return 2000

def macro_split(calories):
    protein = int(calories * 0.30 / 4)
    carbs = int(calories * 0.45 / 4)
    fats = int(calories * 0.25 / 9)
    return protein, carbs, fats

def fitness_tips(bmi, goal):
    tips = []
    if bmi < 18.5:
        tips.append("Increase calorie intake and avoid excessive cardio.")
    if bmi > 30:
        tips.append("Avoid high-impact workouts; focus on low-intensity cardio.")
    if goal == "Weight Loss":
        tips.append("Maintain hydration and follow a calorie deficit.")
    if goal == "Muscle Gain":
        tips.append("Ensure adequate protein intake and proper rest.")
    return tips

# --------------------------------------------------
# Workout Plan with Intensity
# --------------------------------------------------
def workout_plan(goal, level):
    intensity_factor = {"Beginner": 1, "Intermediate": 1.5, "Advanced": 2}
    f = intensity_factor[level]

    return {
        "Monday": f"Cardio + Strength\n• Squats – {int(12*f)} reps\n• Push-ups – {int(10*f)} reps\n• Walking – {int(20*f)} mins",
        "Tuesday": f"Core Workout\n• Plank – {int(30*f)} sec\n• Crunches – {int(15*f)} reps",
        "Wednesday": f"Full Body\n• Lunges – {int(12*f)} reps\n• Shoulder Press – {int(10*f)} reps",
        "Thursday": f"Cardio\n• Jogging – {int(25*f)} mins\n• Jump Rope – {int(10*f)} mins",
        "Friday": f"Strength Training\n• Squats – {int(15*f)} reps\n• Deadlifts – {int(10*f)} reps",
        "Saturday": "Active Recovery\n• Yoga – 30 mins\n• Stretching – 10 mins",
        "Sunday": "Rest Day\n• Complete Rest"
    }

# --------------------------------------------------
# Diet Plan
# --------------------------------------------------
def diet_plan(diet, budget):
    if diet == "Vegetarian":
        return [
            "Breakfast: Oats / Idli",
            "Lunch: Rice + Dal + Vegetables",
            "Dinner: Chapati + Sabzi"
        ]
    else:
        return [
            "Breakfast: Eggs",
            "Lunch: Chicken + Rice",
            "Dinner: Fish + Vegetables"
        ]

# --------------------------------------------------
# Session State for Progress Tracking
# --------------------------------------------------
if "progress" not in st.session_state:
    st.session_state.progress = []

# --------------------------------------------------
# Sidebar Inputs
# --------------------------------------------------
st.sidebar.title("👤 User Profile")

name = st.sidebar.text_input("Name")
age = st.sidebar.slider("Age", 16, 60, 21)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.slider("Height (cm)", 140, 200, 170)
weight = st.sidebar.slider("Weight (kg)", 40, 120, 65)

goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Weight Loss", "Muscle Gain", "General Fitness"]
)

level = st.sidebar.selectbox(
    "Workout Intensity Level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.sidebar.selectbox(
    "Goal Duration",
    ["4 Weeks", "8 Weeks", "12 Weeks"]
)

diet = st.sidebar.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
budget = st.sidebar.selectbox("Budget Level", ["Low", "Medium", "High"])

# --------------------------------------------------
# Main UI
# --------------------------------------------------
st.title("💪 AI-Based Personalized Workout & Diet Planner")
st.caption(f"Generated on: {date.today()}")

st.info("ℹ️ BMI progress will become meaningful after multiple weekly entries.")

if st.button("🚀 Generate Personalized Plan"):

    bmi = calculate_bmi(weight, height)
    calories = calorie_estimate(goal)
    protein, carbs, fats = macro_split(calories)
    category = bmi_category(bmi)

    # Save progress
    st.session_state.progress.append({
        "Date": date.today(),
        "Weight": weight,
        "BMI": bmi
    })

    # Health Analysis
    st.subheader("📊 Health Analysis")
    st.metric("BMI", f"{bmi:.2f}", category)

    # Workout Plan
    st.subheader("🏋️ Weekly Workout Plan (Detailed)")
    plan = workout_plan(goal, level)
    for day, details in plan.items():
        st.markdown(f"**{day}**")
        st.write(details)
        st.markdown("---")

    # Diet Plan
    st.subheader("🥗 Diet Plan")
    meals = diet_plan(diet, budget)
    for meal in meals:
        st.write("•", meal)

    # Calories & Macros
    st.subheader("🔥 Calories & Macronutrients")
    st.write(f"Calories: **{calories} kcal/day**")
    st.write(f"Protein: **{protein} g**, Carbs: **{carbs} g**, Fats: **{fats} g**")

    # Fitness Tips
    st.subheader("⚠️ Smart Fitness Tips")
    for tip in fitness_tips(bmi, goal):
        st.warning(tip)

    # BMI Progress Chart
    st.subheader("📈 BMI Progress Chart")
    df = pd.DataFrame(st.session_state.progress)
    st.line_chart(df.set_index("Date")["BMI"])

    # --------------------------------------------------
    # Download Fitness Plan
    # --------------------------------------------------
    download_text = f"""
AI PERSONALIZED FITNESS PLAN
---------------------------

Name: {name}
Age: {age}
Gender: {gender}

Height: {height} cm
Weight: {weight} kg
BMI: {bmi:.2f} ({category})

GOAL:
{goal}
Intensity Level: {level}
Goal Duration: {duration}

WEEKLY WORKOUT PLAN:
"""

    for day, details in plan.items():
        download_text += f"\n{day}:\n{details}\n"

    download_text += "\nDIET PLAN:\n"
    for meal in meals:
        download_text += f"- {meal}\n"

    download_text += f"""
DAILY CALORIES & MACROS:
Calories: {calories} kcal/day
Protein: {protein} g
Carbohydrates: {carbs} g
Fats: {fats} g

Generated On: {date.today()}
"""

    st.download_button(
        label="📥 Download This Fitness Plan",
        data=download_text,
        file_name="AI_Personalized_Fitness_Plan.txt",
        mime="text/plain"
    )

    st.success("✅ Personalized fitness plan generated successfully!")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("Internship Project | AI-Based Personalized Workout & Diet Planner (Python + Streamlit)")
