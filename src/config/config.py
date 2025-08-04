from dataclasses import dataclass, field

@dataclass
class Config:
    data_folder: str = '../../data'
    index_path: str = '../../models/faiss.index'
    meta_path: str = '../../models/texts.pkl'
    model_path: str = '../../models'
    emotion_labels: list = field(default_factory=lambda: ["sadness", "grief", "fear", "remorse", "disappointment", "nervousness", "embarrassment"])
    intent_labels: list = field(default_factory=lambda: [
        "Course Information",
        "Enrollment / Course Registration",
        "Withdrawal or Drop Course",
        "Access Issues (portal/login)",
        "Technical Support",
        "Tuition/Fees Inquiry",
        "Scholarship/Financial Aid",
        "Mental Health Concerns",
        "Stress or Burnout",
        "Bullying or Harassment",
        "Administrative Support",
        "Campus Facilities",
        "Housing/Accommodation",
        "Extracurricular Activities",
        "General Complaint"
    ])
