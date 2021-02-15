"""
https://cppsecrets.com/users/3081149711010610511611464104111116109971051084699111109/Python-Program-to-Extract-Text-from-Indian-Driving-Licence.php
"""

from PIL import Image
import pytesseract
import datetime
import sys
import os
import os.path
import re
import cv2
import numpy as np

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
# Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# It's important to include double quotes around the dir path.

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# class to extract text from an image where the image file is passed as an argument
# to the command
class Text_Extractor():
    # Constructor
    def __init__(self):
        image_file = './image.jpg'
        self.image_file = image_file
        print(image_file)
        if self is None:
            return 0

    # Function to extract the text from image as string
    def extract_text(self):
        try:
            image = cv2.imread('img.jpg')
            print(image)
            # Convert to gray
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Resize the image
            image = cv2.resize(image, None, fx=2, fy=2)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(image, config=tessdata_dir_config)
            return text
        except Exception as e:
            print(str(e))


# class to validate if an image is a drivers licence
class Drivers_Licence_Validator:
    # Constructor
    def __init__(self, text):
        self.text = text

    # Function to validate  an Indian driving licence
    def is_licence(self):
        res = self.text.split('/n')
        for word in res:
            if word == 'Driving' or 'DRIVING':
                print("Document is a Indian Drivers licence")
                return True
            else:
                print("Document is not a Indian Drivers licence")
                print("Please try again with a valid Drivers licence")
                return False

    # Function to find the age of the licence holder
    def age(self, y, m, d):
        dob = datetime.date(y, m, d)
        today = datetime.date.today()
        years = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            years -= 1
        return years

    # Function to validate if driving licence is expired or not
    def is_valid(self):
        if (self.is_licence()):
            res = self.text.split()
            list_of_states = {'JK', 'HP', 'PN', 'CH', 'UK', 'UA', 'HR', 'DL', 'RJ', 'UP', 'BR', 'SK', 'AR', 'AS', 'NL',
                              'MN', 'ML', 'TR', 'MZ', 'WB', 'JH', 'OR', 'OD', 'CG', 'MP', 'GJ', 'MH', 'DD', 'DN', 'TS',
                              'AP', 'KA', 'KL', 'TN', 'PY', 'GA', 'AN', 'LD'}
            match = None
            day = None
            month = None
            year = None
            date_of_expiry = None
            dob = None
            count = 0
            s = None
            strings_with_states = []
            # get all the dates in a list
            p = re.compile('d+/d+/d+')
            if (p.findall(self.text)):
                dates = p.findall(self.text)
            else:
                p = re.compile('d+-d+-d+')
                dates = p.findall(self.text)
            now = datetime.datetime.now()
            for date in dates:
                if '/' in date:
                    day, month, year = date.split("/")
                else:
                    day, month, year = date.split("-")
                age = self.age(int(year), int(month), int(day))
                temp_date = datetime.datetime(int(year), int(month), int(day))
                if temp_date >= now:
                    date_of_expiry = temp_date
                if age >= 18:
                    dob = temp_date
            if date_of_expiry:
                print("Date of expiry :" + str(date_of_expiry.strftime('%Y-%m-%d')))
            else:
                print("Cannot determine the date of expiry or the licence has expired")
            if dob:
                print("Date of birth :" + str(dob.strftime('%Y-%m-%d')))
            elif 'DOB' in res:
                index = res.index('DOB')
                if ':' not in res[index + 1]:
                    print('DOB is: ' + res[index + 1])
                else:
                    print('DOB is: ' + res[index + 2])
            else:
                print("Cannot determine the date of birth")
            # check for strings with state codes
            for word in res:
                for state in list_of_states:
                    if state in word:
                        strings_with_states.append(word)
            # get the driving licence # from the strings with state codes
            for string in strings_with_states:
                for i in string:
                    if (i.isdigit()):
                        count = count + 1

                if count < 13:
                    index = res.index(string)
                    s = res[index] + res[index + 1]
                    if len(s) >= 15:
                        for i in s:
                            if (i.isdigit()):
                                count = count + 1
                        if count > 13:
                            s = s[-16:]
                            print('Driving licence # is :' + s)
                            break
                            break
                else:
                    print('Driving licence # is :' + string)
                    break
                    break
            # get the name next to the string 'Name' in the text extracted
            if 'Name' in res:
                index = res.index('Name')
                print('Name of licence holder: ' + res[index + 1] + ' ' + res[index + 2])
            return True


def main():
    te = Text_Extractor()
    image_text = te.extract_text()
    print(image_text)  # call the text extractor function
    # dlv=Drivers_Licence_Validator(image_text)
    # dlv.is_valid()				# call  the licence validation function


main()
