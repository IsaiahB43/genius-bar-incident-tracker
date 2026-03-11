import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

DEVICE_TYPES = {
    "iPhone": ["iPhone 14", "iPhone 14 Pro", "iPhone 15", "iPhone 15 Pro",
               "iPhone 15 Pro Max", "iPhone 16", "iPhone 16 Pro",
               "iPhone 17", "iPhone 17 Pro Max"],
    "MacBook": ["MacBook Air M1", "MacBook Air M2", "MacBook Pro 14 M2",
                "MacBook Pro 16 M2", "MacBook Pro M3"],
    "iPad": ["iPad 9th Gen", "iPad 10th Gen", "iPad Air M1", "iPad Pro 12.9"],
    "Apple Watch": ["Apple Watch Series 7", "Apple Watch Series 8",
                    "Apple Watch Series 9", "Apple Watch Ultra",
                    "Apple Watch Series 10", "Apple Watch Series 11"],
    "AirPods": ["AirPods 3rd Gen", "AirPods Pro 2nd Gen"],
}

ISSUE_CATEGORIES = {
    "Battery": ["Battery draining fast", "Battery not charging",
                "Battery swollen", "Battery health degraded"],
    "Screen": ["Screen cracked", "Screen unresponsive",
               "Display flickering", "Dead pixels"],
    "Software": ["Device not booting", "App crashes",
                 "iOS update failed", "Device stuck in recovery mode"],
    "Water Damage": ["Liquid detected", "Speaker muffled after water exposure",
                     "Charging port corroded"],
    "Hardware": ["Button not working", "Camera not working",
                 "Speaker not working", "Face ID not working"],
    "Data Recovery": ["Lost photos after update", "Contacts deleted",
                      "Device wiped accidentally"],
}

RESOLUTION_TYPES = ["Repaired", "Replaced", "No Issue Found", "Customer Education", "Escalated to Repair Center"]
PRIORITY_LEVELS = ["Low", "Medium", "High"]
STATUSES = ["Resolved", "Escalated", "In Progress", "Open"]

TECHNICIANS = [
    {"id": "T001", "name": "Isaiah Benton", "role": "Technical Expert"},
    {"id": "T002", "name": "Marcus Johnson", "role": "Technical Expert"},
    {"id": "T003", "name": "Priya Patel", "role": "Technical Specialist"},
    {"id": "T004", "name": "Jordan Lee", "role": "Technical Specialist"},
    {"id": "T005", "name": "Ashley Rivera", "role": "Technical Specialist"},
]

def generate_cases(n=1000):
    cases = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    for i in range(1, n + 1):
        device_type = random.choices(
            list(DEVICE_TYPES.keys()),
            weights=[50, 25, 15, 7, 3]
        )[0]
        device_model = random.choice(DEVICE_TYPES[device_type])

        issue_category = random.choices(
            list(ISSUE_CATEGORIES.keys()),
            weights=[25, 20, 30, 10, 10, 5]
        )[0]
        issue_description = random.choice(ISSUE_CATEGORIES[issue_category])

        priority = random.choices(
            PRIORITY_LEVELS, weights=[50, 35, 15]
        )[0]

        base_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        day_weights = [6, 5, 4, 4, 5, 6, 9]  # Sun Mon Tue Wed Thu Fri Sat
        target_day = random.choices(range(7), weights=day_weights)[0]
        current_day = base_date.weekday() + 1
        days_shift = (target_day - current_day) % 7
        intake_date = base_date + timedelta(days=days_shift)

        resolution_hours = round(random.uniform(0.5, 72), 1)

        status = random.choices(
            STATUSES, weights=[70, 10, 10, 10]
        )[0]

        resolution_type = random.choice(RESOLUTION_TYPES)
        technician = random.choice(TECHNICIANS)
        satisfaction = random.choices([1, 2, 3, 4, 5], weights=[3, 5, 12, 30, 50])[0]

        cases.append({
            "case_id": f"GB-{i:04d}",
            "intake_date": intake_date.strftime("%Y-%m-%d %H:%M"),
            "device_type": device_type,
            "device_model": device_model,
            "issue_category": issue_category,
            "issue_description": issue_description,
            "priority_level": priority,
            "status": status,
            "resolution_time_hours": resolution_hours,
            "resolution_type": resolution_type,
            "technician_id": technician["id"],
            "technician_name": technician["name"],
            "technician_role": technician["role"],
            "customer_satisfaction": satisfaction,
        })

    return cases

def save_to_database(cases):
    conn = sqlite3.connect("data/genius_bar.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            intake_date TEXT,
            device_type TEXT,
            device_model TEXT,
            issue_category TEXT,
            issue_description TEXT,
            priority_level TEXT,
            status TEXT,
            resolution_time_hours REAL,
            resolution_type TEXT,
            technician_id TEXT,
            technician_name TEXT,
            technician_role TEXT,
            customer_satisfaction INTEGER
        )
    """)

    for case in cases:
        cursor.execute("""
            INSERT OR IGNORE INTO cases VALUES (
                :case_id, :intake_date, :device_type, :device_model,
                :issue_category, :issue_description, :priority_level,
                :status, :resolution_time_hours, :resolution_type,
                :technician_id, :technician_name, :technician_role,
                :customer_satisfaction
            )
        """, case)

    conn.commit()
    conn.close()
    print(f"✅ {len(cases)} cases saved to data/genius_bar.db")

if __name__ == "__main__":
    print("Generating Genius Bar case data...")
    cases = generate_cases(1000)
    save_to_database(cases)