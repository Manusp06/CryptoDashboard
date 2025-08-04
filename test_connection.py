import psycopg2

def test_connection():
    try:
        # Replace these values with your database credentials
        conn = psycopg2.connect(
            host="localhost",
            database="crypto_database",  # Your database name
            user="postgres",  # Your username
            password= "password"  # Your password
        )
        
        # Check the current database
        cursor = conn.cursor()
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        
        print(f"Successfully connected to the database: {current_db}")
        
        # Close the connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")

if __name__ == "__main__":
    test_connection()
