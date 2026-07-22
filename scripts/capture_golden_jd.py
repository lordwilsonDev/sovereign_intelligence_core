import json, sys
sys.path.insert(0, '/Users/lordwilson/msb-v2')
from cognitive_compiler.career_harness_v1 import CareerHarness

harness = CareerHarness()
golden = []

samples = [
    "Senior Python developer with 5+ years in cloud infrastructure and Kubernetes",
    "Entry-level data analyst proficient in Excel and SQL",
    "Staff Security Engineer at CloudCorp working on zero-trust architecture",
    "VP Engineering leading 3 teams with Python and microservices",
    "Principal Researcher in NLP with PyTorch and transformers",
    "Junior Backend Engineer - remote - Go and gRPC",
    "Product Manager with 3 years in developer tools and roadmap strategy",
    "Infrastructure Engineer - Kubernetes, Terraform, AWS",
    "AI Safety Researcher - PhD preferred - alignment and interpretability",
    "Full-stack engineer: React, Node.js, PostgreSQL, remote",
    "Senior ML Engineer at Acme - PyTorch, deep learning, MLOps",
    "Data Scientist - statistics, Python, A/B testing, experiments",
    "DevOps Lead - CI/CD, Docker, Kubernetes, GitHub Actions",
    "Frontend Developer - React, TypeScript, CSS-in-JS, design systems",
    "Engineering Manager - remote - people ops, hiring, agile",
    "Site Reliability Engineer - on-call, monitoring, SLI/SLO, incident response",
    "Research Scientist - NLP - LLMs, RLHF, scalable training",
    "Software Engineer 2 - mid-level - backend APIs, REST, auth",
    "Senior Platform Engineer - hybrid - Terraform, AWS, Python",
    "Director of Engineering - 10+ years - enterprise SaaS",
]

for text in samples:
    result = harness._parse_jd(text, fallback_company="Unknown", fallback_role="Unknown")
    golden.append({
        "input": text,
        "output": {
            "company": result.company,
            "role": result.role,
            "skills": result.skills,
            "requirements": result.requirements,
            "responsibilities": result.responsibilities,
            "seniority": result.seniority,
            "remote": result.remote,
        }
    })

with open("/Users/lordwilson/msb-v2/golden_jd.json", "w") as f:
    json.dump(golden, f, indent=2)
print(f"Captured {len(golden)} golden samples.")
