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
            self.logged_in = True
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
        option = int(input("1. Login\n2. Register User\n0. Exit\n"))
        if option == 1:
            self.login()
        elif option == 2:
            self.register_user()
            
        

    def follow(self):
        following_id = input("Who would you like to follow?\n")
        following_user = db_session.query(User).where(User.username == following_id).first()
        if following_user in self.current_user.following:
            print("You already follow " + following_id)
        else:
            if following_user is not None:
                db_session.add(Follower(self.current_user.username, following_id))
                db_session.commit()
                print("Now you are following " + following_id)
            else:
                print("This user does not exist.")
        

    def unfollow(self):
        following_id = input("Who would you like to unfollow?\n")
        currently_following = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) & (Follower.following_id == following_id)).first()
        if currently_following is not None:
            db_session.delete(currently_following)
            db_session.commit()
            print("You no longer follow " + following_id)
        else:
            print("You don't follow " + following_id)
        


    def tweet(self):
        content = input("Create Tweet: ")
        tags = input("Enter Your Tags: ")
        tags = tags.split()
        tweet = Tweet(content, self.current_user.username, datetime.now())
        db_session.add(tweet)
        db_session.commit()
        for tag in tags:
            current = db_session.query(Tag).where(Tag.content == tag).first()
            if current is None:
                current = Tag(tag)
                db_session.add(current)
                db_session.commit()
            db_session.add(TweetTag(tweet.id, current.id))
        db_session.commit()
        

    
    def view_my_tweets(self):
        tweets = self.current_user.tweets
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        following = self.current_user.following
        for user in following:
            if len(user.tweets) >= 5:
                self.print_tweets(user.tweets[0:5])
            else:
                self.print_tweets(user.tweets)

    def search_by_user(self):
        username = input("Username: ")
        user = db_session.query(User).where(User.username == username).first()
        if user is None:
            print("There is no user by that name")
        else:
            self.print_tweets(user.tweets)

    def search_by_tag(self):
        content = input("Tag: ")
        tag = db_session.query(Tag).where(Tag.content == content).first()
        if tag is None or len(tag.tweets) == 0:
            print("There is no tweets with this tag")
        else:
            self.print_tweets(tag.tweets)
        

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()


        print("Welcome to ATCS Twitter!")
        self.startup()
        # If there startup option is exit, this while loop will not run
        while self.logged_in:
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
