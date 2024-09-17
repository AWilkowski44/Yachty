import connection
import util




def user_register(username, password):

    hashed_pw = util.hash_password(password)

    @connection.connection_handler
    def add_user_to_base(cursor, username, hashed_pw):

        query = """
                INSERT INTO users (password, login_email)
                VALUES (%(password)s, %(login)s)
        """
        cursor.execute(query, {'password': hashed_pw, 'login': username})

    add_user_to_base(username=username, hashed_pw=hashed_pw)

    return True


def check_credentials(login, password):

    @connection.connection_handler
    def check_for_login(cursor, login):
        query = """
            SELECT login_email, password FROM users
            WHERE login_email = %(login)s        
        """
        cursor.execute(query, {'login': login})
        return cursor.fetchone()

    credentials = check_for_login(login=login)

    if credentials:
        pw_hash = credentials['password']
        return util.verify_password(password, pw_hash)
    else:
        return False


