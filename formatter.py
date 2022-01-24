from datetime import datetime, tzinfo, timezone, timedelta
import random
import array

# Time now


def time_now():
    year = int(datetime.strftime(datetime.now(), "%Y"))
    month = int(datetime.strftime(datetime.now(), "%-m"))
    date = int(datetime.strftime(datetime.now(), "%-d"))
    hour = int(datetime.strftime(datetime.now(), "%-H"))
    minute = int(datetime.strftime(datetime.now(), "%-M"))

    time_n = datetime(year, month, date, hour, minute,
                      tzinfo=timezone(timedelta(hours=+0)))
    print(time_n)
    return time_n


# Format text message with new font
def format_me(my_txt):
    border_top = '**************'
    my_msg1 = 'HARIF_BOT'
    border_bottom = '**********'
    my_msg2 = str(my_txt)
    msg = "<code>" + str(border_top) + "</code>" + "\n<code>" + str(my_msg1) + "</code>" + \
        "\n<code>" + str(border_bottom) + "</code>" + \
        "\n<code>" + str(my_msg2) + "</code>"
    msg = "<code>" + str(my_msg1) + "</code>" + "\n<code>" + \
        str(border_bottom) + "</code>" + "\n<code>" + str(my_msg2) + "</code>"
    return msg


# Convert Unix timestamp to Datetime
def unix_to_date(unix_ts):
    time_stamp = datetime.utcfromtimestamp(
        unix_ts).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


def time_stamp_now(current_time):
    time_stamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    return time_stamp

# Set Login Expiry


def set_login_expiry(login_ts):
    login_expiry = datetime.strptime(
        login_ts, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=30)
    login_expiry = datetime.strftime(login_expiry, "%Y-%m-%d %H:%M:%S")
    return login_expiry


# Set Session Expiry
def set_session_expiry(session_ts):
    session_expiry = datetime.strptime(
        session_ts, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=30)
    session_expiry = datetime.strftime(session_expiry, "%Y-%m-%d %H:%M:%S")
    return session_expiry


# Generate password

def generate_pass_hs():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']

    SYMBOLS = ['@', '#', '$', '%']

    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
        password = password + x

    # print out password
    print(password)
    return password
