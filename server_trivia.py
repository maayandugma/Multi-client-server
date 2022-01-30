import socket
import Protocol_constants
import select
import random
import Json_data

users = {}
questions = {} #Contain the socket of the client and the answer of the question and the index
logged_users = {} # a dictionary of client hostnames to usernames
client_sockets = []  # Contain connected client's socket


ERROR_MSG = "Error! "
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"


def build_and_send_message(sock, cmd, data):
	"""Builds a new message using Protocol_constants, wanted code and message.
	    	Prints debug info, then sends it to the given socket.
	    	Paramaters: conn (socket object), code (str), data (str)
	    	Returns: Nothing """

	msg = Protocol_constants.build_message(cmd, data)
	sock.send(msg.encode())
	print("[SERVER] ", msg)  # Debug print


def recv_message_and_parse(sock):
	"""Recieves a new message from given socket,
		then parses the message using Protocol_constants.
		Paramaters: conn (socket object)
		Returns: cmd (str) and data (str) of the received message.
		If error occured, will return None, None"""

	full_msg = sock.recv(1024).decode()

	cmd, data = Protocol_constants.parse_message(full_msg)
	print("[CLIENT] ", full_msg)  # Debug print
	return cmd, data


def load_questions(sock):
	"""
	Loads questions bank from Json data file. This file get the questions from Trivia website.
	Recieves: -
	Returns: The question that will be asked
	"""
	global questions
	index = random.randrange(10) #I get a random number that will be the index of the question and answer
	question = Json_data.question_list[index]
	questions[sock.getpeername()] = [Json_data.correct_answer[index], index]

	return question

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	server_socket = socket.socket()
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()

	return server_socket


		
def send_error(sock, data):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["login_failed_msg"], data)


def print_client_sockets(client_sockets):
	for client in client_sockets:
		print(client.getpeername())

##### MESSAGE HANDLING

def handle_getscore_message(sock, username):
	"""
	Gets from the player message code,MY_SCORE,and send back to the player he's score
	Recieves: sock, username
	Return: None
	"""
	global users
	dict_username = users[username]
	score = dict_username["score"]
	build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["client score"], str(score))


	
def handle_logout_message(sock):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	global client_sockets
	global users
	username = logged_users[sock.getpeername()]
	del logged_users[sock.getpeername()]
	del users[username]
	client_sockets.remove(sock)
	sock.close()



def handle_login_message(sock, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	data_list = data.split(Protocol_constants.DATA_DELIMITER)
	user_name = data_list[0]
	password = data_list[1]
	if user_name in load_user_database().keys():
		value = load_user_database()[user_name]
		print(f"value:{value}")
		if password == value["password"]:
			logged_users[sock.getpeername()] = user_name
			users[user_name] = value
			build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["login_ok_msg"], "")
		else:
			send_error(sock, "the password wrong")
	else:
		send_error(sock, "the user doesn't exist")

def handle_highscore_message(sock):
	"""
	Get socket. send the point of all the player that connect to the player that ask for.
	the point will be sort from the high to the low
	:return: None
	"""

	global users
	msg = ""
	user_keys = []
	user_score = []
	user_value = users.values()
	for key in users:
		user_keys.append(key)
	for value in user_value:
		user_score.append(value["score"])
	sort_score = sorted(user_score, reverse=True)
	for score in sort_score:
		index = user_score.index(score)
		msg += f"{user_keys[index]}:{user_score[index]}\n"
	build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["high_score_msg"], msg)



def handle_logged_message(sock):
	global users
	users_key = ""
	for key in users:
		users_key += f"{key} "
	build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["connected client"], users_key )

def handle_question_message(sock):
	"""
	Get message code ,"GET_QUESTION", and sand to the client a random question.
	Recieves: socket
	Return : None
	"""
	question = load_questions(sock)
	index = questions[sock.getpeername()][1]
	answer = Json_data.protocol_answer[index]
	msg = f"{question}#{answer}"
	build_and_send_message(sock, Protocol_constants.PROTOCOL_SERVER["the_question_msg"], msg)

def handle_answer_message(sock, data, username):
	"""
	Get socket,message -the answer ,and the username.
	check if the answer correct ,send a message to the player if he answer wrong or right.

	"""
	global users
	global questions


	answer_option = Json_data.ls_answer[questions[sock.getpeername()][1]]
	if answer_option[int(data)-1] == questions[sock.getpeername()][0]:# Check if the player answer right

		build_and_send_message(sock, "CORRECT_ANSWER", "")
		username_dict = users[username]
		username_dict["score"] += 5  # Updating player points
	else:
		build_and_send_message(sock, "WRONG_ANSWER", f"The answer is {questions[sock.getpeername()][0]}")  # Send to the player that he was wrong


def handle_client_message(sock, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users

	if sock.getpeername() not in logged_users:
		if cmd == Protocol_constants.PROTOCOL_CLIENT["login_msg"]:
			handle_login_message(sock, data)
		else:
			send_error(sock, "wrong command: you need first to connect")
	else:
		if cmd in Protocol_constants.PROTOCOL_CLIENT.values():
			if cmd == Protocol_constants.PROTOCOL_CLIENT["ask_for_score"]:
				handle_getscore_message(sock, logged_users[sock.getpeername()])
			elif cmd == Protocol_constants.PROTOCOL_CLIENT["get_all_score"]:
				handle_highscore_message(sock)
			elif cmd == Protocol_constants.PROTOCOL_CLIENT["connected client"]:
				handle_logged_message(sock)
			elif cmd == Protocol_constants.PROTOCOL_CLIENT["logout_msg"]:
				handle_logout_message(sock)
			elif cmd == Protocol_constants.PROTOCOL_CLIENT["ask_for_question"]:
				handle_question_message(sock)
			elif cmd == Protocol_constants.PROTOCOL_CLIENT["answer_msg"]:
				handle_answer_message(sock, data, logged_users[sock.getpeername()])


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	global client_sockets
	global messages_to_send
	
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()


	while True:

		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], []) #The server scaning for new clients
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("New client join",{client_address})
				client_sockets.append(client_socket) # Add nee client to the list

			else:
				try:
					cmd, data = recv_message_and_parse(current_socket)
					print(f"cmd={cmd} data={data}")

				except:

					print("connection closed")
					handle_logout_message(current_socket)

				else:
					if cmd == "":
						handle_logout_message(current_socket)
					else:
						handle_client_message(current_socket, cmd, data)




main()


	