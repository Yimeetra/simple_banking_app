import sqlite3
import socket

class Server:
    def __init__(self, port: int):
        self.port = port
        self.con = sqlite3.connect("clients.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, login CHAR(128), balance INTEGER)")
        
    
    def get_user_balance(self, id: int):
        return self.cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchall()[0][2]
    
    def create_user(self, login: str, balance: int):
        self.cur.execute("INSERT INTO clients (login, balance) VALUES (?, ?)", (login, balance))
        self.con.commit()
        
    def remove_user(self, id: int):
        self.cur.execute("DELETE FROM clients WHERE id = ?", (id,))
        
    def update_user_balance(self, id: int, balance: int):
        self.cur.execute("UPDATE clients SET balance = ? WHERE id = ?", (balance, id))
        self.con.commit()
        
    def listen(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(("127.0.0.1", self.port))
        
        server_sock.listen()
        
        while 1:
            client_sock, client_addr = server_sock.accept()
            data = client_sock.recv(1024)
            operation = data[0]

            #   Posible packets:
            #   0  id
            #   1  sender_id  reciever_id  amount
            match operation:
                case 0: 
                    id = int(data[1])
                    client_sock.send(f"{self.get_user_balance(id)}".encode())
                    
                case 1:
                    sender_id = int(data[1])
                    reciever_id = int(data[2])
                    amount = int.from_bytes(data[3:7])
                    
                    print(amount, self.get_user_balance(sender_id))
                    if amount > self.get_user_balance(sender_id):
                        client_sock.send((0).to_bytes())
                    else:
                        self.update_user_balance(sender_id, self.get_user_balance(sender_id)-amount)
                        self.update_user_balance(reciever_id, self.get_user_balance(reciever_id)+amount)
                        client_sock.send((1).to_bytes())
                    
                case 2: break
                    
                    
            
        
if __name__ == "__main__":
    server = Server(9999)
    server.listen()