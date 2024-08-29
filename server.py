import sqlite3
import socket

GET_BALANCE = 0
SEND_MONEY = 1

class Server:
    def __init__(self, port):
        self.port = port
        self.con = sqlite3.connect("clients.db")
        self.cur = self.con.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, login CHAR(128), balance INTEGER)")
        
    
    def get_user_balance(self, id):
        return self.cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchall()[0][2]
    
    def create_user(self, login, balance):
        self.cur.execute("INSERT INTO clients (login, balance) VALUES (?, ?)", (login, balance))
        self.con.commit()
        
    def remove_user(self, id):
        self.cur.execute("DELETE FROM clients WHERE id = ?", (id,))
        
    def update_user_balance(self, id, balance):
        self.cur.execute("UPDATE clients SET balance = ? WHERE id = ?", (balance, id))
        self.con.commit()
        
    def listen(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(("127.0.0.1", self.port))
        
        server_sock.listen()
        
        while True:
            client_sock, client_addr = server_sock.accept()
            data = client_sock.recv(1024)
            operation = data[0].to_bytes()

            
            match operation:
                case b'0': 
                    id = int(data[1].to_bytes())
                    client_sock.send(f"{self.get_user_balance(id)}".encode())
                case b'1': break
            
        
if __name__ == "__main__":
    server = Server(9999)
    server.listen()