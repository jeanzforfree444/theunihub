import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theunihub.settings')

django.setup()

import random
from django.contrib.auth.models import User
from main.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile, UNIVERSITY_CHOICES
from django.utils import timezone

def create_users():
    """Creates sample users and returns a list of user instances."""

    users = []
    
    user_data = [
        {'username': 'aaronhxx_1', 'first_name': 'Aaron', 'last_name': 'Hughes', 'email': 'aaron_hughes@outlook.com', 'password': 'GreenTree42#', 'staff': True, 'superuser': True, 'bio': 'I created the design for this website.', 'university': 'glasgow', 'school': 'Science & Engineering', 'department': 'Mathematics & Statistics', 'degree': 'Mathematics', 'start': 2023},
        {'username': 'euan_galloway', 'first_name': 'Euan', 'last_name': 'Galloway', 'email': 'euan_galloway@hotmail.com', 'password': 'MountainPeak57!', 'staff': True, 'superuser': False, 'bio': 'I helped with the marketing of this company!', 'university': 'edinburgh', 'school': 'Science & Engineering', 'department': 'Computing Science', 'degree': 'Software Engineering', 'start': 2023},
        {'username': 'phoebe6504', 'first_name': 'Phoebe', 'last_name': 'Hope', 'email': 'phoebe_hope@gmail.com', 'password': 'SunnySky12$', 'staff': True, 'superuser': False, 'bio': 'I was the lead developer of the website you are on right now.', 'university': 'strathclyde', 'school': 'Social Sciences', 'department': 'Business', 'degree': 'Accounting', 'start': 2023},
        {'username': 'urango123', 'first_name': 'Urangoo', 'last_name': 'Ganzorig', 'email': 'urangoo_ganzorig@live.com', 'password': 'OceanBreeze29&', 'staff': True, 'superuser': False, 'bio': 'The brains behind this websites system.', 'university': 'dundee', 'school': 'Health Sciences', 'department': 'Nursing', 'degree': 'Adult Nursing', 'start': 2024},
        {'username': 'grace.caskie21', 'first_name': 'Grace', 'last_name': 'Caskie', 'email': 'grace_caskie@icloud.com', 'password': 'RiverFlow63@', 'staff': False, 'superuser': False, 'bio': 'Switched my university and my degree and now I love being a student.', 'university': 'strathclyde', 'school': 'Life Sciences', 'department': 'Sports', 'degree': 'Sports Science', 'start': 2025},
        {'username': 'niamhm143', 'first_name': 'Niamh', 'last_name': 'McGee', 'email': 'niamh_mcgee@hotmail.co.uk', 'password': 'HappyDays84!', 'staff': False, 'superuser': False, 'bio': 'Everyone thinks my degree is easy because of my university but it really is not!', 'university': 'caledonian', 'school': 'Arts', 'department': 'English', 'degree': 'English Literature', 'start': 2022},
        {'username': 'katie.fraserxo', 'first_name': 'Katie', 'last_name': 'Fraser', 'email': 'katie_fraser@live.com', 'password': 'BlueWater21+', 'staff': False, 'superuser': False, 'bio': "I'm not just a pretty face but I'm also smart lol.", 'university': 'st_andrews', 'school': 'Life Sciences', 'department': 'Law', 'degree': 'Scots Law', 'start': 2023},
        {'username': 'amelie_c_x', 'first_name': 'Amelie', 'last_name': 'Carrigan', 'email': 'amelie_carrigan@outlook.co.uk', 'password': 'DesertRose88@', 'staff': False, 'superuser': False, 'bio': 'Trying to work it all out!', 'university': '', 'school': '', 'department': '', 'degree': '', 'start': 0},
        {'username': 'james_smith92', 'first_name': 'James', 'last_name': 'Smith', 'email': 'james_smith92@yahoo.com', 'password': 'MountainSun42!', 'staff': False, 'superuser': False, 'bio': 'A passionate electrical engineer.', 'university': 'glasgow', 'school': 'Science & Engineering', 'department': 'Engineering', 'degree': 'Electrical Engineering', 'start': 2022},
        {'username': 'isla_brown03', 'first_name': 'Isla', 'last_name': 'Brown', 'email': 'isla_brown03@icloud.com', 'password': 'AutumnLeaves56@', 'staff': False, 'superuser': False, 'bio': 'I enjoy reading and learning new things every day.', 'university': '', 'school': '', 'department': '', 'degree': '', 'start': 0},
        {'username': 'oscar_lee4', 'first_name': 'Oscar', 'last_name': 'Lee', 'email': 'oscar_lee4@hotmail.com', 'password': 'StormySky77$', 'staff': False, 'superuser': False, 'bio': 'Always striving to innovate and improve myself.', 'university': 'stirling', 'school': 'Science & Engineering', 'department': 'Engineering', 'degree': 'Mechanical Engineering', 'start': 2022},
        {'username': 'lucy_davies85', 'first_name': 'Lucy', 'last_name': 'Davies', 'email': 'lucy_davies85@gmail.com', 'password': 'WindyDay82$', 'staff': False, 'superuser': False, 'bio': 'Learning and growing one step at a time.', 'university': 'queens', 'school': 'Design', 'department': 'Interior Design', 'degree': 'Interior Design', 'start': 2023},
        {'username': 'jake_walker96', 'first_name': 'Jake', 'last_name': 'Walker', 'email': 'jake_walker96@aol.com', 'password': 'BrightSky21@', 'staff': False, 'superuser': False, 'bio': 'Tech enthusiast and aspiring entrepreneur.', 'university': 'napier', 'school': 'Technology', 'department': 'Computer Science', 'degree': 'Cybersecurity', 'start': 2025},
        {'username': 'ella_martin77', 'first_name': 'Ella', 'last_name': 'Martin', 'email': 'ella_martin77@gmail.com', 'password': 'SunnyBeach42!', 'staff': False, 'superuser': False, 'bio': 'Love to explore and learn new things.', 'university': 'qmu', 'school': 'Arts', 'department': 'Fine Arts', 'degree': 'Photography', 'start': 2022},
        {'username': 'noah_clark88', 'first_name': 'Noah', 'last_name': 'Clark', 'email': 'noah_clark88@outlook.com', 'password': 'CloudyDay21$', 'staff': False, 'superuser': False, 'bio': 'Music lover and avid coder.', 'university': 'edinburgh', 'school': 'Music', 'department': 'Engineering', 'degree': 'Sound Engineering', 'start': 2023},
        {'username': 'emily_russell44', 'first_name': 'Emily', 'last_name': 'Russell', 'email': 'emily_russell44@hotmail.com', 'password': 'OceanBreeze25@', 'staff': False, 'superuser': False, 'bio': 'Love solving problems and working on projects.', 'university': 'aberdeen', 'school': 'Engineering', 'department': 'Civil Engineering', 'degree': 'Structural Engineering', 'start': 2024},
        {'username': 'matthew_hall9', 'first_name': 'Matthew', 'last_name': 'Hall', 'email': 'matthew_hall9@icloud.com', 'password': 'GoldenSky43$', 'staff': False, 'superuser': False, 'bio': 'Tech lover and adventurer.', 'university': '', 'school': '', 'department': '', 'degree': '', 'start': 0},
        {'username': 'olivia_white55', 'first_name': 'Olivia', 'last_name': 'White', 'email': 'olivia_white55@gmail.com', 'password': 'GoldenSun23$', 'staff': False, 'superuser': False, 'bio': 'Exploring the world of data science and analytics.', 'university': 'cardiff', 'school': 'Technology', 'department': 'Data Science', 'degree': 'Cybersecurity', 'start': 2024},
        {'username': 'harry_green11', 'first_name': 'Harry', 'last_name': 'Green', 'email': 'harry_green11@aol.com', 'password': 'ForestWalk56@', 'staff': False, 'superuser': False, 'bio': 'Adventurer at heart, currently studying Engineering.', 'university': 'kcl', 'school': 'Arts', 'department': 'Fashion', 'degree': 'Textiles', 'start': 2025},
    ]

    for data in user_data:
    
        user, created = User.objects.get_or_create(username=data['username'], email=data['email'], is_staff=data['staff'], is_superuser=data['superuser'])
    
        if created:
            
            user.set_password(data['password'])
            
            user.save()
            
            profile = UserProfile.objects.create(
                user=user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                bio=data['bio'],
                university=data['university'],
                school=data['school'],
                department=data['department'],
                degree=data['degree'],
                start_year=data['start'],
                profile_picture="profile_pictures/default.jpg"
            )

            users.append(user)
    
    return users

def create_categories():
    """Creates sample categories."""

    categories = []

    category_data = [
        {"name": "Academics", "description": "Stay ahead in your university studies with expert insights, study techniques, and academic resources. Whether you need help with coursework, exam strategies, or time management, this category covers everything from essay writing tips to research methodologies. Learn how to maximise productivity, tackle tough subjects, and make the most of your academic journey. Engage with fellow students and faculty members to get advice, discuss study materials, and explore ways to enhance your learning experience."},
        {"name": "Accommodation", "description": "Finding the perfect place to live while studying can be challenging. This category covers everything about university accommodation, from dorm life and private rentals to tips on budgeting, dealing with landlords, and making your space feel like home. Learn about the best areas to live, how to handle housing applications, and ways to navigate shared living situations. Whether you're searching for a new place or need help with roommate conflicts, this section has all the advice you need."},
        {"name": "Career", "description": "Get ahead in your career journey with advice on internships, networking, job applications, and workplace skills. This category provides resources on CV writing, interview preparation, and building a strong professional portfolio. Discover insights from alumni, career coaches, and industry professionals to help you land your dream job. Whether you're exploring career options, looking for part-time work, or preparing for graduation, you'll find useful tips to boost your employability and confidence."},
        {"name": "Coding", "description": "For students passionate about programming, this category is dedicated to everything coding-related. Learn new programming languages, explore software development, and tackle real-world coding challenges. Whether you're a beginner learning Python or an advanced developer working on AI, you'll find tutorials, troubleshooting tips, and project ideas here. Engage with the coding community, share your experiences, and get support for your coursework, hackathons, and personal projects."},
        {"name": "Diversity", "description": "University life is enriched by diverse cultures, backgrounds, and perspectives. This category celebrates inclusivity, covering topics like equality, representation, and student experiences from all walks of life. Whether discussing cultural events, LGBTQ+ support, disability inclusion, or international student life, this space is for fostering understanding and creating a welcoming campus environment. Share your stories, raise awareness, and learn how universities promote diversity and inclusion."},
        {"name": "Events", "description": "Stay updated on the latest university events, from academic conferences and guest lectures to social gatherings and student activities. Whether you're looking for networking opportunities, career fairs, or entertainment on campus, this category keeps you informed. Learn how to organise your own events, join clubs, and make the most of university life by participating in activities that match your interests. Don't miss out on the biggest happenings in student life!"},
        {"name": "Fitness", "description": "Balancing university life with health and fitness is key to success. This category provides workout tips, sports recommendations, and advice on maintaining an active lifestyle. Whether you're looking for gym routines, home workouts, or ways to stay fit on a budget, you'll find motivation and expert guidance here. Learn about university sports clubs, fitness challenges, and how to stay healthy despite a busy academic schedule."},
        {"name": "Funding", "description": "Managing finances at university can be stressful, but this category offers guidance on scholarships, student loans, budgeting, and financial aid. Get tips on applying for grants, finding part-time jobs, and making your student budget stretch further. Learn about government funding, bursaries, and ways to reduce student debt. Whether you need help covering tuition fees or daily expenses, this section helps you take control of your finances and make smart money decisions."},
        {"name": "Health", "description": "Your health matters, and this category focuses on staying physically well while at university. Learn about nutrition, exercise, illness prevention, and campus health services. Get advice on maintaining a balanced lifestyle, handling common student health concerns, and accessing medical support when needed. Whether it's dealing with flu season, improving your diet, or understanding student health insurance, this section has you covered."},
        {"name": "Mental Wellbeing", "description": "University life can be overwhelming, and mental well-being is just as important as physical health. This category provides support and advice on handling stress, anxiety, and depression. Learn about mindfulness, self-care, and coping mechanisms to maintain emotional balance. Discover campus counseling resources, peer support networks, and real stories from students navigating mental health challenges. You're not alone—find guidance and encouragement here."},
        {"name": "Research", "description": "For students engaged in academic research, this category offers insights into conducting studies, writing research papers, and accessing scholarly resources. Whether you're working on a thesis, a group project, or an independent study, find guidance on methodologies, data analysis, and academic publishing. Learn how to collaborate with faculty, apply for research grants, and contribute to your field with groundbreaking discoveries."},
        {"name": "Studying", "description": "Mastering effective study techniques is crucial for academic success. This category provides tips on time management, note-taking strategies, and exam preparation. Learn about different study methods like active recall, spaced repetition, and Pomodoro techniques to boost retention and productivity. Discover resources for online learning, recommended study apps, and ways to stay focused in a distracting environment. Whether you're struggling with motivation, managing multiple deadlines, or looking for ways to improve concentration, this section offers practical advice to help you study smarter, not harder. Engage in discussions with fellow students, share your best practices, and explore new ways to make learning more efficient and enjoyable."},
        {"name": "Societies", "description": "University societies are a great way to meet new people, develop skills, and explore interests. This category highlights student-run clubs, from academic and cultural groups to hobby-based and professional organisations. Learn how to join, start, or lead a society and make the most of extracurricular activities. Whether you're into debating, gaming, volunteering, or music, discover opportunities to get involved and enhance your university experience."},
        {"name": "Tips & Help", "description": "University can be challenging, but this category is dedicated to providing practical advice for students. Whether you need help with study habits, productivity hacks, or general life skills, this section has all the guidance you need. Find tips on managing stress, staying organised, making friends, and handling university challenges. Whatever your question, this space is full of student-friendly advice and support."},
        {"name": "Travel Abroad", "description": "Studying or traveling abroad opens up a world of opportunities. This category covers student exchange programs, studying overseas, and travel tips for university breaks. Learn about scholarships for international study, visa applications, and cultural adaptation. Get recommendations on affordable travel, hidden destinations, and ways to make the most of your global experiences while balancing studies and finances."},
    ]
        
    for data in category_data:

        views = random.randint(400, 1200)
        
        category, created = Category.objects.get_or_create(name=data["name"], description=data["description"], views=views, points=random.randint(200, views))
        
        categories.append(category)
    
    return categories

def create_articles(users, categories):
    """Creates sample articles."""

    articles = []
    
    article_data = [
        {"category": "Academics","title": "Student Advisers: What Do They Do?","summary": "Student advisers play a crucial role in guiding students through their academic journey. Learn how they can help you with course selection, career advice, and more.","content": "Student advisers are dedicated professionals who assist students in navigating their academic paths. They provide guidance on course selection, degree requirements, and career planning. Advisers also help students overcome academic challenges and connect them with resources like tutoring or mental health services. Building a strong relationship with your adviser can significantly enhance your university experience.","university": ""},
        {"category": "Academics","title": "How to Ace Your Finals: Expert Tips","summary": "Struggling with finals? Discover expert tips to help you study effectively, manage stress, and perform your best during exam season.","content": "Finals can be overwhelming, but with the right strategies, you can ace them. Start by creating a study schedule that breaks down your material into manageable chunks. Use active learning techniques like flashcards and practice exams. Don’t forget to take breaks and prioritize sleep to keep your mind sharp. On exam day, stay calm, read questions carefully, and manage your time wisely. Remember, preparation is key to success!","university": ""},
        {"category": "Academics","title": "What Resources Does UoE Offer?","summary": "The University of Edinburgh (UoE) provides a wide range of academic resources to support student success. Find out what’s available to you.",
        "content": "The University of Edinburgh offers numerous resources to help students excel academically. These include libraries with extensive collections, online databases, and study spaces. The university also provides academic support services like writing centers, tutoring, and workshops on study skills. Additionally, students can access career services, mental health support, and technology resources. Make the most of these tools to enhance your learning experience.","university": "edinburgh"},
        {"category": "Accommodation","title": "How to Find the Perfect Student Accommodation","summary": "Finding the right student accommodation can be challenging. Learn how to evaluate your options and choose the best place to live during your studies.",
        "content": "When searching for student accommodation, consider factors like location, cost, and amenities. On-campus housing offers convenience and a sense of community, while private rentals provide more independence. Visit potential places in person or take virtual tours to get a feel for the space. Don’t forget to read reviews and check contracts carefully. Start your search early to secure the best options and make your university life comfortable.","university": ""},
        {"category": "Accommodation","title": "Campus vs. Private: What's Best for You?","summary": "Deciding between campus and private accommodation? Compare the pros and cons to find the best fit for your lifestyle and budget.","content": "Campus accommodation is ideal for students who want to be close to classes and university facilities. It often includes meal plans and a built-in social network. On the other hand, private accommodation offers more freedom and flexibility, allowing you to choose your location and housemates. However, it may require more responsibility for bills and maintenance. Consider your priorities, budget, and preferences to make the right choice.","university": ""
    },
    {
        "category": "Accommodation",
        "title": "Murano Accommodation: Quick Tour & Guide",
        "summary": "Murano Student Village is a popular accommodation option for University of Glasgow students. Here’s what you need to know about living there.",
        "content": "Murano Student Village is one of the largest student accommodations in Glasgow, offering a vibrant community for students. It features en-suite rooms, shared kitchens, and social spaces like common rooms and outdoor areas. Located just a short bus ride from the university, it provides easy access to campus and the city center. With regular events and a friendly atmosphere, Murano is a great place to meet new people and enjoy your university life.",
        "university": "glasgow"
    },
    {
        "category": "Career",
        "title": "Building a Strong CV: Tips for University Students",
        "summary": "A strong CV is essential for landing internships and jobs. Learn how to highlight your skills, experiences, and achievements effectively.",
        "content": "Your CV is your first impression on potential employers, so make it count. Start by tailoring your CV to the job or internship you’re applying for. Highlight relevant skills, experiences, and achievements, such as coursework, part-time jobs, or volunteer work. Use action verbs and quantify your accomplishments where possible. Keep the layout clean and professional, and proofread carefully for errors. A well-crafted CV can open doors to exciting opportunities.",
        "university": ""
    },
    {
        "category": "Career",
        "title": "How to Network Effectively as a Student",
        "summary": "Networking is a valuable skill for students. Discover tips on building professional relationships and expanding your career opportunities.",
        "content": "Networking can help you gain insights, advice, and job opportunities. Start by attending university events, career fairs, and industry conferences. Be proactive in introducing yourself and asking thoughtful questions. Follow up with new contacts via LinkedIn or email to maintain the connection. Remember, networking is about building genuine relationships, so focus on how you can help others as well. Over time, your network can become a powerful resource for your career.",
        "university": ""
    },
    {
        "category": "Career",
        "title": "Internships: How to Find the Right One for You",
        "summary": "Internships are a great way to gain experience and boost your career prospects. Learn how to find and secure the perfect internship.",
        "content": "Finding the right internship requires research and preparation. Start by identifying your career interests and goals. Use university career services, online job boards, and networking to discover opportunities. Tailor your application materials to each position, emphasizing relevant skills and experiences. Prepare for interviews by practicing common questions and researching the company. A successful internship can provide valuable experience and help you stand out in the job market.",
        "university": ""
    },
    {
        "category": "Coding",
        "title": "Introduction to AI: Everything You Need to Know",
        "summary": "Artificial Intelligence (AI) is transforming industries. Get started with this beginner-friendly guide to understanding AI and its applications.",
        "content": "AI refers to the simulation of human intelligence in machines. It includes technologies like machine learning, natural language processing, and computer vision. AI is used in various fields, from healthcare to finance, to automate tasks and analyze data. To get started with AI, learn programming languages like Python and explore online courses or tutorials. Understanding AI can open up exciting career opportunities and help you stay ahead in a tech-driven world.",
        "university": ""
    },
    {
        "category": "Coding",
        "title": "Python for Beginners: A Comprehensive Guide",
        "summary": "Python is one of the most popular programming languages. This guide will help beginners learn the basics and start coding in Python.",
        "content": "Python is known for its simplicity and versatility, making it ideal for beginners. Start by installing Python and setting up your development environment. Learn the basics, such as variables, loops, and functions, before moving on to more advanced topics like object-oriented programming and libraries. Practice by working on small projects or solving coding challenges. With its wide range of applications, Python is a valuable skill for anyone interested in coding.",
        "university": ""
    },
    {
        "category": "Coding",
        "title": "Building Your First Web App: A Step-by-Step Guide",
        "summary": "Ready to create your first web app? Follow this step-by-step guide to learn the basics of web development and build a functional app.",
        "content": "Building a web app involves several steps, from planning to deployment. Start by defining your app’s purpose and features. Learn the basics of HTML, CSS, and JavaScript for front-end development, and choose a back-end technology like Node.js or Django. Use frameworks like React or Angular to streamline development. Test your app thoroughly and deploy it using platforms like Heroku or AWS. With practice, you can create web apps that solve real-world problems.",
        "university": ""
    },
    {
        "category": "Diversity",
        "title": "Stirling Celebrates New Diversity Win",
        "summary": "The University of Stirling has been recognized for its commitment to diversity and inclusion. Learn about its latest achievements.",
        "content": "The University of Stirling has received accolades for its efforts to promote diversity and inclusion on campus. Initiatives include scholarships for underrepresented groups, cultural events, and support services for international students. The university also fosters an inclusive environment through training programs and policies that promote equality. These efforts have made Stirling a welcoming place for students from all backgrounds, enriching the campus community.",
        "university": "stirling"
    },
    {
        "category": "Diversity",
        "title": "Going International: Making the Most of Foreign Exchange",
        "summary": "Studying abroad is an exciting opportunity. Discover how to make the most of your foreign exchange experience.",
        "content": "Foreign exchange programs offer a chance to explore new cultures, learn languages, and gain global perspectives. Before you go, research your destination and prepare for cultural differences. Take advantage of academic opportunities and immerse yourself in local activities. Stay open-minded and build connections with people from diverse backgrounds. Studying abroad can be a transformative experience that enhances your personal and professional growth.",
        "university": "glasgow"
    },
    {
        "category": "Diversity",
        "title": "Pride: Building a More Inclusive Campus",
        "summary": "Universities are working to create more inclusive environments for LGBTQ+ students. Learn how campuses are celebrating Pride and promoting equality.",
        "content": "Pride events on campus celebrate LGBTQ+ identities and promote inclusivity. Universities are implementing policies to support LGBTQ+ students, such as gender-neutral facilities and anti-discrimination measures. Student organizations also play a key role in fostering a sense of community and advocating for change. By participating in Pride events and supporting LGBTQ+ initiatives, students can help create a more inclusive and welcoming campus environment.",
        "university": ""
    },
    {
        "category": "Events",
        "title": "How to Organise Your Own University Events",
        "summary": "Organizing university events can be rewarding. Follow these steps to plan and execute successful events on campus.",
        "content": "Organizing a university event requires careful planning and teamwork. Start by defining your event’s purpose and target audience. Secure a venue, budget, and necessary permissions. Promote your event through social media, posters, and word of mouth. On the day, coordinate with volunteers and ensure everything runs smoothly. After the event, gather feedback to improve future events. Hosting successful events can enhance campus life and build your organizational skills.",
        "university": ""
    },
    {
        "category": "Events",
        "title": "Upcoming Events You Can't Miss at Glasgow",
        "summary": "The University of Glasgow hosts a variety of exciting events. Check out what’s coming up and mark your calendar!",
        "content": "The University of Glasgow offers a vibrant events calendar, including academic lectures, cultural festivals, and social gatherings. Highlights include the annual Glasgow International Festival, career fairs, and student society events. Attending these events is a great way to meet new people, learn new skills, and make the most of your university experience. Stay updated by checking the university’s event website or following student organizations on social media.",
        "university": "glasgow"
    },
    {
        "category": "Events",
        "title": "The Benefits of Attending Networking Events as a Student",
        "summary": "Networking events are a valuable opportunity for students. Learn how they can help you build connections and advance your career.",
        "content": "Networking events provide a platform to meet professionals, alumni, and peers in your field. They offer insights into industry trends, career advice, and potential job opportunities. To make the most of these events, prepare an elevator pitch, bring business cards, and follow up with new contacts. Networking can help you build relationships that support your academic and professional goals, so don’t miss out on these opportunities.",
        "university": ""
    },
    {
        "category": "Fitness",
        "title": "Make The Most Of Your University Gym",
        "summary": "Your university gym is a great resource for staying fit. Discover tips for using it effectively and maintaining a healthy lifestyle.",
        "content": "University gyms offer a range of facilities, from cardio machines to group fitness classes. Start by creating a workout plan that fits your schedule and goals. Take advantage of free or discounted training sessions to learn proper techniques. Stay motivated by working out with friends or joining fitness challenges. Regular exercise can boost your energy, reduce stress, and improve your overall well-being, so make the most of your gym membership.",
        "university": ""
    },
    {
        "category": "Fitness",
        "title": "Home Workouts for Busy Students",
        "summary": "Struggling to find time for the gym? Try these home workout routines designed for busy students.",
        "content": "Home workouts are a convenient way to stay active, even with a packed schedule. Focus on bodyweight exercises like squats, push-ups, and planks that require no equipment. Use online videos or apps for guided routines. Even short, 20-minute sessions can be effective if done consistently. Incorporate stretching and mindfulness exercises to improve flexibility and reduce stress. With a little creativity, you can maintain a fitness routine that fits your lifestyle.",
        "university": ""
    },
    {
        "category": "Fitness",
        "title": "Top 5 University Sports Clubs You Should Join",
        "summary": "Joining a sports club is a great way to stay active and meet new people. Here are the top 5 clubs to consider at the University of St Andrews.",
        "content": "The University of St Andrews offers a wide range of sports clubs, from rugby to rowing. Joining a club is a fantastic way to stay fit, develop new skills, and make friends. Popular options include the football club, tennis club, and swimming club. Many clubs welcome beginners and offer training sessions. Participating in sports can also boost your mental health and provide a break from academic pressures. Explore your options and find a club that suits your interests.",
        "university": "st_andrews"
    },
    {
        "category": "Funding",
        "title": "How to Apply for Scholarships and Grants",
        "summary": "Scholarships and grants can ease the financial burden of university. Learn how to find and apply for these opportunities.",
        "content": "Start by researching scholarships and grants offered by your university, government, and private organizations. Check eligibility criteria and deadlines carefully. Prepare a strong application by highlighting your achievements, goals, and financial need. Write a compelling personal statement and gather recommendation letters. Applying for funding can be time-consuming, but the rewards are worth it. Scholarships and grants can help you focus on your studies without financial stress.",
        "university": ""
    },
    {
        "category": "Funding",
        "title": "Managing Your Student Budget: Tips and Tricks",
        "summary": "Managing your finances as a student can be challenging. Follow these tips to create a budget and save money.",
        "content": "Start by tracking your income and expenses to understand your spending habits. Create a budget that prioritizes essentials like rent and groceries. Look for ways to save, such as cooking at home or using student discounts. Avoid unnecessary expenses and consider part-time work or side hustles to boost your income. Sticking to a budget can help you avoid debt and make the most of your university experience.",
        "university": ""
    },
    {
        "category": "Funding",
        "title": "How to Find Part-Time Jobs as a Student",
        "summary": "Balancing work and studies can be tough, but part-time jobs offer valuable experience and income. Learn how to find the right job for you.",
        "content": "Start by looking for on-campus jobs, which often offer flexible hours. Check job boards, university career services, and local businesses for opportunities. Tailor your CV and cover letter to each position, emphasizing your skills and availability. Balance your work hours with your academic commitments to avoid burnout. A part-time job can provide financial support, work experience, and transferable skills for your future career.",
        "university": ""
    },
    {
        "category": "Health",
        "title": "Staying Healthy During University: A Student's Guide",
        "summary": "Maintaining your health is crucial for academic success. Discover tips for staying physically and mentally healthy during university.",
        "content": "University life can be demanding, but prioritizing your health is essential. Eat a balanced diet, exercise regularly, and get enough sleep. Stay hydrated and avoid excessive caffeine or junk food. Take breaks to relax and manage stress through mindfulness or hobbies. Don’t hesitate to seek help from university health services if you’re struggling. A healthy lifestyle can boost your energy, focus, and overall well-being.",
        "university": ""
    },
    {
        "category": "Health",
        "title": "Health Resources for Students: Where to Seek Help",
        "summary": "Universities offer a range of health resources to support students. Learn where to find help for physical and mental health concerns.",
        "content": "Most universities provide health services, including clinics, counseling, and wellness programs. These resources can help you address physical health issues, manage stress, or cope with mental health challenges. Don’t hesitate to reach out if you’re feeling overwhelmed. Many services are free or low-cost for students. Taking care of your health is a key part of succeeding in university and beyond.",
        "university": ""
    },
    {
        "category": "Health",
        "title": "The Importance of Sleep: How to Manage Your Schedule",
        "summary": "Sleep is essential for academic performance and overall health. Learn how to prioritize sleep and manage your schedule effectively.",
        "content": "Lack of sleep can negatively impact your focus, memory, and mood. Aim for 7-9 hours of sleep per night by creating a consistent bedtime routine. Avoid caffeine and screens before bed, and create a comfortable sleep environment. Manage your time effectively to balance academics, social life, and rest. Prioritizing sleep can improve your productivity, health, and overall university experience.",
        "university": ""
    },
    {
        "category": "Mental Wellbeing",
        "title": "Dealing with Stress and Anxiety During Exams",
        "summary": "Exams can be stressful, but there are ways to manage anxiety. Discover strategies to stay calm and perform your best.",
        "content": "Exam stress is common, but it can be managed with the right techniques. Start by preparing early and breaking your study material into manageable chunks. Practice relaxation techniques like deep breathing or meditation. Stay organized and avoid last-minute cramming. On exam day, stay positive and focus on doing your best. Remember, your worth is not defined by your grades.",
        "university": ""
    },
    {
        "category": "Mental Wellbeing",
        "title": "Mindfulness Practices to Calm Your Mind as a Student",
        "summary": "Mindfulness can help you stay focused and reduce stress. Learn simple practices to incorporate into your daily routine.",
        "content": "Mindfulness involves paying attention to the present moment without judgment. Start with short practices like deep breathing or body scans. Use apps or guided videos to help you get started. Incorporate mindfulness into everyday activities, such as eating or walking. Regular practice can improve your focus, reduce stress, and enhance your overall well-being. Give it a try and see the benefits for yourself.",
        "university": ""
    },
    {
        "category": "Mental Wellbeing",
        "title": "How to Maintain Your Mental Health During University",
        "summary": "University life can be challenging, but taking care of your mental health is essential. Discover tips for staying balanced and resilient.",
        "content": "Maintaining mental health during university requires self-care and support. Stay connected with friends and family, and don’t hesitate to seek help if you’re struggling. Practice stress management techniques like exercise, mindfulness, or journaling. Set realistic goals and take breaks when needed. Remember, it’s okay to ask for help, and many universities offer counseling services to support students.",
        "university": ""
    },
    {
        "category": "Research",
        "title": "How to Conduct Academic Research: A Beginner's Guide",
        "summary": "Academic research can be daunting for beginners. Follow this guide to learn the basics and get started on your research project.",
        "content": "Start by choosing a research topic that interests you and aligns with your academic goals. Conduct a literature review to understand existing research and identify gaps. Develop a research question and design a methodology to answer it. Collect and analyze data, then present your findings in a clear and structured manner. Seek feedback from professors or peers to improve your work. Research is a valuable skill that can enhance your academic and professional career.",
        "university": ""
    },
    {
        "category": "Research",
        "title": "Writing a Research Paper: Step-by-Step Process",
        "summary": "Writing a research paper requires careful planning and execution. Follow these steps to produce a high-quality paper.",
        "content": "Start by selecting a topic and conducting thorough research. Organize your findings and create an outline to structure your paper. Write a clear introduction, body, and conclusion, supported by evidence and citations. Revise your draft for clarity, coherence, and grammar. Finally, format your paper according to academic guidelines. Writing a research paper can be challenging, but with practice, you can develop strong research and writing skills.",
        "university": ""
    },
    {
        "category": "Research",
        "title": "Applying for Research Grants: What You Need to Know",
        "summary": "Research grants can fund your academic projects. Learn how to find and apply for grants successfully.",
        "content": "Research grants provide funding for academic projects, from fieldwork to lab experiments. Start by identifying grant opportunities through your university, government, or private organizations. Read the guidelines carefully and prepare a strong proposal that outlines your research question, methodology, and expected outcomes. Highlight the significance of your research and your qualifications. Applying for grants can be competitive, but persistence and preparation can pay off.",
        "university": "strathclyde"
    },
    {
        "category": "Studying",
        "title": "Mastering Time Management as a University Student",
        "summary": "Time management is key to academic success. Discover strategies to stay organized and make the most of your time.",
        "content": "Effective time management starts with setting clear goals and priorities. Use tools like planners or apps to schedule your tasks and deadlines. Break large tasks into smaller, manageable steps. Avoid procrastination by staying focused and minimizing distractions. Take regular breaks to recharge and maintain productivity. With good time management, you can balance academics, social life, and personal commitments more effectively.",
        "university": ""
    },
    {
        "category": "Studying",
        "title": "Best Study Apps to Help You Stay Organised",
        "summary": "Technology can enhance your study routine. Explore the best apps for note-taking, time management, and more.",
        "content": "There are many apps designed to help students stay organized and productive. Popular options include Evernote for note-taking, Trello for task management, and Forest for focus. Use flashcard apps like Quizlet for memorization and Pomodoro timers to manage study sessions. Experiment with different tools to find what works best for you. Incorporating technology into your study routine can boost your efficiency and help you achieve your academic goals.",
        "university": ""
    },
    {
        "category": "Studying",
        "title": "Exam Preparation Strategies for Success",
        "summary": "Preparing for exams doesn’t have to be stressful. Follow these strategies to study effectively and perform your best.",
        "content": "Start by creating a study plan that covers all your material and allows time for review. Use active learning techniques like summarizing, teaching others, or solving practice problems. Stay organized with notes and study guides. Take care of your physical and mental health by eating well, exercising, and getting enough sleep. On exam day, stay calm and confident, and trust in your preparation.",
        "university": ""
    },
    {
        "category": "Societies",
        "title": "How to Get Involved in University Societies",
        "summary": "University societies are a great way to meet people and pursue your interests. Learn how to get involved and make the most of your experience.",
        "content": "Joining a society is a fantastic way to enrich your university life. Start by exploring the wide range of societies available, from academic clubs to hobby groups. Attend introductory meetings or events to learn more. Don’t be afraid to try something new or take on a leadership role. Societies offer opportunities to develop skills, make friends, and have fun. Get involved and make the most of your time at university.",
        "university": "glasgow"
    },
    {
        "category": "Societies",
        "title": "Starting Your Own University Club: A Guide",
        "summary": "Have a unique interest? Start your own university club and bring like-minded students together. Here’s how to get started.",
        "content": "Starting a university club is a rewarding way to pursue your passions and build a community. Begin by identifying a niche or interest that isn’t already represented. Recruit members and establish a committee to share responsibilities. Register your club with the university and plan events or activities to engage members. Starting a club requires effort, but it can be a fulfilling experience that leaves a lasting impact on campus.",
        "university": "aberdeen"
    },
    {
        "category": "Tips & Help",
        "title": "How to Stay Organised in University: Tips and Tools",
        "summary": "Staying organized is essential for academic success. Discover tips and tools to manage your time, tasks, and responsibilities effectively.",
        "content": "Staying organized in university requires planning and discipline. Use tools like planners, calendars, or apps to keep track of deadlines and commitments. Break tasks into smaller steps and prioritize them. Keep your study space tidy and create a routine that works for you. Regularly review and adjust your plans to stay on track. With good organization, you can reduce stress and achieve your academic goals more easily.",
        "university": ""
    },
    {
        "category": "Tips & Help",
        "title": "Surviving Your First Year of University",
        "summary": "The first year of university can be overwhelming. Follow these tips to navigate the transition and make the most of your experience.",
        "content": "Starting university is an exciting but challenging time. Take time to adjust to your new environment and build a routine. Attend orientation events to meet people and learn about campus resources. Stay on top of your studies by attending lectures and staying organized. Don’t be afraid to ask for help if you’re struggling. With time, you’ll find your footing and make the most of your university journey.",
        "university": ""
    },
    {
        "category": "Travel Abroad",
        "title": "Studying Abroad: How to Find the Right Program",
        "summary": "Studying abroad is an exciting opportunity. Learn how to choose the right program and prepare for your international experience.",
        "content": "Studying abroad offers a chance to explore new cultures and gain global perspectives. Start by researching programs that align with your academic and personal goals. Consider factors like location, language, and cost. Apply early and prepare for the application process, including visas and funding. Once accepted, learn about your destination and plan for cultural differences. Studying abroad can be a life-changing experience that broadens your horizons.",
        "university": ""
    },
    {
        "category": "Travel Abroad",
        "title": "Top Travel Destinations for University Students",
        "summary": "Traveling is a great way to explore the world during university. Discover the top destinations for students on a budget.",
        "content": "University is a great time to travel and explore new places. Popular destinations for students include cities with rich history, vibrant cultures, and affordable costs. Consider places like Prague, Bangkok, or Barcelona. Look for student discounts on flights, accommodations, and attractions. Traveling can broaden your perspective, create lasting memories, and enhance your university experience. Start planning your next adventure today!",
        "university": ""
    },
    {
        "category": "Travel Abroad",
        "title": "How to Adjust to Life in a New Country While Studying",
        "summary": "Adjusting to life in a new country can be challenging. Learn tips for adapting to a new culture and making the most of your experience.",
        "content": "Moving to a new country for studies is an exciting but challenging experience. Start by learning about the local culture, language, and customs. Stay open-minded and embrace new experiences. Build a support network by connecting with other international students or joining clubs. Take care of your mental health and seek help if you’re feeling homesick or overwhelmed. With time, you’ll adapt and create a fulfilling life in your new home.",
        "university": ""
    }
]
    
    for data in article_data:
    
        category = Category.objects.get(name=data["category"])

        views = random.randint(300, 1100)
        
        article = Article.objects.create(
            category=category,
            title=data["title"],
            summary=data["summary"],
            content=data["content"],
            views=views,
            points=random.randint(100, views),
            author=random.choice(users),
            related_university=data["university"],
            created_on=timezone.now(),
        )
        articles.append(article)
    
    return articles

def create_comments(users, articles):
    """Creates sample comments for articles."""

    comments = []
    
    comment_data = [
        "Great article! Thanks for sharing.",
        "I found this very helpful.",
        "This topic is fascinating!",
        "Really insightful, I learned a lot.",
        "I totally agree with this!",
        "Could you expand on this point?",
        "This was exactly what I needed!",
        "Well written and very informative.",
        "I never thought about it this way before.",
        "Thanks for the tips!",
        "Excellent breakdown of the topic.",
        "I have a different perspective on this.",
        "Super helpful, appreciate it!",
        "Really made me think, thanks!",
        "This article is a must-read!",
        "I'll be sharing this with my friends.",
        "More articles like this, please!",
        "I have some questions, can you elaborate?",
        "Brilliant insights, well done!",
        "This answered so many of my questions.",
        "Such a well-organised article!",
        "Wish I had read this earlier!",
        "Can't wait to try this out!",
        "This makes so much sense now.",
        "Very useful, thanks for writing!",
        "I love how this is explained.",
        "One of the best reads today!",
        "I'll be bookmarking this for later.",
        "What are your thoughts on the latest updates?",
        "Can you recommend more resources on this?",
        "Interesting take, I hadn't considered that!",
        "This really resonated with me.",
        "Thanks for breaking this down so clearly.",
        "Incredibly well-researched piece!",
        "I'd love a follow-up on this topic.",
        "Good points, but I have some doubts.",
        "This cleared up my confusion!",
        "I struggled with this before, but now I get it.",
        "Looking forward to reading more from you!",
        "I just sent this to my group chat!",
        "Simple and straight to the point!",
        "Could you provide more examples?",
        "Fantastic read, keep up the great work!",
        "This gave me a new perspective.",
        "I'll apply this to my studies immediately!",
        "Well-structured and easy to understand.",
        "Your writing style makes learning fun!",
        "Just what I was looking for!",
        "Very eye-opening, thanks for sharing.",
        "You explained this better than my professor!"
    ]

    for article in articles:

        for _ in range(2):

            comment = Comment.objects.create(
                article=article,
                author=random.choice(users),
                content=random.choice(comment_data),
                written_on=timezone.now(),
            )

            comments.append(comment)

    additional_comments = 100 - (len(articles) * 2)

    for _ in range(additional_comments):

        comment = Comment.objects.create(
            article=random.choice(articles),
            author=random.choice(users),
            content=random.choice(comment_data),
            written_on=timezone.now(),
        )

        comments.append(comment)
    
    return comments

def create_forums():
    """Creates sample forums."""

    forums = []

    forum_data = [
        {"name": "UofG General Discussion", "description": "..."},
        {"name": "Freshers & Orientation", "description": "..."},
        {"name": "Course Advice & Module Selection", "description": "..."},
        {"name": "Study Tips & Exam Preparation", "description": "..."},
        {"name": "Housing & Accommodation", "description": "..."},
        {"name": "Job Recommendations", "description": "..."},
        {"name": "Sports & Arts Clubs", "description": "..."},
        {"name": "Mental Wellbeing Experiences", "description": "..."},
        {"name": "Travelling Abroad Advice", "description": "..."},
        {"name": "Library & Study Spaces", "description": "..."},
        {"name": "Campus Gossip", "description": "..."},
        {"name": "Finance, Loans & Budgeting", "description": "..."},
        {"name": "Essay Writing & Academic Skills", "description": "..."},
        {"name": "Placements & Vocation Advice", "description": "..."},
        {"name": "Student Politics & Activism", "description": "..."},
        {"name": "Science Discussions", "description": "..."},
        {"name": "Art, Music & Creative Projects", "description": "..."},
        {"name": "Cafes, Food & Nightlife", "description": "..."},
        {"name": "Roommate & Flatmate Finder", "description": "..."},
        {"name": "Coding Problems", "description": "..."},
        {"name": "UoE General Discussion", "description": "..."},
        {"name": "Starthclyde General Discussion", "description": "..."},
        {"name": "Dundee General Discussion", "description": "..."},
        {"name": "Stirling General Discussion", "description": "..."},
    ]

    for data in forum_data:
        
        forum = Forum.objects.create(name=data["name"], description=data["description"])
        
        forums.append(forum)

    return forums

def create_threads(users, forums):
    """Creates sample threads in forums."""

    threads = []

    thread_data = [
        {"title": "What's happening on campus this week?", "forum": "UofG General Discussion", "topic": "...", "university": "glasgow"},
        {"title": "Anyone else struggling with coursework?", "forum": "UofG General Discussion", "topic": "...", "university": "glasgow"},
        {"title": "Best places to study?", "forum": "UofG General Discussion", "topic": "...", "university": "glasgow"},
        {"title": "Freshers events worth going to?", "forum": "Freshers & Orientation", "topic": "...", "university": ""},
        {"title": "What to pack for uni?", "forum": "Freshers & Orientation", "topic": "...", "university": ""},
        {"title": "How to make friends as a fresher?", "forum": "Freshers & Orientation", "topic": "...", "university": ""},
        {"title": "Best electives to take?", "forum": "Course Advice & Module Selection", "topic": "...", "university": ""},
        {"title": "Is this module difficult?", "forum": "Course Advice & Module Selection", "topic": "...", "university": ""},
        {"title": "Switching courses—need advice!", "forum": "Course Advice & Module Selection", "topic": "...", "university": ""},
        {"title": "How do you prepare for exams?", "forum": "Study Tips & Exam Preparation", "topic": "...", "university": ""},
        {"title": "Best study techniques?", "forum": "Study Tips & Exam Preparation", "topic": "...", "university": ""},
        {"title": "Handling stress during exams?", "forum": "Study Tips & Exam Preparation", "topic": "...", "university": ""},
        {"title": "How do you find affordable housing?", "forum": "Housing & Accommodation", "topic": "...", "university": ""},
        {"title": "Private or uni accommodation?", "forum": "Housing & Accommodation", "topic": "...", "university": ""},
        {"title": "Flatmate horror stories", "forum": "Housing & Accommodation", "topic": "...", "university": ""},
        {"title": "Best part-time jobs for students?", "forum": "Job Recommendations", "topic": "...", "university": ""},
        {"title": "Balancing work and studies?", "forum": "Job Recommendations", "topic": "...", "university": ""},
        {"title": "Is on-campus work worth it?", "forum": "Job Recommendations", "topic": "...", "university": ""},
        {"title": "Best Irish clubs to join?", "forum": "Sports & Arts Clubs", "topic": "...", "university": "queens"},
        {"title": "How competitive are sports teams?", "forum": "Sports & Arts Clubs", "topic": "...", "university": ""},
        {"title": "Creative societies worth checking out?", "forum": "Sports & Arts Clubs", "topic": "...", "university": ""},
        {"title": "Dealing with academic stress?", "forum": "Mental Wellbeing Experiences", "topic": "...", "university": ""},
        {"title": "How to avoid burnout?", "forum": "Mental Wellbeing Experiences", "topic": "...", "university": ""},
        {"title": "Uni counselling services—any good?", "forum": "Mental Wellbeing Experiences", "topic": "...", "university": ""},
        {"title": "Best ways to save money as a student?", "forum": "Finance, Loans & Budgeting", "topic": "...", "university": ""},
        {"title": "Should I get a student loan?", "forum": "Finance, Loans & Budgeting", "topic": "...", "university": ""},
        {"title": "Part-time job or more study time?", "forum": "Finance, Loans & Budgeting", "topic": "...", "university": ""},
        {"title": "What are the best essay writing resources?", "forum": "Essay Writing & Academic Skills", "topic": "...", "university": ""},
        {"title": "How to reference properly?", "forum": "Essay Writing & Academic Skills", "topic": "...", "university": ""},
        {"title": "Avoiding plagiarism?", "forum": "Essay Writing & Academic Skills", "topic": "...", "university": ""},
        {"title": "Best places to eat on campus?", "forum": "Cafes, Food & Nightlife", "topic": "...", "university": ""},
        {"title": "Cheapest food spots for students?", "forum": "Cafes, Food & Nightlife", "topic": "...", "university": ""},
        {"title": "Best clubs & bars near uni?", "forum": "Cafes, Food & Nightlife", "topic": "...", "university": "edinburgh"},
        {"title": "Looking for a flatmate!", "forum": "Roommate & Flatmate Finder", "topic": "...", "university": ""},
        {"title": "How to find good roommates?", "forum": "Roommate & Flatmate Finder", "topic": "...", "university": ""},
        {"title": "Roommate red flags?", "forum": "Roommate & Flatmate Finder", "topic": "...", "university": ""},
        {"title": "Trouble debugging my Python script", "forum": "Coding Problems", "topic": "...", "university": ""},
        {"title": "Best websites to practice coding?", "forum": "Coding Problems", "topic": "...", "university": ""},
        {"title": "How to get better at Java?", "forum": "Coding Problems", "topic": "...", "university": ""},
        {"title": "Best cafes near campus?", "forum": "UoE General Discussion", "topic": "...", "university": "edinburgh"},
        {"title": "How's the workload at UoE?", "forum": "UoE General Discussion", "topic": "...", "university": "edinburgh"},
        {"title": "UoE freshers week—worth it?", "forum": "UoE General Discussion", "topic": "...", "university": "edinburgh"},
        {"title": "Strathclyde's best study spaces?", "forum": "Starthclyde General Discussion", "topic": "...", "university": "strathclyde"},
        {"title": "Best clubs at Strathclyde?", "forum": "Starthclyde General Discussion", "topic": "...", "university": "strathclyde"},
        {"title": "How good are Strathclyde lectures?", "forum": "Starthclyde General Discussion", "topic": "...", "university": "strathclyde"},
        {"title": "Best spots to hang out in Dundee?", "forum": "Dundee General Discussion", "topic": "...", "university": "dundee"},
        {"title": "UoD accommodation—worth it?", "forum": "Dundee General Discussion", "topic": "...", "university": "dundee"},
        {"title": "How's the social life in Dundee?", "forum": "Dundee General Discussion", "topic": "...", "university": "dundee"},
        {"title": "How difficult is Stirling coursework?", "forum": "Stirling General Discussion", "topic": "...", "university": "stirling"},
        {"title": "Best things to do in Stirling?", "forum": "Stirling General Discussion", "topic": "...", "university": "stirling"},
        {"title": "Stirling nightlife—how is it?", "forum": "Stirling General Discussion", "topic": "...", "university": "stirling"},
    ]

    for data in thread_data:

            forum = Forum.objects.get(name=data["forum"])

            thread = Thread.objects.create(
                forum=forum,
                title=data["title"],
                topic=data["topic"],
                related_university=data["university"],
                author=random.choice(users),
                started_on=timezone.now(),
            )

            threads.append(thread)

    return threads

def create_posts(users, threads):
    """Creates posts within threads."""

    posts = []

    post_data = [
        "I totally agree with this point! I've had a similar experience, and it's great to see others thinking the same way. Do you think this applies to all situations or just specific cases?",
        "Interesting perspective! I hadn't considered it that way before. Personally, I feel like there are some exceptions, but overall, this makes a lot of sense.",
        "Can someone explain this a bit more? I'm struggling to understand how this connects to the broader topic. Would appreciate any insights!",
        "I had the same issue last year, and this advice really helped me out. One thing I'd add is that it also depends on personal learning style. What worked for you?",
        "This is a great discussion! I think it's important to also consider the long-term impact of these choices. Has anyone here faced any unexpected consequences from going this route?",
        "I completely agree with what you're saying, but I do think there's another side to consider. What about cases where this doesn't apply? I'd love to hear different experiences.",
        "Great insights! I actually tried this approach, and it worked well for me. However, I did face some challenges along the way—has anyone else dealt with similar issues?",
        "I've read a lot about this topic, and there seems to be a divide in opinions. Some argue that this is the best approach, while others say it's not always practical. What do you think?",
        "I found this perspective really interesting! It reminds me of a similar discussion I had with my professor. We talked about how this approach can be both beneficial and risky, depending on the context.",
        "I'm not sure I completely agree, but I see where you're coming from. I had a different experience, but maybe that's because my situation was slightly different. Anyone else feel the same way?",
        "This is a well-thought-out argument! I'd love to see more examples of how this works in real-world situations. Has anyone applied this successfully?",
        "I think the key here is balance. Too much focus on one approach might not be ideal, but ignoring it completely isn't great either. It's all about finding what works best for you.",
        "This has been a hot topic lately, and I appreciate the insights shared here! Have any studies or reports backed this up? I'd be interested in reading more about it.",
        "I just tried this approach, and it's definitely helpful. However, I ran into some unexpected difficulties—any tips on overcoming them?",
        "This post really got me thinking! I never saw it from this angle before. It makes me wonder how this could be applied in different scenarios.",
        "I was skeptical at first, but after reading everyone's experiences, I'm starting to see the benefits. Thanks for the discussion—definitely gave me some food for thought!",
        "I completely understand where you're coming from. I had a similar experience, and it took me a while to figure out the best way forward. Sharing experiences like this is so valuable!",
        "I've read multiple viewpoints on this, and I think both sides have valid arguments. At the end of the day, it probably depends on the specific situation and the individuals involved.",
        "Great discussion! I think we often underestimate the impact of small choices in the long run. This is something worth thinking about more deeply.",
        "One thing I'd add is that this also depends on the environment you're in. A supportive environment makes this easier to implement, whereas a challenging one can make it much harder.",
        "I love how this thread is bringing different perspectives together! It really highlights how complex this issue is. There's no one-size-fits-all solution, but hearing experiences helps a lot.",
        "This approach is definitely effective in many cases, but I wonder if it holds up in high-pressure situations. Anyone have experience with this?",
        "I was just discussing this with a friend the other day! It's interesting how different people approach this problem. Some prefer a structured method, while others are more flexible.",
        "This is one of those things that seems simple at first but gets more complex the more you think about it. There are so many variables at play!",
        "I think the main takeaway here is that we should always be open to adapting. What works today might not work tomorrow, and staying flexible is key.",
        "I really appreciate this discussion! It's so helpful to hear from different perspectives. I wish more people talked about this aspect of the topic.",
        "This is actually quite similar to something I read in a book recently. The author made a strong case for this approach—might be worth checking out for anyone interested!",
        "I like the direction this conversation is going! It's refreshing to see people sharing both successes and challenges instead of just focusing on one side.",
        "I've seen people debate this before, but I think what really matters is how you apply it in real life. Theory is great, but experience makes the biggest difference.",
        "Great post! It made me reflect on my own experiences. I hadn't realized how much this topic had influenced my decisions over the years.",
        "I'd be curious to hear if anyone has tried a completely different approach and still ended up with similar results. Sometimes, different paths lead to the same outcome.",
        "I think the discussion here shows how important it is to consider different viewpoints before making a decision. You never know which perspective will be the most helpful.",
        "I've been following this discussion closely, and it's making me rethink my approach. I might give this method a try and see how it works for me.",
        "This was a great read! I feel like there are some key takeaways here that I'll definitely apply to my own situation.",
        "I appreciate everyone sharing their thoughts! It really helps to see different perspectives, especially from those with more experience in this area.",
        "It's always great to learn from other people's experiences. Even if I don't fully agree with everything, there's always something valuable to take away from discussions like this.",
        "I think one thing we can all agree on is that there's no perfect solution. Every approach has its strengths and weaknesses, and it's all about finding the right fit for you.",
        "I wasn't sure what to expect from this discussion, but it ended up being incredibly insightful! I'll definitely be taking some of these ideas into account moving forward.",
        "I love seeing discussions like this! It's so important to exchange ideas and challenge our own thinking from time to time.",
        "This has been a really helpful conversation. It's great to see so many different opinions and experiences being shared in one place.",
        "I hadn't considered this angle before, but now that I see it, it makes a lot of sense. It just goes to show how valuable discussions like this can be!",
        "I think it's easy to overlook this aspect, but it's actually one of the most important things to keep in mind. I appreciate this thread for bringing it up!",
        "I really appreciate this breakdown! It helped clarify some things I had been struggling to understand for a while.",
        "It's fascinating how something so simple on the surface can have so many different interpretations. That's why discussions like this are so valuable!",
        "I feel like this is one of those things that everyone talks about, but few people actually take the time to understand. This discussion is definitely shedding some light on it!",
        "I was looking for exactly this kind of discussion! It's been really helpful to see so many different perspectives on the same issue.",
        "I've been trying to figure this out for a while, and this discussion has helped clarify things for me. Thanks to everyone who contributed!",
        "One of the best discussions I've seen in a while! It's always great when people share their real-life experiences rather than just theories.",
        "I'll definitely be revisiting this thread in the future! There's so much good advice here that I want to take my time processing it all.",
    ]

    for thread in threads:
        
        for _ in range(2):
        
            post = Post.objects.create(
                thread=thread,
                author=random.choice(users),
                content=random.choice(post_data),
                likes=random.randint(50, 300),
                written_on=timezone.now(),
            )

            posts.append(post)

    additional_posts = 100 - (len(threads) * 2)

    for _ in range(additional_posts):
        
        post = Post.objects.create(
            thread=random.choice(threads),
            author=random.choice(users),
            content=random.choice(post_data),
            written_on=timezone.now(),
        )

        posts.append(post)
    
    return posts

def favourite_articles(users, articles):
    """Adds random articles to users' favourites."""

    for user in users:
        
        profile = user.userprofile
        
        fav_articles = random.sample(articles, k=random.randint(1, 10))
        
        profile.favourite_articles.set(fav_articles)

def save_threads(users, threads):
    """Adds random threads to users' saved."""

    for user in users:

        profile = user.userprofile

        fav_threads = random.sample(threads, k=random.randint(1, 10))

        profile.saved_threads.set(fav_threads)


def populate():
    """Main function to populate the database."""

    print("Populating TheUniHub database...")

    # Create users
    print("Creating users...")
    users = create_users()
    print(f"Created {len(users)} users.")

    # Create categories
    print("Creating categories...")
    categories = create_categories()
    print(f"Created {len(categories)} categories.")

    # Create articles
    print("Writing articles...")
    articles = create_articles(users, categories)
    print(f"Wrote {len(articles)} articles.")

    # Create comments
    print("Writing comments...")
    comments = create_comments(users, articles)
    print(f"Wrote {len(comments)} comments.")

    # Create forums
    print("Creating forums...")
    forums = create_forums()
    print(f"Created {len(forums)} forums.")

    # Create threads
    print("Starting threads...")
    threads = create_threads(users, forums)
    print(f"Started {len(threads)} threads.")

    # Create posts
    print("Writing posts...")
    posts = create_posts(users, threads)
    print(f"Wrote {len(posts)} posts.")

    # Add favourite articles
    print("Favourting articles...")
    favourite_articles(users, articles)
    print("Assigned favourite articles.")

    # Add saved threads
    print("Saving threads...")
    save_threads(users, threads)
    print("Assigned saved threads.")

    print("Database population complete.")

if __name__ == '__main__':
    
    populate()