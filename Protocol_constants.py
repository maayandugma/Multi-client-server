# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"ask_for_score" : "MY_SCORE",
"ask_for_question" : "GET_QUESTION",
"get_all_score" : "HIGHSCORE",
"connected client" : "LOGGED",
"answer_msg" : "SEND_ANSWER"

}

PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"client score" : "YOUR_SCORE",
"high_score_msg" : "ALL_SCORE",
"connected client" : "LOGGED_ANSWER",
"the_question_msg" : "YOUR_QUESTION"


}


ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data=None):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occurred
	"""
	full_msg = ""
	first_str = cmd + " " * (CMD_FIELD_LENGTH - len(cmd))
	if data != None and len(cmd) <= CMD_FIELD_LENGTH and len(data) <= MAX_DATA_LENGTH:
		second_str = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
		full_msg = f"{first_str}{DELIMITER}{second_str}{DELIMITER}{data}"
	elif data == None and len(cmd) <= CMD_FIELD_LENGTH:
		second_str = "0000"
		full_msg = f"{first_str}{DELIMITER}{second_str}{DELIMITER}"
	elif len(cmd) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
		return ERROR_RETURN
	return full_msg



def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occurred, returns None, None
	"""
	data_list = data.split(DELIMITER)
	if data.count(DELIMITER) != 2:
		return ERROR_RETURN
	elif int(data_list[1]) != len(data_list[2]) or len(data_list[0]) != CMD_FIELD_LENGTH:
		return ERROR_RETURN
	elif len(data_list[1]) != LENGTH_FIELD_LENGTH:
		return ERROR_RETURN
	else:
		cmd = data_list[0]
		msg = data_list[-1]
		cmd = cmd.replace(" ","")
		return cmd, msg
	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	if msg.count(DATA_DELIMITER) == expected_fields:
		return msg.split(DATA_DELIMITER)
	else:
		return ERROR_RETURN


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	new_list = [str(i) for i in msg_fields]

	return DATA_DELIMITER.join(new_list)

