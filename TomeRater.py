class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        self.books_price = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("%s's email has been updated with %s" % (self.name, self.email))

    def __repr__(self):
        return "User - %s, email - %s, books read - %s, prices - %s" % (self.name, self.email, self.books, self.books_price)

    def __eq__(self, other_user):
        if self.name == other_user.name and  self.email == other_user.email:
            return True

    def read_book(self, book, rating = None, price = 0):
        self.books[book] = rating
        self.books_price[book] = price

    def get_average_rating(self):
        ratings_sum = 0
        for rating_value in self.books.values():
            if rating_value == None: continue
            ratings_sum += rating_value
        return ratings_sum / len(self.books)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Book(object):
    def __init__(self, title, isbn, price=0):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("This book's ISBN has been updated with %s" % self.isbn)

    def add_rating(self, rating):
        if rating >= 0 and rating <=4:
          self.ratings.append(rating)
        else:
          print("Invalid Rating")

    def __eq__(self, other_book):
        if other_book.title == self.title and self.isbn == other_book.isbn:
            return True

    def get_average_rating(self):
        total_rating = 0
        for value in self.ratings:
            total_rating += value
        return total_rating / len(self.ratings)

    def __repr__(self):
        return "%s with ISBN %s" % (self.title, self.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, price=0):
        self.author = author
        super().__init__(title, isbn, price)


    def get_author(self):
        return self.author

    def __repr__(self):
        return "\"%s\" by %s" % (self.title, self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=0):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "%s, a %s manual on %s" % (self.title, self.level, self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        all_users = "All our users:\n"
        all_books = "All our books:\n"
        result_string =  f"{all_users}\n {all_books}"
        for key in self.users.keys():
            all_users += key + '\n'
        for key in self.books.keys():
            all_books += key.title +'\n'
        return ( f" {all_users}\n {all_books}")

    def __eq__(self, other_tome_rater):
        if len(self.users) == len(other_tome_rater.users) and  len(self.books) == len(other_tome_rater.books):
            return True
        else:
            return False

    def __isbn_check(self, isbn):
        """
        Function checks isbn for duplication.
        """
        if len(self.books) == 0:
            return True
        else:
            for book_obj in self.books.keys():
                if book_obj.isbn != isbn:
                    continue
                else:
                    print("This ISBN belongs to another book. Check ISBN ")
                    return False
            return True

    def __email_check(self, email):
        """
        Function checks email for duplication and
          input email string for required symbols.
        """
        required_characters = ['.com', '.edu', '.org']
        if email in self.users:
            print(f"User {email} already exists")
        elif email.find('@') == -1:
            return False
        for val in required_characters:
            if email.find(val) != -1:
                return True
            else:
                continue
            return False

    def create_book(self, title, isbn, price=0):
        """
        Function takes in title, isbn and book's price, checks isbn for
          duplication and returns the Book object.
        """
        if self.__isbn_check(isbn):
            return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price=0):
        """
        Function takes in title, author, isbn and book's price, checks isbn for
          duplication and returns the Fiction object.
        """
        if self.__isbn_check(isbn):
            return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price=0):
        """
        Function takes in title, subject, level, isbn and book's price,
          checks isbn for duplication and returns the Non_Fiction object.
        """
        if self.__isbn_check(isbn):
            return Non_Fiction(title, subject, level, isbn, price)

    def add_user(self, name, email, user_books = None):
        """
        Function creates a User object and add it to the self.users dictionary.
        """
        if not self.__email_check(email):
            print(f"wrong email \"{email}\"")
        else:
            self.users[email] = User(name, email)
            if user_books:
                for book in user_books:
                    self.add_book_to_user(book, email)


    def add_book_to_user(self, book, email, rating = None, price = 0):
        """
        Function adds a book that user have just read to the list of user's book.
        Function increases the value in self.books when one more user have read a book.
        Firstly, the function checks if input email is in the self.users keys dict.
          Then the function looks for a match between the email and username and calls
          read_book function. If there is a parametr rating, it calls add_rating function from Book class.
        """
        if email not in self.users.keys():
            print("No user with %s!" % email)
        else:
            for user_name in self.users.keys():
                if user_name == email:
                    self.users[user_name].read_book(book.title, rating, book.price)
                if rating:
                    book.add_rating(rating)
        if book in self.books:
            self.books[book] += 1
        else:
            self.books[book] = 1

    def print_catalog(self):
        """
        Function prints current self.books dict.
        """
        print("THIS IS THE CATALOG OF ALL OUR BOOKS:")
        for book, amount in self.books.items():
            print(book.title + ' - rating: ' + str(amount))

    def print_users(self):
        """
        Function prints current self.users dict.
        """
        print("THESE ARE ALL OUR REGISTERED USERS:")
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        """
        Function loops through the self.books dict and seeks for the most read book.
          If there are several books with equal amount of readings the function returns all those books.
          If there is only one most read book the function returns a value of current_most_read_book variable.
        """
        current_most_read_book = None
        counter = 0
        most_read_books = []
        for book_obj, number_of_readings in self.books.items():
            if number_of_readings > counter:
                counter = number_of_readings
                current_most_read_book = book_obj
                most_read_books = []
            elif number_of_readings == counter:
                most_read_books.extend([current_most_read_book, book_obj])
                current_most_read_book = book_obj
            else:
                continue
        if len(most_read_books) > 0:
            output_result_string = ''
            for book in most_read_books:
                output_result_string += book.title + '\n'
            print("The most read books are:")
            return output_result_string
        else:
            return current_most_read_book.title

    def highest_rated_book(self):
        """
        Function iterates through the self.books and returns the book with highest rating.
          If thre are several highest rated books, the function returns them all.
        """
        current_highest_rated_book = None
        counter = 0
        highest_rated_books = []
        for book_obj, rating in self.books.items():
            if rating > counter:
                counter = rating
                current_highest_rated_book = book_obj
                highest_rated_books = []
            elif rating == counter:
                highest_rated_books.extend([current_highest_rated_book, book_obj])
                current_highest_rated_book = book_obj
            else: continue
        if len(highest_rated_books) > 0:
            print(highest_rated_books)
            output_result_string = ''
            for book in highest_rated_books:
                output_result_string += book.title + '\n'
            print("The highest rated books are:")
            return output_result_string
        else:
            return current_highest_rated_book.title

    def most_positive_user(self):
        """
        Function iterates through the self.users and returns the user with highest
         average rating.
        """
        counter = 0
        most_positive_user = None
        for username, user_obj in self.users.items():
            current_user_rating = user_obj.get_average_rating()
            if current_user_rating > counter:
                counter = current_user_rating
                most_positive_user = username
            elif current_user_rating == counter:
                most_positive_user = username
            else: continue
        return self.users[most_positive_user].name

    def get_n_most_read_books(self, n):
        """
        Function takes the 'N' number of books and return 'N' most read books.
         Function split up the self.books dict into two arrays.
         Then the function sorts the arrays synchronously in parallel and print out the most read books.
         If n-parametr is more than total amount of books in self.books then function
         print out an error string.
        """
        number_of_readings_array = []
        books_title_array = []
        for book_obj, readings in self.books.items():
            books_title_array.append(book_obj.title)
            number_of_readings_array.append(readings)
        for i in range(len(number_of_readings_array)):
            for index in range(len(number_of_readings_array) - i - 1):
                if number_of_readings_array[index] < number_of_readings_array[index + 1]:
                    number_of_readings_array[index], number_of_readings_array[index + 1] = number_of_readings_array[index + 1], number_of_readings_array[index]
                    books_title_array[index], books_title_array[index + 1] = books_title_array[index + 1], books_title_array[index]
        if n > len(number_of_readings_array):
            print(f"You've requested too many books. The number of the books in the catalog: {len(number_of_readings_array)} items")
        else:
            print("THE MOST READABLE BOOKS BY YOUR REQUEST:")
            for i in range(n):
                print(books_title_array[i])

    def get_n_most_prolific_readers(self, n):
        users_books = []
        users = []
        if n > len(self.users):
            print(f"You've requested too many users. The number of the users in the database: {len(self.users)} persons")
            return False
        else:
            for title, user_obj in self.users.items():
                users.append(title)
                users_books.append(len(user_obj.books))
            for i in range(len(users)):
                for index in range(len(users) - i - 1):
                    if users_books[index] < users_books[index + 1]:
                        users_books[index], users_books[index + 1] = users_books[index + 1], users_books[index]
                        users[index], users[index + 1] = users[index + 1], users[index]
        print("THE MOST PROLIFIC READERS:")
        for i in range(n):
           print(users[i])

    def get_n_most_expensive_books(self, n):
        """
        Function takes the 'n' number of books and return the most expencive books.
         Function split up the self.books dict into two arrays.
         Then the function sorts the arrays synchronously in parallel and print out most expencive books.
         If n-parametr is more than total amount of books in self.books then function
         print out an error string.
        """
        prices_array = []
        books_title_array = []
        if n > len(self.books):
            print(f"You've requested too many books. The number of the books in the catalog: {len(prices_array)} items")
        elif len(self.books) == 0:
            print("Catalog is empty")
        else:
            for book in self.books.keys():
                prices_array.append(book.price)
                books_title_array.append(book.title)
            for i in range(len(prices_array)):
                for index in range(len(prices_array) - i - 1):
                    if prices_array[index] < prices_array[index + 1]:
                        prices_array[index], prices_array[index + 1] = prices_array[index + 1], prices_array[index]
                        books_title_array[index], books_title_array[index + 1] = books_title_array[index + 1], books_title_array[index]
        print("THE MOST EXPENSIVE BOOKS BY YOUR REQUEST:")
        for i in range(n):
            print(books_title_array[i] + ' - usd ' + str(prices_array[i]))

    def get_worth_of_user(self, user_email):
        """
        Function returns the sum of the costs of all the books read by given user
        """
        sum_of_the_costs = 0
        for price in self.users[user_email].books_price.values():
            sum_of_the_costs += price
        return f"{user_email} - usd {sum_of_the_costs}"
