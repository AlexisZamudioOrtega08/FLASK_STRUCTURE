from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.itemModel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
  
    def get(self, name=None):
        item = ItemModel.find_by_name(name)
        if (item):
            return {'item': item.json()}, 200
        else:
            return {'message': 'Item not found'}, 404

    def post(self):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(data['name'])
        if (item):
            return {'message': 'An item with name <{}> already exists.'.format(data['name'])}, 400
        else:
            item = ItemModel(0, data['name'], data['price'])
            if item.save_to_db(): 
                return {'message': 'Item <{}> created successfully.'.format(data['name'])}, 201
            else: 
                return {'message': 'Item <{}> could not be created.'.format(data['name'])}, 500

    def put(self, name=None):
        data = Item.parser.copy()
        data = data.remove_argument('name').parse_args()
        item = ItemModel.find_by_name(name)
        if (item):
            if item.price == data['price']: return {'message': 'Not changes detected'}, 400
            item.price = data['price']
            if item.save_to_db(): 
                return {'message': 'Item updated'}, 200
            else: 
                return {'message': 'Item not updated'}, 500
        else:
            return {'message': 'Item not found'}, 404
            
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if (item):
            if item.delete_from_db(name):
                return {'message': 'Item deleted'}, 200
            else:
                return {'message': 'Item not deleted'}, 500
        else:
            return {'message': 'Item not found'}, 404

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200