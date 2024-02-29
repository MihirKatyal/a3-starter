import ds_client
import Profile

def user_interface():
    print("Welcome! Please choose an option:")
    print("c - Create a new DSU file")
    print("l - Load an existing DSU file")
    print("p - Post a journal entry online")
    print("u - Update bio online")
    print("v - View current profile info")
    print("q - Quit")
    choice = input("Your choice (c/l/p/u/v/q): ").strip().lower()


    return choice

def admin_mode():
    print("Welcome to Admin mode! Please choose an option:")
    # Admin mode command prompt is handled in a2.py

