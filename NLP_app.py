# main.py
from Recommender.resume_parser import parse_resume
from Recommender.match_jobs import find_matching_jobs

resume_path = "./Selected_Data/sample_resumes/resume2.pdf"
job_data_path = "./Selected_Data/under_100mb.csv"

print("📄 Parsing resume...")
resume_data = parse_resume(resume_path)
print("✅ Resume Data:", resume_data)

print("\n🔍 Finding matching jobs...")
matches = find_matching_jobs(resume_data["skills"], job_data_path)
print("✅ Top Jobs:\n", matches)
