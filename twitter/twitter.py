from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self):
        self.current_user = None
        self.logged_in = False
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        users = db_session.query(User).all()
        while True:
            username = input("What will your twitter handle be?")
            password = input("Enter a password:")
            if input("Re-enter your password:") != password:
                print("Those passwords don't match. Try Again.")
                continue
            for used_username in users:
                if username == used_username:
                    print("That username is already taken. Try Again.")
                    continue
            self.current_user = User(username, password)
            self.logged_id = True
            db_session.add(self.current_user)
            db_session.commit()
            print("Welcome " + username + "!")
            break 

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            user = db_session.query(User).where((User.username == username) & (User.password == password)).first()
            if user is not None:
                print("Welcome " + username + "!")
                self.current_user = user
                self.logged_in = True
                break
            print("Username or password is invalid")
            

    
    def logout(self):
        self.current_user = None
        self.logged_in = False
        print("You have logged out.")
        self.startup()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS Twitter!")
        print("Please select a Menu Option")
        option = int(input("1. Login\n2. Register User\n 0. Exit"))
        if option == 1:
            self.login()
        elif option == 2
            self.register_user()
            
        

    def follow(self):
        pass

    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        # If there startup option is exit, this while loop will not run
        while self.logged_id:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()
