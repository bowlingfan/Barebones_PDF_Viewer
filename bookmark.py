#https://stackoverflow.com/questions/6648493/how-to-open-a-file-for-both-reading-and-writing
import os

"""
bookmark data from txt_file:
directory = NUMBER
"""
class PDF_Bookmark():
    text_file_link = "bookmark_data.txt"
    bookmarks = {}

    def __init__(self):
        self.bookmark_data = None
        if not os.path.isfile(PDF_Bookmark.text_file_link):
            self.bookmark_data = open(PDF_Bookmark.text_file_link, "w")
            self.bookmark_data.close()
        self.import_bookmark_data()

    def __del__(self):
        self.bookmark_data.close()
        self.bookmark_data = None

    def import_bookmark_data(self):
        self.bookmark_data = open(PDF_Bookmark.text_file_link, "r")

        for cline in self.bookmark_data.readlines():
            line = cline.strip('\n')
            data = line.split(" = ")

            directory = data[0]
            page_number = int(data[1])

            PDF_Bookmark.bookmarks.update({directory: page_number})

        self.bookmark_data.close()
    
    def add_bookmark_data(self, directory, page_number):
        self.bookmark_data = open(PDF_Bookmark.text_file_link, "a")

        self.bookmark_data.write(f"{directory} = {page_number}\n")
        PDF_Bookmark.bookmarks.update({directory: page_number})

        self.bookmark_data.close()

    def remove_bookmark_data(self, directory):
        if self.directory_exists(directory):
            self.bookmark_data = open(PDF_Bookmark.text_file_link, "w")

            PDF_Bookmark.bookmarks.pop(directory)
            self.bookmark_data.truncate(0)
            self.bookmark_data.seek(0)
            for directory in PDF_Bookmark.bookmarks:
                self.bookmark_data.write(f"{directory} = {PDF_Bookmark.bookmarks[directory]}\n")

            self.bookmark_data.close()

    def directory_exists(self, directory):
        return directory in PDF_Bookmark.bookmarks

    def get_bookmark_page_number(self, directory):
        if self.directory_exists(directory):
            return PDF_Bookmark.bookmarks[directory]
        else:
            return -1