# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   RRoot, 1/1/2030, Created Script
#   Natalie Ferri, 08/12/2024, Modifying RRoot's Script with
#       class Person and class Student
#   Natalie Ferri, 08/13/2024, Make script more pythonic
# ------------------------------------------------------------------------------------------ #


import json

# Define the Data Constants
MENU = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME = "Enrollments.json"

# Define the Data Variables
students = []  # List to hold Student objects
menu_choice = ''  # Variable to hold the user's menu choice


# Define the Person Class
class Person:
    """
    A class representing person data with error identification.

    ChangeLog:
    Natalie Ferri, 8/12/2024, Created class Person

    proterty first_name: string data
    property last_name: string data

    Inherited by:
        Student class
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        """
        Initialize a Person object with first and last names.
        
        :param first_name: The first name of the person
        :param last_name: The last name of the person
        """
        self._first_name = ''
        self._last_name = ''
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        """
        Get the first name of the person, capitalized.
        
        :return: The first name in title case
        """
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Set the first name with validation.
        
        :param value: The first name to set
        :raises ValueError: If the value is not alphabetic
        """
        if value.isalpha() or not value:
            self._first_name = value
        else:
            raise ValueError("First name must be alphabetic, cannot contain numbers.")

    @property
    def last_name(self) -> str:
        """
        Get the last name of the person, capitalized.
        
        :return: The last name in title case
        """
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Set the last name with validation.
        
        :param value: The last name to set
        :raises ValueError: If the value is not alphabetic
        """
        if value.isalpha() or not value:
            self._last_name = value
        else:
            raise ValueError("Last name must be alphabetic, cannot contain numbers.")

    def __str__(self) -> str:
        """
        Return a string representation of the Person.
        
        :return: A comma-separated string of the first and last name
        """
        return f'{self.first_name},{self.last_name}'


# Define the Student Class
class Student(Person):
    """
    A class representing student data with error identification.

    ChangeLog:
    Natalie Ferri, 8/12/2024, Created class Student

    property course_name: string data
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        """
        Initialize a Student object with first and last names and course name.
        
        :param first_name: The first name of the student
        :param last_name: The last name of the student
        :param course_name: The name of the course the student is enrolled in
        """
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        """
        Get the course name, capitalized.
        
        :return: The course name in title case
        """
        return self._course_name.title()

    @course_name.setter
    def course_name(self, value: str) -> None:
        """
        Set the course name with validation.
        
        :param value: The course name to set
        :raises ValueError: If the value contains invalid characters
        """
        if all(char.isalnum() or char.isspace() for char in value) or not value:
            self._course_name = value
        else:
            raise ValueError("Course name must be alphanumeric")

    def __str__(self) -> str:
        """
        Return a string representation of the Student.
        
        :return: A comma-separated string of the first name, last name, and course name
        """
        return f'{super().__str__()},{self.course_name}'


# Define the FileProcessor Class
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Natalie Ferri, 8/12/2024, Added Student to list
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """
        Read student data from a JSON file and populate the student_data list.

        RRoot,1.1.2030,Created function
        Natalie Ferri, 8/12/2024, list of dictionaries instead of lists

        :param file_name: The name of the file to read from
        :param student_data: The list to populate with Student objects
        :return: The updated list of Student objects
        """
        try:
            # Open file and load JSON data
            with open(file_name, "r") as file:
                list_of_dict_data = json.load(file)
                
                # Convert each dictionary to a Student object and add to the list
                student_data.extend(Student(
                    first_name=student["FirstName"],
                    last_name=student["LastName"],
                    course_name=student["CourseName"]
                ) for student in list_of_dict_data)
                
        except Exception as e:
            IO.output_error_messages("Error reading the file.", e)
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list) -> None:
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Natalie Ferri, 8/12/2024, list of dictionaries instead of lists

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        try:
            # Convert Student objects to dictionaries
            list_of_dict_data = [{
                "FirstName": student.first_name,
                "LastName": student.last_name,
                "CourseName": student.course_name
            } for student in student_data]
            
            # Write the dictionary list to the file
            with open(file_name, "w") as file:
                json.dump(list_of_dict_data, file)
                
            # Output the current student and course names
            IO.output_student_and_course_names(student_data)
        except Exception as e:
            IO.output_error_messages("Error writing to the file. Please ensure the file is not open elsewhere.", e)


# Define the IO Class
class IO:
    '''
    This class includes functions that display a menu with choices, accepts user input,
        present user input, and has error handling.
    '''
    
    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """
        Output custom error messages to the user.
        
        :param message: The custom message to display
        :param error: Optional exception to display technical details
        """
        print(f"{message}\n")
        if error:
            print("-- Technical Error Message --")
            print(f"{error}\n{error.__doc__}\n{type(error)}")

    @staticmethod
    def output_menu(menu: str) -> None:
        """
        Display the menu of choices to the user.
        
        :param menu: The menu string to display
        """
        print(f"\n{menu}\n")

    @staticmethod
    def input_menu_choice() -> str:
        """
        Get and validate the user's menu choice.
        
        :return: The valid menu choice entered by the user
        """
        while True:
            try:
                choice = input("Enter your menu choice number: ")
                if choice in ("1", "2", "3", "4"):
                    return choice
                raise ValueError("Please choose only 1, 2, 3, or 4")
            except ValueError as e:
                IO.output_error_messages(str(e))

    @staticmethod
    def output_student_and_course_names(student_data: list) -> None:
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Natalie Ferri, 8/12/2024, Changed f string

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Natalie Ferri, 8/12/2024, Added Student to read dictionary.

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """
        try:
            # Create a new Student object with user input
            student = Student(
                first_name=input("Enter the student's first name: "),
                last_name=input("Enter the student's last name: "),
                course_name=input("Please enter the name of the course: ")
            )
            
            student_data.append(student)
            print(f"\nYou have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages("One of the values was of incorrect type!", e)
        except Exception as e:
            IO.output_error_messages("Error with the entered data.", e)
        return student_data


# Main Program
students = FileProcessor.read_data_from_file(FILE_NAME, students)  # Load existing student data

while True:
    IO.output_menu(MENU)  # Display the menu
    menu_choice = IO.input_menu_choice()  # Get the user's choice

    if menu_choice == "1":
        students = IO.input_student_data(students)  # Register a new student
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)  # Show current data
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)  # Save data to a file
    elif menu_choice == "4":
        break  # Exit the loop
    else:
        print("Please choose a valid option.")

print("Program Ended")
