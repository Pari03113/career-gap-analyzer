
import streamlit as st
import pandas as pd

# Step 1: Load job-to-skill data from CSV
@st.cache_data
def load_job_skill_data():
    df = pd.read_csv("onet_job_skills.csv")
    return df

# Load the data
job_skill_df = load_job_skill_data()
job_titles = sorted(job_skill_df["Job Title"].unique().tolist())

st.title("📊 Skill Gap Report Generator (Real O*NET Data)")
st.write("Enter your skills and compare them with the skills required for a real job.")

# Step 2: Let user input their own skills
user_input = st.text_area("Enter your skills (comma-separated)", "communication, python, teamwork")

# Step 3: Let user select a job title
selected_job = st.selectbox("Select a target job title", job_titles)

if st.button("Generate Report"):
    # Step 4: Normalize inputs
    user_skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]
    required_skills = job_skill_df[job_skill_df["Job Title"] == selected_job]["Skill"].str.lower().tolist()

    # Step 5: Compare
    matched = [skill for skill in user_skills if skill in required_skills]
    missing = [skill for skill in required_skills if skill not in user_skills]
    match_percent = int((len(matched) / len(required_skills)) * 100) if required_skills else 0

    # Step 6: Show results
    st.subheader("✅ Matched Skills")
    st.write(matched if matched else "No matches found.")

    st.subheader("❌ Missing Skills")
    st.write(missing if missing else "None! You’re a perfect match!")

    st.markdown(f"**📈 Match Score:** {match_percent}%")

    # Step 7: Allow CSV download of results
    df = pd.DataFrame({
        "Your Skill": user_skills + [""] * (len(missing) - len(user_skills)) if len(user_skills) < len(missing) else user_skills,
        "Missing Skill": missing + [""] * (len(user_skills) - len(missing)) if len(missing) < len(user_skills) else missing
    })

    st.download_button(
        label="📥 Download Skill Gap Report as CSV",
        data=df.to_csv(index=False),
        file_name="skill_gap_report.csv",
        mime="text/csv"
    )
