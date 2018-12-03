"""PDFExtractor
Takes in a file name of a PDF, then uses PyPDF and gTTS to turn it into a Google TTS-read mp3 file.
"""

import PyPDF2
from gtts import gTTS
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def convert_to_mp3(file_name):
    """Converts file with the name file_name into an mp3 file.
    """

    # Catches case of file_name not being a .pdf file. (Might not work if in folder with ".pdf" in it.)
    if ".pdf" not in file_name:
        print("Not a pdf file.")
        return

    file_text = ""

    to_open = open(file_name, "rb")
    to_read = PyPDF2.PdfFileReader(to_open)

    # Adds each page to a String to be processed into an mp3
    for a in range(0, to_read.getNumPages()):
        current_page = to_read.getPage(a).extractText()
        file_text += current_page
        print(current_page)

    # Commonly misread symbols in PDFs
    symbol_dict = {
        "™": "\'",
        "ﬁ": "\"",
        "Š": "--"
    }

    new_book_string = ""

    # Rebuilding the book with fixed symbols.
    for word in file_text.split(" "):

        changed_word = word

        # If the word contains characters that are often misread, changes them accordingly
        for character in word:
            if character in symbol_dict:
                changed_word = changed_word.replace(character, symbol_dict.get(character))

        new_book_string += changed_word + " "

    # Turns the string into a .mp3 file for easy listening :)
    to_text = gTTS(text=new_book_string, lang='en')
    to_text.save("audiobook.mp3")


if __name__ == "__main__":

    # Opens dialog to get the PDF file you want
    # Taken from the answer to https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    Tk().withdraw()
    to_convert = askopenfilename()
    convert_to_mp3(to_convert)
