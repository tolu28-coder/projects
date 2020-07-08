import requests
import hashlib
from tkinter import *
from tkinter.messagebox import showinfo


def request_api_data(query_char):
        """
	Gets data corresponding to data of hashed passwords starting with first 5 character 
	given by query_char arguement, this data is obtained from pwned api
        """
        url = 'https://api.pwnedpasswords.com/range/'+ str(query_char)
        response = requests.get(url)
        if response.status_code != 200:
                raise RuntimeError(f'error fetching : {res.status_code},check the api and try again')
        return response

def get_password_leak_count(response,tail):
	#It determines how many times password appears in data obtained from api
        hashes = (line.split(':') for line in response.text.splitlines())
        for h,count in hashes:
                if h == tail:
                        return count

        return 0

    
def pwned_api_check(password):
    #check password if it exists in api response
        sha1password = hashlib.sha1(str(password).encode('utf-8')).hexdigest().upper()
        first_5char,tail = sha1password[:5],sha1password[5:]
        response = request_api_data(first_5char)
        return get_password_leak_count(response,tail)
    

def main(password):
	# a wrapper for pwned_api_check
        count = pwned_api_check(password)
        if count:
                return f'Password has been found this many {count} times try changing it'
        else:
                return 'Password has not been found'


def runmain(widget):
        password = widget.get()
        showinfo(message=main(password))

def showpass(widget):
        password = widget.get()
        showinfo(message=password)



parent = Tk()
Label(parent,text = 'Type password in here').grid(row=0,column = 0)
entrybox = Entry(parent, show="*", width=15)
entrybox.grid(row = 0, column = 1)
Button(parent,text = 'check my password' ,command = lambda: runmain(entrybox)).grid(row = 1,column = 0)
Button(parent,text = 'show password' ,command = lambda: showpass(entrybox)).grid(row = 1,column = 1)
parent.mainloop()

