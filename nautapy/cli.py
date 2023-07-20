import argparse
import os
import sys
import time
import sqlite3
from getpass import getpass

from requests import RequestException

from nautapy.exceptions import NautaException
from nautapy.nauta_api import NautaClient, NautaProtocol
from nautapy import utils
from nautapy.__about__ import __cli__ as prog_name, __version__ as version
from nautapy import appdata_path

from base64 import b85encode, b85decode


USERS_DB = os.path.join(appdata_path, "users.db")


def users_db_connect():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS default_user (user TEXT)")

    conn.commit()
    return cursor, conn


def _get_default_user():
    cursor, _ = users_db_connect()

    # Search for explicit default value
    cursor.execute("SELECT user FROM default_user LIMIT 1")
    rec = cursor.fetchone()
    if rec:
        return rec[0]

    # If no explicit value exists, find the first user
    cursor.execute("SELECT * FROM users LIMIT 1")

    rec = cursor.fetchone()
    if rec:
        return rec[0]


def _find_credentials(user, default_password=None):
    cursor, _ = users_db_connect()
    cursor.execute("SELECT * FROM users WHERE user LIKE ?", (user + '%',))

    rec = cursor.fetchone()
    if rec:
        return rec[0], b85decode(rec[1]).decode('utf-8')
    else:
        return user, default_password


def add_user(args):
    password = args.password or getpass("Contraseña para {}: ".format(args.user))

    cursor, connection = users_db_connect()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (args.user, b85encode(password.encode('utf-8'))))
    connection.commit()

    print("Usuario guardado: {}".format(args.user))


def set_default_user(args):
    cursor, connection = users_db_connect()
    cursor.execute("SELECT count(user) FROM default_user")
    res = cursor.fetchone()

    if res[0]:
        cursor.execute("UPDATE default_user SET user=?", (args.user,))
    else:
        cursor.execute("INSERT INTO default_user VALUES (?)", (args.user,))

    connection.commit()

    print("Usuario predeterminado: {}".format(args.user))


def remove_user(args):
    cursor, connection = users_db_connect()
    cursor.execute("DELETE FROM users WHERE user=?", (args.user,))
    connection.commit()

    print("Usuario eliminado: {}".format(args.user))


def set_password(args):
    password = args.password or getpass("Contraseña para {}: ".format(args.user))

    cursor, connection = users_db_connect()
    cursor.execute("UPDATE users SET password=? WHERE user=?", (b85encode(password.encode('utf-8')), args.user))

    connection.commit()

    print("Contraseña actualizada: {}".format(args.user))


def list_users(args):
    cursor, _ = users_db_connect()

    for rec in cursor.execute("SELECT user FROM users"):
        print(rec[0])


def _get_credentials(args):
    user = args.user or _get_default_user()
    password = args.password or None

    if not user:
        print(
            "No existe ningún usuario. Debe crear uno. "
            "Ejecute '{} --help' para más ayuda".format(
                prog_name
            ),
            file=sys.stderr
        )
        sys.exit(1)

    return _find_credentials(user=user, default_password=password)


def up(args):
    user, password = _get_credentials(args)
    client = NautaClient(user=user, password=password)

    print(
        "Conectando usuario: {}".format(
            client.user,
        )
    )

    if args.batch:
        client.login()
        print("[Sesión iniciada]")
        print("Tiempo restante: {}".format(utils.val_or_error(lambda: client.remaining_time)))
    else:
        with client.login():
            login_time = int(time.time())
            print("[Sesión iniciada]")
            print("Tiempo restante: {}".format(utils.val_or_error(lambda: client.remaining_time)))
            print(
                "Presione Ctrl+C para desconectarse, o ejecute '{} down' desde otro terminal".format(
                    prog_name
                )
            )

            try:
                while True:
                    if not client.is_logged_in:
                        break

                    elapsed = int(time.time()) - login_time

                    print(
                        "\rTiempo de conexión: {}".format(
                            utils.seconds2strtime(elapsed)
                        ),
                        end=""
                    )

                    if args.session_time:
                        if args.session_time < elapsed:
                            break

                        print(
                            " La sesión se cerrará en {}".format(
                                utils.seconds2strtime(args.session_time - elapsed)
                            ),
                            end=""
                        )

                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                print("\n\nCerrando sesión ...")
                print("Tiempo restante: {}".format(utils.val_or_error(lambda: client.remaining_time)))


            
        print("Sesión cerrada con éxito.")
        #print("Crédito: {}".format(
        #    utils.val_or_error(lambda: client.user_credit)
        #))


def down(args):
    client = NautaClient(user=None, password=None)

    if client.is_logged_in:
        client.load_last_session()
        client.user = client.session.__dict__.get("username")
        client.logout()
        print("Sesión cerrada con éxito")
    else:
        print("No hay ninguna sesión activa")


def is_logged_in(args):
    client = NautaClient(user=None, password=None)

    print("Sesión activa: {}".format(
        "Sí" if client.is_logged_in
        else "No"
    ))


def is_online(args):
    print("Online: {}".format(
        "Sí" if NautaProtocol.is_connected()
        else "No"
    ))


def info(args):
    user, password = _get_credentials(args)
    client = NautaClient(user, password)

    if client.is_logged_in:
        client.load_last_session()

    print("Usuario Nauta: {}".format(user))
    print("Tiempo restante: {}".format(
        utils.val_or_error(lambda: client.remaining_time)
    ))
    #print("Crédito: {}".format(
    #    utils.val_or_error(lambda: client.user_credit)
    #))


def run_connected(args):
    user, password = _get_credentials(args)
    client = NautaClient(user, password)

    if not NautaProtocol.is_connected():
        with client.login():
            os.system("".join(args.cmd))
    elif args.reuse_connection:
        os.system("".join(args.cmd))
        if not client.is_logged_in:
            print("No hay ninguna sesión activa")
            return
        client.load_last_session()
        client.user = client.session.__dict__.get("username")
        client.logout()
        print("Sesión cerrada con éxito")
    else:
        print("ya hay una conexión activa a internet, si aún así desea usar -run-connected agregue el flag --reuse-connection")


def create_user_subparsers(subparsers):
    users_parser = subparsers.add_parser("users")
    user_subparsers = users_parser.add_subparsers()

    # Add user
    user_add_parser = user_subparsers.add_parser("add")
    user_add_parser.set_defaults(func=add_user)
    user_add_parser.add_argument("user", help="Usuario Nauta")
    user_add_parser.add_argument("password", nargs="?", help="Password del usuario Nauta")

    # Set default user
    user_set_default_parser = user_subparsers.add_parser("set-default")
    user_set_default_parser.set_defaults(func=set_default_user)
    user_set_default_parser.add_argument("user", help="Usuario Nauta")

    # Set user password
    user_set_password_parser = user_subparsers.add_parser("set-password")
    user_set_password_parser.set_defaults(func=set_password)
    user_set_password_parser.add_argument("user", help="Usuario Nauta")
    user_set_password_parser.add_argument("password", nargs="?", help="Password del usuario Nauta")

    # Remove user
    user_remove_parser = user_subparsers.add_parser("remove")
    user_remove_parser.set_defaults(func=remove_user)
    user_remove_parser.add_argument("user", help="Usuario Nauta")

    user_list_parser = user_subparsers.add_parser("list")
    user_list_parser.set_defaults(func=list_users)


def main():
    parser = argparse.ArgumentParser(prog=prog_name)
    parser.add_argument("--version", action="version", version="{} v{}".format(prog_name, version))
    parser.add_argument("-d", "--debug", action="store_true", help="show debug info")

    subparsers = parser.add_subparsers()

    # Create user subparsers in another function
    create_user_subparsers(subparsers)

    # loggin parser
    up_parser = subparsers.add_parser("up")
    up_parser.set_defaults(func=up)
    up_parser.add_argument("-t", "--session-time", action="store", default=None, type=int, help="Tiempo de desconexión en segundos")
    up_parser.add_argument("-b", "--batch", action="store_true", default=False, help="Ejecutar en modo no interactivo")
    up_parser.add_argument("user", nargs="?", help="Usuario Nauta")
    up_parser.add_argument("password", nargs="?", help="Password del usuario Nauta")

    # Logout parser
    down_parser = subparsers.add_parser("down")
    down_parser.set_defaults(func=down)

    # Is logged in parser
    is_logged_in_parser = subparsers.add_parser("is-logged-in")
    is_logged_in_parser.set_defaults(func=is_logged_in)

    # Is online parser
    is_online_parser = subparsers.add_parser("is-online")
    is_online_parser.set_defaults(func=is_online)

    # User information parser
    info_parser = subparsers.add_parser("info")
    info_parser.set_defaults(func=info)
    info_parser.add_argument("user", nargs="?", help="Usuario Nauta")
    info_parser.add_argument("password", nargs="?", help="Password del usuario Nauta")

    # Run connected parser
    run_connected_parser = subparsers.add_parser("run-connected")
    run_connected_parser.set_defaults(func=run_connected)
    run_connected_parser.add_argument("-u", "--user", required=False, help="Usuario Nauta")
    run_connected_parser.add_argument("-p", "--password", required=False, help="Password del usuario Nauta")
    run_connected_parser.add_argument("-rc", "--reuse-connection", action="store_true", required=False, 
                                      help="ejecuta el comando incluso si hay una conexión activa, luego cierra "
                                      "la sesión si es posible")
    run_connected_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="The command line to run")

    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except NautaException as ex:
        print(ex.args[0], file=sys.stderr)
    except RequestException:
        print("Hubo un problema en la red, por favor revise su conexión", file=sys.stderr)

