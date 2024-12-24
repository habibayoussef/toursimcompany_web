from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
app = Flask(__name__)
app.secret_key = "wesamhabiba"
tourss = [
    {"id": 1, "name": "Pyramids of Giza", "price": "$50/person", "description": "Visit the majestic pyramids and the Great Sphinx.", "image_url": "https://i.pinimg.com/736x/3e/15/a2/3e15a27f292bc44875693976b02cb9c0.jpg"},
    {"id": 2, "name": "Luxor and Karnak Temples", "price": "$80/person", "description": "Explore ancient temples and their rich history.", "image_url": "https://i.pinimg.com/474x/b5/62/34/b56234b9654fcf5a577a06bd1309e45a.jpg"},
    {"id": 3, "name": "Nile Cruise", "price": "$150/person", "description": "Enjoy a luxurious cruise along the Nile River.", "image_url": "https://i.pinimg.com/736x/f5/51/af/f551afa6b495422bb79756e03a6ea442.jpg"},
    {"id": 4, "name": "Aswan and Abu Simbel", "price": "$100/person", "description": "Discover the beauty of Aswan and the Abu Simbel temples.", "image_url": "https://i.pinimg.com/736x/ae/e1/0e/aee10ec85d7a274bfa65cc1ad85517a6.jpg"},
    {"id": 5, "name": "Cairo Tower", "price": "$70/person", "description": "Experience the tranquility of Siwa's desert oasis.", "image_url": "https://i.pinimg.com/474x/c1/6e/db/c16edb3d517ce7bc59d7d20e7b5cdcd4.jpg"},
    {"id": 6, "name": "Siwa Oasis", "price": "$70/person", "description": "Experience the tranquility of Siwa's desert oasis.", "image_url": "https://i.pinimg.com/474x/47/3f/11/473f11d9fd2d9e2e96eedb3c2135a964.jpg"},
]

# Sample data for Airlines
airplanes = [
    {"id": 1, "name": "Egypt Air", "price": "$300/person", "description": "Reliable domestic and international flights.", "image_url": "https://i.pinimg.com/736x/f2/f0/9f/f2f09f923f990c655ea6f6f3774bc707.jpg"},
    {"id": 2, "name": "Emirates Air", "price": "$500/person", "description": "Luxury flights with premium service.", "image_url": "https://i.pinimg.com/736x/2a/e8/b5/2ae8b56fbfb783e54d84e0b68b3e38c9.jpg"},
    {"id": 3, "name": "Qatar Air", "price": "$500/person", "description": "Luxury flights with premium service.", "image_url": "https://i.pinimg.com/736x/ee/a0/86/eea086b67ea9bf0dcee539ba06174248.jpg"},
]

# Sample data for Hotels
hotels = [
    {"id": 1, "name": "Hilton Cairo", "price": "$120/night", "description": "A luxury hotel in the heart of Cairo.", "image_url": "https://i.pinimg.com/474x/8e/66/92/8e6692a623146d86c16b811cdfa05853.jpg"},
    {"id": 2, "name": "Ramses Hilton", "price": "$100/night", "description": "Affordable comfort with great amenities.", "image_url": "https://i.pinimg.com/474x/7a/a1/94/7aa19415266b8ad0ad570b7d2ecc3e8e.jpg"},
    {"id": 3, "name": "Hilton hurghada", "price": "$120/night", "description": "A luxury hotel in the heart of Cairo.", "image_url": "https://i.pinimg.com/474x/17/ca/06/17ca06c108252e23ed8f230c894fe736.jpg"},
    {"id": 4, "name": "four season", "price": "$100/night", "description": "Affordable comfort with great amenities.", "image_url": "https://i.pinimg.com/474x/6b/61/9b/6b619b18f89bcdceec7e223c28e99f8e.jpg"},
]

packages = [ 
    {'id': 1, 
     'title': 'Affordable Package', 
     'image': 'Register - Login.jpeg', 
     'description': 'Activities:\n'
                    'Visit Sultanahmet Square: Explore landmarks like Blue Mosque and Hagia Sophia.\n' 
                    'Explore Grand Bazaar: Wander through the historic market and enjoy window shopping.\n'
                    'Bosphorus Ferry Ride: A scenic ride offering views of Istanbul\'s European and Asian sides.\n'
                    'Galata Tower Viewpoint: Climb the tower for a panoramic city view.\n'
                    'Explore Istiklal Street and Taksim Square: Experience Istanbul\'s vibrant culture and nightlife.\n'
                    'Topkapi Palace Gardens: Walk through Ottoman history in these serene gardens.\n'
                    'Meals:\n'
                    '- Breakfast: Simit (Turkish bagel) with tea (~$2).\n'
                    '- Lunch/Dinner: Kebab wraps, pide (Turkish pizza), or köfte (~$5-$7 per meal).\n'
                    '- Desserts: Baklava or Turkish delight (~$2).\n'
                    'Transportation: Use the Istanbulkart for Public Transport: Metro, buses, trams, and ferries (~$1 per ride).\n'
                    'Duration: 3 Days, 2 Nights.\n'
                    'Total Cost ($120 Per Person)', 
     'tickets': 5
    },
    {'id': 2, 
     'title': 'Standard Package', 
     'image': '🌊💙.jpeg', 
     'description': 'Activities:\n'
                    'Visit the Dolmabahce Palace: Explore the opulent palace that was home to the last Ottoman sultans.\n'
                    'Explore the Bosphorus Bridge: Enjoy panoramic views of the Bosphorus from the famous bridge connecting Europe and Asia.\n'
                    'Visit the Spice Bazaar: Discover the flavors and aromas of Turkish spices and sweets.\n'
                    'Explore the Istanbul Modern Art Museum: Experience contemporary art in the heart of the city.\n'
                    'Take a Cruise on the Golden Horn: Enjoy the scenic views of Istanbul’s historical peninsula.\n'
                    'Visit the Chora Church: Admire the stunning Byzantine mosaics and frescoes.\n'
                    'Meals:\n'
                    '- Breakfast: Menemen (Turkish scrambled eggs with vegetables) with tea (~$3).\n'
                    '- Lunch/Dinner: Lamb kebabs, manti (Turkish dumplings), or meze (~$7-$10 per meal).\n'
                    '- Desserts: Künefe (cheese dessert) or Turkish delight (~$3).\n'
                    'Transportation: Istanbulkart for public transport including metro, buses, and ferries (~$1 per ride).\n'
                    'Duration: 3 Days, 2 Nights.\n'
                    'Total Estimated Cost: $180 per person (including accommodation and transport).',
     'tickets': 3
    },
    {'id': 3, 
     'title': 'Comfort Package', 
     'image': 'download (28).jpeg', 
     'description': 'Activities:\n'
                    'Stay at a Comfortable Hotel in the Heart of Istanbul: A cozy, well-located hotel with easy access to the city\'s attractions.\n'
                    'Visit the Sultanahmet Area: Take your time exploring the Blue Mosque and Hagia Sophia at a relaxed pace.\n'
                    'Leisure Time at Gülhane Park: Enjoy a peaceful walk in one of the city\'s most beautiful parks with lush gardens and relaxing views.\n'
                    'Take a Bosphorus Cruise: Enjoy a relaxed 1-2 hour boat tour with breathtaking views of the city.\n'
                    'Explore the Turkish Baths: Experience a traditional Turkish bath (hammam) for ultimate relaxation.\n'
                    'Meals:\n'
                    '- Breakfast: Turkish breakfast spread with fresh bread, olives, cheeses, tomatoes, and cucumbers (~$10).\n'
                    '- Lunch/Dinner: Light Turkish dishes like lentil soup, lahmacun (Turkish pizza), or grilled vegetables (~$6-$8).\n'
                    '- Desserts: Traditional Turkish ice cream or sweet pastries (~$3).\n'
                    'Transportation: Comfortable travel by taxi or private transfer (~$15 per day for all transfers).\n'
                    'Duration: 4 Days, 3 Nights.\n'
                    'Total Estimated Cost: $250 per person (including accommodation and transport).',
     'tickets': 4
    },
    {'id': 4, 
     'title': 'Classy Package', 
     'image': '27 Best Things to do in Istanbul, Turkey.jpeg', 
     'description': 'Activities:\n'
                    'Stay at the Ritz-Carlton Istanbul: A luxury experience in the heart of the city with stunning views of the Bosphorus.\n'
                    'Private Yacht Cruise on the Bosphorus: Enjoy a private luxury yacht tour along the Bosphorus, with gourmet meals and drinks.\n'
                    'Visit the Hagia Sophia: Explore this iconic Byzantine church turned mosque, a true architectural masterpiece.\n'
                    'Exclusive Shopping at Istinye Park Mall: Shop at high-end brands and boutiques in one of the most luxurious malls in Istanbul.\n'
                    'Spa and Wellness Experience at Four Seasons Hotel: Relax and rejuvenate at a world-class spa.\n'
                    'Dinner at Mikla Restaurant: Enjoy fine dining with a panoramic view of Istanbul.\n'
                    'Meals:\n'
                    '- Breakfast: Organic Turkish breakfast spread with gourmet cheeses, olives, and fresh bread (~$20).\n'
                    '- Lunch/Dinner: Fine dining at Michelin-starred restaurants with a variety of international and Turkish fusion dishes (~$50-$70 per meal).\n'
                    '- Desserts: Specially crafted Turkish pastries and gourmet desserts (~$10).\n'
                    'Transportation: Private chauffeur-driven car for all transfers within Istanbul (~$100 per day).\n'
                    'Duration: 5 Days, 4 Nights.\n'
                    'Total Estimated Cost: $2000 per person (including luxury accommodation, meals, and exclusive experiences).',
     'tickets': 2
    }
]



def init_db():

        with sqlite3.connect('hotels.db') as conn:
         c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                image_url TEXT NOT NULL,
                description TEXT
            )
        ''')
        # إضافة بعض الفنادق الافتراضية (إذا كانت قاعدة البيانات فارغة)
        c.execute('SELECT COUNT(*) FROM hotels')
        if c.fetchone()[0] == 0:
            hotels_data = [
                ("Bosphorus Hotel", 100, 5, "WhatsApp Image 2024-12-21 at 01.32.27_0e3fcabd.jpg", "Luxury hotel in the city center."),
                ("Taksim Hotel", 75, 4, "WhatsApp Image 2024-12-21 at 01.26.07_1ec237d2.jpg", "Affordable stay near the beach."),
                ("Sultan Ahmed Hotel", 150, 5, "WhatsApp Image 2024-12-21 at 01.32.27_62b67ada.jpg", "Exclusive resort with amazing views.")
            ]
            c.executemany('''
                INSERT INTO hotels (name, price, rating, image_url, description)
                VALUES (?, ?, ?, ?, ?)
            ''', hotels_data)

        conn.commit()
# دالة لجلب الفنادق من قاعدة البيانات مع تصفية
def get_hotels(price=None, rating=None, rooms=None):
    with sqlite3.connect('hotels.db') as conn:
        c = conn.cursor()
        query = 'SELECT * FROM hotels WHERE 1=1'
        params = []
        if price:
            try:
                min_price, max_price = map(int, price.split('-'))
                query += ' AND price BETWEEN ? AND ?'
                params.extend([min_price, max_price])
            except ValueError:
                pass
        if rating:
            query += ' AND rating = ?'
            params.append(int(rating))
        c.execute(query, params)
        hotels = c.fetchall()
    return hotels
# دالة لتهيئة قاعدة البيانات الخاصة بالحجوزات
def in_db():
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    # إنشاء جدول الغرف
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (hotel_id) REFERENCES hotels (id)
        )
    ''')
    # إنشاء جدول الحجوزات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms (id)
        )
    ''')
    # إضافة بيانات تجريبية
    cursor.execute("INSERT OR IGNORE INTO hotels (id, name) VALUES (1, 'Hotel A'), (2, 'Hotel B')")
    cursor.execute("INSERT OR IGNORE INTO rooms (id, hotel_id, name) VALUES (1, 1, 'Room 101'), (2, 1, 'Room 102'), (3, 2, 'Room 201')")
    conn.commit()
    conn.close()
   

@app.route('/index', methods=['GET', 'POST'])
def index():
    # استدعاء دالة init_db لتأكيد أن قاعدة البيانات مهيأة
    init_db()

    price = request.form.get('price')
    rating = request.form.get('rating')
    rooms = request.form.get('rooms')

    hotels = get_hotels(price, rating, rooms)

    return render_template('mapp.html', hotels=hotels,)


@app.route('/cappodociah', methods=['GET', 'POST'])
def cappodociah():
    # استدعاء دالة init_db لتأكيد أن قاعدة البيانات مهيأة
    init_db()

    price = request.form.get('price')
    rating = request.form.get('rating')
    rooms = request.form.get('rooms')

    hotels = get_hotels(price, rating, rooms)

    return render_template('cappodocia_hotels.html', hotels=hotels,)
@app.route("/search", methods=["POST"])
def search():
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    if datetime.strptime(end_date, "%Y-%m-%d") < datetime.strptime(start_date, "%Y-%m-%d"):
        return "Error: End date cannot be earlier than start date!"

    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()

    # استعلام للعثور على الغرف المتاحة
    query = '''
        SELECT DISTINCT rooms.id, rooms.name, hotels.name AS hotel_name
        FROM rooms
        JOIN hotels ON rooms.hotel_id = hotels.id
        WHERE rooms.id NOT IN (
            SELECT room_id
            FROM bookings
            WHERE (start_date <= ? AND end_date >= ?)
        )
    '''
    cursor.execute(query, (end_date, start_date))
    available_rooms = cursor.fetchall()
    conn.close()
    return render_template("results.html", rooms=available_rooms, start_date=start_date, end_date=end_date)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session or session.get('is_admin') != True:
        return redirect(url_for('home'))  

    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        tickets = request.form['tickets']
        accommodation = request.form['accommodation']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        transportation = request.form['transportation']
        activities = request.form['activities']
        meals = request.form['meals']   

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO new_packages (name, destination ,tickets ,accommodation ,start_date ,end_date ,transportation ,activities, meals)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, destination ,tickets ,accommodation ,start_date ,end_date ,transportation ,activities, meals))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))  
    return render_template('admin.html')

@app.route("/book", methods=["POST"])
def book():
    room_id = request.form["room_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()

    # إضافة حجز جديد
    cursor.execute(
        "INSERT INTO bookings (room_id, start_date, end_date) VALUES (?, ?, ?)",
        (room_id, start_date, end_date)
    )
    conn.commit()
    conn.close()

    return "تم الحجز بنجاح!"


@app.route('/turkey')
def turkey():
    return render_template('hero.html')
@app.route('/packages')
def show_packages():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM new_packages')
    new_packages = cursor.fetchall()  # هنا جلبنا البيانات
    conn.close()
    return render_template('istanbul.html', packages=packages, new_packages=new_packages)
# دالة إنشاء قاعدة بيانات المستخدمين وحزم المستخدمين
@app.route('/cappodocia')
def cappodocia():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM new_packages')
    new_packages = cursor.fetchall()  # هنا جلبنا البيانات
    conn.close()
    return render_template('cappodocia.html', packages=packages, new_packages=new_packages)
def idb():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # إنشاء جدول المستخدمين إذا لم يكن موجودًا
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # إنشاء جدول الحزم
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        destination TEXT NOT NULL,
        accommodation TEXT NOT NULL,
        transportation TEXT NOT NULL,
        activities TEXT,
        meals TEXT NOT NULL,
        days INTEGER NOT NULL,
        total INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    cursor.execute('''
  CREATE TABLE IF NOT EXISTS new_packages (
    p_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    destination TEXT NOT NULL,
    tickets INTEGER NOT NULL,
    accommodation INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    transportation TEXT NOT NULL,
    activities TEXT NOT NULL,
    meals TEXT NOT NULL
)

    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            p_id INTEGER NOT NULL,
            tickets INTEGER NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (p_id) REFERENCES new_packages(id)
        )
    ''')
    conn.commit()
    conn.close()


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template('create_account.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'wesam' and password == 'habiba':
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin'))

        # تحقق من المستخدم العادي
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for("profile"))
        else:
            return "Invalid username or password!"

    return render_template('login.html')


@app.route("/profile")
def profile():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if not result:
        return redirect(url_for("login"))  # أو صفحة خطأ

    user_id = result[0]

    cursor.execute('SELECT destination, accommodation, transportation, activities, meals, days, total FROM packages WHERE user_id = ?', (user_id,))
    packages = cursor.fetchall()
    conn.close()

    return render_template("profile.html", username=username, packages=packages)



@app.route("/create_package", methods=["GET", "POST"])
def create_package():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    if request.method == "POST":
        destination = request.form["destination"]
        accommodation = request.form["accommodation"]
        transportation = request.form["transportation"]
        activities = ",".join(request.form.getlist("activities"))  # تحويل الأنشطة إلى نص
        meals = request.form["meals"]
        days = int(request.form["days"])
        total = int(request.form["total"])

        # إضافة الحزمة إلى قاعدة البيانات
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO packages (user_id, destination, accommodation, transportation, activities, meals, days, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, destination, accommodation, transportation, activities, meals, days, total))

        conn.commit()
        conn.close()

        return redirect(url_for("profile"))

    return render_template("create_package.html")
@app.route('/hotel/<int:hotel_id>')
def hotel_details(hotel_id):
    # جلب التفاصيل الخاصة بالفندق باستخدام الـ id
    conn = sqlite3.connect('hotels.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hotels WHERE id = ?', (hotel_id,))
    hotel = cursor.fetchone()
    conn.close()

    if hotel:
        return render_template('hotel_details.html', hotel=hotel)
    else:
        return "Hotel not found!", 404
    

@app.route('/book_package/<int:p_id>', methods=['GET', 'POST'])
def book_package(p_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM new_packages WHERE p_id = ?', (p_id,))
    new_package = cursor.fetchone()

    if request.method == 'POST':
        tickets = int(request.form['tickets'])
        total_price = tickets * 10  # تعديل السعر حسب التذاكر

        # التحقق من أن عدد التذاكر المتاحة يكفي
        if tickets > new_package[3]:  # new_package[3] هو عدد التذاكر المتاحة
            return "Not enough tickets available!"
        
        # إضافة الحجز إلى جدول bookings
        cursor.execute(''' 
            INSERT INTO bookings (username, p_id, tickets, total_price)
            VALUES (?, ?, ?, ?)
        ''', (session['username'], p_id, tickets, total_price))

        # تقليل عدد التذاكر المتاحة
        cursor.execute('UPDATE new_packages SET tickets = tickets - ? WHERE p_id = ?', (tickets, p_id))
        conn.commit()
        conn.close()

        # إرجاع رسالة النجاح مع توجيه العميل
        return render_template('book.html', new_package=new_package, success=True)
    
    conn.close()
    return render_template('book.html', new_package=new_package)
@app.route('/')
def home():
    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    # جلب جميع التعليقات من الجدول
    c.execute("SELECT comment FROM feedbacks")
    feedbacks = c.fetchall()
    conn.close()
    return render_template('home.html', feedbacks=feedbacks)

# معالجة إرسال تعليق جديد
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    comment = request.form['comment']
    if comment.strip():  # التأكد من أن التعليق غير فارغ
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        # إدخال التعليق في قاعدة البيانات
        c.execute("INSERT INTO feedbacks (comment) VALUES (?)", (comment,))
        conn.commit()
        conn.close()
    return redirect('/')

# إنشاء قاعدة البيانات إذا لم تكن موجودة
def feedback():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    # إنشاء جدول التعليقات
    c.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    #basmala
tours = [
    {"id": 1, "name": "Desert Safari", "price": "$25", "description": "Experience the Arabian desert with a safari tour.", "image_url": "https://i.pinimg.com/736x/8d/fc/c6/8dfcc6e4176f35de25c42752d1d3f59c.jpg"},
    {"id": 2, "name": "Burj Khalifa Tour", "price": "$30", "description": "Explore the world's tallest building.", "image_url": "https://i.pinimg.com/736x/21/75/a7/2175a7746fea324f1d7f973d600c1c78.jpg"},
    {"id": 3, "name": "Dhow Cruise", "price": "$35", "description": "Enjoy a luxurious dinner cruise on a traditional Dhow.", "image_url": "https://i.pinimg.com/736x/8b/4f/be/8b4fbebd113c868153d7c630a0a56db4.jpg"},
    {"id": 4, "name": "Dubai Mall Tour", "price": "$20", "description": "A day at one of the world's largest shopping malls.", "image_url": "https://i.pinimg.com/736x/cc/dc/44/ccdc447d2629ef503a0e1f711c595bd3.jpg"},
    {"id": 5, "name": "Palm Jumeirah Visit", "price": "$28", "description": "Visit the iconic Palm Jumeirah island.", "image_url": "https://i.pinimg.com/736x/0b/fe/12/0bfe12bcf0e876d79265c10e2a2f487b.jpg"},
]

@app.route("/indexx")
def indexx():
    return render_template("indexx.html")
@app.route("/new")
def new():
    return render_template("new.html", tours=tours)
def initialize_db():
    conn = sqlite3.connect('travel_buddy.db')
    c = conn.cursor()
    
    # حذف الجدول القديم إذا كان موجودًا
    c.execute('DROP TABLE IF EXISTS users')
    
    # إنشاء جدول جديد
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            start_date TEXT,
            end_date TEXT,
            answer1 TEXT,
            answer2 TEXT,
            answer3 TEXT,
            answer4 TEXT,
            answer5 TEXT,
            phone_number TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# حفظ البيانات في قاعدة البيانات
def save_user_data(data):
    conn = sqlite3.connect('travel_buddy.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, country, start_date, end_date, answer1, answer2, answer3, answer4, answer5, phone_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['country'], data['start_date'], data['end_date'], data['answer1'], data['answer2'], data['answer3'], data['answer4'], data['answer5'], data['phone_number']))
    conn.commit()
    conn.close()

# البحث عن مستخدمين مشابهين
def find_similar_users(data, user_id):
    conn = sqlite3.connect('travel_buddy.db')
    c = conn.cursor()
    
    # البحث عن مستخدمين لديهم 3 إجابات متطابقة على الأقل
    query = '''
        SELECT name, phone_number
        FROM users
        WHERE country = ? AND
              start_date = ? AND
              end_date = ? AND
              id != ? AND
              ((CASE WHEN answer1 = ? THEN 1 ELSE 0 END +
                CASE WHEN answer2 = ? THEN 1 ELSE 0 END +
                CASE WHEN answer3 = ? THEN 1 ELSE 0 END +
                CASE WHEN answer4 = ? THEN 1 ELSE 0 END +
                CASE WHEN answer5 = ? THEN 1 ELSE 0 END) >= 3)
    '''
    
    c.execute(query, (
        data['country'], data['start_date'], data['end_date'], user_id,
        data['answer1'], data['answer2'], data['answer3'], data['answer4'], data['answer5']
    ))
    
    results = c.fetchall()
    conn.close()
    return results
@app.route('/tb')
def tb():
    return render_template('tb.html')

@app.route('/submit', methods=['POST'])  
def submit():
    user_data = {
        'name': request.form['name'],
        'country': request.form['country'],
        'start_date': request.form['start_date'],
        'end_date': request.form['end_date'],
        'answer1': request.form['answer1'],
        'answer2': request.form['answer2'],
        'answer3': request.form['answer3'],
        'answer4': request.form['answer4'],
        'answer5': request.form['answer5'],
        'phone_number': request.form['phone_number']
    }

    # حفظ البيانات في قاعدة البيانات
    save_user_data(user_data)

    # الحصول على ID المستخدم الذي تم إضافته
    conn = sqlite3.connect('travel_buddy.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE phone_number = ?', (user_data['phone_number'],))
    user_id = c.fetchone()[0]
    conn.close()

    # البحث عن مستخدمين مشابهين
    similar_users = find_similar_users(user_data, user_id)

    if similar_users:
        return render_template('tbr.html', similar_users=similar_users)
    else:
        return render_template('tbr.html', message=" You have unique ideas that no one else has! 😊 Sorry, try again later to find someone with special ideas like yours.")
      
      
      
      

@app.route("/book-airplane/<int:airplane_id>")
def book_airplane(airplane_id):
    # Find the selected airplane by ID
    selected_airplane = next((airplane for airplane in airplanes if airplane["id"] == airplane_id), None)
    return render_template("booking_airplane.html", airplane=selected_airplane)

 
@app.route("/confirm-booking", methods=["POST"])
def confirm_booking():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    airplane_id = request.form.get("airplane_id")

    # Ensure airplane_id is a valid integer
    if not airplane_id:
        return "Airplane ID is missing", 400

    # Find the selected airplane by ID
    selected_airplane = next((airplane for airplane in airplanes if airplane["id"] == int(airplane_id)), None)

    # If the airplane is not found, return an error
    if not selected_airplane:
        return "Airplane not found", 404

    # Prepare the booking data
    booking_data = {
        "name": name,
        "email": email,
        "airplane": selected_airplane["name"],
        "price": selected_airplane["price"]
    }

    # Pass both booking data and airplane data to the confirmation page
    return render_template("booking_confirmation.html", data=booking_data, airplane_data=selected_airplane)


# Hotel booking route
@app.route("/book-hotel/<int:hotel_id>")
def book_hotel(hotel_id):
    # Find the selected hotel by ID
    selected_hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    return render_template("booking_hotel.html", hotel=selected_hotel)

@app.route("/confirm-hotel", methods=["POST"])
def confirm_hotel():
    # Get form data from the booking
    name = request.form.get("name")
    email = request.form.get("email")
    hotel_id = request.form.get("hotel_id")

    # Debugging step: print the values
    print(f"Hotel ID: {hotel_id}")

    # Find the selected hotel by ID
    selected_hotel = next((hotel for hotel in hotels if str(hotel["id"]) == hotel_id), None)

    # Check if the hotel was found
    if not selected_hotel:
        return "Hotel not found, please try again."

    # Create the booking data
    hotel_booking_data = {
        "name": name,
        "email": email,
        "hotel": selected_hotel["name"],
        "price": selected_hotel["price"]
    }

    # Render the confirmation page with only hotel data and None for airplane data
    return render_template("booking_confirmation.html", data=hotel_booking_data, airplane_data=None)




 
# Main index route
@app.route("/e")
def e():
    return render_template("e.html", tours=tours, hotels=hotels, airplanes=airplanes)

# Egypt Tours route
@app.route("/tours")
def egypt_tours():
    return render_template("tours.html", tourss=tourss)

@app.route("/airplanes")
def airplanes_page():
    return render_template("airplanes.html", airplanes=airplanes)

@app.route("/hotels")
def hotels_page():
    return render_template("hotels.html", hotels=hotels)

 
@app.route("/home")
def h():
    return render_template("e.html")

# About page route
@app.route("/about")
def about():
    return render_template("about.html")
tours = [
    {"id": 1, "name": "Eiffel Tower", "price": "€50/person", "description": "Experience the stunning views from the Eiffel Tower.", "image_url": "https://i.pinimg.com/736x/c9/dc/0f/c9dc0f5918a0a0a2fdc3e919cc6a18d7.jpg"},
    {"id": 2, "name": "Louvre Museum", "price": "€70/person", "description": "Discover iconic art pieces, including the Mona Lisa.", "image_url": "https://i.pinimg.com/736x/7c/fc/95/7cfc95e9beeb5914a037c4d1229043d3.jpg"},
    {"id": 3, "name": "Seine River Cruise", "price": "€30/person", "description": "Enjoy a romantic cruise along the Seine River.", "image_url": "https://i.pinimg.com/474x/a4/20/ac/a420ac22e157760f158e9efae67c4338.jpg"},
    {"id": 4, "name": "Mont Saint-Michel", "price": "€100/person", "description": "Explore the stunning island and its Gothic abbey.", "image_url": "https://i.pinimg.com/736x/96/31/9c/96319c724f0bcf0e40921cf629d59346.jpg"},
    {"id": 5, "name": "Versailles Palace", "price": "€80/person", "description": "Experience the grandeur of the French monarchy.", "image_url": "https://i.pinimg.com/736x/f8/30/71/f8307193aed8c63e7b8b4fabb71c474c.jpg"},
    {"id": 6, "name": "disney land", "price": "€60/person", "description": "Stroll through the beautiful lavender fields of Provence.", "image_url": "https://i.pinimg.com/474x/4b/3b/25/4b3b25926e0b304c8a747c4e9ae9d676.jpg"},
]

# Sample data for Airlines
airplanes = [
    {"id": 1, "name": "France air", "price": "€400/person", "description": "Premium flights to and from France.", "image_url": "https://i.pinimg.com/736x/09/a9/0f/09a90fa9d51a34a21c759bab08c7c774.jpg"},
    {"id": 2, "name": "egypt air", "price": "€350/person", "description": "Luxury and comfort with top-notch service.", "image_url": "https://i.pinimg.com/736x/f2/f0/9f/f2f09f923f990c655ea6f6f3774bc707.jpg"},
    {"id": 3, "name": "qatar air", "price": "€380/person", "description": "Fly to France with ease and elegance.", "image_url": "https://i.pinimg.com/736x/83/e5/d4/83e5d4359c0c1ff5d1f17f2ba3bd5f0e.jpg"},
]

# Sample data for Hotels
hotels = [
    {"id": 1, "name": "Le Meurice", "price": "€500/night", "description": "A luxury hotel in the heart of Paris.", "image_url": "https://i.pinimg.com/474x/25/fe/73/25fe734b007863bba3465450cc23309f.jpg"},
    {"id": 2, "name": "Hôtel Ritz Paris", "price": "€600/night", "description": "Iconic hotel with world-class service.", "image_url": "https://i.pinimg.com/474x/94/ed/82/94ed823f0fd9198df3e84dd3b8b7d773.jpg"},
    {"id": 3, "name": "Sofitel Marseille", "price": "€200/night", "description": "Luxury stay by the Mediterranean.", "image_url": "https://i.pinimg.com/474x/45/18/2f/45182fea3b60b83655100273600a0b5a.jpg"},
    {"id": 4, "name": "Château de Mercuès", "price": "€300/night", "description": "Stay in a charming French castle.", "image_url": "https://i.pinimg.com/736x/dd/50/63/dd50635dd4c62fc8ea333b2f898d5283.jpg"},
]

@app.route("/booking-airplane/<int:airplane_id>")
def book_airplanee(airplane_id):
    # Find the selected airplane by ID
    selected_airplane = next((airplane for airplane in airplanes if airplane["id"] == airplane_id), None)
    return render_template("booking_airplane.html", airplane=selected_airplane)

@app.route("/confirm-bookingg", methods=["POST"])
def confirm_bookingg():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    airplane_id = request.form.get("airplane_id")

    # Ensure airplane_id is valid
    if not airplane_id:
        return "Airplane ID is missing", 400

    # Find the airplane by ID
    selected_airplane = next((airplane for airplane in airplanes if airplane["id"] == int(airplane_id)), None)

    if not selected_airplane:
        return "Airplane not found", 404

    booking_data = {
        "name": name,
        "email": email,
        "airplane": selected_airplane["name"],
        "price": selected_airplane["price"]
    }

    return render_template("booking_confirmation.html", data=booking_data, airplane_data=selected_airplane)

@app.route("/book-hotel/<int:hotel_id>")
def book_hotell(hotel_id):
    selected_hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)
    return render_template("booking_hotel.html", hotel=selected_hotel)

@app.route("/confirm-hotell", methods=["POST"])
def confirm_hotell():
    name = request.form.get("name")
    email = request.form.get("email")
    hotel_id = request.form.get("hotel_id")

    selected_hotel = next((hotel for hotel in hotels if str(hotel["id"]) == hotel_id), None)

    if not selected_hotel:
        return "Hotel not found, please try again."

    hotel_booking_data = {
        "name": name,
        "email": email,
        "hotel": selected_hotel["name"],
        "price": selected_hotel["price"]
    }

    return render_template("booking_confirmationn.html", data=hotel_booking_data, airplane_data=None)

@app.route("/m")
def m():
    return render_template("m.html", tours=tours, hotels=hotels, airplanes=airplanes)

@app.route("/tourss")
def france_tourss():
    return render_template("tourss.html", tours=tours)

@app.route("/airplaness")
def airplanes_pagee():
    return render_template("airplaness.html", airplanes=airplanes)

@app.route("/hotelss")
def hotels_pagee():
    return render_template("hotelss.html", hotels=hotels)

@app.route("/homee")
def homee():
    return render_template("m.html")

@app.route("/aboutt")
def aboutt():
    return render_template("aboutt.html")
if __name__ == '__main__':
    idb()
    in_db()
    initialize_db()
    feedback()
    app.run(debug=True)