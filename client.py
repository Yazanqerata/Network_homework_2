import socket

HOST = '127.0.0.1'
PORT = 8000

csock= socket.socket()
csock.connect((HOST, PORT))

account_number = input("Enter your account number: ")
password = input("Enter your password: ")

csock.send(account_number.encode())
csock.send(password.encode())

response = csock.recv(1024).decode()
if response == "Authentication successful":
    print("Authentication successful")
else:
    print("Authentication failed")
    csock.close()
    exit()

while True:
    operation = input("Enter operation (balance, deposit, withdraw, exit): ")
    csock.send(operation.encode())

    if operation == "balance":
        balance = float(csock.recv(1024).decode())
        print("Your balance is:",balance)
    elif operation == "deposit":
        amount = float(input("Enter deposit amount: "))
        csock.send(str(amount).encode())
        new_balance = float(csock.recv(1024).decode())
        print("New balance:",new_balance)
    elif operation == "withdraw":
        amount = float(input("Enter withdrawal amount: "))
        csock.send(str(amount).encode())
        result = csock.recv(1024).decode()
        print("your balance now is :",result)
    elif operation == "exit":
        final_balance = float(csock.recv(1024).decode())
        print("Final balance:",final_balance)
        csock.close()
        break
    else:
        print("Invalid operation")