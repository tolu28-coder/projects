import requests
import hashlib
from tkinter import *
from tkinter.messagebox import showinfo

password = 'password123'
hashing = 'CBFDA'


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/'+ str(query_char)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching : {res.status_code},check the api and try again')
    return res

def get_password_leak_count(response,tail):
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
    count = pwned_api_check(password)
    if count:
        return f'Password has been found this many {count} times try changing it'
    else:
        return 'Password has not been found'


def action(widget):
    password = widget.get()
    showinfo(message=main(password))


parent = Tk()
Label(parent,text = 'Type password in here').grid(row=0,column = 0)
entrybox = Entry(parent, show="*", width=15)
entrybox.grid(row = 0, column = 1)
Button(parent,text = 'check my password' ,command = lambda: action(entrybox)).grid(row = 1)
parent.mainloop()

