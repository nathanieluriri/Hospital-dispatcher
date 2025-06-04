import sqlite3

def seed_database(db_path="database.db"):
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        user_type TEXT CHECK (user_type IN ('Patients', 'Emergency_Contacts')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK (user_type IN ('Dispatcher', 'Hospital_Staff')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS hospitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT UNIQUE NOT NULL,
        longitude FLOAT NOT NULL,
        latitude FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ambulances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        associated_hospital INTEGER,
        ambulance_status TEXT NOT NULL CHECK (ambulance_status IN ('Available', 'Busy', 'Offline')),
        ambulance_type TEXT NOT NULL,
        longitude FLOAT NOT NULL,
        latitude FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_assigned_time TIMESTAMP,
        FOREIGN KEY (associated_hospital) REFERENCES hospitals(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS emergency_request (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        assigned_ambulance_id INTEGER,
        severity TEXT NOT NULL,
        longitude FLOAT NOT NULL,
        latitude FLOAT NOT NULL,
        request_time TIMESTAMP NOT NULL,
        dispatch_time TIMESTAMP,
        arrival_time TIMESTAMP,
        response_duration INTEGER,
        dispatch_delay INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (assigned_ambulance_id) REFERENCES ambulances(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS password_reset_token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS access_token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS refresh_token (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        previous_access_token INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (previous_access_token) REFERENCES access_token(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS secret_keys (
        id INTEGER PRIMARY KEY,
        key_1 TEXT,
        key_2 TEXT,
        key_3 TEXT,
        key_4 TEXT
    );

    INSERT OR REPLACE INTO secret_keys (id, key_1, key_2, key_3, key_4)
    VALUES (
        1,
        '4d29a94e2c5da300149c0dbfbb5ee3fe729f93f170cf76f129b48d6245db592e',
        'ab073cc84b679bb30b6632d85070908dd4c3a4d5a9554eecac3a3ee476f9fec6',
        'e4c4190c7df62807c9fa56257a5b465e8e5afc5e1a77f37970be61f2bf7686e6',
        'cd55a271b5ff46dc24d493f10d834445fa19ed1dca41363bf16c80cfabb08fe1'
    );
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        print("Database seeded successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()
