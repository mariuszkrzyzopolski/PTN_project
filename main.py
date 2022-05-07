import click

from database.database import DB, get_database
from rooms.rooms_service import create_room, delete_room, join_room, set_topic, vote_for_topic
from users.users_service import login, list_users, delete_user, register


@click.group()
@click.pass_context
def run(ctx):
    conn = get_database()
    ctx.obj = {
        "db": DB(conn)
    }


@run.command("clear_db", help="generate a new DB and clear old one")
@click.pass_obj
def clear_db(obj):
    obj["db"].initialize_db()


@run.group("user")
@click.option("--username", required=True)
@click.password_option()
@click.pass_obj
def user(obj, username, password):
    logged_user = login(obj["db"], username, password)
    obj["user"] = logged_user


@run.command("register")
@click.option("--username", required=True)
@click.password_option()
@click.pass_obj
def register_user(obj, username, password):
    register(obj["db"], username, password)


@user.command("list")
@click.option("--mode", required=True)
@click.pass_obj
def list_exist(obj, mode):
    list_users(obj["db"], mode)


@user.command("remove")
@click.pass_obj
def remove_user(obj):
    delete_user(obj["db"], obj["user"].username)


@user.group("room")
@click.option("--room_id")
@click.password_option()
@click.pass_obj
def room(obj, room_id, password):
    obj["room_id"] = room_id
    obj["room_password"] = password


@room.command("create")
@click.pass_obj
def create_new_room(obj):
    create_room(obj["db"], obj["room_password"], obj["user"].username)


@room.command("delete")
@click.pass_obj
def delete_exist_room(obj):
    delete_room(obj["db"], obj["room_id"], obj["user"].username)


@room.command("join")
@click.pass_obj
def join_exist_room(obj):
    join_room(obj["db"], obj["room_id"], obj["room_password"], obj["user"].username)


@room.command("set_topic")
@click.option("--topic_text", required=True)
@click.pass_obj
def set_room_topic(obj, topic_text):
    set_topic(obj["db"], obj["room_id"], obj["room_password"], topic_text)


@room.command("vote")
@click.option("--value", required=True)
@click.pass_obj
def vote_room(obj, value):
    vote_for_topic(obj["db"], obj["room_id"], obj["room_password"], value, obj["user"].username)


if __name__ == '__main__':
    run()
