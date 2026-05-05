# Client-Server-Chat-Project
A simple client-server chat app written in Python. Developed during the Networking course for the First Level Professional Master in Cybersecurity (2024/25, Università di Pisa). 

The project's goal was to create a server that handles client registration requests using username, IP address, and selected port, and connects those users to a chat on demand.
There are some small issues to address, such as the inability to use the !help command while chatting with another user.

# Usage
First, you need to start the server via terminal. To use the client you need to open a new terminal, in this case more than one to add more users. Then you need to type "python chat_client.py <username> <IP $address> <port>". The username must be 3 letters long and uppercase. Since its a local application you'll need to type 127.0.0.1 as your IP, while for practical reason you'll nee to type a port number within the range of 2000-2010.

# Command List
!register - Send your data (nickname, IP & port) to the server

!quit - To quit

!who - Available users list

!connect client_name - Start a chat with a user")

!disconnect - Disconnect from the chat
