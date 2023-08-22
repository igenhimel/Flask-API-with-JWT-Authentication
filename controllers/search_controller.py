from flask_restx import Namespace, Resource, reqparse
from models.db import elasticsearch_connection
from models.searchmodel_es import PropertySearch
from custom_jwt_required import custom_jwt_required

search_api = Namespace('search', description='search & sort operations')

es = elasticsearch_connection()

search_parser = reqparse.RequestParser()
search_parser.add_argument('title', type=str, required=False, help='Title')
search_parser.add_argument('amenities', type=str, required=False, help='Amenities')
search_parser.add_argument('price', type=float, required=False, help='Price')
search_parser.add_argument('location', type=str, required=False, help='Location')

sorting_parser = reqparse.RequestParser()
sorting_parser.add_argument('sort_order', type=str, required=False, choices=('asc', 'desc'), help='Sorting order: ascending(asc) or descending(desc) - By Price')

@search_api.route('/property')
class SearchProperty(Resource):
    @custom_jwt_required
    @search_api.expect(search_parser, sorting_parser)
    @search_api.response(200, 'Success')
    @search_api.response(400, 'Bad Request')
    @search_api.response(401, 'Unauthorized')
    @search_api.response(404, 'Not Found')
    @search_api.response(500, 'Internal server error')
    def get(self):
        """
        Property Search and Sort API 
        """
        search_args = search_parser.parse_args()
        title = search_args.get('title')
        amenities = search_args.get('amenities')
        price = search_args.get('price')
        location = search_args.get('location')

        args = sorting_parser.parse_args()
        sort_order = args.get('sort_order')
        if sort_order is None:
           sort_order = 'asc'  # Default to ascending order if not specified

        # Build the search query based on the provided parameters
        search_body = {
        "query": {
          "bool": {
            "must": [
                {"match": {"title": title}} for title in [title] if title
            ] + [
                {"match": {"amenities": amenities}} for amenities in [amenities] if amenities
            ] + [
                {"range": {"price": {"lte": price}}} for price in [price] if price
            ] + [
                {"match": {"location": location}} for location in [location] if location
            ]
                }
             }
            }

        response = es.search(index='property', size=10000, body=search_body, sort=[{"price": {"order": sort_order}}])
        hits = response['hits']['hits']

        if hits:
            # Search results found
            properties = [PropertySearch(**hit['_source']) for hit in hits]
            return {"message": "Search results found: Order - " + sort_order, "results": [property.to_dict() for property in properties]}, 200
        else:
            # No results found
            return {"message": "No search results found"}, 404
