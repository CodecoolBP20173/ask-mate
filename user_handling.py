import bcrypt
import connection


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def new_user_to_db(cursor, new_user_information):
    cursor.execute("""INSERT INTO users(
                                        user_name, 
                                        registration_date, 
                                        password) 
                      VALUES (%(user_name)s, 
                              %(registration_date)s, 
                              %(password)s);""", new_user_information)

    
@connection.connection_handler
def get_user_name_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT user_name FROM users
                    WHERE id=%('u_id')s;
                    """, {'u_id': user_id})
    return cursor.fetchone()