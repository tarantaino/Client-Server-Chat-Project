import socket
import sys
import threading

current_chat = None  #flag per la chat, se attiva o meno
udp_active = True #flag per verificare se udp è ancora in ascolto

#loop ricezione udp
def receive_udp(udp_s):
    global current_chat, udp_active
    while True:
        try:
            msg, addr = udp_s.recvfrom(1024)
            msg_decoded = msg.decode()

            # Se arriva "Disconnecting" con !disonnect - flag = none, stacca utente dalla chat
            if msg_decoded.strip() == "Disconnecting":
                print(f"\nUser {addr[0]}:{addr[1]} disconnected from the chat. Type !help for command list.")
                current_chat = None
            else:
                print(f"\n{msg_decoded}")
                current_chat = addr  #memorizza utente per lo scambio dei messaggi
        except OSError: #se dà errore e udp è ancora in ascolto
            if udp_active:
                    print("ERR in UDP Receive")
            break #altrimenti si ferma




#controlli sugli input - numero di input passati e formato
if len(sys.argv) != 4:
    print("ERR, correct format: python client.py <nickname> <your_ip> <your_port>")
    sys.exit()
elif len(sys.argv[1]) != 3:
    print("ERR: nickname must be 3 characters long")
    sys.exit()
elif str(sys.argv[1]) == str(sys.argv[1]).lower():
    print("ERR: nickname must have uppercase characters ")
    sys.exit()
elif str(sys.argv[2]) != "127.0.0.1":
    print("ERR: your IP must be 127.0.0.1")
    sys.exit()
elif int(sys.argv[3]) not in range(2000, 2010):    #messo range di porte per utilità
    print("ERR: port must be in range 2000-2010")
    sys.exit()
  
#creazione socket tcp + connessione server su 8888  
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Failed to create socket. Error code: " + str(msg[0]) + ", Error message: " + msg[1])
    sys.exit()
    
print("Socket created")

port = 8888
ip = "127.0.0.1"

s.connect((ip, port))
print("Socket Connected")
print(f"Host IP & Port: {ip}:{port}\n")   
    
NICK = str(sys.argv[1])
IP = str(sys.argv[2])
PORT = int(sys.argv[3])
data = f"{NICK} {IP} {PORT}"
print("Welcome to the server. Type !register for register your data to the server. Type !help for command list.\n")

#apertura socket udp
udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_s.bind(("", PORT))
threading.Thread(target=receive_udp, args=(udp_s,), daemon=True).start()

#loop per i comandi
while True:
    try:
        commands = input("> ")
        
        if current_chat: #se la chat è attiva, esegui eventuali condizioni - !disconnect
            if commands == "!disconnect":
                udp_s.sendto(b"Disconnecting", current_chat)
                print("Disconnecting from chat.")
                current_chat = None
            else:
                udp_s.sendto(f"{NICK} says: {commands}".encode(), current_chat)
                print(f"{NICK} says: {commands}") #altrimenti continua l'invio dei messaggi
            continue   
           
        if commands == "!help":
            print("Available commands:\n")
            print("!register - Send your data (nickname, IP & port) to the server!")
            print("!quit - To quit")
            print("!who - Available users list")
            print("!connect client_name - Start a chat with a user")
            print("!disconnect - Disconnect from the chat")

        elif commands == "!register":
            s.sendall(data.encode())
            print("Data sent to the server!\n")
            reply = s.recv(4096)
            print(reply.decode())

        elif commands == "!quit":
            udp_active = False
            s.sendall(b"!quit")
            s.close()
            udp_s.close()
            print("All connections are closed. 'Till next time!")
            sys.exit()

        elif commands == "!who":
            s.sendall(b"!who")
            print("Here all available users:")
            users_list = s.recv(4096)
            print(users_list.decode().strip())

        elif commands.startswith("!connect "):
            user_nick = commands.split(" ", 1)[1]
            connect_msg = f"!connect {user_nick}"
            s.sendall(connect_msg.encode())
            r = s.recv(1024).decode()
            if r.startswith("User not found") or r.startswith("ERR"):
                print(r)
            else:
                user_nick, user_ip, user_port = r.split(" ")
                user_port = int(user_port)
                print(f"Connecting to {user_nick} at {user_ip}:{user_port} ...\n")
                udp_s.sendto(f"Chat request from {NICK}".encode(), (user_ip, user_port))
                current_chat = (user_ip, user_port)

        else:
            print("Unknown command. Please type !help for the command list!")

        
    
    except Exception as e:
        print(f"An error occured - {e}.")
        sys.exit()