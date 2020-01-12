import argparse
import os
import sys
import time
import sqlite3

from nautacli.exceptions import NautaException
from nautacli.nauta_api import NautaClient, NautaProtocol
from nautacli import utils
from nautacli.__about__ import __name__ as prog_name, __version__ as version

from base64 import b85encode, b85decode


USERS_DB = "/tmp/users.db"


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
    cursor, connection = users_db_connect()
    cursor.execute("INSERT INTO users VALUES (?, ?)", (args.user, b85encode(args.password.encode('utf-8'))))
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
    cursor, connection = users_db_connect()
    cursor.execute("UPDATE users SET password=? WHERE user=?", (b85encode(args.password.encode('utf-8')), args.user))

    connection.commit()

    print("Contraseña actualizada: {}".format(args.user))


def list_users(args):
    cursor, _ = users_db_connect()

    for rec in cursor.execute("SELECT user FROM users"):
        print(rec[0])


def _get_credentials(args):
    user = args.__dict__.get("user", _get_default_user())
    password = args.__dict__.get("password", None)

    if not user:
        print(
            "No existe ningun usuario. Debe crear uno. "
            "Ejecute '{} --help' para mas ayuda".format(
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
        "Conectando usuario: {}. Tiempo restante: {}".format(
            client.user,
            utils.val_or_error(lambda: client.remaining_time)
        )
    )

    if args.batch:
        client.login()
    else:
        with client.login():
            login_time = int(time.time())
            print("[Sesion iniciada]")
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
                        "\rTiempo de conexion: {}.".format(
                            utils.seconds2strtime(elapsed)
                        ),
                        end=""
                    )

                    if args.session_time:
                        if args.session_time > elapsed:
                            break

                        print(
                            " La sesion se cerrara en {}.".format(
                                utils.seconds2strtime(args.session_time - elapsed)
                            ),
                            end=""
                        )


                    time.sleep(1)
            except KeyboardInterrupt:
                pass

            print("Cerrando sesion ...")
        print("Sesion cerrada con exito")


def down(args):
    user, password = _get_credentials(args)
    client = NautaClient(user, password)

    if client.is_logged_in:
        client.load_last_session()
        client.logout()
        print("Sesion cerrada con exito")
    else:
        print("No hay ninguna sesion activa")


def is_logged_in(args):
    client = NautaClient(user=None, password=None)

    print("Sesion activa: {}".format(
        "Si" if client.is_logged_in
        else "No"
    ))


def is_online(args):
    print("Online: {}".format(
        "Si" if NautaProtocol.is_connected()
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
    print("Credito: {}".format(
        utils.val_or_error(lambda: client.user_credit)
    ))


def run_connected(args):
    user, password = _get_credentials(args)
    client = NautaClient(user, password)

    with client.login():
        os.system(args.command)


def create_user_subparsers(subparsers):
    users_parser = subparsers.add_parser("users")
    user_subparsers = users_parser.add_subparsers()

    # Add user
    user_add_parser = user_subparsers.add_parser("add")
    user_add_parser.set_defaults(func=add_user)
    user_add_parser.add_argument("user", help="Usuario Nauta")
    user_add_parser.add_argument("password", help="Password del usuario Nauta")

    # Set default user
    user_set_default_parser = user_subparsers.add_parser("set-default")
    user_set_default_parser.set_defaults(func=set_default_user)
    user_set_default_parser.add_argument("user", help="Usuario Nauta")

    # Set user password
    user_set_password_parser = user_subparsers.add_parser("set-password")
    user_set_password_parser.set_defaults(func=set_password)
    user_set_password_parser.add_argument("user", help="Usuario Nauta")
    user_set_password_parser.add_argument("password", help="Password del usuario Nauta")

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
    up_parser.add_argument("-t", "--session-time", required=False, help="Tiempo de desconexion")
    up_parser.add_argument("-b", "--batch", required=False, help="Ejecutar en modo no interactivo")
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
    run_connected_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="The command line to run")

    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except NautaException as ex:
        print(ex.args[0], file=sys.stderr)

