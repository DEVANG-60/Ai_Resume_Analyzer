ROADMAP = {

    "Python": [
        "Learn Python fundamentals",
        "Practice functions, lists and dictionaries",
        "Build a small Python project"
    ],

    "SQL": [
        "Learn SQL basics",
        "Practice SELECT, JOIN and GROUP BY",
        "Work with a sample database"
    ],

    "Machine Learning": [
        "Learn supervised and unsupervised learning",
        "Study common ML algorithms",
        "Build a machine learning project"
    ],

    "Deep Learning": [
        "Learn neural network fundamentals",
        "Understand CNNs and deep learning models",
        "Build a deep learning project"
    ],

    "FastAPI": [
        "Learn FastAPI basics",
        "Create REST APIs",
        "Deploy a machine learning API"
    ],

    "Docker": [
        "Understand containers",
        "Create a Dockerfile",
        "Containerize a project"
    ],

    "TensorFlow": [
        "Learn TensorFlow basics",
        "Build neural networks",
        "Train an image or text model"
    ],

    "PyTorch": [
        "Learn PyTorch tensors",
        "Build neural networks",
        "Train a small deep learning model"
    ],

    "NLP": [
        "Learn text preprocessing",
        "Study NLP concepts",
        "Build an NLP project"
    ],

    "Transformers": [
        "Understand transformer architecture",
        "Learn attention mechanisms",
        "Use a pretrained transformer"
    ],

    "LLM": [
        "Understand large language models",
        "Learn prompting and embeddings",
        "Build a small LLM application"
    ],

    "RAG": [
        "Understand embeddings",
        "Learn vector search",
        "Build a simple RAG application"
    ],

    "AWS": [
        "Learn basic AWS services",
        "Deploy a simple application",
        "Practice cloud deployment"
    ],

    "Power BI": [
        "Learn Power BI basics",
        "Create dashboards",
        "Build a data visualization project"
    ],

    "OpenCV": [
        "Learn image processing basics",
        "Practice OpenCV functions",
        "Build a computer vision project"
    ],

    "YOLO": [
        "Understand object detection",
        "Learn YOLO fundamentals",
        "Build an object detection project"
    ],

    "Git": [
        "Learn Git commands",
        "Practice branching and merging",
        "Use GitHub for project collaboration"
    ]
}


def generate_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        if skill in ROADMAP:

            roadmap.append({
                "skill": skill,
                "steps": ROADMAP[skill]
            })

    return roadmap