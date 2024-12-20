import mysql.connector
import uuid
from contextlib import contextmanager
from datetime import datetime


# MySQL connection details
host = "localhost"
user = "root"
password = "dataset2024"
database = "customer_service"


# Database connection manager
@contextmanager
def get_db_connection():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    try:
        yield connection
    finally:
        connection.close()


# Generate a new UUID for interaction_id
def generate_interaction_id():
    return str(uuid.uuid4())


# Function to get the current timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Create database and table with updated schema
def setup_database():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS customer_service")
        connection.database = "customer_service"

        # Create the interactions table if it doesn't exist, with new fields added
        create_table_query = """
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id CHAR(36) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            channel ENUM('chat', 'email', 'voice') NOT NULL,
            timestamp DATETIME NOT NULL,
            message_logs TEXT NOT NULL,
            issue_description TEXT,
            sentiment_score DECIMAL(5,2),
            sentiment ENUM('POSITIVE', 'NEUTRAL', 'NEGATIVE')
        )
        """
        cursor.execute(create_table_query)

        # Create the customer_summary table with user_id as primary key
        create_summary_table_query = """
        CREATE TABLE IF NOT EXISTS customer_summary (
            user_id VARCHAR(255) PRIMARY KEY,
            summary TEXT NOT NULL
        )
        """
        cursor.execute(create_summary_table_query)

        connection.commit()
        print("Database and tables setup complete.")


# Insert interaction record with new fields
def insert_interaction(interaction):
    # Ensure the timestamp is automatically set if not provided
    if not interaction[3]:  # If the timestamp (4th element) is not provided
        interaction = interaction[:3] + (get_current_timestamp(),) + interaction[4:]

    with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO interactions (
            interaction_id, user_id, channel, timestamp, message_logs, 
            issue_description, sentiment_score, sentiment
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, interaction)
        connection.commit()
        print(f"Inserted interaction with ID {interaction[0]}.")


# Update interaction record with new fields
def update_interaction(interaction_id, new_values):
    # Ensure the timestamp is automatically set if not provided
    if not new_values[2]:  # If the timestamp (3rd element) is not provided
        new_values = new_values[:2] + (get_current_timestamp(),) + new_values[3:]

    with get_db_connection() as connection:
        cursor = connection.cursor()
        update_query = """
        UPDATE interactions SET
            user_id = %s,
            channel = %s,
            timestamp = %s,
            message_logs = %s,
            issue_description = %s,
            sentiment_score = %s,
            sentiment = %s
        WHERE interaction_id = %s
        """
        cursor.execute(update_query, (*new_values, interaction_id))
        connection.commit()
        print(f"Updated interaction with ID {interaction_id}.")


# Obtaining list of customer from database
def get_unique_customer_keys():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT DISTINCT user_id FROM interactions"
        cursor.execute(query)
        
        # Yield each customer key one at a time
        for customer_key in cursor.fetchall():
            yield customer_key[0]



# Query interactions by user_id with sorting based on timestamp
def query_user(user_id, sort_order='ASC'):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = """
        SELECT interaction_id, user_id, channel, timestamp, message_logs, 
               issue_description, sentiment_score, sentiment 
        FROM interactions WHERE user_id = %s ORDER BY timestamp """ + sort_order
        cursor.execute(query, (user_id,))
        interactions = cursor.fetchall()
        if interactions:
            for row in interactions:
                print(row)
        else:
            print(f"No interactions found for user_id {user_id}.")


# Retrieve complaint context
def retrieve_user_messages(user_id):
    # Initialize variables to store message logs and issue descriptions
    message_logs = []
    issue_descriptions = []

    # Query all interactions for the given user_id
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = """
        SELECT message_logs, issue_description
        FROM interactions WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        interactions = cursor.fetchall()

        if interactions:
            for message_log, issue_description in interactions:
                message_logs.append(message_log)
                issue_descriptions.append(issue_description)
        
        # Combine all message_logs and issue_descriptions into the desired format
        combined_message_logs = "\n".join(message_logs)
        combined_issue_descriptions = " ".join(issue_descriptions)

        # Return the formatted string
        return f"Coversation of user with agent: {combined_message_logs}\nkeywords: {combined_issue_descriptions}"
    return f"No interactions found for user_id {user_id}."


# Retrieve timestamped message logs 
def retrieve_user_timestamped_messages(user_id):
    # Initialize variables to store message logs and issue descriptions
    message_logs = []
    issue_descriptions = []


    # Query all interactions for the given user_id
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = """
        SELECT timestamp, message_logs, issue_description
        FROM interactions WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        interactions = cursor.fetchall()

        if interactions:
            for timestamp, message_log, issue_description in interactions:
                timestamp_str = timestamp.strftime(r"%d-%m-%Y %H:%M:%S")
                message_logs.append(timestamp_str + ": " + message_log)
                issue_descriptions.append(issue_description)
        
        # Combine all message_logs and issue_descriptions into the desired format
        combined_message_logs = "\n".join(message_logs)
        combined_issue_descriptions = " ".join(issue_descriptions)

        # Return the formatted string
        return f"Coversation of user with agent: {combined_message_logs}\nkeywords: {combined_issue_descriptions}"
    return f"No interactions found for user_id {user_id}."


# Query all interactions
def query_interactions():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM interactions"
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)


# Insert into backend table: customer_summary
def insert_customer_summary(user_id, summary_text):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO customer_summary (user_id, summary) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE summary = VALUES(summary)
        """
        cursor.execute(insert_query, (user_id, summary_text))
        connection.commit()
        print(f"Inserted/Updated summary for user_id {user_id}.")


# Main function
if __name__ == "__main__":
    # Setup the database (creating tables)
    setup_database()

    # Example interaction record with no timestamp (timestamp will be generated automatically)
    interaction = (
        generate_interaction_id(),  # interaction_id (UUID)
        "customer_001",             # user_id
        "chat",                     # channel
        None,                       # timestamp (to be generated)
        "Customer: Hello! I need help.",  # message_logs
        "Unable to login to account",     # issue_description
        0.85,                       # sentiment_score
        "POSITIVE"                  # sentiment
    )

    insert_interaction(interaction)

    # Example: Query all interactions for a specific user
    query_user("customer_001")

    # Example: Modifying the interaction record with new values
    new_values = (
        "customer_001",  # new user_id
        "chat",                 # new channel
        None,                   # timestamp (to be generated automatically)
        "Customer: Still need help.",  # new message_logs
        "Unable to reset password",    # new issue_description
        0.60,                         # new sentiment_score
        "NEUTRAL"                     # new sentiment
    )

    # Update the interaction with ID (replace with actual ID)
    update_interaction("123e4567-e89b-12d3-a456-426614174000", new_values)

    # Query and display updated records
    query_interactions()
