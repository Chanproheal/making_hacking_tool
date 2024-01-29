The guest_login program is a program that automatically fills in an id and password in an input form that exists on a login page and finds a password to log that id into the website.

This guest_login specifies a login page, target_url, and finds the password for the target login page by automatically filling in the password.

In that guest_login.py, we're fixing the username to be admin.

Usage : 
Example) python guest_login.py

********* Caution when using the program**********
You need to specify the URL of the target you want.
target_url = {URL you want to search}.
Example) "http://myhomepage/login.php", "namver.com/login.php"

Since different pages may have different names and values for input, you'll need to change that file to match your target page.
>> data_dict ={"username":"admin","password":"","Login":"submit"}
Where "username", "password", and "Login" are the names of the input formats used for input, respectively, please change them to match your page.
In the case of "admin", the username is fixed to admin in the file, but if you want to use a different username, change the "admin" part to "{your desired username}" and use it.
Since this file is for testing purposes, there are not many passwords in passwords.txt, but if you have your own password dictionary file, you can delete the existing passwords.txt and rename it to passwords.txt and use it. Also, the geust_login.py file and the passwords.txt file must be in the same path for it to work properly.
