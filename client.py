import socket

def authenticate_user():
    myAudioClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    myAudioClient.connect(("localhost", 5050))

    while True:
        print("Register (Press R)\nSign in (Press S)\nQuit (Press Q)")

        userInput = input("Waiting for Input: ")
        myAudioClient.send(userInput.encode())

        if userInput == "R":
            userLog = input("Username: ")
            userPass = input("Password: ")
            myAudioClient.send(userLog.encode())
            myAudioClient.send(userPass.encode())

            serverReply = myAudioClient.recv(1024).decode()
            print(serverReply)

        elif userInput == "S":
            userLog = input("Username: ")
            userPass = input("Password: ")
            myAudioClient.send(userLog.encode())
            myAudioClient.send(userPass.encode())

            serverReply = myAudioClient.recv(1024).decode()

            if serverReply == "You're signed in":
                break
            else:
                print("Error. Wrong Credentials Entered. Please Try Again")
                break

        elif userInput == "Q":
            myAudioClient.send("Q".encode())
            myAudioClient.close()
            break

        else:
            print("Please enter one of the valid input values ('R', 'S', 'Q')")

        if serverReply == "You're signed in":
            break

authenticate_user()