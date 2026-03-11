import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect("data/genius_bar.db")

# ---- 1. Most common issue categories ----
def most_common_issues():
    conn = get_connection()
    query = """
        SELECT issue_category, COUNT(*) as total_cases
        FROM cases
        GROUP BY issue_category
        ORDER BY total_cases DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- 2. Average resolution time by device type ----
def avg_resolution_by_device():
    conn = get_connection()
    query = """
        SELECT device_type, 
               ROUND(AVG(resolution_time_hours), 2) as avg_hours
        FROM cases
        GROUP BY device_type
        ORDER BY avg_hours DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- 3. Escalation rate by issue category ----
def escalation_rate_by_issue():
    conn = get_connection()
    query = """
        SELECT issue_category,
               COUNT(*) as total,
               SUM(CASE WHEN status = 'Escalated' THEN 1 ELSE 0 END) as escalated,
               ROUND(100.0 * SUM(CASE WHEN status = 'Escalated' THEN 1 ELSE 0 END) / COUNT(*), 1) as escalation_rate_pct
        FROM cases
        GROUP BY issue_category
        ORDER BY escalation_rate_pct DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- 4. Technician performance ----
def technician_performance():
    conn = get_connection()
    query = """
        SELECT technician_name, technician_role,
               COUNT(*) as total_cases,
               ROUND(AVG(customer_satisfaction), 2) as avg_satisfaction,
               ROUND(AVG(resolution_time_hours), 2) as avg_resolution_hours
        FROM cases
        GROUP BY technician_name
        ORDER BY avg_satisfaction DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- 5. Busiest days of the week ----
def busiest_days():
    conn = get_connection()
    query = """
        SELECT strftime('%w', intake_date) as day_number,
               CASE strftime('%w', intake_date)
                   WHEN '0' THEN 'Sunday'
                   WHEN '1' THEN 'Monday'
                   WHEN '2' THEN 'Tuesday'
                   WHEN '3' THEN 'Wednesday'
                   WHEN '4' THEN 'Thursday'
                   WHEN '5' THEN 'Friday'
                   WHEN '6' THEN 'Saturday'
               END as day_of_week,
               COUNT(*) as total_cases
        FROM cases
        GROUP BY day_number
        ORDER BY day_number
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- 6. Customer satisfaction distribution ----
def satisfaction_distribution():
    conn = get_connection()
    query = """
        SELECT customer_satisfaction as rating,
               COUNT(*) as total
        FROM cases
        GROUP BY customer_satisfaction
        ORDER BY customer_satisfaction
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---- RUN ALL QUERIES ----
if __name__ == "__main__":
    print("\n📊 Most Common Issues:")
    print(most_common_issues().to_string(index=False))

    print("\n⏱ Avg Resolution Time by Device:")
    print(avg_resolution_by_device().to_string(index=False))

    print("\n🚨 Escalation Rate by Issue:")
    print(escalation_rate_by_issue().to_string(index=False))

    print("\n👤 Technician Performance:")
    print(technician_performance().to_string(index=False))

    print("\n📅 Busiest Days of the Week:")
    print(busiest_days().to_string(index=False))

    print("\n⭐ Satisfaction Distribution:")
    print(satisfaction_distribution().to_string(index=False))