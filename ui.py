import ds_client
import Profile

def user_interface():
    profile = None  # This will hold the user's profile information
    while True:
        print("Welcome! Please choose an option:")
        print("c - Create a new DSU file")
        print("l - Load an existing DSU file")
        print("p - Post a journal entry online")
        print("u - Update bio online")
        print("v - View current profile info")
        print("q - Quit")
        choice = input("Your choice (c/l/p/u/v/q): ").strip().lower()

        if choice == 'c':
            profile = create_profile()
        elif choice == 'l':
            profile = load_profile()
        elif choice == 'p' and profile:
            publish_post(profile)
        elif choice == 'u' and profile:
            update_bio(profile)
        elif choice == 'v' and profile:
            view_profile_info(profile)
        elif choice == 'q':
            break
        else:
            print("Invalid option or no profile loaded. Please choose 'c' to create or 'l' to load a profile.")

def create_profile():
    dsuserver = input("Enter DS server IP: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    new_profile = Profile.Profile(dsuserver, username, password)
    # Here you might add additional attributes to your Profile instance
    return new_profile

def load_profile():
    path = input("Enter the path to your DSU file: ").strip()
    loaded_profile = Profile.Profile()
    try:
        loaded_profile.load_profile(path)
        print("Profile loaded successfully.")
    except Profile.DsuFileError:
        print("Failed to load profile.")
    return loaded_profile

def publish_post(profile):
    print("Your journal entries:")
    for i, post in enumerate(profile.get_posts()):
        print(f"{i}: {post.entry}")
    post_index = int(input("Select the index of the post you want to publish: "))
    try:
        post = profile.get_posts()[post_index]
        if ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, message=post.entry):
            print("Post published successfully.")
        else:
            print("Failed to publish post.")
    except IndexError:
        print("Invalid post index.")

def update_bio(profile):
    new_bio = input("Enter your new bio: ").strip()
    if ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, bio=new_bio):
        print("Bio updated successfully.")
        profile.bio = new_bio  # Update local profile bio
    else:
        print("Failed to update bio.")

def view_profile_info(profile):
    print("Current profile information:")
    print(f"Server: {profile.dsuserver}")
    print(f"Username: {profile.username}")
    print(f"Bio: {profile.bio}")
    print("Posts:")
    for post in profile.get_posts():
        print(f"- {post.entry}")

if __name__ == "__main__":
    user_interface()
