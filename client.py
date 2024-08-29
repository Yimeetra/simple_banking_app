import socket

class Client:
    def __init__(self, id: int, port: int):
        self.id = id
        self.port = port

    def check_balance(self):
        sock = socket.socket()
        sock.connect(('127.0.0.1', self.port))
        sock.send((0).to_bytes()+self.id.to_bytes())
        balance = int(sock.recv(1024))
        sock.close()
        return balance
        
    def make_transaction(self, reciever_id: int, amount: int):
        sock = socket.socket()
        sock.connect(('127.0.0.1', self.port))
        sock.send((1).to_bytes()+
                       (1).to_bytes()+
                       (2).to_bytes()+
                       amount.to_bytes(4))
        
        is_done = int.from_bytes(sock.recv(1024)) == 1
        sock.close()
        return is_done
    

if __name__ == "__main__":
    client = Client(1, 9999)

    print("Choose your action:")
    print("1 - check your balance")
    print("2 - make a transaction")
   
    action  = input()
    
    match action:
        case '1':
            print(f"Your balance is {client.check_balance()}")
        case '2':
            while 1:
                try:
                    reciever_id = int(input("Input reciever id: "))
                    
                    break
                except ValueError:
                    print('Id must be integer')
                    
            while 1:
                try:
                    amount = int(input("Input amount of money to send: "))
                    break
                except ValueError:
                    print('Amount must be integer')           
            
            if client.make_transaction(reciever_id, amount):
                print(f"You sent {amount} to user with id {reciever_id}!")
                print(f"Your remain is {client.check_balance()}")
            else:
                print("You have not enough money")
                