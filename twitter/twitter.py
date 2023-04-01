from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self, current_user=None, logged_in=False):
        self.current_user = current_user
        self.logged_in = logged_in
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
        while True:
            # Ask for username and password
            username = input("What will your twitter handle be?\n")
            password = input("Enter a password: ")
            # Prompt again if passwords don't match
            if input("Re-enter your password: ") != password:
                print("Those passwords don't match. Try Again.")
                continue
            # Prompt again if username is taken
            if db_session.query(User).where(User.username == username).first() is not None:
                print("This username is already taken. Try again.")
                continue
            # Set object instance variables and add to database 
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
            # Prompt for username and password
            username = input("Username: ")
            password = input("Password: ")
            # Query for this specific login, and if there is nothing that has the inputted login info, prompt again
            user = db_session.query(User).where((User.username == username) & (User.password == password)).first()
            if user is None:
                print("Username or password is invalid")
            else:
                # If login info is correct, update instance variables to reflect
                print("Welcome " + username + "!")
                self.current_user = user
                self.logged_in = True
                break 

    
    def logout(self):
        # Reset login info
        self.current_user = None
        self.logged_in = False
        print("You have logged out.")
        # Prompt again if they want to access a different account
        self.startup()

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        # Welcome user and prompt them to choose a valid menu option
        print("Welcome to ATCS Twitter!")
        while True:
            print("Please select a Menu Option")
            option = int(input("1. Login\n2. Register User\n0. Exit\n"))
            if option == 1:
                self.login()
                break
            elif option == 2:
                self.register_user()
                break
            elif option == 0:
                break
            else:
                print("Choose a valid option. Try again.")
            
            
        

    def follow(self):
        # Prompt and query requested user to follow
        following_id = input("Who would you like to follow?\n")
        following_user = db_session.query(User).where(User.username == following_id).first()
        # If the user already follows the request following, tell them
        if following_user in self.current_user.following:
            print("You already follow " + following_id)
        else:
            # Make sure the requested user exists and then follow them if they do
            if following_user is not None:
                db_session.add(Follower(self.current_user.username, following_id))
                db_session.commit()
                print("Now you are following " + following_id)
            else:
                print("This user does not exist.")
        

    def unfollow(self):
        # Prompt for requested user to unfollow
        following_id = input("Who would you like to unfollow?\n")
        currently_following = db_session.query(Follower).where((Follower.follower_id == self.current_user.username) & (Follower.following_id == following_id)).first()
        # Delete from the user's following if they do follow them
        if currently_following is not None:
            db_session.delete(currently_following)
            db_session.commit()
            print("You no longer follow " + following_id)
        else:
            print("You don't follow " + following_id)
        


    def tweet(self):
        # Prompt for tweet's content and tags
        content = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces: ") 
        tweet = Tweet(content, self.current_user.username, datetime.now())
        db_session.add(tweet)
        db_session.commit()
        # Create tweet tag to connect the tweet and tag
        for tag in tags.split():
            current = db_session.query(Tag).where(Tag.content == tag).first()
            if current is None:
                current = Tag(tag)
                db_session.add(current)
                db_session.commit()
            db_session.add(TweetTag(tweet.id, current.id))
        db_session.commit()
        print("Your tweet has been posted!")
        

    
    def view_my_tweets(self):
        # Get list of user's tweets and print them
        self.print_tweets(self.current_user.tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        # Print 5 most recent tweets from following list
        users = [user.username for user in self.current_user.following]
        tweets = db_session.query(Tweet).where(Tweet.username.in_(users)).order_by(Tweet.timestamp.desc()).limit(5)
        self.print_tweets(tweets)
        

    def search_by_user(self):
        # Prompt user for requested user and print all tweets by that user
        username = input("Username: ")
        user = db_session.query(User).where(User.username == username).first()
        if user is None:
            print("There is no user by that name")
        else:
            self.print_tweets(user.tweets)

    def search_by_tag(self):
        # Prompt user for requested tag and print all tweets with that tag
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
