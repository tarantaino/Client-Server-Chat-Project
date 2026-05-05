import socket
import sys
from _thread import start_new_thread

users = {} #dizionario per lista utenti
active_chats = {} #dizionario per chat attive

HOST = "127.0.0.1"
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created!")

try:
        s.bind((HOST, PORT))
except socket.error as msg:
        print("Bind failed. Error Code: " + str(msg[0] + " Message " + msg[1]))
        sys.exit()

print("Socket bind complete")

s.listen(10)
print("Socket now listening\n")

def clientthread(conn):
    print("Welcome to the server!\n")

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        
        if " " in data and data.count(" ") == 2: #se gli spazi nell'input sono due
            try:
                nick, ip, port = data.split(" ") #separazione dati in base agli spazi
                port = int(port)
                if nick in users: #se il nick è già presente ritorna la stringa
                    conn.sendall(b"User already registered!\n")
                else:
                    users[nick] = (ip, port) #altrimenti associa nick: ip, port e salva in users
                    conn.sendall(b"User registered successfully!\n")
                    print(f"{nick} registered successfully with {ip}:{port}\n")
            except ValueError:
                conn.sendall(b"Invalid data format. Use: <nickaname> <ip> <port>")
                           
         #condizioni per i comandi
        elif data.startswith("!"):
            if data == "!who":
                if not users:
                    conn.sendall(b"No users online.\n")
                else:
                        users_list = "\n".join(f"{nickname}, {ip}:{port}" for nickname, (ip, port) in users.items())
                        conn.sendall(users_list.encode())   #invio stampa utenti online 
                        
       
            if data == "!quit":
                print(f"{nick}, {ip}:{port} has left...\n")
                del users[nick] #se !quit -> cancella utente dal dizionario
 
            if data.startswith("!connect "):
                p = data.split(" ", 1) #!connect + nome utente, catturo nome utente
                if len(p) < 2: #se non passo il nome utente - ritorna errore
                    conn.sendall(b"ERR - No username provided\n")
                else:
                    user_nick = p[1] #altrimenti verifico l'esistenza del nickname passato

                if user_nick not in users: #controllo se è realmente online/occupato in una chat
                    conn.sendall(b"User not found or offline.\n")
                elif nick in active_chats or user_nick in active_chats:
                    conn.sendall(b"ERR - One of the users is already in a chat.\n")
                else:
                    user_ip, user_port = users[user_nick]
                    r = f"{user_nick} {user_ip} {user_port}"
                    active_chats[nick] = user_nick
                    active_chats[user_nick] = nick
                    conn.sendall(r.encode())
                    print(f"User {nick} is now in chat with {user_nick}\n")

                
                    
                                           
        
    conn.close()    
    
while 1: #loop accettazione connessioni
    conn, addr = s.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientthread,(conn,))

s.close()