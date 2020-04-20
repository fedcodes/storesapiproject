from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#The api works with resources, and every resource has to be a class

#Class to return the item name
class Item(Resource):
    #this defines that only some arguments may be changed.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='this field may not be left blank'
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id'
    )

    #This requires the user to authenticate before it can call the get method.
    @jwt_required()
    def get(self, name):
        #Extraction of filtering by name.
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with that name already exists.'.format(name)}, 400
        #This will get the JSON  payload from a request but only if it meets parse args arguments.
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        #call method for inserting items
        try:
            item.save_to_db()
        except:
            #In case the item insertion fails.
            return {'message': 'An error occurred inserting the item.'}, 500 #Internal Server Error
        #This returns the code for created item
        return item.json(), 201


#this deletes the item with that item name
    def delete(self, name):
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()

            return {'message': 'Item deleted'}

    def put(self, name):
        #this defines that the item has to pass the conditions set in the parse args.
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
