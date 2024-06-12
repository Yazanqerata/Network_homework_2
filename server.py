import socket
import threading
accounts = {
    "02706": 1000.0,
    "02602": 5000.0,
    "01234": 500.0
}
def get_balance(account_number):
    return accounts[account_number]

def deposit(account_number, amount):
    accounts[account_number] += amount
    return accounts[account_number]

def withdraw(account_number, amount):
    if accounts[account_number] >= amount:
        accounts[account_number] -= amount
        return accounts[account_number]
    else:
        return "you dont have enough money"

HOST = '127.0.0.1'
PORT = 8000

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

def handle_client(cc, cadd):
    print(f"New connection from {cadd}")

    # Authenticate the client
    account_number = cc.recv(1024).decode()
    password = cc.recv(1024).decode()
    # Verify the account number and password
    if account_number in accounts and password == "0000":
        cc.send("Authentication successful".encode())
    else:
        cc.send("Authentication failed".encode())
        cc.close()
        return

    while True:
        operation = cc.recv(1024).decode()
        if operation == "balance":
            balance = get_balance(account_number)
            cc.send(str(balance).encode())
        elif operation == "deposit":
            amount = float(cc.recv(1024).decode())
            new_balance = deposit(account_number, amount)
            cc.send(str(new_balance).encode())
        elif operation == "withdraw":
            amount = float(cc.recv(1024).decode())
            result = withdraw(account_number, amount)
            cc.send(str(result).encode())
        elif operation == "exit":
            cc.send(str(get_balance(account_number)).encode())
            cc.close()
            print("Connection with", cadd, "closed")
            break
        else:
            pass

while True:
    cc, cadd = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(cc, cadd))
    client_thread.start()

