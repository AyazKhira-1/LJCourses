"""
Database seeding script for LJCourses platform
"""
from datetime import datetime, timedelta
from app.db import SessionLocal, engine
from app.models import Base, User, UserRole, Category, Course, Lesson, Enrollment, LessonProgress

def clear_database(db):
    """Clear all data from tables"""
    print("Clearing existing data...")
    db.query(LessonProgress).delete()
    db.query(Enrollment).delete()
    db.query(Lesson).delete()
    db.query(Course).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Database cleared")

def seed_categories(db):
    """Create course categories"""
    print("\nSeeding categories...")
    categories_data = [
        {"name": "Mathematics", "slug": "mathematics"},
        {"name": "Physics", "slug": "physics"},
        {"name": "Chemistry", "slug": "chemistry"},
        {"name": "Computer Science", "slug": "computer-science"},
        {"name": "Electrical Engineering", "slug": "electrical-engineering"},
        {"name": "Electronics Engineering", "slug": "electronics-engineering"},
        {"name": "Mechanical Engineering", "slug": "mechanical-engineering"},
        {"name": "Communication Skills", "slug": "communication-skills"},
        {"name": "Environmental Studies", "slug": "environmental-studies"},
        {"name": "Engineering Drawing", "slug": "engineering-drawing"},
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
    """Create instructor users - LJIET Faculty"""
    print("\nSeeding instructor users...")
    instructors_data = [
        {
            "full_name": "Prof. DBP",
            "designation": "Mechanical Engineering Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/DBP.png",
            "email": "dbp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. DRP",
            "designation": "Mathematics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/DRP.png",
            "email": "drp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. AAP",
            "designation": "Electronics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/AAP.png",
            "email": "aap@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. RVT",
            "designation": "Physics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/RVT.png",
            "email": "rvt@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. HBD",
            "designation": "Electronics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/HBD.png",
            "email": "hbd@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. KDL",
            "designation": "Computer Science Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/KDL.png",
            "email": "kdl@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. HRS",
            "designation": "Mathematics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/HRS.png",
            "email": "hrs@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. NRS",
            "designation": "Electrical Engineering Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/NRS.png",
            "email": "nrs@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. SAB",
            "designation": "Mathematics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/SAB.png",
            "email": "sab@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. AAG",
            "designation": "Communication & Environmental Studies Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/AAG.png",
            "email": "aag@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. YIK",
            "designation": "Computer Science Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/YIK.png",
            "email": "yik@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. ANP",
            "designation": "Engineering Graphics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/ANP.png",
            "email": "anp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. PKS",
            "designation": "Mathematics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/PKS.png",
            "email": "pks@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. SPJ",
            "designation": "Chemistry Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/SPJ.png",
            "email": "spj@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. MMP",
            "designation": "Mathematics Faculty, LJIET",
            "profile_image": "static/uploads/profile_photos/instructors/MMP.png",
            "email": "mmp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. ARP",
            "designation": "Engineering Graphics Faculty, LJIET",
            "email": "arp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. VVP",
            "designation": "Mechanical Engineering Faculty, LJIET",
            "email": "vvp@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. PBS",
            "designation": "Electrical Engineering Faculty, LJIET",
            "email": "pbs@mail.ljku.edu.in"
        },
        {
            "full_name": "Prof. DRS",
            "designation": "Electronics Faculty, LJIET",
            "email": "drs@mail.ljku.edu.in"
        }
    ]

    instructors = []
    for instr_data in instructors_data:
        email = instr_data.pop("email")
        instructor = User(
            email=email,
            role=UserRole.INSTRUCTOR,
            bio="LJIET Faculty member.",
            major="Engineering",
            **instr_data
        )
        instructor.set_password("Instructor@2026")
        db.add(instructor)
        instructors.append(instructor)
        print(f"  ✓ Instructor: {instr_data['full_name']} - {instr_data['designation']}")

    db.commit()
    return instructors

# Instructor index reference:
# 0=DBP, 1=DRP, 2=AAP, 3=RVT, 4=HBD, 5=KDL, 6=HRS, 7=NRS, 8=SAB,
# 9=AAG, 10=YIK, 11=ANP, 12=PKS, 13=SPJ, 14=MMP, 15=ARP, 16=VVP, 17=PBS, 18=DRS

def seed_courses(db, categories, instructors):
    """Create courses from LJIET YouTube channel"""
    print("\nSeeding courses...")

    cat_map = {cat.slug: cat for cat in categories}

    courses_data = [
        {
            "instructor": instructors[0],  # DBP
            "category": cat_map["mechanical-engineering"],
            "title": "Basic Mechanical Engineering",
            "slug": "gtu-basic-mechanical-engineering-dbp",
            "small_description": "GTU Basic Mechanical Engineering course by Prof. DBP covering all fundamental concepts.",
            "description": "Comprehensive course on Basic Mechanical Engineering as per GTU syllabus. Covers thermodynamics, IC engines, power plants, manufacturing processes, and more.",
            "thumbnail": "static/uploads/course_thumbnails/Basic_Mechanical_Engineering_(DBP).png",
            "duration_hours": 24.5,
            "difficulty_level": "Beginner",
            "rating": 4.8,
            "course_purpose": "Build a strong foundation in mechanical engineering concepts for first-year engineering students.",
            "learning_objectives": ["Understand thermodynamic principles", "Learn about IC engines and power plants", "Study manufacturing processes", "Understand material science basics", "Learn about power transmission systems"],
            "topics_covered": ["Thermodynamics", "IC Engines", "Power Plants", "Manufacturing", "Material Science", "Power Transmission"],
            "num_lessons": 49,
            "published_at": datetime.now() - timedelta(days=365)
        },
        {
            "instructor": instructors[1],  # DRP
            "category": cat_map["mathematics"],
            "title": "Mathematics-II",
            "slug": "gtu-mathematics-2-drp",
            "small_description": "GTU Mathematics-II course by Prof. DRP with 67 detailed video lectures.",
            "description": "Complete Mathematics-II course covering Differential Equations, Laplace Transforms, Fourier Series, and Partial Differential Equations as per GTU curriculum.",
            "thumbnail": "static/uploads/course_thumbnails/Mathematics-II_(DRP).png",
            "duration_hours": 33.5,
            "difficulty_level": "Intermediate",
            "rating": 4.9,
            "course_purpose": "Master advanced mathematical concepts required for engineering applications.",
            "learning_objectives": ["Solve differential equations", "Apply Laplace transforms", "Understand Fourier series", "Solve PDEs", "Apply numerical methods"],
            "topics_covered": ["Differential Equations", "Laplace Transforms", "Fourier Series", "PDE", "Numerical Methods"],
            "num_lessons": 67,
            "published_at": datetime.now() - timedelta(days=300)
        },
        {
            "instructor": instructors[2],  # AAP
            "category": cat_map["electronics-engineering"],
            "title": "Basic Electronics",
            "slug": "gtu-basic-electronics-aap",
            "small_description": "GTU Basic Electronics course by Prof. AAP with 43 video lectures.",
            "description": "Learn fundamentals of electronics including semiconductor devices, diodes, transistors, amplifiers, and digital electronics as per GTU syllabus.",
            "thumbnail": "static/uploads/course_thumbnails/Basic_Electronics_(AAP).png",
            "duration_hours": 21.5,
            "difficulty_level": "Beginner",
            "rating": 4.7,
            "course_purpose": "Understand fundamental electronic components and circuits used in engineering.",
            "learning_objectives": ["Understand semiconductor physics", "Analyze diode and transistor circuits", "Learn about amplifiers", "Study digital logic basics", "Understand power supplies"],
            "topics_covered": ["Semiconductors", "Diodes", "Transistors", "Amplifiers", "Digital Electronics", "Power Supplies"],
            "num_lessons": 43,
            "published_at": datetime.now() - timedelta(days=330)
        },
        {
            "instructor": instructors[3],  # RVT
            "category": cat_map["physics"],
            "title": "Physics-I",
            "slug": "gtu-physics-1-rvt",
            "small_description": "GTU Physics-I course by Prof. RVT with 32 video lectures.",
            "description": "Comprehensive physics course covering Optics, Quantum Mechanics, Electromagnetic Theory, and Laser applications for first-year engineering students.",
            "thumbnail": "static/uploads/course_thumbnails/Physics-I_(RVT).png",
            "duration_hours": 16.0,
            "difficulty_level": "Intermediate",
            "rating": 4.8,
            "course_purpose": "Develop a strong understanding of physics principles essential for engineering applications.",
            "learning_objectives": ["Understand wave optics and interference", "Study quantum mechanics fundamentals", "Learn electromagnetic theory", "Understand laser principles", "Study optical fiber communication"],
            "topics_covered": ["Wave Optics", "Quantum Mechanics", "Electromagnetic Theory", "Lasers", "Optical Fiber", "Interference"],
            "num_lessons": 32,
            "published_at": datetime.now() - timedelta(days=350)
        },
        {
            "instructor": instructors[4],  # HBD
            "category": cat_map["electronics-engineering"],
            "title": "Basic Electronics",
            "slug": "gtu-basic-electronics-hbd",
            "small_description": "GTU Basic Electronics course by Prof. HBD with 31 video lectures.",
            "description": "Alternative Basic Electronics course covering PN junction diodes, BJT, FET, Op-Amps, and digital electronics fundamentals.",
            "thumbnail": "static/uploads/course_thumbnails/Basic_Electronics_(HBD).png",
            "duration_hours": 15.5,
            "difficulty_level": "Beginner",
            "rating": 4.6,
            "course_purpose": "Provide clear understanding of electronic devices and circuits for engineering students.",
            "learning_objectives": ["Analyze PN junction characteristics", "Understand BJT and FET operation", "Study Op-Amp circuits", "Learn digital logic gates", "Understand rectifier circuits"],
            "topics_covered": ["PN Junction", "BJT", "FET", "Op-Amps", "Logic Gates", "Rectifiers"],
            "num_lessons": 31,
            "published_at": datetime.now() - timedelta(days=340)
        },
        {
            "instructor": instructors[5],  # KDL
            "category": cat_map["computer-science"],
            "title": "Programming for Problem Solving",
            "slug": "gtu-programming-problem-solving-kdl",
            "small_description": "GTU C Programming course by Prof. KDL covering problem solving with C language.",
            "description": "Learn C programming from scratch including data types, control structures, arrays, strings, functions, pointers, structures, and file handling.",
            "thumbnail": "static/uploads/course_thumbnails/Programming_for_Problem_Solving_(KDL).png",
            "duration_hours": 22.5,
            "difficulty_level": "Beginner",
            "rating": 4.8,
            "course_purpose": "Develop programming skills and logical thinking for solving engineering problems using C.",
            "learning_objectives": ["Master C programming fundamentals", "Work with arrays and strings", "Understand pointers and memory", "Implement functions and recursion", "Handle files in C"],
            "topics_covered": ["C Language", "Data Types", "Control Structures", "Arrays", "Pointers", "Functions", "Structures", "File Handling"],
            "num_lessons": 45,
            "published_at": datetime.now() - timedelta(days=320)
        },
        {
            "instructor": instructors[6],  # HRS
            "category": cat_map["mathematics"],
            "title": "Mathematics-I",
            "slug": "gtu-mathematics-1-hrs",
            "small_description": "GTU Mathematics-I course by Prof. HRS with 54 detailed lectures.",
            "description": "First semester Mathematics covering Matrices, Differential Calculus, Integral Calculus, and Sequences & Series as per GTU syllabus.",
            "thumbnail": "static/uploads/course_thumbnails/Mathematics-I_(HRS).png",
            "duration_hours": 27.0,
            "difficulty_level": "Intermediate",
            "rating": 4.9,
            "course_purpose": "Build mathematical foundations essential for all engineering disciplines.",
            "learning_objectives": ["Master matrix operations", "Learn differential calculus", "Apply integral calculus", "Understand sequences and series", "Solve engineering math problems"],
            "topics_covered": ["Matrices", "Differential Calculus", "Integral Calculus", "Sequences", "Series", "Partial Derivatives"],
            "num_lessons": 54,
            "published_at": datetime.now() - timedelta(days=400)
        },
        {
            "instructor": instructors[7],  # NRS
            "category": cat_map["electrical-engineering"],
            "title": "Basic Electrical Engineering",
            "slug": "gtu-basic-electrical-engineering-nrs",
            "small_description": "GTU Basic Electrical Engineering course by Prof. NRS.",
            "description": "Comprehensive course on electrical engineering fundamentals including DC circuits, AC circuits, transformers, electrical machines, and electrical installations.",
            "thumbnail": "static/uploads/course_thumbnails/Basic_Electrical_Engineering_(NRS).png",
            "duration_hours": 20.0,
            "difficulty_level": "Beginner",
            "rating": 4.7,
            "course_purpose": "Understand fundamental electrical engineering concepts and their practical applications.",
            "learning_objectives": ["Analyze DC and AC circuits", "Understand transformer principles", "Study DC and AC motors", "Learn about electrical installations", "Understand power systems basics"],
            "topics_covered": ["DC Circuits", "AC Circuits", "Transformers", "DC Motors", "AC Motors", "Electrical Installations"],
            "num_lessons": 40,
            "published_at": datetime.now() - timedelta(days=360)
        },
        {
            "instructor": instructors[8],  # SAB
            "category": cat_map["mathematics"],
            "title": "Mathematics-I",
            "slug": "gtu-mathematics-1-sab",
            "small_description": "GTU Mathematics-I course by Prof. SAB with 52 video lectures.",
            "description": "Alternative Mathematics-I course covering Indeterminate Forms, Improper Integrals, Gamma & Beta Functions, Matrices, and Differential Equations.",
            "thumbnail": "static/uploads/course_thumbnails/Mathematics-I_(SAB).png",
            "duration_hours": 26.0,
            "difficulty_level": "Intermediate",
            "rating": 4.8,
            "course_purpose": "Provide solid mathematical foundation with detailed explanations and solved examples.",
            "learning_objectives": ["Evaluate indeterminate forms", "Solve improper integrals", "Apply Gamma and Beta functions", "Perform matrix operations", "Solve first-order ODEs"],
            "topics_covered": ["Indeterminate Forms", "Improper Integrals", "Gamma Function", "Beta Function", "Matrices", "ODEs"],
            "num_lessons": 52,
            "published_at": datetime.now() - timedelta(days=380)
        },
        {
            "instructor": instructors[9],  # AAG
            "category": cat_map["communication-skills"],
            "title": "English Communication Skills",
            "slug": "gtu-english-aag",
            "small_description": "GTU English course by Prof. AAG with 28 video lectures.",
            "description": "Develop professional English communication skills including grammar, vocabulary, reading comprehension, technical writing, and presentation skills.",
            "thumbnail": "static/uploads/course_thumbnails/English_Communication_Skills_(AAG).png",
            "duration_hours": 14.0,
            "difficulty_level": "Beginner",
            "rating": 4.5,
            "course_purpose": "Enhance English communication abilities for engineering students in academic and professional settings.",
            "learning_objectives": ["Improve grammar and vocabulary", "Develop technical writing skills", "Enhance reading comprehension", "Learn presentation techniques", "Master professional communication"],
            "topics_covered": ["Grammar", "Vocabulary", "Technical Writing", "Comprehension", "Presentation Skills", "Professional Communication"],
            "num_lessons": 28,
            "published_at": datetime.now() - timedelta(days=310)
        },
        {
            "instructor": instructors[9],  # AAG
            "category": cat_map["environmental-studies"],
            "title": "Environmental Science",
            "slug": "gtu-environmental-science-aag",
            "small_description": "GTU Environmental Science course by Prof. AAG with 25 video lectures.",
            "description": "Study of environment, ecosystems, biodiversity, pollution, and sustainable development as per GTU curriculum for first-year engineering.",
            "thumbnail": "static/uploads/course_thumbnails/Environmental_Science_(AAG).png",
            "duration_hours": 12.5,
            "difficulty_level": "Beginner",
            "rating": 4.5,
            "course_purpose": "Create environmental awareness and understanding of sustainability among engineering students.",
            "learning_objectives": ["Understand ecosystems and biodiversity", "Study environmental pollution types", "Learn about sustainable development", "Understand environmental legislation", "Study natural resource management"],
            "topics_covered": ["Ecosystems", "Biodiversity", "Air Pollution", "Water Pollution", "Sustainable Development", "Environmental Laws"],
            "num_lessons": 25,
            "published_at": datetime.now() - timedelta(days=280)
        },
        {
            "instructor": instructors[10],  # YIK
            "category": cat_map["computer-science"],
            "title": "Programming for Problem Solving",
            "slug": "gtu-programming-problem-solving-yik",
            "small_description": "GTU Programming course by Prof. YIK with 51 video lectures.",
            "description": "Master C programming with emphasis on problem-solving techniques, algorithms, data structures basics, and programming paradigms.",
            "thumbnail": "static/uploads/course_thumbnails/Programming_for_Problem_Solving_(YIK).png",
            "duration_hours": 25.5,
            "difficulty_level": "Beginner to Intermediate",
            "rating": 4.7,
            "course_purpose": "Develop algorithmic thinking and C programming proficiency for solving real-world problems.",
            "learning_objectives": ["Master C programming syntax", "Develop problem-solving algorithms", "Work with dynamic memory", "Implement sorting and searching", "Handle file I/O operations"],
            "topics_covered": ["C Programming", "Algorithms", "Arrays", "Strings", "Pointers", "Dynamic Memory", "Sorting", "Searching"],
            "num_lessons": 51,
            "published_at": datetime.now() - timedelta(days=290)
        },
        {
            "instructor": instructors[11],  # ANP
            "category": cat_map["engineering-drawing"],
            "title": "Engineering Graphics & Design",
            "slug": "gtu-engineering-graphics-design-anp",
            "small_description": "GTU Engineering Graphics & Design course by Prof. ANP with 39 video lectures.",
            "description": "Learn engineering drawing and CAD fundamentals including orthographic projections, isometric views, sections, and AutoCAD/SolidWorks basics.",
            "thumbnail": "static/uploads/course_thumbnails/Engineering_Graphics_and_Design_(ANP).png",
            "duration_hours": 19.5,
            "difficulty_level": "Beginner",
            "rating": 4.6,
            "course_purpose": "Develop spatial visualization and technical drawing skills essential for engineering design.",
            "learning_objectives": ["Draw orthographic projections", "Create isometric views", "Understand sections and developments", "Learn CAD software basics", "Read and interpret engineering drawings"],
            "topics_covered": ["Orthographic Projection", "Isometric Views", "Sections", "Development", "AutoCAD", "SolidWorks"],
            "num_lessons": 39,
            "published_at": datetime.now() - timedelta(days=370)
        },
        {
            "instructor": instructors[12],  # PKS
            "category": cat_map["mathematics"],
            "title": "Mathematics-I",
            "slug": "gtu-mathematics-1-pks",
            "small_description": "GTU Mathematics-I course by Prof. PKS with 67 comprehensive lectures.",
            "description": "Extensive Mathematics-I course with detailed problem solving covering Calculus, Linear Algebra, and Differential Equations.",
            "thumbnail": "static/uploads/course_thumbnails/Mathematics_I_(PKS).png",
            "duration_hours": 33.5,
            "difficulty_level": "Intermediate",
            "rating": 4.9,
            "course_purpose": "Provide in-depth mathematical knowledge with extensive problem-solving practice.",
            "learning_objectives": ["Master calculus techniques", "Solve linear algebra problems", "Apply differential equations", "Understand mathematical proofs", "Solve GTU exam problems"],
            "topics_covered": ["Calculus", "Linear Algebra", "Differential Equations", "Integration", "Partial Derivatives", "Series"],
            "num_lessons": 67,
            "published_at": datetime.now() - timedelta(days=390)
        },
        {
            "instructor": instructors[13],  # SPJ
            "category": cat_map["chemistry"],
            "title": "Chemistry",
            "slug": "gtu-chemistry-spj",
            "small_description": "GTU Chemistry course by Prof. SPJ with 40 video lectures.",
            "description": "First-year engineering chemistry covering Electrochemistry, Spectroscopy, Water Treatment, Polymers, and Corrosion as per GTU syllabus.",
            "thumbnail": "static/uploads/course_thumbnails/Chemistry_(SPJ).png",
            "duration_hours": 20.0,
            "difficulty_level": "Intermediate",
            "rating": 4.7,
            "course_purpose": "Understand chemical principles and their applications in engineering and technology.",
            "learning_objectives": ["Master electrochemistry concepts", "Understand spectroscopic methods", "Learn water treatment processes", "Study polymer chemistry", "Understand corrosion and prevention"],
            "topics_covered": ["Electrochemistry", "Spectroscopy", "Water Treatment", "Polymers", "Corrosion", "Fuels"],
            "num_lessons": 40,
            "published_at": datetime.now() - timedelta(days=345)
        },
        {
            "instructor": instructors[14],  # MMP
            "category": cat_map["mathematics"],
            "title": "Mathematics-II",
            "slug": "lju-sem2-mathematics-2-mmp",
            "small_description": "LJU Sem-II Mathematics-II course by Prof. MMP with 60 video lectures.",
            "description": "Semester-II Mathematics covering Vector Calculus, Complex Analysis, Probability & Statistics, and Numerical Methods for CE/IT/CSE/EC branches.",
            "thumbnail": "static/uploads/course_thumbnails/Mathematics_II_(MMP).png",
            "duration_hours": 30.0,
            "difficulty_level": "Intermediate to Advanced",
            "rating": 4.8,
            "course_purpose": "Advanced mathematical tools required for higher semester engineering subjects.",
            "learning_objectives": ["Apply vector calculus", "Understand complex analysis", "Master probability and statistics", "Implement numerical methods", "Solve engineering math problems"],
            "topics_covered": ["Vector Calculus", "Complex Analysis", "Probability", "Statistics", "Numerical Methods", "Laplace Transform"],
            "num_lessons": 60,
            "published_at": datetime.now() - timedelta(days=120)
        },
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
            thumbnail=course_data.get("thumbnail", ""),
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
        course._num_lessons = course_data["num_lessons"]
        print(f"  ✓ Course: {course_data['title']} ({course_data['category'].name})")

    db.commit()
    return courses

def seed_lessons(db, courses):
    """Create lessons for each course with YouTube embed URLs"""
    print("\nSeeding lessons...")

    # Default YouTube embed URL from LJIET channel
    video_url = "static/uploads/course_lessons/LJ_University_Green_Campus.mp4"

    # Lesson titles per course - representative topics matching GTU syllabus
    lesson_topics = {
        "gtu-basic-mechanical-engineering-dbp": [
            "Introduction to Mechanical Engineering", "Properties of Materials", "Stress and Strain Concepts",
            "Types of Engineering Materials", "Iron Carbon Diagram", "Heat Treatment Processes",
            "Manufacturing Process Overview", "Casting Process", "Welding Techniques",
            "Lathe Machine Operations", "Drilling and Boring", "Milling Operations",
            "Thermodynamics Introduction", "Laws of Thermodynamics", "Heat Engines and Cycles",
            "Carnot Cycle", "Otto Cycle", "Diesel Cycle",
            "IC Engine Components", "Two Stroke Engine", "Four Stroke Engine",
            "SI vs CI Engines", "Engine Performance", "Cooling Systems",
            "Lubrication Systems", "Power Plants Overview", "Steam Power Plant",
            "Gas Turbine Power Plant", "Nuclear Power Plant", "Hydro Power Plant",
            "Renewable Energy Sources", "Solar Energy", "Wind Energy",
            "Power Transmission Elements", "Belt and Chain Drives", "Gear Systems",
            "Coupling Types", "Bearing Types", "Clutch and Brake Systems",
            "Pumps Introduction", "Centrifugal Pumps", "Reciprocating Pumps",
            "Compressors", "Refrigeration Basics", "Air Conditioning Fundamentals",
            "Fluid Mechanics Basics", "Pressure Measurement", "Flow Measurement",
            "Engineering Workshop Safety", "Course Revision and Summary",
        ],
        "gtu-mathematics-2-drp": [
            "Introduction to ODE", "First Order ODE", "Exact Differential Equations",
            "Linear First Order ODE", "Bernoullis Equation", "Orthogonal Trajectories",
            "Higher Order ODE Introduction", "Homogeneous Linear ODE", "Non-Homogeneous ODE",
            "Method of Undetermined Coefficients", "Variation of Parameters", "Cauchy-Euler Equation",
            "Simultaneous ODE", "Applications of ODE", "Laplace Transform Definition",
            "Laplace of Standard Functions", "Properties of Laplace Transform", "Inverse Laplace Transform",
            "Partial Fractions Method", "Convolution Theorem", "Laplace Transform of Derivatives",
            "Solving ODE using Laplace", "Unit Step Function", "Dirac Delta Function",
            "Periodic Functions Laplace", "Fourier Series Introduction", "Fourier Coefficients",
            "Dirichlets Conditions", "Even and Odd Functions", "Half Range Series",
            "Fourier Cosine Series", "Fourier Sine Series", "Parsevals Theorem",
            "Complex Form of Fourier Series", "Fourier Integral", "Fourier Transform",
            "Properties of Fourier Transform", "Inverse Fourier Transform", "Fourier Sine Transform",
            "Fourier Cosine Transform", "PDE Introduction", "Formation of PDE",
            "Solution of PDE", "Method of Separation", "Heat Equation",
            "Wave Equation", "Laplace Equation", "Applications of PDE",
            "Numerical Methods Intro", "Bisection Method", "Newton-Raphson Method",
            "Regula Falsi Method", "Fixed Point Iteration", "Gauss Elimination",
            "Gauss-Seidel Method", "LU Decomposition", "Numerical Integration",
            "Trapezoidal Rule", "Simpsons Rule", "Eulers Method",
            "Runge-Kutta Method", "Adams-Bashforth Method", "Curve Fitting",
            "Interpolation Methods", "Lagrange Interpolation", "Course Summary",
        ],
        "gtu-basic-electronics-aap": [
            "Introduction to Electronics", "Semiconductor Physics", "Intrinsic Semiconductors",
            "Extrinsic Semiconductors", "PN Junction Diode", "Diode Characteristics",
            "Diode Applications", "Half Wave Rectifier", "Full Wave Rectifier",
            "Bridge Rectifier", "Filter Circuits", "Zener Diode",
            "Voltage Regulation", "Special Purpose Diodes", "LED and Photodiode",
            "BJT Introduction", "BJT Configurations", "CE Characteristics",
            "CB Characteristics", "BJT Biasing", "Fixed Bias Circuit",
            "Voltage Divider Bias", "BJT as Switch", "BJT as Amplifier",
            "FET Introduction", "JFET Characteristics", "MOSFET Operation",
            "FET Biasing", "FET Applications", "Op-Amp Introduction",
            "Op-Amp Characteristics", "Inverting Amplifier", "Non-Inverting Amplifier",
            "Summing Amplifier", "Difference Amplifier", "Integrator and Differentiator",
            "Comparator Circuits", "Number Systems", "Logic Gates",
            "Boolean Algebra", "Combinational Circuits", "Course Summary",
        ],
        "gtu-physics-1-rvt": [
            "Wave Optics Introduction", "Interference of Light", "Youngs Double Slit Experiment",
            "Newtons Rings", "Thin Film Interference", "Michelson Interferometer",
            "Diffraction Introduction", "Single Slit Diffraction", "Diffraction Grating",
            "Resolving Power", "Polarization of Light", "Malus Law",
            "Brewsters Law", "Double Refraction", "Quantum Mechanics Introduction",
            "Blackbody Radiation", "Photoelectric Effect", "Compton Effect",
            "de Broglie Hypothesis", "Heisenberg Uncertainty Principle", "Schrodinger Equation",
            "Particle in a Box", "Electromagnetic Theory Basics", "Maxwells Equations",
            "Electromagnetic Waves", "Poynting Vector", "Laser Fundamentals",
            "Laser Types", "Laser Applications", "Optical Fiber Introduction",
            "Fiber Optic Communication", "Course Summary and Revision",
        ],
        "gtu-basic-electronics-hbd": [
            "Electronics Fundamentals", "Atomic Structure", "Energy Bands",
            "PN Junction Formation", "Diode VI Characteristics", "Diode as Rectifier",
            "Half and Full Wave Rectification", "Capacitor Filter", "Zener Diode Regulator",
            "Bipolar Junction Transistor", "BJT Operating Regions", "CE Configuration",
            "CB Configuration", "CC Configuration", "Transistor Biasing Techniques",
            "Thermal Stability", "Small Signal Analysis", "JFET Structure",
            "JFET Characteristics", "MOSFET Types", "MOSFET Applications",
            "Operational Amplifier Basics", "Ideal Op-Amp", "Op-Amp Applications",
            "Number System Conversions", "Binary Arithmetic", "Basic Logic Gates",
            "Universal Gates", "Boolean Theorems", "K-Map Simplification",
            "Combinational Logic Design",
        ],
        "gtu-programming-problem-solving-kdl": [
            "Introduction to Programming", "Problem Solving Approach", "Algorithms and Flowcharts",
            "C Language Overview", "Data Types and Variables", "Operators in C",
            "Input and Output Functions", "Formatted I/O", "Decision Making - if Statement",
            "if-else and Nested if", "Switch Case Statement", "while Loop",
            "for Loop", "do-while Loop", "Nested Loops",
            "Break and Continue", "Pattern Programs", "Introduction to Arrays",
            "One Dimensional Arrays", "Array Operations", "Two Dimensional Arrays",
            "Matrix Operations", "Strings in C", "String Functions",
            "String Manipulation Programs", "Introduction to Functions", "Function Types",
            "Call by Value", "Call by Reference", "Recursion",
            "Recursive Programs", "Storage Classes", "Introduction to Pointers",
            "Pointer Arithmetic", "Pointers and Arrays", "Pointers and Strings",
            "Dynamic Memory Allocation", "malloc and calloc", "Introduction to Structures",
            "Structure Operations", "Array of Structures", "Nested Structures",
            "Introduction to File Handling", "File Operations in C", "Course Summary",
        ],
        "gtu-mathematics-1-hrs": [
            "Introduction to Matrices", "Types of Matrices", "Matrix Operations",
            "Determinants", "Properties of Determinants", "Inverse of a Matrix",
            "Rank of a Matrix", "Echelon Form", "System of Linear Equations",
            "Cramers Rule", "Gauss Elimination Method", "Eigenvalues Introduction",
            "Eigenvectors", "Cayley-Hamilton Theorem", "Diagonalization",
            "Successive Differentiation", "Leibnitz Theorem", "Indeterminate Forms",
            "LHospitals Rule", "Taylors Series", "Maclaurins Series",
            "Partial Differentiation", "Eulers Theorem", "Total Derivatives",
            "Jacobians", "Maxima and Minima", "Lagrange Multipliers",
            "Curve Tracing", "Rectification", "Double Integrals",
            "Triple Integrals", "Change of Order", "Applications of Double Integrals",
            "Area by Integration", "Volume by Integration", "Beta Function",
            "Gamma Function", "Relation Between Beta and Gamma", "Improper Integrals",
            "Convergence Tests", "Sequences Introduction", "Series Introduction",
            "Convergence of Series", "Comparison Test", "Ratio Test",
            "Root Test", "Integral Test", "Alternating Series",
            "Absolute Convergence", "Power Series", "Radius of Convergence",
            "Taylors Theorem", "Fourier Series Introduction", "Course Summary",
        ],
        "gtu-basic-electrical-engineering-nrs": [
            "Introduction to Electrical Engineering", "Electric Charge and Current", "Voltage and EMF",
            "Ohms Law", "Resistances in Series", "Resistances in Parallel",
            "Kirchhoffs Current Law", "Kirchhoffs Voltage Law", "Mesh Analysis",
            "Nodal Analysis", "Superposition Theorem", "Thevenins Theorem",
            "Nortons Theorem", "Maximum Power Transfer", "Star-Delta Transformation",
            "AC Fundamentals", "AC Waveform Parameters", "Phasor Representation",
            "AC through R L C", "Series RLC Circuit", "Parallel RLC Circuit",
            "Power in AC Circuits", "Power Factor", "Resonance",
            "Three Phase Systems", "Star and Delta Connection", "Three Phase Power",
            "Transformer Principle", "EMF Equation of Transformer", "Transformer Losses",
            "Transformer Efficiency", "DC Motor Principle", "Types of DC Motors",
            "DC Motor Characteristics", "AC Motor Introduction", "Induction Motor Principle",
            "Synchronous Motor", "Electrical Safety", "Earthing and Wiring",
            "Course Summary and Revision",
        ],
        "gtu-mathematics-1-sab": [
            "Indeterminate Forms Introduction", "LHospitals Rule Examples", "0/0 Form",
            "Infinity/Infinity Form", "0 x Infinity Form", "1^Infinity Form",
            "Improper Integrals Type I", "Improper Integrals Type II", "Convergence of Improper Integrals",
            "Comparison Test for Integrals", "Gamma Function Definition", "Gamma Function Properties",
            "Gamma Function Problems", "Beta Function Definition", "Beta Function Properties",
            "Relation Between Beta and Gamma", "Beta Gamma Function Problems", "Matrices Introduction",
            "Types of Matrices", "Matrix Operations", "Determinants",
            "Properties of Determinants", "Inverse of Matrix", "Rank of Matrix",
            "Echelon Form", "Normal Form", "System of Linear Equations",
            "Homogeneous Systems", "Non-Homogeneous Systems", "Cramers Rule",
            "Gauss Elimination", "Eigenvalues", "Eigenvectors",
            "Properties of Eigenvalues", "Cayley-Hamilton Theorem", "Diagonalization",
            "Quadratic Forms", "Successive Differentiation", "nth Derivative",
            "Leibnitz Theorem", "Leibnitz Theorem Problems", "Taylors Expansion",
            "Maclaurins Expansion", "Partial Differentiation", "Eulers Theorem",
            "Total Derivatives", "Chain Rule", "Jacobians",
            "Maxima and Minima of Two Variables", "Lagrange Multipliers Method", "First Order ODE",
            "Course Summary",
        ],
        "gtu-english-aag": [
            "Introduction to Communication", "Process of Communication", "Barriers to Communication",
            "Types of Communication", "Verbal Communication Skills", "Non-Verbal Communication",
            "Listening Skills", "Active Listening Techniques", "Parts of Speech Review",
            "Tenses and Usage", "Subject-Verb Agreement", "Common Grammatical Errors",
            "Vocabulary Building Techniques", "Word Formation", "Synonyms and Antonyms",
            "Reading Comprehension Strategies", "Skimming and Scanning", "Note Making",
            "Paragraph Writing", "Essay Writing", "Report Writing",
            "Letter Writing Formal", "Email Writing", "Technical Writing Basics",
            "Presentation Skills", "Group Discussion Skills", "Interview Preparation",
            "Course Summary",
        ],
        "gtu-environmental-science-aag": [
            "Introduction to Environmental Studies", "Multidisciplinary Nature", "Ecosystems Introduction",
            "Types of Ecosystems", "Food Chains and Webs", "Ecological Pyramids",
            "Energy Flow in Ecosystem", "Biogeochemical Cycles", "Biodiversity Introduction",
            "Types of Biodiversity", "Threats to Biodiversity", "Conservation of Biodiversity",
            "Natural Resources", "Water Resources", "Forest Resources",
            "Energy Resources", "Air Pollution", "Water Pollution",
            "Soil Pollution", "Noise Pollution", "Solid Waste Management",
            "Environmental Impact Assessment", "Sustainable Development", "Climate Change",
            "Course Summary",
        ],
        "gtu-programming-problem-solving-yik": [
            "Introduction to Computers", "Number Systems", "Problem Solving Steps",
            "Algorithms", "Flowcharts", "C Language Introduction",
            "Structure of C Program", "Compilation Process", "Data Types in C",
            "Variables and Constants", "Operators", "Expressions and Precedence",
            "printf and scanf", "Decision Making - if", "if-else Statement",
            "Nested if-else", "Switch Statement", "Conditional Operator",
            "while Loop", "for Loop", "do-while Loop",
            "Nested Loops", "Break Continue Goto", "Pattern Printing Programs",
            "Arrays Introduction", "Array Declaration and Initialization", "Array Operations",
            "Searching in Arrays", "Sorting Arrays - Bubble Sort", "Sorting Arrays - Selection Sort",
            "Two Dimensional Arrays", "Matrix Addition Subtraction", "Matrix Multiplication",
            "Strings Declaration", "String Library Functions", "String Programs",
            "Functions Introduction", "Function Declaration and Definition", "Function Arguments",
            "Recursion", "Recursion Examples", "Pointers Introduction",
            "Pointer Operations", "Pointers and Arrays", "Dynamic Memory Allocation",
            "Structures", "Structure and Functions", "Union",
            "File Handling Introduction", "File Read Write Operations", "Course Summary",
        ],
        "gtu-engineering-graphics-design-anp": [
            "Introduction to Engineering Graphics", "Drawing Instruments and Usage", "Types of Lines",
            "Lettering and Dimensioning", "Scales - Plain and Diagonal", "Conic Sections Introduction",
            "Ellipse Construction", "Parabola Construction", "Hyperbola Construction",
            "Cycloid and Involute", "Orthographic Projection Principles", "First Angle Projection",
            "Third Angle Projection", "Projection of Points", "Projection of Lines",
            "Line Inclined to One Plane", "Line Inclined to Both Planes", "Projection of Planes",
            "Plane Inclined to HP", "Plane Inclined to VP", "Projection of Solids",
            "Prism Projections", "Pyramid Projections", "Cylinder Projections",
            "Cone Projections", "Solids Inclined to One Plane", "Section of Solids Introduction",
            "Section of Prism", "Section of Pyramid", "Section of Cylinder",
            "Section of Cone", "Development of Surfaces", "Development of Prism",
            "Development of Cylinder", "Isometric Projection Principles", "Isometric View of Solids",
            "AutoCAD Introduction", "CAD Commands Basics", "Course Summary",
        ],
        "gtu-mathematics-1-pks": [
            "Course Introduction", "Indeterminate Forms 0/0", "Indeterminate Forms Infinity",
            "LHospitals Rule Advanced", "Taylor Series", "Maclaurin Series",
            "Taylor Series Problems", "Improper Integrals Type I", "Improper Integrals Type II",
            "Convergence Tests for Integrals", "Gamma Function", "Gamma Function Problems",
            "Beta Function", "Beta Function Problems", "Beta-Gamma Relation",
            "Applications of Beta Gamma", "Matrix Introduction", "Types of Matrices",
            "Matrix Addition and Multiplication", "Transpose and Properties", "Determinants",
            "Minors and Cofactors", "Properties of Determinants", "Adjoint and Inverse",
            "Rank of Matrix", "Echelon and Normal Form", "System of Equations - Consistent",
            "System of Equations - Inconsistent", "Cramers Rule", "Gauss Elimination",
            "Gauss Jordan Method", "Eigenvalues", "Eigenvectors",
            "Properties of Eigenvalues", "Cayley-Hamilton Theorem", "Cayley-Hamilton Problems",
            "Diagonalization", "Quadratic Forms", "Successive Differentiation",
            "nth Derivative Standard Results", "Leibnitz Theorem", "Leibnitz Problems",
            "Partial Differentiation", "Partial Derivatives of Higher Order", "Eulers Theorem",
            "Eulers Theorem Problems", "Total Derivative", "Chain Rule",
            "Jacobians", "Jacobian Problems", "Maxima and Minima Two Variables",
            "Lagrange Multipliers", "Double Integrals", "Change of Order of Integration",
            "Triple Integrals", "Applications of Multiple Integrals", "Sequences",
            "Series and Convergence", "Tests of Convergence", "Power Series",
            "Taylor and Maclaurin Series", "Fourier Series Introduction", "Fourier Series Problems",
            "Half Range Fourier Series", "Parsevals Theorem", "First Order ODE",
            "Course Revision and Summary",
        ],
        "gtu-chemistry-spj": [
            "Introduction to Engineering Chemistry", "Atomic Structure Review", "Chemical Bonding",
            "Electrochemistry Introduction", "Electrochemical Cells", "EMF of a Cell",
            "Nernst Equation", "Types of Electrodes", "Batteries and Fuel Cells",
            "Corrosion Introduction", "Types of Corrosion", "Galvanic Corrosion",
            "Factors Affecting Corrosion", "Corrosion Prevention Methods", "Protective Coatings",
            "Spectroscopy Introduction", "UV-Visible Spectroscopy", "IR Spectroscopy",
            "Applications of Spectroscopy", "Water Chemistry", "Hardness of Water",
            "Determination of Hardness", "Water Softening Methods", "Ion Exchange Process",
            "Reverse Osmosis", "Polymer Chemistry Introduction", "Types of Polymers",
            "Polymerization Reactions", "Addition Polymerization", "Condensation Polymerization",
            "Engineering Polymers", "Polymer Properties", "Fuels Introduction",
            "Classification of Fuels", "Calorific Value", "Solid Fuels",
            "Liquid Fuels", "Gaseous Fuels", "Lubricants",
            "Course Summary",
        ],
        "lju-sem2-mathematics-2-mmp": [
            "Vector Differentiation Introduction", "Gradient of a Scalar Field", "Directional Derivative",
            "Divergence of a Vector Field", "Curl of a Vector Field", "Vector Identities",
            "Line Integrals", "Surface Integrals", "Volume Integrals",
            "Greens Theorem", "Stokes Theorem", "Gauss Divergence Theorem",
            "Applications of Vector Calculus", "Complex Numbers Review", "Analytic Functions",
            "Cauchy-Riemann Equations", "Harmonic Functions", "Complex Integration",
            "Cauchys Integral Theorem", "Cauchys Integral Formula", "Taylors Series Complex",
            "Laurents Series", "Singularities and Residues", "Residue Theorem",
            "Applications of Residues", "Probability Introduction", "Conditional Probability",
            "Bayes Theorem", "Random Variables", "Probability Distributions",
            "Binomial Distribution", "Poisson Distribution", "Normal Distribution",
            "Mean and Variance", "Moments", "Correlation",
            "Regression", "Curve Fitting", "Method of Least Squares",
            "Numerical Solutions of Equations", "Bisection Method", "Newton-Raphson Method",
            "Regula Falsi", "Secant Method", "Fixed Point Iteration",
            "Gauss Elimination Numerical", "Gauss-Seidel Iterative Method", "LU Decomposition",
            "Numerical Integration", "Trapezoidal Rule", "Simpsons One-Third Rule",
            "Simpsons Three-Eighth Rule", "Eulers Method for ODE", "Modified Eulers Method",
            "Runge-Kutta Second Order", "Runge-Kutta Fourth Order", "Interpolation Introduction",
            "Newtons Forward Difference", "Newtons Backward Difference", "Course Summary",
        ],
    }

    # Generate generic lesson titles for courses not explicitly listed
    def generate_lesson_titles(course_title, num_lessons):
        """Generate numbered lesson titles for a given course"""
        titles = []
        for i in range(1, num_lessons + 1):
            titles.append(f"Lecture {i} - {course_title}")
        return titles

    all_lessons = []
    for course in courses:
        num = getattr(course, '_num_lessons', 10)
        slug = course.slug

        if slug in lesson_topics:
            titles = lesson_topics[slug][:num]
            # If fewer topics than lessons, pad with numbered lectures
            while len(titles) < num:
                titles.append(f"Lecture {len(titles)+1} - {course.title}")
        else:
            titles = generate_lesson_titles(course.title, num)

        for idx, title in enumerate(titles, 1):
            lesson = Lesson(
                course_id=course.id,
                order=idx,
                title=title,
                description=f"{title} - {course.title} | LJIET First Year Engineering",
                video_duration=1200 + (idx * 60) % 600,  # 20-30 min per lecture
                video_url=video_url
            )
            db.add(lesson)
            all_lessons.append(lesson)
        print(f"  ✓ Added {len(titles)} lessons for: {course.title}")

    db.commit()
    return all_lessons

def seed_users(db):
    """Create student and HOD user accounts"""
    print("\nSeeding student & HOD users...")

    student_user = User(
        email="24002170410016@mail.ljku.edu.in",
        full_name="Ayaz Khira",
        role=UserRole.STUDENT,
        bio="Enthusiastic learner passionate about technology and innovation.",
        major="Computer Engineering"
    )
    student_user.set_password("Student@2026")
    db.add(student_user)
    print(f"  ✓ Student User: {student_user.email}")

    hod_user = User(
        email="hod@mail.ljku.edu.in",
        full_name="Dr. Head of Department",
        role=UserRole.HOD,
        designation="Head of Department, Computer Science",
        bio="HOD - Computer Science Department, LJIET.",
        major="Computer Science"
    )
    hod_user.set_password("Hod@2026")
    db.add(hod_user)
    print(f"  ✓ HOD User: {hod_user.email}")

    additional_students = [
        {"email": "28002170410017@mail.ljku.edu.in", "full_name": "Priya Sharma", "bio": "Tech enthusiast.", "major": "IT"},
        {"email": "28002170410018@mail.ljku.edu.in", "full_name": "Rahul Patel", "bio": "Future engineer.", "major": "CE"},
        {"email": "28002170410019@mail.ljku.edu.in", "full_name": "Ananya Gupta", "bio": "Creative learner.", "major": "EC"},
        {"email": "28002170410020@mail.ljku.edu.in", "full_name": "Vikram Singh", "bio": "Focused student.", "major": "ME"},
        {"email": "28002170410021@mail.ljku.edu.in", "full_name": "Neha Reddy", "bio": "Aspiring developer.", "major": "CSE"},
        {"email": "28002170410022@mail.ljku.edu.in", "full_name": "Arjun Kumar", "bio": "Data enthusiast.", "major": "AI-ML"},
        {"email": "28002170410023@mail.ljku.edu.in", "full_name": "Sneha Patel", "bio": "Design lover.", "major": "CSD"},
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
        user.set_password("Student@2026")
        db.add(user)
        other_students.append(user)
        print(f"  ✓ Student User: {user.email}")

    db.commit()
    return student_user, other_students, hod_user

def seed_enrollments(db, students, courses):
    """Create course enrollments"""
    print("\nSeeding enrollments...")

    main_student = students[0]
    other_students = students[1:]
    enrollments = []

    # Enroll main student in first 4 courses
    for i, course in enumerate(courses[:4]):
        enrollment = Enrollment(
            student_id=main_student.id,
            course_id=course.id,
            enrolled_at=datetime.now() - timedelta(days=30-i*5),
            last_accessed=datetime.now() - timedelta(hours=12)
        )
        db.add(enrollment)
        enrollments.append(enrollment)
        print(f"  ✓ Enrolled {main_student.email} in: {course.title}")

    import random
    for student in other_students:
        num_courses = random.randint(2, 4)
        student_courses = random.sample(courses, min(num_courses, len(courses)))
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
    import random

    progress_count = 0
    for enrollment in enrollments:
        course = next(c for c in courses if c.id == enrollment.course_id)
        lessons = sorted(course.lessons, key=lambda l: l.order)

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
    print("Source: LJIET First Year Engineering YouTube Channel")
    print("="*60)

    print("\nRecreating database tables...")
    # Drop all tables and recreate (needed to remove old 'instructors' table)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    db = SessionLocal()

    try:
        clear_database(db)
        categories = seed_categories(db)
        instructors = seed_instructors(db)
        courses = seed_courses(db, categories, instructors)
        lessons = seed_lessons(db, courses)
        main_student, other_students, hod_user = seed_users(db)
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
        print(f"  • Students: {len(all_students)}")
        print(f"  • HOD: 1")
        print(f"  • Enrollments: {len(enrollments)}")
        print(f"\n🔐 Login Credentials:")
        print(f"  Student: 24002170410016@mail.ljku.edu.in / Student@2026")
        print(f"  Instructor (any): <initials>@mail.ljku.edu.in / Instructor@2026")
        print(f"  HOD: hod@mail.ljku.edu.in / Hod@2026")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
