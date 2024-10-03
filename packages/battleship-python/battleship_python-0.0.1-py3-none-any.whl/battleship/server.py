#
# This file is part of the battleship-python project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import json
import logging
import selectors
import socket
import sys
import urllib.parse

from battleship.engine import BattleshipError, Engine, UnknownPlayer
from battleship.parser import (
    InternalError,
    InvalidParams,
    InvalidRequest,
    MethodNotFound,
    NotificationMessage,
    ParseError,
    ResultMessage,
    ServerError,
)


def create_server(address, family):
    logging.info(f"Ready to accept requests on {address}")
    sock = socket.create_server(address, family=family)
    sock.setblocking(False)
    return sock


def event_stream(select):
    while True:
        yield from select.select()


def fd_stream(select):
    for key, _ in event_stream(select):
        yield key.fileobj


def read_message(sockfd):
    if not (payload := sockfd.readline()):
        raise ConnectionError("Client disconnected")
    return payload


def write_message(sockfd, message):
    payload = json.dumps(message).encode()
    sockfd.write(payload + b"\n")


def notify(sockfd, method, params=None):
    message = NotificationMessage(method, params=params)
    write_message(sockfd, message)


def send_result(sockfd, id, result=None):
    if id is None:
        return
    message = ResultMessage(id, result)
    write_message(sockfd, message)


def send_error(sockfd, error, force=False):
    if error["id"] is None and not force:
        return
    write_message(sockfd, error)


class Server:
    def __init__(self, addresses):
        self.addresses = addresses
        self.socks = None
        self.select = None
        self.stream = None
        self.clients = {}
        self.engine = Engine()

    def prepare(self):
        if self.socks is None:
            self.socks = {create_server(address, family) for address, family in self.addresses}
            self.select = selectors.DefaultSelector()
            for sock in self.socks:
                self.select.register(sock, selectors.EVENT_READ)
        self.stream = fd_stream(self.select)

    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.select = None
        for sock, client in self.clients.items():
            client.close()
            sock.close()
        if self.socks is not None:
            for sock in self.socks:
                sock.close()
            self.socks = None

    def register_player(self, client, name):
        self.engine.register_player(client, name)
        logging.info("Registered player %r", name)

    def new_game(self, client):
        self.engine.new_game(client)
        player = self.engine.get_player(client)
        logging.info("New game from %r", player.name)

    def leave_game(self, client):
        player, game = self.engine.leave_game(client)
        logging.info("Player %s left the game", player.name)
        if game is None:
            return
        adversary = game.adversary(player)
        if adversary is None:
            return
        notify(adversary.id, "adversary_quit")

    def quit(self, client):
        try:
            self.engine.quit(client)
        except UnknownPlayer:
            # a client that disconnected without registering
            pass

    def join_game(self, client, game_id):
        player, game = self.engine.join_game(client, game_id)
        logging.info("Player %r joined game. Let the game begin!", player.name)
        notify(game.player1.id, "adversary_joined", [player.name])
        notify(game.player1.id, "your_turn")

    def list_games(self):
        game_ids = self.engine.list_games()
        logging.info("Found %d games", len(game_ids))
        return game_ids

    def fire(self, client, at, uid):
        _game, winner, player, adversary, ship = self.engine.fire(client, at)
        if ship is None:
            reply = "water"
        else:
            reply = "hit " + type(ship).__name__
        logging.info("%r fired at %r at %s: %s", player.name, adversary.name, at, reply)
        send_result(client, uid, reply)
        notify(adversary.id, "fired_upon", [at, reply])
        if winner is None:
            notify(adversary.id, "your_turn")
        else:
            notify(player.id, "you_win")
            notify(adversary.id, "you_loose")

    def handle_client(self, client):
        try:
            payload = read_message(client)
        except OSError:
            self.quit(client)
            raise

        try:
            message = json.loads(payload)
        except Exception as error:
            send_error(client, ParseError(f"Invalid JSON-RPC message: {error!r}"), force=True)
            return

        uid, reply = None, None
        try:
            uid = message.get("id")
            method = message["method"]
        except (TypeError, KeyError) as error:
            send_error(client, InvalidRequest(uid, repr(error)))
            return

        params = message.get("params", [])
        try:
            if method == "register":
                try:
                    name = params[0]
                except Exception as error:
                    send_error(client, InvalidParams(uid, str(error)))
                    return
                self.register_player(client, name)
            elif method == "new_game":
                self.new_game(client)
            elif method == "leave_game":
                reply = self.leave_game(client)
            elif method == "join_game":
                game_id = params[0] if params else None
                self.join_game(client, game_id)
            elif method == "list_games":
                reply = self.list_games()
            elif method == "fire":
                try:
                    x, y = params[0]
                    target = int(x), int(y)
                except Exception as error:
                    send_error(client, InvalidParams(uid, str(error)), force=True)
                    return
                # we returned the result to the client in fire because we
                # might need to notify of win after
                return self.fire(client, target, uid)
            else:
                send_error(client, MethodNotFound(uid, method))
                return
        except BattleshipError as error:
            send_error(client, ServerError(uid, -3200, str(error)))
            return
        except Exception as error:
            logging.exception("unexpected server error")
            send_error(client, InternalError(uid, repr(error)))
            return

        send_result(client, uid, reply)

    def handle_new_connection(self, sock, addr):
        sock.setblocking(False)
        client = sock.makefile("rwb", buffering=1)
        self.clients[sock] = client
        self.select.register(sock, selectors.EVENT_READ)
        n = len(self.select.get_map()) - 1
        logging.info(f"new client from {addr}. Now handling {n} clients")

    def handle_connection_error(self, sock):
        del self.clients[sock]
        self.select.unregister(sock)
        sock.close()

    def run_once(self):
        sock = next(self.stream)
        if sock in self.socks:
            sock, addr = sock.accept()
            self.handle_new_connection(sock, addr)
            return
        client = self.clients[sock]
        try:
            self.handle_client(client)
        except OSError as error:
            logging.info(f"client error: {error!r}")
            self.handle_connection_error(sock)
        return True

    def run(self):
        self.prepare()
        while self.run_once():
            pass

    def server_exit(self):
        for client in self.clients.values():
            try:
                notify(client, "server_exit")
            except OSError:
                logging.exception("failed to notify client of server exit")

    def __enter__(self):
        self.prepare()
        return self

    def __exit__(self, *args):
        self.server_exit()
        self.close()


def tcp_address(host, port):
    return (host, port), socket.AF_INET


def unix_address(address):
    return address, socket.AF_UNIX


def parse_address(url):
    if "://" not in url:
        url = f"tcp://{url}"
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme == "unix":
        return unix_address(parsed.path)
    return tcp_address(parsed.hostname, parsed.port)


def main(args=None):
    args = args or sys.argv[1:]
    logging.basicConfig(level="INFO", format="%(asctime)-15s: %(message)s")

    addresses = [parse_address(address) for address in args]

    try:
        with Server(addresses) as server:
            server.run()
    except (KeyboardInterrupt, EOFError):
        logging.info("Server finished")


if __name__ == "__main__":
    main()
