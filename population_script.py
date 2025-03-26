import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theunihub.settings')

django.setup()

import random
from django.contrib.auth.models import User
from main.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile, UNIVERSITY_CHOICES
from django.utils import timezone

def create_users():
    """
    Create a set of sample users with associated profiles for testing purposes.

    This function generates a list of users with predefined data, including usernames, names, emails,
    passwords, and staff/superuser status. It also creates corresponding UserProfile instances with
    additional details such as bio, university, and academic information. Returns the list of created users.
    """

    users = []
    
    # Predefined user data with expanded details for realism
    user_data = [
        {'username': 'aaronhxx_1', 'first_name': 'Aaron', 'last_name': 'Hughes', 'email': 'aaron_hughes@outlook.com', 'password': 'GreenTree42#', 'staff': True, 'superuser': True, 'bio': 'I created the design for this website.', 'university': 'glasgow', 'school': 'Science & Engineering', 'department': 'Mathematics & Statistics', 'degree': 'Mathematics', 'start': 2023, 'profile_picture': 'profile_pictures/aaron.jpg'},
        {'username': 'euan_galloway', 'first_name': 'Euan', 'last_name': 'Galloway', 'email': 'euan_galloway@hotmail.com', 'password': 'MountainPeak57!', 'staff': True, 'superuser': False, 'bio': 'I helped with the marketing of this company!', 'university': 'edinburgh', 'school': 'Science & Engineering', 'department': 'Computing Science', 'degree': 'Software Engineering', 'start': 2023, 'profile_picture': 'profile_pictures/euan.jpeg'},
        {'username': 'phoebe6504', 'first_name': 'Phoebe', 'last_name': 'Hope', 'email': 'phoebe_hope@gmail.com', 'password': 'SunnySky12$', 'staff': True, 'superuser': False, 'bio': 'I was the lead developer of the website you are on right now.', 'university': 'strathclyde', 'school': 'Social Sciences', 'department': 'Business', 'degree': 'Accounting', 'start': 2023, 'profile_picture': 'profile_pictures/phoebe.jpeg'},
        {'username': 'worriless', 'first_name': 'Urangoo', 'last_name': 'Ganzorig', 'email': 'urangoo_ganzorig@live.com', 'password': 'OceanBreeze29&', 'staff': True, 'superuser': False, 'bio': 'The brains behind this websites system.', 'university': 'dundee', 'school': 'Health Sciences', 'department': 'Nursing', 'degree': 'Adult Nursing', 'start': 2024, 'profile_picture': 'profile_pictures/urangoo.jpeg'},
        {'username': 'ailsa_brown03', 'first_name': 'Ailsa', 'last_name': 'brown', 'email': 'alisa_brown@icloud.com', 'password': 'RiverFlow63@', 'staff': False, 'superuser': False, 'bio': 'Switched my university and my degree and now I love being a student.', 'university': 'strathclyde', 'school': 'Life Sciences', 'department': 'Sports', 'degree': 'Sports Science', 'start': 2025, 'profile_picture': 'profile_pictures/ailsa.jpeg'},
        {'username': 'niamhm143', 'first_name': 'Niamh', 'last_name': 'McGee', 'email': 'niamh_mcgee@hotmail.co.uk', 'password': 'HappyDays84!', 'staff': False, 'superuser': False, 'bio': 'Everyone thinks my degree is easy because of my university but it really is not!', 'university': 'caledonian', 'school': 'Arts', 'department': 'English', 'degree': 'English Literature', 'start': 2022, 'profile_picture': 'profile_pictures/niamh.jpeg'},
        {'username': 'katie.fraserxo', 'first_name': 'Katie', 'last_name': 'Fraser', 'email': 'katie_fraser@live.com', 'password': 'BlueWater21+', 'staff': False, 'superuser': False, 'bio': "I'm not just a pretty face but I'm also smart lol.", 'university': 'st_andrews', 'school': 'Life Sciences', 'department': 'Law', 'degree': 'Scots Law', 'start': 2023, 'profile_picture': 'profile_pictures/katie.jpeg'},
        {'username': 'amelie_c_x', 'first_name': 'Amelie', 'last_name': 'Carrigan', 'email': 'amelie_carrigan@outlook.co.uk', 'password': 'DesertRose88@', 'staff': False, 'superuser': False, 'bio': 'Trying to work it all out!', 'university': '', 'school': '', 'department': '', 'degree': '', 'start': 0, 'profile_picture': 'profile_pictures/amelie.jpeg'},
        {'username': 'james_smith92', 'first_name': 'James', 'last_name': 'Smith', 'email': 'james_smith92@yahoo.com', 'password': 'MountainSun42!', 'staff': False, 'superuser': False, 'bio': 'A passionate electrical engineer.', 'university': 'glasgow', 'school': 'Science & Engineering', 'department': 'Engineering', 'degree': 'Electrical Engineering', 'start': 2022, 'profile_picture': 'profile_pictures/james.jpeg'},
        {'username': 'oscar_lee4', 'first_name': 'Oscar', 'last_name': 'Lee', 'email': 'oscar_lee4@hotmail.com', 'password': 'StormySky77$', 'staff': False, 'superuser': False, 'bio': 'Always striving to innovate and improve myself.', 'university': 'stirling', 'school': 'Science & Engineering', 'department': 'Engineering', 'degree': 'Mechanical Engineering', 'start': 2022, 'profile_picture': 'profile_pictures/oscar.jpeg'},
        {'username': 'lucy_davies85', 'first_name': 'Lucy', 'last_name': 'Davies', 'email': 'lucy_davies85@gmail.com', 'password': 'WindyDay82$', 'staff': False, 'superuser': False, 'bio': 'Learning and growing one step at a time.', 'university': 'queens', 'school': 'Design', 'department': 'Interior Design', 'degree': 'Interior Design', 'start': 2023, 'profile_picture': 'profile_pictures/lucy.jpeg'},
        {'username': 'jake_walker96', 'first_name': 'Jake', 'last_name': 'Walker', 'email': 'jake_walker96@aol.com', 'password': 'BrightSky21@', 'staff': False, 'superuser': False, 'bio': 'Tech enthusiast and aspiring entrepreneur.', 'university': 'napier', 'school': 'Technology', 'department': 'Computer Science', 'degree': 'Cybersecurity', 'start': 2025, 'profile_picture': 'profile_pictures/jake.jpeg'},
        {'username': 'ella_martin77', 'first_name': 'Ella', 'last_name': 'Martin', 'email': 'ella_martin77@gmail.com', 'password': 'SunnyBeach42!', 'staff': False, 'superuser': False, 'bio': 'Love to explore and learn new things.', 'university': 'qmu', 'school': 'Arts', 'department': 'Fine Arts', 'degree': 'Photography', 'start': 2022, 'profile_picture': 'profile_pictures/ella.jpeg'},
        {'username': 'noah_clark88', 'first_name': 'Noah', 'last_name': 'Clark', 'email': 'noah_clark88@outlook.com', 'password': 'CloudyDay21$', 'staff': False, 'superuser': False, 'bio': 'Music lover and avid coder.', 'university': 'edinburgh', 'school': 'Music', 'department': 'Engineering', 'degree': 'Sound Engineering', 'start': 2023, 'profile_picture': 'profile_pictures/noah.jpeg'},
        {'username': 'emily_russell44', 'first_name': 'Emily', 'last_name': 'Russell', 'email': 'emily_russell44@hotmail.com', 'password': 'OceanBreeze25@', 'staff': False, 'superuser': False, 'bio': 'Love solving problems and working on projects.', 'university': 'aberdeen', 'school': 'Engineering', 'department': 'Civil Engineering', 'degree': 'Structural Engineering', 'start': 2024, 'profile_picture': 'profile_pictures/emily.jpeg'},
        {'username': 'matthew_hall9', 'first_name': 'Matthew', 'last_name': 'Hall', 'email': 'matthew_hall9@icloud.com', 'password': 'GoldenSky43$', 'staff': False, 'superuser': False, 'bio': 'Tech lover and adventurer.', 'university': '', 'school': '', 'department': '', 'degree': '', 'start': 0, 'profile_picture': 'profile_pictures/matthew.jpeg'},
        {'username': 'olivia_white55', 'first_name': 'Olivia', 'last_name': 'White', 'email': 'olivia_white55@gmail.com', 'password': 'GoldenSun23$', 'staff': False, 'superuser': False, 'bio': 'Exploring the world of data science and analytics.', 'university': 'cardiff', 'school': 'Technology', 'department': 'Data Science', 'degree': 'Cybersecurity', 'start': 2024, 'profile_picture': 'profile_pictures/olivia.jpeg'},
        {'username': 'harry_green11', 'first_name': 'Harry', 'last_name': 'Green', 'email': 'harry_green11@aol.com', 'password': 'ForestWalk56@', 'staff': False, 'superuser': False, 'bio': 'Adventurer at heart, currently studying Engineering.', 'university': 'kcl', 'school': 'Arts', 'department': 'Fashion', 'degree': 'Textiles', 'start': 2025, 'profile_picture': 'profile_pictures/harry.jpeg'},
    ]

    # Iterate through user data to create or retrieve users and their profiles
    for data in user_data:
    
        user, created = User.objects.get_or_create(username=data['username'], email=data['email'], is_staff=data['staff'], is_superuser=data['superuser'])
    
        if created:
            
            user.set_password(data['password']) # Securely set the user's password
            
            user.save()
            
            # Create a UserProfile with additional personal and academic details
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
                profile_picture=data['profile_picture'] # Default profile picture
            )

            users.append(user)
    
    return users

def create_categories():
    """
    Generate a variety of sample categories with detailed descriptions.

    Creates categories covering key aspects of university life, each with an expanded description to provide
    more context and value to users. Assigns random view and point counts for realism.
    """

    categories = []

    category_data = [
        {
            "name": "Academics", 
            "description": "Boost your academic performance with expert advice tailored for university students across the UK. This category dives deep into study techniques, revision strategies, and tools to excel in coursework and exams. From mastering complex subjects like quantum physics to crafting standout essays in literature, you’ll find resources here to sharpen your skills. Connect with peers to swap notes, discuss challenging topics, and get tips from those who’ve been there. Whether you’re aiming for a first-class degree or just trying to survive a tricky semester, this is your go-to hub for all things academic."
        },
        {
            "name": "Accommodation", 
            "description": "Navigating student housing can feel like a maze, but this category simplifies it all. Explore everything from university halls to private rentals, with detailed advice on budgeting, negotiating with landlords, and turning a cramped flat into a cosy home. Learn the ins and outs of tenancy agreements, how to spot a dodgy deal, and the best areas to live near your campus. Whether you’re sorting out bills with flatmates or dealing with noisy neighbours, this section offers practical solutions and real student stories to guide you through the housing jungle."
        },
        {
            "name": "Career", 
            "description": "Kickstart your professional journey with comprehensive career guidance designed for university students. This category covers crafting a cracking CV, nailing job interviews, and landing internships that set you apart. Get insider tips from alumni, career advisors, and industry pros on networking effectively and building a LinkedIn profile that shines. Whether you’re after part-time gigs to fund your studies or plotting your post-graduation path, you’ll find strategies here to boost your employability and step confidently into the working world."
        },
        {
            "name": "Coding", 
            "description": "Dive into the world of programming with a category tailored for coders at all levels. Whether you’re a fresher picking up Python or a final-year student tackling machine learning projects, this section offers tutorials, debugging tips, and project inspiration. Explore languages like Java, C++, and JavaScript, and get advice on everything from coding bootcamps to acing tech interviews. Join a community of student developers to share code snippets, troubleshoot errors, and collaborate on innovative ideas that could shape your future in tech."
        },
        {
            "name": "Diversity", 
            "description": "Celebrate the rich tapestry of university life with a category dedicated to diversity and inclusion. From cultural festivals to discussions on gender equality and disability access, this space explores how universities foster welcoming communities. Hear from international students, LGBTQ+ groups, and underrepresented voices sharing their journeys and challenges. Whether you’re keen to learn about global traditions, support inclusivity campaigns, or understand intersectionality, this category connects you with stories and resources that make campuses more vibrant and equitable."
        },
        {
            "name": "Events", 
            "description": "Never miss out on what’s happening with this lively category tracking university events across Scotland and beyond. From academic symposiums and career fairs to freshers’ balls and music gigs, we’ve got the lowdown on must-attend occasions. Learn how to plan your own events, promote them effectively, and get involved with student societies hosting everything from debates to charity fundraisers. Whether you’re a social butterfly or just looking to network, this section keeps you in the loop and ready to make unforgettable uni memories."
        },
        {
            "name": "Fitness", 
            "description": "Stay fit and energised amidst uni chaos with this category packed with fitness advice for students. Discover affordable workout plans—think gym sessions, park runs, or yoga in your room—tailored to tight schedules and tighter budgets. Get the scoop on joining uni sports teams, mastering home exercises, and eating right to fuel your body and brain. Whether you’re training for a marathon or just want to dodge the fresher’s 15, this section offers motivation, routines, and tips to keep you active and thriving."
        },
        {
            "name": "Funding", 
            "description": "Take control of your finances with this essential guide to student funding. Learn the nitty-gritty of applying for scholarships, managing loans, and stretching your budget to cover rent, books, and the odd pint. This category breaks down UK student finance options, bursary applications, and part-time job ideas that won’t derail your studies. From avoiding debt traps to scoring discounts, it’s all about empowering you to fund your uni years smartly and stress-free—because money worries shouldn’t hold you back."
        },
        {
            "name": "Health", 
            "description": "Keep your body in top shape with this category focused on physical health at university. Get practical advice on eating well on a student budget, dodging freshers’ flu, and making the most of campus health services. Learn how to spot early signs of illness, manage minor ailments, and navigate NHS appointments as a student. Whether it’s tips on hydration or surviving late-night study sessions, this section helps you prioritise wellness so you can tackle uni life with energy and resilience."
        },
        {
            "name": "Mental Wellbeing", 
            "description": "University can test your mental resilience, but this category is here to support your emotional health. Explore strategies for managing stress, anxiety, and homesickness with advice on mindfulness, relaxation techniques, and building a support network. Discover uni counselling services, peer-led groups, and real student experiences that show you’re not alone. Whether it’s coping with exam pressure or finding balance, this space offers tools and encouragement to nurture your mental wellbeing throughout your academic journey."
        },
        {
            "name": "Research", 
            "description": "Unlock the secrets of academic research with this category for curious minds. Perfect for undergrads dipping into projects or postgrads crafting theses, it covers research design, literature reviews, and data crunching. Learn how to secure funding, collaborate with lecturers, and present findings that impress. From lab experiments to social surveys, this section equips you with skills and resources to push boundaries in your field and make a mark in academia."
        },
        {
            "name": "Studying", 
            "description": "Elevate your study game with this comprehensive category on effective learning. Packed with proven methods like active recall, mind mapping, and time-blocking, it’s your toolkit for smashing exams and assignments. Get app recommendations, tackle procrastination, and find quiet study nooks on campus. Whether you’re juggling lectures or cramming for finals, connect with students sharing their best hacks to help you work smarter, not harder, and enjoy the process along the way."
        },
        {
            "name": "Societies", 
            "description": "Supercharge your uni experience with societies, and this category shows you how. Dive into student-led groups spanning everything from robotics to salsa dancing, with tips on joining, leading, or even starting your own. Discover how societies boost your CV, forge lifelong friendships, and let you unwind from academic grind. Whether you’re into politics, baking, or cosplay, this is your guide to finding your tribe and making uni more than just lectures."
        },
        {
            "name": "Tips & Help", 
            "description": "Tackle uni challenges head-on with this treasure trove of practical advice. From sorting your timetable to surviving group projects, this category offers hacks for every student scenario. Learn how to cook on a budget, mend a broken laptop charger, or negotiate with a stingy landlord. It’s a mix of life skills, uni-specific wisdom, and peer support to ensure you thrive—not just survive—throughout your degree."
        },
        {
            "name": "Travel Abroad", 
            "description": "Broaden your horizons with this category on studying and travelling abroad. Get the full scoop on exchange programmes, visa headaches, and packing for a semester overseas. Explore budget-friendly destinations, cultural dos and don’ts, and funding options to make it happen. Whether you’re eyeing a term in Tokyo or a summer in Seville, this section inspires and equips you to embrace global adventures while balancing your studies."
        },
    ]
    
    # Create or retrieve categories with random engagement metrics
    for data in category_data:

        views = random.randint(400, 1200)
        
        category, created = Category.objects.get_or_create(name=data["name"], description=data["description"], views=views, points=random.randint(200, views))
        
        categories.append(category)
    
    return categories

def create_articles(users, categories):
    """
    Generate sample articles linked to categories and authored by users.

    Creates articles with expanded summaries and content to provide more detailed insights. Assigns random
    authors from the user list, view counts, and points to simulate engagement.
    """

    articles = []
    
    article_data = [
        {
            "category": "Academics",
            "title": "Student Advisers: What Do They Do?",
            "summary": "Unsure about what a student adviser can offer? This article explores their vital role in supporting your academic and personal growth at university, from course planning to wellbeing guidance.",
            "content": "Student advisers are unsung heroes in the university ecosystem, offering tailored support to help you thrive. They assist with choosing modules that align with your career goals, deciphering degree requirements, and even advising on resits or extensions. Beyond academics, they connect you to wellbeing resources like counselling or study skills workshops. Regular check-ins can turn them into a mentor, helping you navigate everything from tricky coursework to post-graduation plans. Building that rapport could be the key to unlocking your full potential at uni.",
            "university": ""
        },
        {
            "category": "Academics",
            "title": "How to Ace Your Finals: Expert Tips",
            "summary": "Finals looming and feeling the pressure? This article shares expert strategies to revise smarter, stay calm, and smash your exams with confidence.",
            "content": "Finals season doesn’t have to be a nightmare if you’ve got a solid game plan. Kick off by mapping out a revision timetable—split your topics into bite-sized chunks and tackle them daily. Techniques like active recall (testing yourself) and spaced repetition beat passive re-reading hands down. Take 5-minute breaks every hour to avoid burnout, and prioritise sleep—cramming all night rarely works. On the big day, skim the paper first, allocate time per question, and don’t panic if you blank—just move on and circle back. With preparation and poise, you’ll ace it!",
            "university": ""
        },
        {
            "category": "Academics",
            "title": "What Resources Does UoE Offer?",
            "summary": "Curious about what the University of Edinburgh has up its sleeve? Dive into the wealth of academic and support resources available to give your studies a boost.",
            "content": "The University of Edinburgh (UoE) is a treasure trove of resources waiting to be tapped. Its libraries house millions of books, journals, and digital archives—perfect for essay research or dissertation prep. Beyond that, the Academic Skills Centre offers workshops on essay writing and critical thinking, while peer tutoring can rescue you from calculus conundrums. Career services dish out CV advice, and mental health support is just a drop-in away. Whether you’re after quiet study pods or cutting-edge software, UoE’s got your back—explore and make the most of it!",
            "university": "edinburgh"
        },
        {
            "category": "Accommodation",
            "title": "How to Find the Perfect Student Accommodation",
            "summary": "Stressed about where to live during uni? This guide walks you through finding a place that suits your budget, lifestyle, and study needs without the hassle.",
            "content": "Picking the right student digs is a big deal—get it wrong, and you’re stuck with a leaky flat or a two-hour commute. Start by weighing up location: close to campus saves time, but city centre spots might offer better nightlife. Halls are a safe bet for freshers—utilities included, instant mates—but private rentals give you freedom (and maybe a garden). Set a budget, factoring in rent, bills, and Wi-Fi, then scour listings on sites like Rightmove or uni portals. Visit in person if you can, check for damp, and read the tenancy fine print. Start early—good places go fast!",
            "university": ""
        },
        {
            "category": "Accommodation",
            "title": "Campus vs. Private: What's Best for You?",
            "summary": "Torn between uni halls and a private flat? Compare the perks and pitfalls of each to find your ideal home-away-from-home.",
            "content": "Choosing between campus and private accommodation is a classic student dilemma. Halls put you in the thick of it—steps from lectures, built-in socials, and no faffing with bills or dodgy landlords. But they can be noisy, and rules might cramp your style. Private rentals offer space, quiet, and the chance to pick your flatmates—ideal if you’re after independence. The catch? You’re sorting utilities, repairs, and maybe a longer trek to class. Weigh your priorities: convenience or control? Budget or vibe? Test both waters if you can—your perfect pad depends on you.",
            "university": ""
        },
        {
            "category": "Accommodation",
            "title": "Murano Accommodation: Quick Tour & Guide",
            "summary": "Thinking of staying at Murano Student Village in Glasgow? Get the full scoop on what life’s like in this buzzing uni hotspot.",
            "content": "Murano Student Village is a cornerstone of University of Glasgow living, housing hundreds in a lively, student-centric setup. Expect en-suite rooms with decent storage, shared kitchens for late-night chats, and communal spaces—think study lounges and a courtyard for sunny days. It’s a 15-minute bus to campus or a brisk walk if you’re keen, with shops and takeaways nearby. Regular socials like quiz nights or film marathons keep the vibe buzzing, though thin walls mean earplugs might be handy. It’s not plush, but it’s a cracking spot to start your uni adventure.",
            "university": "glasgow"
        },
        {
            "category": "Career",
            "title": "Building a Strong CV: Tips for University Students",
            "summary": "Need a CV that stands out to employers? This article offers top tips to showcase your skills and experience, tailored for uni students looking to impress.",
            "content": "Your CV is your ticket to internships, part-time jobs, or that dream graduate role—so make it brilliant. Start with a clean layout: name at the top, then sections for education, experience, and skills. Tailor it to each gig—highlight that barista job for teamwork or a group project for problem-solving. Use punchy verbs like ‘organised’ or ‘delivered’, and chuck in numbers where you can (e.g., ‘boosted sales by 20%’). Keep it to one page, proofread for typos, and get a mate to check it. A cracking CV opens doors—start building yours now!",
            "university": ""
        },
        {
            "category": "Career",
            "title": "How to Network Effectively as a Student",
            "summary": "Networking can feel daunting, but it’s a game-changer for your career. Learn how to build connections at uni that last beyond graduation.",
            "content": "Networking isn’t just for suits—it’s a student superpower. Hit up uni career fairs, guest lectures, or society events to meet industry folk and alumni. Prep a quick intro—‘Hi, I’m studying X and keen on Y’—and ask smart questions like ‘What’s your top tip for breaking into this field?’ Swap details or connect on LinkedIn after, then follow up with a polite ‘Great to meet you’ message. It’s not about begging for jobs; it’s building genuine links. Start small, stay curious, and watch your network grow into a career goldmine.",
            "university": ""
        },
        {
            "category": "Career",
            "title": "Internships: How to Find the Right One for You",
            "summary": "Want hands-on experience to boost your CV? This guide helps you hunt down internships that match your goals and get you career-ready.",
            "content": "Internships are your fast track to real-world skills and employer nods. First, figure out what you want—marketing? Tech? Something niche? Check uni career portals, sites like Indeed, or even cold-email companies you fancy. Tailor your CV and cover letter—show passion, not just grades. Ace the interview by researching the firm and rehearsing answers to ‘Why us?’ or ‘Tell us about a challenge you’ve faced.’ Be flexible with hours or remote options, and don’t shy from small firms—experience trumps prestige. Land one, and you’re steps ahead post-uni.",
            "university": ""
        },
        {
            "category": "Coding",
            "title": "Introduction to AI: Everything You Need to Know",
            "summary": "Fascinated by artificial intelligence? This beginner’s guide unpacks AI basics, its real-world uses, and how to dip your toes into this exciting field.",
            "content": "Artificial Intelligence (AI) is everywhere—think Netflix recommendations or self-driving cars. It’s machines mimicking human smarts, using tricks like machine learning (teaching systems with data) or natural language processing (chatbots that actually get you). Start with Python—it’s the go-to language—via freebies like Codecademy or Coursera. Try a simple project, like a film predictor, to see AI in action. It’s not all sci-fi; it’s problem-solving with code. Dive in, experiment, and you could be shaping the future—AI’s a massive uni skill to nab.",
            "university": ""
        },
        {
            "category": "Coding",
            "title": "Python for Beginners: A Comprehensive Guide",
            "summary": "New to coding? This article takes you through Python’s basics step-by-step, making it easy for any uni student to start programming.",
            "content": "Python’s the coding world’s golden child—simple, versatile, and beginner-friendly. Download it free, grab an editor like VS Code, and you’re off. Start with variables (storing data like numbers or text), then loops (repeating tasks) and functions (chunking code). Build a calculator or quiz game to test your chops. Stuck? Google’s your mate, and forums like Stack Overflow save lives. Python powers everything from web apps to data analysis—learn it at uni, and you’re sorted for projects, jobs, or just impressing your mates.",
            "university": ""
        },
        {
            "category": "Coding",
            "title": "Building Your First Web App: A Step-by-Step Guide",
            "summary": "Dream of creating your own web app? Follow this clear, student-friendly guide to go from zero to a working app, no experience needed.",
            "content": "Building a web app sounds daunting, but it’s doable with the right steps. Pick a goal—say, a to-do list app. Learn HTML for structure, CSS for style, and JavaScript for interactivity—free tutorials on W3Schools are ace. Add a back-end with Python’s Django or Node.js to handle data (think user logins). Use GitHub to store your code and Heroku to launch it live. Test it with mates, tweak bugs, and boom—you’ve got a portfolio piece. It’s a uni project that screams ‘hire me’ to tech recruiters!",
            "university": ""
        },
        {
            "category": "Diversity",
            "title": "Stirling Celebrates New Diversity Win",
            "summary": "The University of Stirling’s latest diversity award is big news. Find out how they’re leading the charge for an inclusive campus.",
            "content": "Stirling Uni’s just nabbed a diversity gong, and it’s well-earned. They’ve rolled out scholarships for underrepresented students, from low-income locals to refugees, plus cultural bashes like Diwali and Pride that pack out the atrium. Training for staff and students tackles bias head-on, while support hubs help international freshers settle in. It’s not just talk—policies like flexible assessments for disabled students show real impact. Stirling’s proving diversity isn’t a buzzword; it’s the backbone of a cracking uni community. Get involved and see it for yourself!",
            "university": "stirling"
        },
        {
            "category": "Diversity",
            "title": "Going International: Making the Most of Foreign Exchange",
            "summary": "Dreaming of studying abroad? This article shares how Glasgow students can max out their foreign exchange experience, from prep to living it up overseas.",
            "content": "A foreign exchange through the University of Glasgow is your ticket to a global adventure. Pick a spot—maybe Paris or Sydney—via the uni’s partner list, then nail the application with a solid personal statement. Prep wise, sort your visa early, brush up on basic lingo, and pack light but smart (plug adapters are gold). Once there, dive in—join local clubs, try the food, and don’t just stick with Brits. It’s a chance to grow, network, and spice up your CV. Glasgow makes it easy—grab it with both hands!",
            "university": "glasgow"
        },
        {
            "category": "Diversity",
            "title": "Pride: Building a More Inclusive Campus",
            "summary": "How are unis championing LGBTQ+ inclusion? This piece explores Pride events and policies making campuses safer and prouder for all.",
            "content": "Pride isn’t just a party—it’s a movement reshaping uni life. Campuses across the UK host rainbow-flag-filled weeks with talks, film nights, and marches, spotlighting LGBTQ+ voices. Beyond the glitter, unis are stepping up with gender-neutral loos, anti-bullying rules, and societies like QueerSoc offering safe spaces. Students lead the charge—think petitions for trans rights or ally training. It’s about belonging, not just tolerance. Join in, whether you’re out or an ally—every campus can be a bit prouder with your help.",
            "university": ""
        },
        {
            "category": "Events",
            "title": "How to Organise Your Own University Events",
            "summary": "Fancy running your own uni bash? This guide breaks down planning and pulling off events that students will rave about.",
            "content": "Organising a uni event—be it a quiz, gig, or debate—is a buzz worth chasing. Start with a clear idea: what’s the vibe, who’s it for? Book a free campus room or bar, then pitch it to your students’ union for funding or kit like mics. Spread the word—posters, Insta stories, group chats—and rope in mates to help on the day. Keep it simple: snacks, a playlist, and a loose schedule work wonders. Post-event, ask what rocked or flopped. It’s a CV booster and a laugh—go for it!",
            "university": ""
        },
        {
            "category": "Events",
            "title": "Upcoming Events You Can't Miss at Glasgow",
            "summary": "Glasgow’s event scene is buzzing—don’t miss out! Check out the must-see happenings at the University of Glasgow this term.",
            "content": "The University of Glasgow keeps your calendar packed. Think guest lectures from big names in science, the Freshers’ Fayre with freebies galore, or the GUU’s legendary ceilidhs—kilts optional but encouraged. The Glasgow International Comedy Fest spills onto campus too, plus career fairs linking you with top firms. Check the uni’s online hub or follow @UofGEvents on Twitter for dates. Whether you’re into learning, laughing, or landing a job, these events are your chance to shine and unwind—don’t sleep on them!",
            "university": "glasgow"
        },
        {
            "category": "Events",
            "title": "The Benefits of Attending Networking Events as a Student",
            "summary": "Not sure if networking events are worth your time? Discover how they can connect you to opportunities and turbocharge your uni experience.",
            "content": "Networking events are gold dust for students—think career fairs, alumni mixers, or industry panels. You’ll meet pros who’ve been where you are, ready to spill advice on breaking into their field. Prep a 30-second ‘who I am’ pitch, bring a notebook (or your phone), and ask stuff like ‘What skills do I need most?’ Follow up with a quick LinkedIn add—‘Loved your chat on X!’—and you’ve got a contact for life. It’s not just jobs; it’s confidence, insights, and mates. Hit one up—you’ll thank yourself later.",
            "university": ""
        },
        {
            "category": "Fitness",
            "title": "Make The Most Of Your University Gym",
            "summary": "Got a uni gym membership going to waste? This article shows you how to use it to stay fit, de-stress, and feel ace on a student budget.",
            "content": "Your uni gym’s a hidden gem—cheap (or free) and packed with kit to keep you moving. Start with a plan: 30 minutes thrice a week—treadmill sprints, weights, or a spin class if they’ve got one. Most offer free intros with trainers—book one to nail your form. Drag a mate along for motivation or join a uni challenge (think ‘10k steps a day’). It’s not just physical—sweating it out blasts exam stress too. Check your uni’s gym timetable online and dive in—fitness doesn’t get easier than this!",
            "university": ""
        },
        {
            "category": "Fitness",
            "title": "Home Workouts for Busy Students",
            "summary": "No time for the gym? These quick, equipment-free home workouts fit into your hectic uni life and keep you in tip-top shape.",
            "content": "Busy with lectures and deadlines? Home workouts are your saviour—no kit, no excuses. Try a 20-minute blast: 10 squats, 10 press-ups, and a 30-second plank—repeat five times. YouTube’s bursting with free HIIT or yoga vids—pick one and follow along. Chuck in a stretch sesh to unwind after essays. No space? Even a corner of your room works. It’s cheap, flexible, and beats the fresher’s flab. Stick with it thrice weekly, and you’ll feel fitter, sharper, and ready to tackle anything uni throws at you.",
            "university": ""
        },
        {
            "category": "Fitness",
            "title": "Top 5 University Sports Clubs You Should Join",
            "summary": "Love sport? This rundown of St Andrews’ top five sports clubs shows you where to get active, make mates, and shine on the field.",
            "content": "The University of St Andrews serves up sports clubs for every taste—here’s the cream of the crop. The Rugby Club’s fierce but friendly, with training for all levels. Netball’s a fast-paced fave, mixing fun with fitness. Rowing’s hardcore—early river sessions, epic team spirit. Badminton’s chill but competitive, perfect for a quick sweat. And the Golf Club? You’re in the home of golf—casual rounds or tourneys, it’s unreal. Most welcome newbies—check their Freshers’ Week stalls or Insta. Join up, and you’ll score fitness, pals, and bragging rights!",
            "university": "st_andrews"
        },
        {
            "category": "Funding",
            "title": "How to Apply for Scholarships and Grants",
            "summary": "Cash-strapped at uni? This guide unravels how to snag scholarships and grants to ease the financial squeeze.",
            "content": "Scholarships and grants are free money—don’t sleep on them. Start with your uni’s website—most list awards for grades, sports, or hardship. Check SAAS for Scottish students or external sites like The Scholarship Hub. Read the rules: some need essays, others proof of need. Write a cracking personal statement—why you, why now?—and nab a lecturer’s reference. Apply early—deadlines sneak up. It’s a slog, but bagging £500 or £5,000 cuts loan stress and buys you breathing room. Get hunting—your wallet will thank you!",
            "university": ""
        },
        {
            "category": "Funding",
            "title": "Managing Your Student Budget: Tips and Tricks",
            "summary": "Struggling to stretch your loan? Learn savvy budgeting tricks to keep your finances in check through uni.",
            "content": "Uni’s pricey, but a tight budget can work wonders. Track your cash—apps like Monzo show where it’s going (spoiler: probably Greggs). Set limits: £50 for food, £20 for nights out. Cook in bulk—chilli or pasta saves quid and time. Hunt student discounts—Unidays or NUS cards slash costs on everything from train fares to Netflix. Skip impulse buys; if it’s not essential, sleep on it. Need extra? Flog old textbooks or grab a bar shift. Budgeting’s dull but doable—master it, and uni’s less of a money pit.",
            "university": ""
        },
        {
            "category": "Funding",
            "title": "How to Find Part-Time Jobs as a Student",
            "summary": "Need cash without wrecking your studies? This article reveals where to find part-time work that fits your uni life and keeps your budget afloat.",
            "content": "Part-time jobs keep your bank balance ticking over without derailing your degree. Start on campus—library assistant roles or café shifts often fit around lectures and pay a fair whack. Venture off-site to local pubs, retail spots, or tutoring gigs—flexible hours are key. Check uni job boards, StudentJob UK, or pop into places with a CV (keep it short: skills, availability, enthusiasm). Nail quick interviews with a smile and a line like ‘I’m reliable and up for a challenge!’ Aim for 10-15 hours a week max—cash in pocket, studies intact, sorted.",
            "university": ""
        },
        {
            "category": "Health",
            "title": "Staying Healthy During University: A Student's Guide",
            "summary": "Want to dodge the fresher’s flu and stay fighting fit? This guide offers practical tips to keep your health on track amidst uni chaos.",
            "content": "Uni life’s a whirlwind, but staying healthy keeps you in the game. Eat smart—batch-cook veg-packed meals like curry or stew to avoid living off Pot Noodles. Hydrate like it’s your job; a reusable bottle saves cash and the planet. Squeeze in exercise—walk to lectures, hit the gym, or dance in your room. Dodge germs with handwashing, especially in winter, and don’t skip GP registration—NHS is free and fab. Sleep, eat, move—nail the basics, and you’ll power through deadlines and nights out with energy to spare.",
            "university": ""
        },
        {
            "category": "Health",
            "title": "Health Resources for Students: Where to Seek Help",
            "summary": "Feeling under the weather at uni? Discover the health resources available to students, from campus clinics to mental health support.",
            "content": "When your health wobbles, uni’s got your back—if you know where to look. Most campuses have a health centre—book for coughs, cuts, or contraception; it’s usually free. Register with a local GP pronto—NHS covers everything from flu jabs to emergencies. Mental health’s covered too—uni counselling’s a lifeline for stress or blues, often with drop-ins or short waits. Check your student union for wellbeing workshops or peer groups. Feeling rough? Don’t tough it out—tap these resources and get back to smashing uni life.",
            "university": ""
        },
        {
            "category": "Health",
            "title": "The Importance of Sleep: How to Manage Your Schedule",
            "summary": "Skimping on sleep to cram? This article explains why rest is your secret weapon and how to fit it into a packed uni schedule.",
            "content": "Sleep’s not optional—it’s your brain’s reset button. Skip it, and you’re foggy, grumpy, and rubbish at remembering stuff (science says 7-9 hours is the sweet spot). Build a routine: set a bedtime alarm, ditch screens an hour before, and sip herbal tea, not Red Bull. Juggle uni chaos by scheduling naps—20 minutes post-lecture revives you—or shifting late-night Netflix to weekends. Room dark, quiet, comfy? Sorted. Prioritise shut-eye like it’s a deadline—your grades, mood, and health will thank you big time.",
            "university": ""
        },
        {
            "category": "Mental Wellbeing",
            "title": "Dealing with Stress and Anxiety During Exams",
            "summary": "Exams got you frazzled? Learn how to tackle stress and anxiety with simple, effective strategies to keep your cool and perform at your best.",
            "content": "Exam stress is a beast, but you can tame it. Start early—break revision into chunks so you’re not drowning the night before. Breathe deep when panic hits: 4 seconds in, 4 out—repeat till you’re steady. Ditch all-nighters; sleep trumps cramming for clear thinking. Chat to mates or a lecturer if you’re stuck—venting helps. On the day, focus on one question at a time, sip water, and fake confidence—it tricks your brain. You’re tougher than you think; these tricks turn stress into fuel for smashing it.",
            "university": ""
        },
        {
            "category": "Mental Wellbeing",
            "title": "Mindfulness Practices to Calm Your Mind as a Student",
            "summary": "Overwhelmed by uni life? This piece introduces mindfulness tricks to quiet your mind and boost focus, no guru required.",
            "content": "Mindfulness sounds hippy-dippy, but it’s just paying attention on purpose—and it’s a game-changer for students. Try a 5-minute breather: sit, close your eyes, focus on air going in and out—thoughts wander, bring ‘em back. Apps like Headspace guide you, or just listen to rain sounds while eating lunch slowly. Walk to class noticing trees, not your phone. It cuts stress, sharpens focus, and stops you spiralling. No time? Even 60 seconds works. Give it a go—your headspace will feel less like a warzone.",
            "university": ""
        },
        {
            "category": "Mental Wellbeing",
            "title": "How to Maintain Your Mental Health During University",
            "summary": "Uni can be a mental marathon—here’s how to stay steady. Get tips to nurture your wellbeing and dodge burnout through the chaos.",
            "content": "Uni’s a thrill ride, but your mental health needs TLC to keep up. Connect—call home, grab coffee with mates; isolation’s the enemy. Move daily—a jog or dance sesh blasts tension. Spot trouble early: if you’re snappy or stuck in bed, chat to uni counselling (it’s free and confidential). Set boundaries—say no to extra shifts if you’re knackered. Journal five minutes nightly to offload worries. It’s not weakness to ask for help; it’s strength. Build these habits, and you’ll ride uni’s waves without sinking.",
            "university": ""
        },
        {
            "category": "Research",
            "title": "How to Conduct Academic Research: A Beginner's Guide",
            "summary": "New to research? This beginner’s guide breaks down how to start, from picking a topic to digging up gold-standard sources.",
            "content": "Research sounds posh, but it’s just organised curiosity. Pick a topic you’re into—say, climate change or Victorian novels—then narrow it (e.g., ‘wind farms in Scotland’). Hit the library or Google Scholar for peer-reviewed articles; Wikipedia’s a start, not a source. Skim abstracts to spot gems, then note key points—author, date, findings. Ask a lecturer what’s hot in your field—they’ll point you right. It’s a slog at first, but you’ll soon be piecing together ideas like a pro. Start small, and watch it click!",
            "university": ""
        },
        {
            "category": "Research",
            "title": "Writing a Research Paper: Step-by-Step Process",
            "summary": "Dreading that research paper? Follow this step-by-step process to craft a cracking piece, from brainstorm to bibliography.",
            "content": "A research paper’s less scary with a plan. Pick a question—‘How does X affect Y?’—then dig into books and journals for answers. Outline it: intro (why it matters), lit review (what’s out there), method (how you’ll explore), results, conclusion. Write the messy first draft—don’t fuss over perfection. Cite as you go (Harvard or whatever uni wants) to dodge plagiarism hell. Revise twice: once for flow, once for typos. Ask a mate or tutor to skim it. It’s grunt work, but a solid paper’s a uni badge of honour!",
            "university": ""
        },
        {
            "category": "Research",
            "title": "Applying for Research Grants: What You Need to Know",
            "summary": "Need funding for your Strathclyde research? This article unpacks how to snag grants, with tips tailored for uni projects.",
            "content": "Research grants turn ideas into reality, and Strathclyde students can bag them with grit. Scout uni funding pages—think internal pots or external bodies like UKRI. Pick a project with punch: clear aim, doable scope (e.g., ‘testing X’s impact on Y’). Write a killer proposal—why it’s new, how you’ll do it, what you need (£££ for kit, travel?). Get a supervisor’s nod; their backing boosts cred. Deadlines are brutal, so start early and triple-check forms. It’s a slog, but funding’s your ticket to serious research kudos.",
            "university": "strathclyde"
        },
        {
            "category": "Studying",
            "title": "Mastering Time Management as a University Student",
            "summary": "Time slipping through your fingers? Learn how to juggle uni life with ace time management tricks that actually work.",
            "content": "Uni’s a time vortex—lectures, mates, naps—but you can tame it. Grab a planner or app (Google Calendar’s free) and block out deadlines, classes, study slots. Prioritise: tackle big essays first, not Instagram. Use Pomodoro—25 minutes on, 5 off—to blitz tasks without frying. Say no to extra pints if you’re swamped. Review weekly—shift stuff as life happens. Procrastination’s the enemy; start small (10 minutes) to beat it. Master this, and you’ll have time for work, play, and a decent kip—uni life, sorted!",
            "university": ""
        },
        {
            "category": "Studying",
            "title": "Best Study Apps to Help You Stay Organised",
            "summary": "Tech to the rescue! Check out the best apps to keep your uni studies on track, from notes to deadlines.",
            "content": "Apps can turn study chaos into order—here’s the pick of the bunch. Notion’s a beast for notes, timetables, and to-dos in one sleek spot. Evernote scans handwritten scribbles—perfect for lecture hoarders. Todoist pings you deadlines so nothing slips. Forest gamifies focus—grow a tree while you work, or it dies if you faff. Quizlet’s flashcard magic drills facts fast. All free tiers rock; upgrade if you’re flush. Test a few—your phone’s your new study mate, keeping you sharp and sorted!",
            "university": ""
        },
        {
            "category": "Studying",
            "title": "Exam Preparation Strategies for Success",
            "summary": "Exams looming? This article dishes out proven prep strategies to boost your revision and nail those grades.",
            "content": "Exams aren’t a lottery—prep right, and you’ll smash ‘em. Map a revision plan weeks out—split topics, hit weak spots first. Active recall’s king: quiz yourself, don’t just read. Past papers reveal patterns; time yourself to mimic the real deal. Group study with mates can spark ideas—just don’t chat rubbish. Sleep and snacks (nuts, not crisps) fuel your brain. Day before, chill—review notes, pack your bag. In the exam, read every question twice, pace it, and breathe. Solid prep’s your superpower—go own it!",
            "university": ""
        },
        {
            "category": "Societies",
            "title": "How to Get Involved in University Societies",
            "summary": "Want to dive into Glasgow’s society scene? Find out how to join, shine, and make the most of uni clubs.",
            "content": "Glasgow Uni’s societies—over 100!—are your ticket to fun and skills. Freshers’ Fair’s the launchpad: roam stalls, grab freebies, sign up to faves (think debating, gaming, baking). No fair? Check the GUU site or Insta for meet-ups. Go to taster seshs—most welcome newbies, no pressure. Chat to members, volunteer for small roles (flyers, teas). It’s less about talent, more about vibe—find your crew, from rugby to robotics. Time’s tight, so pick two max. You’ll make mates, boost your CV, and love uni more!",
            "university": "glasgow"
        },
        {
            "category": "Societies",
            "title": "Starting Your Own University Club: A Guide",
            "summary": "Got a niche passion at Aberdeen? This guide walks you through launching your own club, from idea to reality.",
            "content": "No Aberdeen society fits your vibe? Start one! Pick your thing—say, urban gardening or K-pop—then pitch it to mates for buy-in. Chat to the Aberdeen Uni Students’ Association (AUSA)—they’ll greenlight it if it’s fresh and doable. Draft a quick aim (‘connect X fans’), nab five members, and book a room (free via AUSA). Spread word—posters, Discord, freshers’ chats. Host a kick-off: pizza, a plan, divvy up roles. It’s work—funding bids, event wrangling—but you’ll leave a legacy and find your tribe!",
            "university": "aberdeen"
        },
        {
            "category": "Tips & Help",
            "title": "How to Stay Organised in University: Tips and Tools",
            "summary": "Uni life a mess? Get top tips and tools to stay on top of deadlines, notes, and everything else.",
            "content": "Staying organised at uni’s a survival skill. Grab a planner—paper or digital (Trello’s ace)—and log every deadline, lecture, shift. Colour-code by priority—red for ‘do now’, green for ‘chill’. File notes weekly; a binder or OneNote keeps them findable. Tidy your desk—clutter kills focus. Set phone reminders for big stuff—‘Essay due!’—and review daily: what’s today, what’s next? Batch tasks—emails one go, reading another. It’s a faff to start, but you’ll dodge chaos and feel like a boss juggling uni life.",
            "university": ""
        },
        {
            "category": "Tips & Help",
            "title": "Surviving Your First Year of University",
            "summary": "First year feeling overwhelming? This survival guide shares hacks to settle in, study smart, and enjoy the ride.",
            "content": "Year one’s a rollercoaster—new digs, new faces, new rules. Hit freshers’ events; even if it’s awkward, you’ll find your people. Lectures? Go, take notes—miss ‘em, and you’re lost. Budget early—£20 a week for food works if you cook. Homesick? Call family, but don’t bail every weekend. Ask for help—tutors, older students, Google. Sleep trumps all-nighters; burnout’s real. Join a society or two for fun, not just CV points. It’s a steep curve—mess up, learn, laugh. You’ll survive and maybe even love it!",
            "university": ""
        },
        {
            "category": "Travel Abroad",
            "title": "Studying Abroad: How to Find the Right Program",
            "summary": "Fancy a semester overseas? Learn how to pick the perfect study abroad programme to suit your goals and wanderlust.",
            "content": "Studying abroad’s a blast if you nail the programme. Check your uni’s exchange list—Europe’s Erasmus+ or global tie-ups like Australia. Match it to your course—credits must transfer—or go wild with something new (Spanish in Madrid?). Budget matters: some spots (Eastern Europe) are cheap, others (USA) pricey—hunt scholarships on uni sites. Chat to returnees at study abroad fairs; they’ll spill real tea. Apply early—visas and forms take ages. Pick right, and you’ll study, travel, and grow—best uni perk going!",
            "university": ""
        },
        {
            "category": "Travel Abroad",
            "title": "Top Travel Destinations for University Students",
            "summary": "Craving a break from uni? Discover top travel spots that mix adventure, culture, and student-friendly prices.",
            "content": "Uni breaks beg for travel—here’s where to go on a budget. Prague’s a stunner—cheap beer, fairy-tale streets, £20 hostels. Lisbon’s got sun, seafood, and trams for pennies. Budapest mixes thermal baths with wild nightlife—student heaven. Morocco’s Marrakech dazzles with markets and £5 meals, but haggle hard. Closer to home, Edinburgh’s a gem if you’re elsewhere in the UK. Book flights on Skyscanner, crash in hostels via Hostelworld, and use student cards for discounts. Pack light, roam free—memories beat lectures any day!",
            "university": ""
        },
        {
            "category": "Travel Abroad",
            "title": "How to Adjust to Life in a New Country While Studying",
            "summary": "Struggling to settle abroad? This guide offers tips to adapt to a new country and make the most of your study experience.",
            "content": "Landing in a new country for uni’s thrilling but tough. Learn a few local phrases—‘hello’, ‘thanks’—to break ice and dodge gaffes. Explore early—map your campus, find a cheap café, feel less lost. Homesick? Skype mates, cook a fave dish, but don’t hide—join uni clubs to bond (language swaps are gold). Culture shock’s normal—queue etiquette or spicy food might baffle you; laugh it off. Ask international offices for visa or bank help. It takes weeks, not days—embrace the weird, and it’ll feel like home soon!",
            "university": ""
        },
    ]
    
    # Create articles with random metrics and authors
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
    """
    Add sample comments to articles to simulate user interaction.

    Generates a set number of comments per article and additional random comments to reach a target total,
    using a predefined list of varied responses.
    """

    comments = []
    
    comment_data = [
        "Brilliant article! Really opened my eyes to some new ideas.",
        "Super helpful—thanks for putting this together!",
        "This is spot on. I’ve been wondering about this for ages.",
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

    # Add two comments per article
    for article in articles:

        for _ in range(2):

            comment = Comment.objects.create(
                article=article,
                author=random.choice(users),
                content=random.choice(comment_data),
                written_on=timezone.now(),
            )

            comments.append(comment)

    # Add extra comments randomly
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
    """
    Create sample forums with detailed descriptions for community discussion.

    Generates forums with expanded descriptions to encourage engagement across various university-related topics.
    """

    forums = []

    forum_data = [
        {
            "name": "UofG General Discussion", 
            "description": "The beating heart of University of Glasgow chat! From campus quirks to upcoming gigs, this is your space to connect with fellow students. Share your highs and lows, ask about that weird building on Hillhead, or just rant about the library queues—it’s all fair game here."
        },
        {
            "name": "Freshers & Orientation", 
            "description": "New to uni? This forum’s your survival kit for freshers’ week and beyond. Swap tips on what to pack, how to ace icebreakers, and where to hide during awkward socials. Ask about orientation schedules or just vent about missing home—veteran students are here to help you settle in."
        },
        {
            "name": "Course Advice & Module Selection", 
            "description": "Overwhelmed by module choices or pondering a course switch? Dive into this forum to compare notes on workloads, lecturers, and hidden gems in the prospectus. Get the lowdown from students who’ve survived that stats module or ditched biology for history—your academic roadmap starts here."
        },
        {
            "name": "Study Tips & Exam Preparation",
            "description": "Struggling to nail your study game or sweating over exams? This forum’s your go-to for cracking revision hacks and exam survival tips. Share your fave techniques—like mind maps or late-night cramming wins—and pick up advice from students who’ve conquered finals. From beating procrastination to acing essays, it’s all about working smarter, not harder, right here."
        },
        {
            "name": "Housing & Accommodation",
            "description": "Flat-hunting or stuck with dodgy landlords? Welcome to your housing lifeline! Chat about uni halls vs private rents, swap horror stories of leaky ceilings, or get the scoop on the best Glasgow postcodes for students. Ask for tips on tenancy agreements, splitting bills, or making a grotty flat feel like home—your accommodation woes get sorted here."
        },
        {
            "name": "Job Recommendations",
            "description": "Skint and jobless? This forum’s buzzing with part-time gig ideas to keep your bank account happy. From bar shifts to tutoring, students spill the beans on where to apply, what pays decently, and how to juggle work with lectures. Post your own job finds or ask for CV tweaks—because a bit of extra cash shouldn’t mean sacrificing your degree."
        },
        {
            "name": "Sports & Arts Clubs",
            "description": "Fancy a kickabout or a paintbrush in hand? This is your hub for all things sports and arts at uni. Discover the best clubs—rugby, netball, theatre, or pottery—share tryout tales, or recruit for your team. Whether you’re a pro or just curious, swap schedules, tips, and banter to dive into the fun side of campus life."
        },
        {
            "name": "Mental Wellbeing Experiences",
            "description": "Feeling the uni blues? This forum’s a safe space to share mental health highs and lows. Talk stress, anxiety, or homesickness—students get it and are here to listen. Swap coping tricks like mindfulness or a good cry, and find out about counselling or support groups. No judgement, just real chat to keep your head above water."
        },
        {
            "name": "Travelling Abroad Advice",
            "description": "Dreaming of a semester in Spain or a jaunt to Japan? Get the lowdown on studying or travelling abroad right here. Ask about exchange programmes, visas, or packing light—students who’ve been there spill their secrets. From budgeting tips to culture shock survival, this forum’s your passport to nailing life overseas."
        },
        {
            "name": "Library & Study Spaces",
            "description": "Need a quiet corner or fed up with noisy libraries? This forum’s your guide to the best study spots on campus. Share your fave haunts—hidden desks, 24-hour zones—or rant about coffee spills and chatterboxes. Ask about booking rooms, Wi-Fi strength, or late-night access; it’s all about finding your perfect revision nook."
        },
        {
            "name": "Campus Gossip",
            "description": "Who’s snogging who, and what’s that lecturer up to? This is your cheeky corner for campus gossip and laughs. Spill the tea on wild nights, weird profs, or that mystery stain in the union—keep it fun, not nasty. Dig for the latest rumours or just enjoy the banter; it’s the juicy side of uni life, unfiltered!"
        },
        {
            "name": "Finance, Loans & Budgeting",
            "description": "Loans not stretching far enough? Dive into this forum for money-saving wisdom and financial know-how. Swap budgeting hacks—like living off £20 a week—ask about SAAS quirks, or get scholarship tips from cash-savvy students. From dodging debt traps to scoring discounts, it’s your space to make every penny count."
        },
        {
            "name": "Essay Writing & Academic Skills",
            "description": "Staring at a blank page or baffled by referencing? This forum’s your academic lifeline. Share essay-writing wins—intros that pop, killer arguments—or beg for help with Harvard style. Students trade tips on research, structure, and dodging word-count panic; it’s all about boosting your skills and smashing those deadlines."
        },
        {
            "name": "Placements & Vocation Advice",
            "description": "Eyeing a placement or career boost? This forum’s packed with real talk on landing work experience. Ask about applications, interviews, or what firms want—students who’ve done it share the dirt. From internships to volunteering, get advice on building your CV and stepping into the job world without tripping up."
        },
        {
            "name": "Student Politics & Activism",
            "description": "Passionate about change? Join the fray in this forum for student politics and activism. Debate campus issues—tuition fees, sustainability—or rally for causes like climate strikes. Share protest plans, dissect uni policies, or just vent about the system; it’s where fired-up students connect and make noise that matters."
        },
        {
            "name": "Science Discussions",
            "description": "Geeking out over science? This forum’s your lab for dissecting theories and experiments. Chat physics brain-benders, biology breakthroughs, or chem lab disasters—students from all unis weigh in. Ask for help with tricky concepts or flex your knowledge; it’s a nerdy haven for curious minds to spark ideas."
        },
        {
            "name": "Art, Music & Creative Projects",
            "description": "Got a creative itch? This forum’s alive with art, music, and project vibes. Share your sketches, gigs, or film ideas—get feedback or find collaborators. Ask about open mics, gallery spaces, or cheap supplies; it’s where uni artists and musos swap inspiration and turn daydreams into real stuff."
        },
        {
            "name": "Cafes, Food & Nightlife",
            "description": "Craving a decent brew or epic night out? This forum dishes the dirt on food and fun. Rate campus cafés, share cheap eats (think £3 meals), or spill on Glasgow’s best clubs and pubs. Ask about student deals or late-night grub spots—it’s your guide to munching and partying like a pro."
        },
        {
            "name": "Roommate & Flatmate Finder",
            "description": "Need a flatmate who’s not a nightmare? This forum’s your matchmaking hub. Post what you’re after—tidy, night owl, vegan?—or browse for potentials. Share horror stories, ask about vibe checks, or arrange meet-ups; it’s all about finding your uni living soulmate without the drama."
        },
        {
            "name": "Coding Problems",
            "description": "Code crashing and burning? This forum’s your tech triage for programming woes. Throw out Python bugs, Java jams, or HTML headaches—student coders jump in with fixes. Share project wins, beg for debug tips, or geek out over algorithms; it’s a lifeline for surviving comp sci at uni."
        },
        {
            "name": "UoE General Discussion",
            "description": "The pulse of University of Edinburgh life beats here! From Old Town antics to Pollock Halls drama, this forum’s your space to connect with UoE mates. Rant about the trek up Arthur’s Seat, ask about quirky traditions, or share your wildest tales—it’s Edinburgh student chat, loud and proud."
        },
        {
            "name": "Strathclyde General Discussion",
            "description": "Strathclyde students, this is your shout! From tech breakthroughs to city centre buzz, dive into all things uni. Ask about the best study spots in the TIC, vent about engineering deadlines, or swap tales from Freshers’ Week—it’s your forum to bond, moan, and revel in Strathclyde life."
        },
        {
            "name": "Dundee General Discussion",
            "description": "Dundee uni crew, gather round! This forum’s your hub for campus craic and beyond. Chat about the Tay’s moody views, dig for gig tips, or ask why the library’s always rammed—it’s all fair game. Share your Dundee highs and lows with students who get it; this is your space."
        },
        {
            "name": "Stirling General Discussion",
            "description": "Stirling students, unite here! From loch-side walks to castle vibes, this forum’s your catch-all for uni chat. Rave about the sports village, puzzle over bus timetables, or spill your latest campus saga—students swap stories and advice to keep the Stirling spirit alive and kicking."
        },
    ]

    for data in forum_data:
        
        forum = Forum.objects.create(name=data["name"], description=data["description"])
        
        forums.append(forum)

    return forums

def create_threads(users, forums):
    """
    Generate sample threads linked to forums and started by users.

    Creates threads with expanded topics to provide more detailed insights. Assigns random
    authors from the user list.
    """

    threads = []

    thread_data = [
        {"title": "What's happening on campus this week?", "forum": "UofG General Discussion", "topic": "Spill the beans on gigs, talks, or random events at Glasgow this week—anything worth dragging myself out of bed for?", "university": "glasgow"},
        {"title": "Anyone else struggling with coursework?", "forum": "UofG General Discussion", "topic": "Deadlines piling up at UofG—am I the only one drowning in essays and crying over stats?", "university": "glasgow"},
        {"title": "Best places to study?", "forum": "UofG General Discussion", "topic": "Need a quiet spot at Glasgow—library’s rammed, any hidden gems for cramming?", "university": "glasgow"},
        {"title": "Freshers events worth going to?", "forum": "Freshers & Orientation", "topic": "Freshers’ week’s here—which events are unmissable, and which are a total snooze?", "university": ""},
        {"title": "What to pack for uni?", "forum": "Freshers & Orientation", "topic": "Packing for uni—what’s essential, and what’s a waste of suitcase space?", "university": ""},
        {"title": "How to make friends as a fresher?", "forum": "Freshers & Orientation", "topic": "Newbie here—how do I go from awkward hellos to actual mates in week one?", "university": ""},
        {"title": "Best electives to take?", "forum": "Course Advice & Module Selection", "topic": "Picking electives—any fun or easy ones you’d swear by?", "university": ""},
        {"title": "Is this module difficult?", "forum": "Course Advice & Module Selection", "topic": "Eyeing a module but scared of the workload—worth the risk or a nightmare?", "university": ""},
        {"title": "Switching courses—need advice!", "forum": "Course Advice & Module Selection", "topic": "Hating my course—how tricky is switching, and any tips to pull it off?", "university": ""},
        {"title": "How do you prepare for exams?", "forum": "Study Tips & Exam Preparation", "topic": "Exams looming—what’s your go-to prep trick to avoid a total meltdown?", "university": ""},
        {"title": "Best study techniques?", "forum": "Study Tips & Exam Preparation", "topic": "What study hacks actually work—flashcards, late nights, or something else?", "university": ""},
        {"title": "Handling stress during exams?", "forum": "Study Tips & Exam Preparation", "topic": "Exam stress hitting hard—how do you keep calm when it’s all kicking off?", "university": ""},
        {"title": "How do you find affordable housing?", "forum": "Housing & Accommodation", "topic": "Rent’s a killer—where do you snag decent, cheap digs near uni?", "university": ""},
        {"title": "Private or uni accommodation?", "forum": "Housing & Accommodation", "topic": "Halls or private flat—which wins for cash, vibe, and avoiding weirdos?", "university": ""},
        {"title": "Flatmate horror stories", "forum": "Housing & Accommodation", "topic": "Got a flatmate from hell? Share your tales—I need a laugh or a warning!", "university": ""},
        {"title": "Best part-time jobs for students?", "forum": "Job Recommendations", "topic": "Skint—where’s the best place to earn a bit without killing my schedule?", "university": ""},
        {"title": "Balancing work and studies?", "forum": "Job Recommendations", "topic": "Working and studying—how do you not lose the plot juggling both?", "university": ""},
        {"title": "Is on-campus work worth it?", "forum": "Job Recommendations", "topic": "Campus jobs—handy or a hassle? Anyone rate the pay and hours?", "university": ""},
        {"title": "Best Irish clubs to join?", "forum": "Sports & Arts Clubs", "topic": "At Queen’s and into Irish stuff—any cracking Gaelic football or hurling clubs?", "university": "queens"},
        {"title": "How competitive are sports teams?", "forum": "Sports & Arts Clubs", "topic": "Thinking of joining a sports team—how tough is it to get in and keep up?", "university": ""},
        {"title": "Creative societies worth checking out?", "forum": "Sports & Arts Clubs", "topic": "Love art or drama—any societies that aren’t a bore or cliquey mess?", "university": ""},
        {"title": "Dealing with academic stress?", "forum": "Mental Wellbeing Experiences", "topic": "Coursework’s frying my brain—how do you cope when it gets too much?", "university": ""},
        {"title": "How to avoid burnout?", "forum": "Mental Wellbeing Experiences", "topic": "Feeling knackered already—any tips to dodge the burnout trap?", "university": ""},
        {"title": "Uni counselling services—any good?", "forum": "Mental Wellbeing Experiences", "topic": "Heard mixed things about uni counselling—worth a shot or a waste?", "university": ""},
        {"title": "Best ways to save money as a student?", "forum": "Finance, Loans & Budgeting", "topic": "Always broke—what’s your top trick to stretch the pennies?", "university": ""},
        {"title": "Should I get a student loan?", "forum": "Finance, Loans & Budgeting", "topic": "Loan or no loan—how do you decide, and is the debt worth it?", "university": ""},
        {"title": "Part-time job or more study time?", "forum": "Finance, Loans & Budgeting", "topic": "Cash vs grades—job to pay bills or extra study hours? Thoughts?", "university": ""},
        {"title": "What are the best essay writing resources?", "forum": "Essay Writing & Academic Skills", "topic": "Essay due soon—any ace books, sites, or tips to save my bacon?", "university": ""},
        {"title": "How to reference properly?", "forum": "Essay Writing & Academic Skills", "topic": "Referencing’s a minefield—how do you nail it without losing marks?", "university": ""},
        {"title": "Avoiding plagiarism?", "forum": "Essay Writing & Academic Skills", "topic": "Terrified of accidental plagiarism—how do you keep it original?", "university": ""},
        {"title": "Best places to eat on campus?", "forum": "Cafes, Food & Nightlife", "topic": "Starving on campus—where’s the best grub that’s not a rip-off?", "university": ""},
        {"title": "Cheapest food spots for students?", "forum": "Cafes, Food & Nightlife", "topic": "Need cheap eats—where’s the best bang for a fiver near uni?", "university": ""},
        {"title": "Best clubs & bars near uni?", "forum": "Cafes, Food & Nightlife", "topic": "Edinburgh nights out—which bars or clubs are worth the hype?", "university": "edinburgh"},
        {"title": "Looking for a flatmate!", "forum": "Roommate & Flatmate Finder", "topic": "Need a flatmate ASAP—tidy, chill, into late-night chats—anyone out there?", "university": ""},
        {"title": "How to find good roommates?", "forum": "Roommate & Flatmate Finder", "topic": "Flatmate hunt on—how do you spot the gems and dodge the duds?", "university": ""},
        {"title": "Roommate red flags?", "forum": "Roommate & Flatmate Finder", "topic": "What screams ‘run’ when picking a flatmate—spill your warning signs!", "university": ""},
        {"title": "Trouble debugging my Python script", "forum": "Coding Problems", "topic": "Python’s doing my head in—any debug wizards got a fix for my mess?", "university": ""},
        {"title": "Best websites to practice coding?", "forum": "Coding Problems", "topic": "Want to sharpen my coding—any sites you rate for practice?", "university": ""},
        {"title": "How to get better at Java?", "forum": "Coding Problems", "topic": "Java’s kicking my arse—how did you crack it without giving up?", "university": ""},
        {"title": "Best cafes near campus?", "forum": "UoE General Discussion", "topic": "Need a coffee fix at UoE—where’s the best brew near campus?", "university": "edinburgh"},
        {"title": "How's the workload at UoE?", "forum": "UoE General Discussion", "topic": "UoE workload—chill or brutal? How do you stay afloat?", "university": "edinburgh"},
        {"title": "UoE freshers week—worth it?", "forum": "UoE General Discussion", "topic": "Edinburgh freshers’ week—epic or overhyped? Sell it to me!", "university": "edinburgh"},
        {"title": "Strathclyde's best study spaces?", "forum": "Strathclyde General Discussion", "topic": "Where’s the top spot to study at Strathclyde—quiet or just cool?", "university": "strathclyde"},
        {"title": "Best clubs at Strathclyde?", "forum": "Strathclyde General Discussion", "topic": "Strathclyde clubs—which ones are worth my time and dues?", "university": "strathclyde"},
        {"title": "How good are Strathclyde lectures?", "forum": "Strathclyde General Discussion", "topic": "Strathclyde lectures—brilliant or a snooze? What’s the vibe?", "university": "strathclyde"},
        {"title": "Best spots to hang out in Dundee?", "forum": "Dundee General Discussion", "topic": "Dundee hangouts—where’s the go-to for a chill day or night?", "university": "dundee"},
        {"title": "UoD accommodation—worth it?", "forum": "Dundee General Discussion", "topic": "Dundee uni halls—cosy or cramped? Should I bother?", "university": "dundee"},
        {"title": "How's the social life in Dundee?", "forum": "Dundee General Discussion", "topic": "Dundee social scene—lively or dead? What’s the real deal?", "university": "dundee"},
        {"title": "How difficult is Stirling coursework?", "forum": "Stirling General Discussion", "topic": "Stirling coursework—tough as nails or a breeze? Help!", "university": "stirling"},
        {"title": "Best things to do in Stirling?", "forum": "Stirling General Discussion", "topic": "Bored in Stirling—what’s the best way to kill time here?", "university": "stirling"},
        {"title": "Stirling nightlife—how is it?", "forum": "Stirling General Discussion", "topic": "Stirling nights out—any spots worth the trek or nah?", "university": "stirling"},
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
    """
    Add sample posts to threads to simulate user interaction.

    Generates a set number of posts per thread and additional random posts to reach a target total,
    using a predefined list of varied responses.
    """

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
        "Great post! It made me reflect on my own experiences. I hadn't realised how much this topic had influenced my decisions over the years.",
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

    # Add two posts per thread
    for thread in threads:
        
        for _ in range(2):
        
            post = Post.objects.create(
                thread=thread,
                author=random.choice(users),
                content=random.choice(post_data),
                written_on=timezone.now(),
            )

            posts.append(post)

    # Add extra posts randomly
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
    print("Favouriting articles...")
    favourite_articles(users, articles)
    print("Assigned favourite articles.")

    # Add saved threads
    print("Saving threads...")
    save_threads(users, threads)
    print("Assigned saved threads.")

    print("Database population complete.")

if __name__ == '__main__':
    
    populate()