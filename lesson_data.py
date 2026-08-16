# lesson_data.py
lessons_content = {
    "cs": [
        {
            "id": 1,
            "title": "Intro to Computing",
            "model_type": "computer",
            "pdf": "cs_intro.pdf",
            "video": "https://www.youtube.com/embed/tpIctyqH29Q",  # Computer Science Introduction (CrashCourse)
            "reading_text": "Introduction to the fundamentals of computing and computer systems.",
            "model_url": "https://visualgo.net/en/array?slide=1"
        },
        {
            "id": 2,
            "title": "Programming Basics",
            "model_type": "code",
            "pdf": "cs_programming.pdf",
            "video": "https://www.youtube.com/embed/8PopR3x-VMY",  # Programming Basics (CrashCourse)
            "reading_text": "Learn the basics of programming and algorithmic thinking.",
            "model_url": "https://visualgo.net/en/recursion?slide=1"
        },
        {
            "id": 3,
            "title": "Data Structures",
            "model_type": "data",
            "pdf": "cs_data_structures.pdf",
            "video": "https://www.youtube.com/embed/DuDz6B4cqVc",  # Data Structures (CrashCourse)
            "reading_text": "Understanding fundamental data structures like arrays, lists, and trees.",
            "model_url": "https://visualgo.net/en/list?slide=1"
        },
        {
            "id": 4,
            "title": "Sorting Algorithms",
            "model_type": "sorting",
            "pdf": "cs_sorting.pdf",
            "video": "https://www.youtube.com/embed/es2T6KY45cA",  # Sorting Algorithms
            "reading_text": "Learn about different sorting algorithms like bubble sort, quick sort, and merge sort.",
            "model_url": "https://visualgo.net/en/sorting?slide=1"
        },
        {
            "id": 5,
            "title": "Search Algorithms",
            "model_type": "search",
            "pdf": "cs_searching.pdf",
            "video": "https://www.youtube.com/embed/P3YID7liBug",  # Search Algorithms
            "reading_text": "Understanding search algorithms like binary search and depth-first search.",
            "model_url": "https://visualgo.net/en/bst"
        },
        {
            "id": 6,
            "title": "Graph Algorithms",
            "model_type": "data",
            "pdf": "cs_graph_algorithms.pdf",
            "video": "https://www.youtube.com/embed/RpgyCJBbl5E?si=fsBCGL-YuoIbEhp-",  # Graph Algorithms
            "reading_text": "Learn about graph algorithms like shortest path and minimum spanning tree.",
            "model_url": "https://visualgo.net/en/graphds"
        }
    ],
    "ai": [
        {
            "id": 1,
            "title": "Machine Learning Intro",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/R9OHn5ZF4Uo",  # Machine Learning (StatQuest)
            "reading_text": "Introduction to machine learning concepts and algorithms.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 2,
            "title": "Neural Networks",
            "model_type": "ai",
            "pdf": "ai_neural_networks.pdf",
            "video": "https://www.youtube.com/embed/aircAruvnKk",  # Neural Networks
            "reading_text": "Learn about artificial neural networks and deep learning.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 3,
            "title": "Natural Language Processing",
            "model_type": "ai",
            "pdf": "ai_nlp.pdf",
            "video": "https://www.youtube.com/embed/fOvTtapxa9c",  # Natural Language Processing
            "reading_text": "Understanding how computers process and understand human language.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 4,
            "title": "Computer Vision",
            "model_type": "ai",
            "pdf": "ai_computer_vision.pdf",
            "video": "https://www.youtube.com/embed/vxuCLe5DcBo",  # Computer Vision
            "reading_text": "Learn how computers interpret and understand visual information.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 5,
            "title": "Reinforcement Learning",
            "model_type": "ai",
            "pdf": "ai_reinforcement.pdf",
            "video": "https://www.youtube.com/embed/KHZVXao4qXs",  # Reinforcement Learning
            "reading_text": "Study of how agents learn to make decisions through trial and error.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 6,
            "title": "Coming Soon",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/JMUxmLyrhSk",  # Placeholder
            "reading_text": "More AI lessons coming soon.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        }
    ],
    # New CSE course
    "cse": [
        {
            "id": 1,
            "title": "Computer Architecture",
            "model_type": "computer",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/GRInNLx3Tug",  # Computer Architecture
            "reading_text": "Understanding computer organization, processors, and system design.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        {
            "id": 2,
            "title": "Operating Systems",
            "model_type": "computer",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/26QPDBe-NB8",  # Operating Systems
            "reading_text": "Learn about OS concepts, processes, memory management, and file systems.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        {
            "id": 3,
            "title": "Database Systems",
            "model_type": "data",
            "pdf": "ai_computer_vision.pdf",
            "video": "https://www.youtube.com/embed/HXV3zeQKqGY",  # Database Systems
            "reading_text": "Study of database design, SQL, and data management systems.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        {
            "id": 4,
            "title": "Computer Networks",
            "model_type": "network",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/k2th3OQCzFc",  # Computer Networks
            "reading_text": "Understanding network protocols, security, and distributed systems.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        {
            "id": 5,
            "title": "Software Engineering",
            "model_type": "code",
            "pdf": "ai_computer_vision.pdf",
            "video": "https://www.youtube.com/embed/0P0Lh_8gbXU",  # Software Engineering
            "reading_text": "Learn software development lifecycle, design patterns, and project management.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        },
        {
            "id": 6,
            "title": "Cybersecurity",
            "model_type": "security",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/SLQ4i_Zg5Vw",  # Cybersecurity
            "reading_text": "Study of security principles, cryptography, and threat protection.",
            "model_url": "https://threejs.org/examples/#webgl_physics_cloth"
        }
    ],
    # New AI/ML course
    "aiml": [
        {
            "id": 1,
            "title": "Supervised Learning",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/F6GSRDoB-CY",  # Supervised Learning
            "reading_text": "Introduction to supervised learning algorithms and regression techniques.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 2,
            "title": "Unsupervised Learning",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/eVplCoae1Pk",  # Unsupervised Learning
            "reading_text": "Learn clustering, dimensionality reduction, and anomaly detection.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 3,
            "title": "Deep Learning Fundamentals",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/n1l-9lIMD7U",  # Deep Learning
            "reading_text": "Understanding neural networks, backpropagation, and deep architectures.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 4,
            "title": "Natural Language Processing",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/fOvTtapxa9c",  # NLP (same as AI course)
            "reading_text": "Study of text processing, language models, and transformer architectures.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 5,
            "title": "Computer Vision",
            "model_type": "ai",
            "pdf": "ai_computer_vision.pdf",
            "video": "https://www.youtube.com/embed/vxuCLe5DcBo",  # Computer Vision (same as AI course)
            "reading_text": "Learn image processing, convolutional networks, and object detection.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        },
        {
            "id": 6,
            "title": "Reinforcement Learning",
            "model_type": "ai",
            "pdf": "ai_ml_intro.pdf",
            "video": "https://www.youtube.com/embed/KHZVXao4qXs",  # Reinforcement Learning (same as AI course)
            "reading_text": "Advanced study of RL algorithms, policy gradients, and applications.",
            "model_url": "https://threejs.org/examples/#webgl_neural_networks"
        }
    ]
}