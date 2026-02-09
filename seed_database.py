"""
Database seeding script for LJCourses platform
Populates all tables with comprehensive sample data
"""
from datetime import datetime, timedelta
from app.db import SessionLocal, engine
from app.models import Base, User, UserRole, Instructor, Category, Course, Lesson, Enrollment, LessonProgress

def clear_database(db):
    """Clear all data from tables"""
    print("Clearing existing data...")
    db.query(LessonProgress).delete()
    db.query(Enrollment).delete()
    db.query(Lesson).delete()
    db.query(Course).delete()
    db.query(Category).delete()
    db.query(Instructor).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Database cleared")

def seed_categories(db):
    """Create course categories"""
    print("\nSeeding categories...")
    categories_data = [
        {"name": "Development", "slug": "development"},
        {"name": "Design", "slug": "design"},
        {"name": "Marketing", "slug": "marketing"},
        {"name": "Business", "slug": "business"},
        {"name": "Data Science", "slug": "data-science"},
        {"name": "Cybersecurity", "slug": "cybersecurity"},
        {"name": "Cloud Computing", "slug": "cloud-computing"},
        {"name": "Artificial Intelligence", "slug": "artificial-intelligence"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories.append(category)
        print(f"  ✓ Category: {cat_data['name']}")
    
    db.commit()
    return categories

def seed_instructors(db):
    """Create instructors"""
    print("\nSeeding instructors...")
    instructors_data = [
        {
            "name": "Mark Smith",
            "designation": "Senior Software Engineer",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAlkpJJ7d0FdGr9XIpfzJfWhIPr_4QHihksGmabJ_m86JU8NGf9Ow42-cPSeGhqmNWjZiFlLGeindj29H6a_YgKsEB85BCNR3-tAl2Wodp8Vl2vKbGIZpnDTxDMfosV1roqK_jLzq7UffuyJFPf6-iB2ynIJy2r3cyJZXF_W4onIYkgSmtGY1cqHtd3S9n1UYlLhrCtXbh94bRWuuo2SbFd0tAomDHm5X6e37ZWm89g7mGtpMsfgqytcyWA0I9FlNd5zt51KALIHi5g"
        },
        {
            "name": "Jane Doe",
            "designation": "UX/UI Design Lead",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAvIrD0p-ycWWNRZOtFFZGJetTvYYstm8aXLjPezKxndjMtIXvb_1MQYpx8ZQFN8LuCr4NHqU0BvVfggnQiLgbh-yH6gCxUjgaIBZlHCvGdaRHotuO14WocdL8uiq-uHpxMsZQYnbjpdWOpi4yrLOKh6gbZzv2MFpwsKjs5At_KVqdKkFBTi1X97OkKN0cCNpoIHuamDHFldBrIvGVJU2cOXa-uLejDTU1kYz_GAeqOAuozFFsw7FkNjECsM3Va3Wdg0dqGTD6PSw-8"
        },
        {
            "name": "Sarah Lee",
            "designation": "Digital Marketing Strategist",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDot6MLYqfV3TM91Mv8odBHOsmu-cgUSlpgGzxbsefum48jp8sTvNqHAH8s8vivpFcDXXf8lO40o0Hx7AdMM50hHnn5P7F4MEeNXJ0aF3cxC2xHyYwXPybebHA6BoRVHsk-aDif2NeY3USc19fwOtYM1BfJK1PdAOOmVbtPT0P1cBO3Sh4YT8VOwgFmLZdBLULR0aEFPDRwLOkPHlrIzhnOoW3d0eDCNVPYuJzjq7UKE5VKdDL_FirxmRZzFKkRwbTmbr3mUcdr_MmO"
        },
        {
            "name": "Dr. Michael Chen",
            "designation": "Data Science Professor",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuBOT7ruXGa4mPXkM7RZv1eHNF0L9Lh1M5j5wHYllhqgeHVT5qlyA5g8daYxFxj1SGfc-TLf61YNf2Q-xcPDVDhtW5xSPWoX5BZjA84lzBYwp5BnwpMcLHaRtkO-TP-5HUZGNLqj-5EJBOtDwHNCn_dgyODzVxkpQ76jgRoKsPVxuQ6iEqp6sxvCmbUaMmztn9t2KRT_rZKjOMDryfrEd86Ic49CNiwxqOU0FIwQXz5Axpl9r-EH8laGE1eH2iUqgou1MQanXQqdA0vF"
        },
        {
            "name": "Emily Rodriguez",
            "designation": "Cybersecurity Expert",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuC0lV7tqekBg4oXdYzqMWjMAiakfj5GhwVmZrKwtTUnJniqKqJJZ8TaTx9Kh8GBKvf0Akh1YRsVDDlW3B8lLRphkj7NqKPf-fhOj8wZXOOtf8kkYIhP9F-Bq5_og9S6aN_gj71ZKoGVG8h-otjcEW-AK53unZbaWCLfb1y77reKLOt77h7Bv8MvmtOQ_clpBXtA_2vA1Y8L7Gh_hmS5VI2P1eisI-3icvwZYwgbf-g_I7PeR6_VV4Uvr92CmQHAvVPX3Tbp4YZmIROl"
        },
        {
            "name": "David Kim",
            "designation": "Cloud Solutions Architect",
            "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuC_5sX3qZ7Y8v9w0x1y2z3A4b5c6d7e8f9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p1q2r3s4t5u6v7w8x9y0z1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x"
        }
    ]
    
    instructors = []
    for instr_data in instructors_data:
        instructor = Instructor(**instr_data)
        db.add(instructor)
        instructors.append(instructor)
        print(f"  ✓ Instructor: {instr_data['name']} - {instr_data['designation']}")
    
    db.commit()
    return instructors

def seed_courses(db, categories, instructors):
    """Create courses with detailed information"""
    print("\nSeeding courses...")
    
    # Map categories by slug for easy access
    cat_map = {cat.slug: cat for cat in categories}
    
    courses_data = [
        {
            "instructor": instructors[0],  # Mark Smith
            "category": cat_map["development"],
            "title": "Full Stack Web Development Bootcamp",
            "slug": "full-stack-web-development-bootcamp",
            "small_description": "Master HTML, CSS, JS, Node, and React in this comprehensive bootcamp.",
            "description": "Become a professional web developer with this comprehensive, hands-on bootcamp designed for modern careers. Learn everything from front-end to back-end development.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuDCuGlOlzueSusvOq36Aj5zyle2UQNw2twth3Bn450cLuYGpPIbrVQ2YaP1TGKY17yZO415RV4m10lNFPTiJM5pwKKGhJHaFe93drzj19j5E5vXJxEpX3LGyC_ToB_VHhTOunMCSBkazy2QiORuri0vNQvsqD8aigZd7BM-ogm7ApKJwdlCr_muljiFnMfxVGTgv5OR-91Eetosub6--k7lm6oHisOJ7rImY7f2SVDiMavAYf5dFET2oWPXja6YKLdEHXd6Ic0f4h2q",
            "duration_hours": 12.5,
            "difficulty_level": "Beginner to Pro",
            "rating": 4.9,
            "course_purpose": "This course is meticulously designed to bridge the gap between theoretical computer science concepts and practical, job-ready skills. Whether you are looking to switch careers into tech or upgrade your current skill set, this bootcamp provides a structured path to mastering full-stack web development.",
            "learning_objectives": [
                "Build responsive websites using HTML5 and CSS3",
                "Create dynamic single-page apps with React",
                "Design RESTful APIs using Node.js & Express",
                "Manage databases with MongoDB and SQL",
                "Implement user authentication and security",
                "Deploy applications to the cloud"
            ],
            "topics_covered": ["HTML5", "CSS3 Grid & Flexbox", "JavaScript ES6+", "React.js", "Node.js Runtime", "Express Framework", "MongoDB", "Git & GitHub"],
            "published_at": datetime.now() - timedelta(days=30)
        },
        {
            "instructor": instructors[1],  # Jane Doe
            "category": cat_map["design"],
            "title": "UI/UX Design Principles & Practices",
            "slug": "ui-ux-design-principles-practices",
            "small_description": "Learn to create user-friendly interfaces and beautiful experiences.",
            "description": "Master the fundamentals of user experience and user interface design. Learn design thinking, prototyping, and how to create intuitive digital experiences that users love.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuCtShuzkMHvxlxOcVou2gYbrUa3uNUQ-Gn20rkSjmLAgeYntiMkAjcSUC20zYGkzZBidNpiSHIYlKWg2t1hWTF0QxAtuvXL5lKohZ1ieoSYKHTP_66teszqaJmS9eMVzgRgpqpaFigXQlR-Pl12xA3SE_JIDrBqxXky8jGH-2drZ2yVcv0xIyR5LUupl0Quk6xEqiynA5jv0n_yJvRINcLs6Z4i9-fCOTXCBIXoTlp4i28UUnoh5qdCQ_CqOEgQtlfckOEy9oKYuPXb",
            "duration_hours": 8.25,
            "difficulty_level": "Intermediate",
            "rating": 4.8,
            "course_purpose": "Understand the principles of creating products that are not only visually appealing but also highly functional and user-centered.",
            "learning_objectives": [
                "Understand UX design fundamentals",
                "Master the design thinking process",
                "Create wireframes and prototypes",
                "Conduct user research and testing",
                "Design accessible interfaces",
                "Use Figma for professional designs"
            ],
            "topics_covered": ["UX Principles", "Design Thinking", "Wireframing", "Prototyping", "User Research", "Figma", "Accessibility", "Color Theory"],
            "published_at": datetime.now() - timedelta(days=45)
        },
        {
            "instructor": instructors[2],  # Sarah Lee
            "category": cat_map["marketing"],
            "title": "Digital Marketing Mastery",
            "slug": "digital-marketing-mastery",
            "small_description": "Learn SEO, social media, email marketing, and analytics strategies.",
            "description": "Comprehensive digital marketing course covering all aspects of modern online marketing. From SEO to social media, learn how to create effective marketing campaigns that drive results.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuCJR4sARXWBIh1MFyVdpgx-q003N2aoBAPc32b5WB-Jj-LgBVx6OCXMJ0X2NcCDkRQLyBmp5AZH8amwZEPTCkqA0DWy2RqzMkxhU3sIbmAhp7Wp92psoJqlH_VjAhc0nAkEeHIyhJZFcviLDJPIxNJ1ZdOozd4qFfXsoukF9OV4NqfTaUBYcVYyaYKiTf0XJhL-50tLT9HPZRAhW3XNwhSMqGU_mtLqZXdRitjpOuDdlVTtzB9saEEBzDDZQea2rnkOa-EZi_R6j38j",
            "duration_hours": 10.75,
            "difficulty_level": "Beginner to Advanced",
            "rating": 4.7,
            "course_purpose": "Learn to create, implement, and optimize digital marketing campaigns across multiple channels to drive business growth.",
            "learning_objectives": [
                "Master SEO and content marketing",
                "Run effective social media campaigns",
                "Create email marketing strategies",
                "Use Google Analytics effectively",
                "Understand PPC advertising",
                "Develop comprehensive marketing plans"
            ],
            "topics_covered": ["SEO", "Content Marketing", "Social Media", "Email Marketing", "Google Analytics", "PPC", "Marketing Automation", "Conversion Optimization"],
            "published_at": datetime.now() - timedelta(days=20)
        },
        {
            "instructor": instructors[3],  # Dr. Michael Chen
            "category": cat_map["data-science"],
            "title": "Python for Data Science and Machine Learning",
            "slug": "python-data-science-machine-learning",
            "small_description": "Master Python, NumPy, Pandas, and Machine Learning algorithms.",
            "description": "Learn data science from scratch using Python. Cover data analysis, visualization, and machine learning with hands-on projects.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuDCuGlOlzueSusvOq36Aj5zyle2UQNw2twth3Bn450cLuYGpPIbrVQ2YaP1TGKY17yZO415RV4m10lNFPTiJM5pwKKGhJHaFe93drzj19j5E5vXJxEpX3LGyC_ToB_VHhTOunMCSBkazy2QiORuri0vNQvsqD8aigZd7BM-ogm7ApKJwdlCr_muljiFnMfxVGTgv5OR-91Eetosub6--k7lm6oHisOJ7rImY7f2SVDiMavAYf5dFET2oWPXja6YKLdEHXd6Ic0f4h2q",
            "duration_hours": 15.0,
            "difficulty_level": "Intermediate to Advanced",
            "rating": 4.9,
            "course_purpose": "Build a strong foundation in data science and machine learning using Python's powerful libraries and frameworks.",
            "learning_objectives": [
                "Master Python programming for data science",
                "Analyze data with Pandas and NumPy",
                "Create visualizations with Matplotlib and Seaborn",
                "Build machine learning models",
                "Work with real-world datasets",
                "Deploy ML models to production"
            ],
            "topics_covered": ["Python", "NumPy", "Pandas", "Matplotlib", "Scikit-learn", "Machine Learning", "Data Visualization", "Statistical Analysis"],
            "published_at": datetime.now() - timedelta(days=60)
        },
        {
            "instructor": instructors[4],  # Emily Rodriguez
            "category": cat_map["cybersecurity"],
            "title": "Cybersecurity Fundamentals",
            "slug": "cybersecurity-fundamentals",
            "small_description": "Learn network security, ethical hacking, and security best practices.",
            "description": "Comprehensive introduction to cybersecurity covering network security, cryptography, ethical hacking, and security operations.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuCtShuzkMHvxlxOcVou2gYbrUa3uNUQ-Gn20rkSjmLAgeYntiMkAjcSUC20zYGkzZBidNpiSHIYlKWg2t1hWTF0QxAtuvXL5lKohZ1ieoSYKHTP_66teszqaJmS9eMVzgRgpqpaFigXQlR-Pl12xA3SE_JIDrBqxXky8jGH-2drZ2yVcv0xIyR5LUupl0Quk6xEqiynA5jv0n_yJvRINcLs6Z4i9-fCOTXCBIXoTlp4i28UUnoh5qdCQ_CqOEgQtlfckOEy9oKYuPXb",
            "duration_hours": 11.5,
            "difficulty_level": "Beginner to Intermediate",
            "rating": 4.8,
            "course_purpose": "Understand the fundamentals of cybersecurity and learn how to protect systems, networks, and data from cyber threats.",
            "learning_objectives": [
                "Understand common cyber threats",
                "Learn network security principles",
                "Master cryptography basics",
                "Practice ethical hacking techniques",
                "Implement security best practices",
                "Respond to security incidents"
            ],
            "topics_covered": ["Network Security", "Cryptography", "Ethical Hacking", "Penetration Testing", "Security Operations", "Incident Response", "Risk Management", "Security Tools"],
            "published_at": datetime.now() - timedelta(days=15)
        },
        {
            "instructor": instructors[5],  # David Kim
            "category": cat_map["cloud-computing"],
            "title": "AWS Cloud Practitioner Essentials",
            "slug": "aws-cloud-practitioner-essentials",
            "small_description": "Start your cloud journey with AWS. Learn core services and concepts.",
            "description": "This course covers the fundamentals of building IT infrastructure on AWS. The course is designed to teach solutions architects how to optimize the use of the AWS Cloud by understanding AWS services and how they fit into cloud-based solutions.",
            "thumbnail": "https://lh3.googleusercontent.com/aida-public/AB6AXuDCuGlOlzueSusvOq36Aj5zyle2UQNw2twth3Bn450cLuYGpPIbrVQ2YaP1TGKY17yZO415RV4m10lNFPTiJM5pwKKGhJHaFe93drzj19j5E5vXJxEpX3LGyC_ToB_VHhTOunMCSBkazy2QiORuri0vNQvsqD8aigZd7BM-ogm7ApKJwdlCr_muljiFnMfxVGTgv5OR-91Eetosub6--k7lm6oHisOJ7rImY7f2SVDiMavAYf5dFET2oWPXja6YKLdEHXd6Ic0f4h2q",
            "duration_hours": 14.5,
            "difficulty_level": "Beginner",
            "rating": 4.8,
            "course_purpose": "Understand the AWS Cloud platform, global infrastructure, and key services to prepare for the Cloud Practitioner certification.",
            "learning_objectives": [
                "Understand AWS Cloud concepts",
                "Navigate the AWS Management Console",
                "Core AWS services (EC2, S3, RDS)",
                "Security and compliance in AWS",
                "AWS pricing and billing"
            ],
            "topics_covered": ["Cloud Computing", "AWS", "EC2", "S3", "Security", "Networking", "Databases"],
            "published_at": datetime.now() - timedelta(days=10)
        }
    ]
    
    courses = []
    for course_data in courses_data:
        course = Course(
            instructor_id=course_data["instructor"].id,
            category_id=course_data["category"].id,
            title=course_data["title"],
            slug=course_data["slug"],
            small_description=course_data["small_description"],
            description=course_data["description"],
            thumbnail=course_data["thumbnail"],
            duration_hours=course_data["duration_hours"],
            difficulty_level=course_data["difficulty_level"],
            rating=course_data["rating"],
            course_purpose=course_data["course_purpose"],
            learning_objectives=course_data["learning_objectives"],
            topics_covered=course_data["topics_covered"],
            published_at=course_data["published_at"]
        )
        db.add(course)
        courses.append(course)
        print(f"  ✓ Course: {course_data['title']} ({course_data['category'].name})")
    
    db.commit()
    return courses

def seed_lessons(db, courses):
    """Create lessons for each course"""
    print("\nSeeding lessons...")
    
    lessons_per_course = [
        # Full Stack Web Development
        [
            {"order": 1, "title": "Welcome to Full Stack Development", "description": "Introduction to the course and what you'll learn", "video_duration": 450},
            {"order": 2, "title": "HTML5 Fundamentals", "description": "Learn HTML5 structure, semantic elements, and best practices", "video_duration": 1200},
            {"order": 3, "title": "CSS3 and Flexbox", "description": "Master CSS styling, layouts with Flexbox", "video_duration": 1500},
            {"order": 4, "title": "CSS Grid Layout", "description": "Create complex layouts with CSS Grid", "video_duration": 1350},
            {"order": 5, "title": "JavaScript Basics", "description": "Variables, data types, and control structures", "video_duration": 1800},
            {"order": 6, "title": "JavaScript ES6+ Features", "description": "Arrow functions, destructuring, spread operator", "video_duration": 1650},
            {"order": 7, "title": "React Introduction", "description": "Components, props, and state management", "video_duration": 2100},
            {"order": 8, "title": "React Hooks", "description": "useState, useEffect, and custom hooks", "video_duration": 1950},
            {"order": 9, "title": "Node.js and Express", "description": "Building REST APIs with Node and Express", "video_duration": 2400},
            {"order": 10, "title": "MongoDB Basics", "description": "NoSQL database fundamentals and CRUD operations", "video_duration": 1800},
            {"order": 11, "title": "Authentication & Security", "description": "JWT, bcrypt, and security best practices", "video_duration": 2250},
            {"order": 12, "title": "Deployment to Cloud", "description": "Deploy your application to production", "video_duration": 1500}
        ],
        # UI/UX Design
        [
            {"order": 1, "title": "Introduction to UX Design", "description": "What is UX and why it matters", "video_duration": 765},
            {"order": 2, "title": "Design Thinking Process", "description": "Empathize, Define, Ideate, Prototype, Test", "video_duration": 920},
            {"order": 3, "title": "User Research Methods", "description": "Conducting interviews, surveys, and usability tests", "video_duration": 1100},
            {"order": 4, "title": "Creating User Personas", "description": "Build detailed user personas from research", "video_duration": 850},
            {"order": 5, "title": "Information Architecture", "description": "Organizing content and navigation structures", "video_duration": 950},
            {"order": 6, "title": "Wireframing Basics", "description": "Low-fidelity to high-fidelity wireframes", "video_duration": 1200},
            {"order": 7, "title": "Prototyping in Figma", "description": "Interactive prototypes and animations", "video_duration": 1450},
            {"order": 8, "title": "Visual Design Principles", "description": "Color, typography, and hierarchy", "video_duration": 1300},
            {"order": 9, "title": "Accessibility in Design", "description": "WCAG guidelines and inclusive design", "video_duration": 900},
            {"order": 10, "title": "Usability Testing", "description": "Plan and conduct effective usability tests", "video_duration": 1050}
        ],
        # Digital Marketing
        [
            {"order": 1, "title": "Digital Marketing Overview", "description": "Introduction to digital marketing channels", "video_duration": 600},
            {"order": 2, "title": "SEO Fundamentals", "description": "On-page and off-page SEO techniques", "video_duration": 1350},
            {"order": 3, "title": "Keyword Research", "description": "Finding and targeting the right keywords", "video_duration": 1100},
            {"order": 4, "title": "Content Marketing Strategy", "description": "Creating valuable content that converts", "video_duration": 1250},
            {"order": 5, "title": "Social Media Marketing", "description": "Facebook, Instagram, LinkedIn strategies", "video_duration": 1400},
            {"order": 6, "title": "Email Marketing Campaigns", "description": "Building lists and creating effective emails", "video_duration": 1150},
            {"order": 7, "title": "Google Analytics", "description": "Track and analyze website performance", "video_duration": 1550},
            {"order": 8, "title": "Google Ads & PPC", "description": "Creating profitable paid campaigns", "video_duration": 1650},
            {"order": 9, "title": "Facebook Ads", "description": "Targeting and optimization strategies", "video_duration": 1500},
            {"order": 10, "title": "Marketing Automation", "description": "Tools and workflows for automation", "video_duration": 1200},
            {"order": 11, "title": "Conversion Rate Optimization", "description": "A/B testing and improving conversions", "video_duration": 1350},
            {"order": 12, "title": "Marketing Analytics & ROI", "description": "Measuring success and calculating ROI", "video_duration": 1000}
        ],
        # Python for Data Science
        [
            {"order": 1, "title": "Python Programming Basics", "description": "Variables, loops, functions in Python", "video_duration": 1500},
            {"order": 2, "title": "NumPy Fundamentals", "description": "Arrays, operations, and broadcasting", "video_duration": 1650},
            {"order": 3, "title": "Pandas for Data Analysis", "description": "DataFrames, series, and data manipulation", "video_duration": 1800},
            {"order": 4, "title": "Data Cleaning Techniques", "description": "Handle missing data and outliers", "video_duration": 1550},
            {"order": 5, "title": "Data Visualization with Matplotlib", "description": "Creating plots and charts", "video_duration": 1400},
            {"order": 6, "title": "Advanced Visualization with Seaborn", "description": "Statistical visualizations", "video_duration": 1300},
            {"order": 7, "title": "Statistical Analysis", "description": "Hypothesis testing and distributions", "video_duration": 1750},
            {"order": 8, "title": "Machine Learning Introduction", "description": "Supervised vs unsupervised learning", "video_duration": 1200},
            {"order": 9, "title": "Linear Regression", "description": "Building predictive models", "video_duration": 1900},
            {"order": 10, "title": "Classification Algorithms", "description": "Logistic regression, decision trees", "video_duration": 2100},
            {"order": 11, "title": "Clustering and PCA", "description": "Unsupervised learning techniques", "video_duration": 1850},
            {"order": 12, "title": "Model Deployment", "description": "Deploy ML models with Flask", "video_duration": 1600}
        ],
        # Cybersecurity
        [
            {"order": 1, "title": "Introduction to Cybersecurity", "description": "Cyber threats landscape overview", "video_duration": 800},
            {"order": 2, "title": "Network Security Basics", "description": "Firewalls, IDS/IPS, VPNs", "video_duration": 1450},
            {"order": 3, "title": "Cryptography Fundamentals", "description": "Encryption, hashing, digital signatures", "video_duration": 1600},
            {"order": 4, "title": "Security Protocols", "description": "SSL/TLS, SSH, and secure communications", "video_duration": 1350},
            {"order": 5, "title": "Web Application Security", "description": "OWASP Top 10 vulnerabilities", "video_duration": 1750},
            {"order": 6, "title": "Ethical Hacking Introduction", "description": "Reconnaissance and scanning techniques", "video_duration": 1550},
            {"order": 7, "title": "Penetration Testing", "description": "Vulnerability assessment and exploitation", "video_duration": 1900},
            {"order": 8, "title": "Security Operations Center", "description": "Monitoring and incident detection", "video_duration": 1400},
            {"order": 9, "title": "Incident Response", "description": "Handling security breaches", "video_duration": 1500},
            {"order": 10, "title": "Risk Management", "description": "Identifying and mitigating risks", "video_duration": 1250},
            {"order": 11, "title": "Security Best Practices", "description": "Policies, procedures, and compliance", "video_duration": 1100}
        ],
        # AWS Cloud Practitioner
        [
            {"order": 1, "title": "Cloud Concepts Overview", "description": "Introduction to cloud computing and AWS", "video_duration": 900},
            {"order": 2, "title": "Global Infrastructure", "description": "Regions, Availability Zones, and Edge Locations", "video_duration": 1100},
            {"order": 3, "title": "Identity & Access Management (IAM)", "description": "Managing users, groups, and roles securely", "video_duration": 1350},
            {"order": 4, "title": "Amazon EC2", "description": "Virtual servers in the cloud", "video_duration": 1500},
            {"order": 5, "title": "Amazon S3", "description": "Object storage classes and features", "video_duration": 1200},
            {"order": 6, "title": "Amazon RDS & DynamoDB", "description": "Relational vs NoSQL databases", "video_duration": 1400},
            {"order": 7, "title": "Networking & VPC", "description": "Subnets, Gateways, and Security Groups", "video_duration": 1600},
            {"order": 8, "title": "AWS Security & Compliance", "description": "Shared Responsibility Model", "video_duration": 1150},
            {"order": 9, "title": "AWS Pricing Models", "description": "On-Demand, Reserved, and Spot instances", "video_duration": 1050},
            {"order": 10, "title": "CloudWatch & CloudTrail", "description": "Monitoring and auditing your resources", "video_duration": 1250},
            {"order": 11, "title": "Elastic Load Balancing", "description": "Distributing traffic across targets", "video_duration": 1300},
            {"order": 12, "title": "Auto Scaling", "description": "Scaling resources to match demand", "video_duration": 1100}
        ]
    ]
    
    all_lessons = []
    video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    
    for course, lessons_data in zip(courses, lessons_per_course):
        for lesson_data in lessons_data:
            lesson = Lesson(
                course_id=course.id,
                order=lesson_data["order"],
                title=lesson_data["title"],
                description=lesson_data["description"],
                video_duration=lesson_data["video_duration"],
                video_url=video_url
            )
            db.add(lesson)
            all_lessons.append(lesson)
        print(f"  ✓ Added {len(lessons_data)} lessons for: {course.title}")
    
    db.commit()
    return all_lessons

def seed_users(db, instructors):
    """Create user accounts"""
    print("\nSeeding users...")
    
    # Create instructor user account
    instructor_user = User(
        email="instructor@mail.ljku.edu.in",
        full_name=instructors[0].name,
        role=UserRole.INSTRUCTOR,
        bio="Passionate educator with 10+ years of experience in software development and teaching.",
        major="Computer Science"
    )
    instructor_user.set_password("Instructor@2024")
    db.add(instructor_user)
    print(f"  ✓ Instructor User: {instructor_user.email}")
    
    # Create the specific student user
    student_user = User(
        email="24002170410016@mail.ljku.edu.in",
        full_name="Ayaz Khira",
        role=UserRole.STUDENT,
        bio="Enthusiastic learner passionate about technology and innovation.",
        major="Computer Engineering"
    )
    student_user.set_password("Student@2024")
    db.add(student_user)
    print(f"  ✓ Student User: {student_user.email}")

    # Create admin user
    admin_user = User(
        email="admin@ljcourses.com",
        full_name="System Administrator",
        role=UserRole.ADMIN,
        bio="Platform administrator.",
        major="Administration"
    )
    admin_user.set_password("Admin@2024")
    db.add(admin_user)
    print(f"  ✓ Admin User: {admin_user.email}")
    
    # Create additional student users
    additional_students = [
        {
            "email": "24002170410017@mail.ljku.edu.in",
            "full_name": "Priya Sharma",
            "bio": "Tech enthusiast interested in web development and design.",
            "major": "Information Technology"
        },
        {
            "email": "24002170410018@mail.ljku.edu.in",
            "full_name": "Rahul Patel",
            "bio": "Future data scientist passionate about AI and machine learning.",
            "major": "Data Science"
        },
        {
            "email": "24002170410019@mail.ljku.edu.in",
            "full_name": "Ananya Gupta",
            "bio": "Creative designer and digital marketing enthusiast.",
            "major": "Digital Marketing"
        },
        {
            "email": "24002170410020@mail.ljku.edu.in",
            "full_name": "Vikram Singh",
            "bio": "Network security specialist in training.",
            "major": "Cybersecurity"
        },
        {
            "email": "24002170410021@mail.ljku.edu.in",
            "full_name": "Neha Reddy",
            "bio": "Aspiring full stack developer.",
            "major": "Computer Science"
        },
        {
            "email": "24002170410022@mail.ljku.edu.in",
            "full_name": "Arjun Kumar",
            "bio": "Data analyst with a passion for big data.",
            "major": "Data Analytics"
        },
        {
            "email": "24002170410023@mail.ljku.edu.in",
            "full_name": "Sneha Patel",
            "bio": "UX researcher and interaction designer.",
            "major": "Design"
        }
    ]
    
    other_students = []
    for student_data in additional_students:
        user = User(
            email=student_data["email"],
            full_name=student_data["full_name"],
            role=UserRole.STUDENT,
            bio=student_data["bio"],
            major=student_data["major"]
        )
        user.set_password("Student@2024")
        db.add(user)
        other_students.append(user)
        print(f"  ✓ Student User: {user.email}")
    
    db.commit()
    return instructor_user, student_user, other_students, admin_user

def seed_enrollments(db, students, courses):
    """Create course enrollments"""
    print("\nSeeding enrollments...")
    
    main_student = students[0]
    other_students = students[1:]
    
    enrollments = []
    
    # Enroll main student in first 3 courses
    for i, course in enumerate(courses[:3]):
        enrollment = Enrollment(
            student_id=main_student.id,
            course_id=course.id,
            enrolled_at=datetime.now() - timedelta(days=30-i*5),
            last_accessed=datetime.now() - timedelta(hours=12)
        )
        db.add(enrollment)
        enrollments.append(enrollment)
        print(f"  ✓ Enrolled {main_student.email} in: {course.title}")
    
    # Enroll other students in various courses
    for student in other_students:
        # Each student enrolls in 2-3 random courses
        import random
        num_courses = random.randint(2, 3)
        student_courses = random.sample(courses, num_courses)
        
        for course in student_courses:
            enrollment = Enrollment(
                student_id=student.id,
                course_id=course.id,
                enrolled_at=datetime.now() - timedelta(days=random.randint(10, 45)),
                last_accessed=datetime.now() - timedelta(hours=random.randint(1, 72))
            )
            db.add(enrollment)
            enrollments.append(enrollment)
        print(f"  ✓ Enrolled {student.email} in {num_courses} courses")
    
    db.commit()
    return enrollments

def seed_lesson_progress(db, enrollments, courses):
    """Create lesson progress records"""
    print("\nSeeding lesson progress...")
    
    progress_count = 0
    
    for enrollment in enrollments:
        # Get lessons for this course
        course = next(c for c in courses if c.id == enrollment.course_id)
        lessons = sorted(course.lessons, key=lambda l: l.order)
        
        # Complete first 2-4 lessons randomly
        import random
        num_completed = random.randint(2, min(4, len(lessons)))
        
        for lesson in lessons[:num_completed]:
            progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson.id,
                is_completed=True,
                started_at=enrollment.enrolled_at + timedelta(days=random.randint(1, 5)),
                completed_at=enrollment.enrolled_at + timedelta(days=random.randint(2, 7)),
                last_accessed=datetime.now() - timedelta(hours=random.randint(1, 48))
            )
            db.add(progress)
            progress_count += 1
        
        # Start but not complete 1-2 more lessons
        if num_completed < len(lessons):
            for lesson in lessons[num_completed:num_completed+random.randint(1, 2)]:
                if lesson.order <= len(lessons):
                    progress = LessonProgress(
                        enrollment_id=enrollment.id,
                        lesson_id=lesson.id,
                        is_completed=False,
                        started_at=enrollment.enrolled_at + timedelta(days=random.randint(3, 10)),
                        last_accessed=datetime.now() - timedelta(hours=random.randint(1, 24))
                    )
                    db.add(progress)
                    progress_count += 1
    
    db.commit()
    print(f"  ✓ Created {progress_count} lesson progress records")

def main():
    """Main seeding function"""
    print("="*60)
    print("LJCourses Database Seeding Script")
    print("="*60)
    
    # Create database tables
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Seed data
        categories = seed_categories(db)
        instructors = seed_instructors(db)
        courses = seed_courses(db, categories, instructors)
        lessons = seed_lessons(db, courses)
        instructor_user, main_student, other_students, admin_user = seed_users(db, instructors)
        all_students = [main_student] + other_students
        enrollments = seed_enrollments(db, all_students, courses)
        seed_lesson_progress(db, enrollments, courses)
        
        print("\n" + "="*60)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • Categories: {len(categories)}")
        print(f"  • Instructors: {len(instructors)}")
        print(f"  • Courses: {len(courses)}")
        print(f"  • Lessons: {len(lessons)}")
        print(f"  • Users: {len(all_students) + 2}")  # +2 for instructor and admin
        print(f"  • Enrollments: {len(enrollments)}")
        print(f"\n🔐 Login Credentials:")
        print(f"  Student: 24002170410016@mail.ljku.edu.in / Student@2024")
        print(f"  Instructor: instructor@mail.ljku.edu.in / Instructor@2024")
        print(f"  Admin: admin@ljcourses.com / Admin@2024")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
