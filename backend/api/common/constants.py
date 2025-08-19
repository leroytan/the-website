# Note: For SMU, the pattern is <user>@<school>.smu.edu.sg.
# A regex is used to match any subdomain under smu.edu.sg.
AUTONOMOUS_UNIVERSITIES_EMAIL_DOMAINS = [
    "u.nus.edu",
    "student.main.ntu.edu.sg",
    "e.ntu.edu.sg",
    r".+\.smu\.edu\.sg$",  # SMU pattern
    "sit.edu.sg",
    "suss.edu.sg",
    "sutd.edu.sg",
]
