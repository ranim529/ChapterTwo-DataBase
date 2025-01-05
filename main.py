import mysql.connector

def is_password_safe(password):

    if (
            len(password) < 8 or  # Less than 8 characters
            not any(char.isdigit() for char in password) or  # No digits
            not any(char.isupper() for char in password) or  # No uppercase letters
            not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~" for char in password)  # No symbols
    ):
        return False
    return True


def generate_safe_password():
    import random
    import string

    digits = random.choice(string.digits)
    uppercase = random.choice(string.ascii_uppercase)
    symbols = random.choice("!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~")
    remaining = ''.join(
        random.choices(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:'\",.<>?/|\\`~", k=5))

    password = digits + uppercase + symbols + remaining
    return ''.join(random.sample(password, len(password)))


def main():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="person"
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            password VARCHAR(255),
            age TINYINT,
            email VARCHAR(255),
            occupation VARCHAR(255)
        )
    """)

    name = input("Enter your name: ")
    password = input("Enter your password: ")
    age = input("Enter your age: ")
    email = input("Enter your email: ")
    occupation = input("Enter your occupation: ")

    if not is_password_safe(password):
        print("The password you entered is unsafe. Generating a safe password...")
        password = generate_safe_password()
        print(f"Your new password is: {password}")

    cursor.execute(
        "INSERT INTO users (name, password, age, email, occupation) VALUES (%s, %s, %s, %s, %s)",
        (name, password, age, email, occupation)
    )
    connection.commit()
    print("Data inserted successfully")

    # Modify all unsafe passwords in the database
    cursor.execute("SELECT id, password FROM users")
    users = cursor.fetchall()

    for user_id, user_password in users:
        if not is_password_safe(user_password):
            print(f"Password for user ID {user_id} is unsafe. Modifying...")
            new_password = generate_safe_password()
            cursor.execute(
                "UPDATE users SET password = %s WHERE id = %s",
                (new_password, user_id)
            )
            print(f"Password for user ID {user_id} updated to: {new_password}")

    connection.commit()

    cursor.execute("SELECT name, password, age, email, occupation FROM users")
    results = cursor.fetchall()

    print("\nData in the 'users' table:")
    for row in results:
        name, password, age, email, occupation = row
        print(f"Name: {name}, Password: {password}, Age: {age}, Email: {email}, Occupation: {occupation}")

    with open("file1.txt", "w") as file1, open("file2.txt", "w") as file2, open("file3.txt", "w") as file3, open(
            "file4.txt", "w") as file4:
        for row in results:
            name, password, age, email, occupation = row
            file1.write(f"{name}, {password}\n")
            file2.write(f"{name}, {age}\n")
            file3.write(f"{name}, {email}\n")
            file4.write(f"{name}, {occupation}\n")

    cursor.close()
    connection.close()
    print("Database connection closed")


if __name__ == "__main__":
    main()
