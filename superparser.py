class SuperParser:
    def __init__(self):
        pass

    def file_contents(self,filename):
        #opens a file (NOT a webpage, as in get_contents), reads the text of the file, assigns it to variable contents and returns contents
        f = open(filename, 'r')
        contents = f.read()
        f.close()
        return contents
