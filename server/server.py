from funcs import *
from tinydb import TinyDB, Query
from flask import Flask
from flask_restful import Resource, Api, reqparse
import argparse
import json

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('--test_data', choices=['true', 'false'], required=True, help='Should the server load test data?')
parser.add_argument('--world_name', '-n', default='MyWorld', help='Override the world name with the value you specify.')
args = parser.parse_args()

msg('DB', 'Initializing database for world')
db = TinyDB('world.json', sort_keys=True, indent=2)

world = db.table('world')
players = db.table('players')
ship_classes = db.table('ship_classes')
cargo = db.table('cargo')
ports = db.table('ports')

if args.test_data == 'true':
    db.drop_tables()
    world.insert({"name": args.world_name})

app = Flask(__name__)
api = Api(app)

if args.test_data == 'true':
    msg('INIT', 'Loading test data')
    spacer()

    msg('INIT', 'Loading test players')
    players.insert({'name': 'Neo', 'home_port': 3, 'money': 100000, 'ships': {'id': 1, 'name': 'Neb', 'class': 1, 'capacity': 10, 'cargo': {}}})
    players.insert({'name': 'Wot', 'home_port': 1, 'money': 50000, 'ships': {'id': 1, 'name': 'Minnow', 'class': 2, 'capacity': 20, 'cargo': {}}})

    msg('INIT', 'Loading test ship classes')
    ship_classes.insert({'name': 'skiff', 'capacity': 10, 'cost': 1000})
    ship_classes.insert({'name': 'barge', 'capacity': 20, 'cost': 3000})

    msg('INIT', 'Loading test cargo')
    cargo.insert({'name': 'tea', 'max_price': 100, 'min_price': 50})
    cargo.insert({'name': 'coffee', 'max_price': 200, 'min_price': 75})

    msg('INIT', 'Loading test ports')
    ports.insert({'name': 'Philadelphia', 'port_type': 'public', 'cargo': {}, 'ships': {}})
    ports.insert({'name': 'Montego Bay', 'port_type': 'public', 'cargo': {}, 'ships': {}})
    ports.insert({'name': 'The Void', 'port_type': 'private', 'owner': 1, 'authorized_players': [1], 'max_cargo': 10000, 'cargo': {}, 'ships': {}})

    msg('INIT', 'Test data load complete')
    #spacer()
    #print(db.tables())
    #db.close()

    print(world.all())

class World(Resource):
    def get(self):
        return world.all(), 200

class ShipClass(Resource):
    def get(self):
        scrp = reqparse.RequestParser()
        scrp.add_argument('name')
        scargs = scrp.parse_args()

        if not scargs['name']:
            return ship_classes.all(), 200
        else:
            FindSC = Query()
            return ship_classes.get(FindSC.name == scargs['name']), 200

    def post(self):
        # TODO: Make post create only and make PUT update only
        scrp = reqparse.RequestParser()
        scrp.add_argument('name', required=True)
        scrp.add_argument('capacity', required=True, type=int)
        scrp.add_argument('cost', required=True, type=int)
        scargs = scrp.parse_args()

        newsc = {
            'name': scargs['name'],
            'capacity': scargs['capacity'],
            'cost': scargs['cost']
        }

        FindSC = Query()

        ship_classes.upsert(newsc, FindSC.name == scargs['name'])
        return newsc, 200

class Cargo(Resource):
    def get(self):
        cargorp = reqparse.RequestParser()
        cargorp.add_argument('name')
        cargs = cargorp.parse_args()

        if not cargs['name']:
            return cargo.all(), 200
        else:
            FindCargo = Query()
            return cargo.get(FindCargo.name == cargs['name']), 200

    def post(self):
        cargorp = reqparse.RequestParser()
        cargorp.add_argument('name', required=True)
        cargorp.add_argument('max_price', required=True, type=int)
        cargorp.add_argument('min_price', required=True, type=int)
        cargs = cargorp.parse_args()

        newcargo = {
            'name': cargs['name'],
            'max_price': cargs['max_price'],
            'min_price': cargs['min_price']
        }

        FindCargo = Query()
        if cargo.contains(FindCargo.name == cargs['name']):
            return {'message': f"'{cargs['name']}' already exists"}, 401
        else:
            cargo.insert(newcargo)
            return newcargo, 200

    def put(self):
        # TODO: Make args optional and only update values that change
        cargorp = reqparse.RequestParser()
        cargorp.add_argument('name', required=True)
        cargorp.add_argument('max_price', required=True, type=int)
        cargorp.add_argument('min_price', required=True, type=int)
        cargs = cargorp.parse_args()

        newcargo = {
            'name': cargs['name'],
            'max_price': cargs['max_price'],
            'min_price': cargs['min_price']
        }

        FindCargo = Query()
        if cargo.contains(FindCargo.name == cargs['name']):
            cargodoc = cargo.get(FindCargo.name == cargs['name'])
            cargo.update(newcargo, doc_ids=[cargodoc.doc_id])
            return newcargo, 200
        else:
            return {'message': f"'{cargs['name']}' does not exist"}, 401

class Player(Resource):
    def get(self):
        return players.all(), 200

class Port(Resource):
    def get(self):
        return ports.all(), 200

api.add_resource(World, '/world')
api.add_resource(ShipClass, '/shipclass')
api.add_resource(Cargo, '/cargo')
api.add_resource(Player, '/player')
api.add_resource(Port, '/port')

if __name__ == '__main__':
    app.run()
