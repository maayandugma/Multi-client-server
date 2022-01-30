import socket
import Protocol_constants # To use Protocol_constants functions or consts, use Protocol_constants.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5555

# HELPER SOCKET METHODS

def build_and_send_message(sock, cmd, data):
    """Builds a new message using Protocol_constants, wanted code and message.
	Prints debug info, then sends it to the given socket.
	Pand(ramaters: conn (socket object), code (str), data (str)
	Returns: Nothing"""
    msg = Protocol_constants.build_message(cmd,data)
    print(f"CLIENT:{msg}")
    sock.send(msg.encode())

def recv_message_and_parse(sock):
    """
    Recieves a new message from given socket,
	then parses the message using Protocol_constants.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occured, will return None, None
	"""
    print("flag")
    full_msg = sock.recv(1024).decode()
    cmd, data = Protocol_constants.parse_message(full_msg)
    return cmd, data

def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def login(sock):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = f"{username}#{password}"
        build_and_send_message(sock, Protocol_constants.PROTOCOL_CLIENT["login_msg"], data)#send message to server
        cmd, data = recv_message_and_parse(sock) # return message from the server
        if "OK" in cmd:
            print("logged-in")
            return


def logout(sock):
    print("good-bye")
    build_and_send_message(sock, Protocol_constants.PROTOCOL_CLIENT["logout_msg"], "")

def build_send_recv_parse(sock, cmd, data):
    build_and_send_message(sock, cmd, data)
    msg_code, data = recv_message_and_parse(sock)
    return msg_code, data

def get_score(sock):
    msg_code, data = build_send_recv_parse(sock, Protocol_constants.PROTOCOL_CLIENT["ask_for_score"], "")
    if msg_code != "YOUR_SCORE":
        print("ERROR")
    else:
        print(f"your score is  {data}")

def get_highscore(sock):

    msg_code, data = build_send_recv_parse(sock, Protocol_constants.PROTOCOL_CLIENT["get_all_score"], "")
    print(data)


def play_question(sock):

    msg_code, data = build_send_recv_parse(sock, Protocol_constants.PROTOCOL_CLIENT["ask_for_question"], "")
    if msg_code == "NO_QUESTIONS":
        logout(sock)
    separation = data.split(Protocol_constants.DATA_DELIMITER)
    print(f"{separation[0]}\n1-{separation[1]}\n2-{separation[2]}\n3-{separation[3]}\n4-{separation[4]}")
    flag = True
    while flag == True:
        answer = input("Please choose an answer[1-4]:")
        if answer in ["1", "2", "3", "4"]:
            flag = False
            response = build_send_recv_parse(sock, "SEND_ANSWER", answer)
            if "WRONG" in response[0]:
                print(response[0],response[1])
            else:
                print(response[0])



def get_logged_users(sock):
    msg_code, data = build_send_recv_parse(sock, Protocol_constants.PROTOCOL_CLIENT["connected client"], "")
    print(data)

def options_game():
    game_op = (
        "p\t Play a trivia question\n"
        "s\t Get my score\n"
        "h\t Get high score\n"
        "l\t Get logged users\n"
        "q\t Quit"
    )
    print(game_op)


def main():
    sock = connect()
    login(sock)
    while True:
        options_game()
        player_choice = input("Please enter your choice:")
        if player_choice == "p":
            play_question(sock)
        elif player_choice == "s":
            get_score(sock)
        elif player_choice == "h":
            get_highscore(sock)
        elif player_choice == "l":
            get_logged_users(sock)
        elif player_choice == 'q':
            logout(sock)
            break
        else:
            build_and_send_message(sock, "", "")
            break





try:
    main()
except KeyboardInterrupt:
    print("ctrl-c")


