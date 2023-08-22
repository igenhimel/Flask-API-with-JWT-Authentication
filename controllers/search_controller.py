from flask_restx import Namespace, Resource, reqparse
from models.db import elasticsearch_connection
from models.searchmodel_es import PropertySearch
from custom_jwt_required import custom_jwt_required

search_api = Namespace('search', description='User operations', path='/api')
es = elasticsearch_connection()

search_parser = reqparse.RequestParser()
search_parser.add_argument('title', type=str,help='Title')
search_parser.add_argument('amenities', type=str,help='Amenities')
search_parser.add_argument('price', type=str, help='Price')
search_parser.add_argument('location', type=str, help='Location')

sorting_parser = reqparse.RequestParser()
sorting_parser.add_argument('sort_order', type=str, required=False, choices=('asc', 'desc'), help='Sorting order: ascending(asc) or descending(desc) - By Price')

@search_api.route('/search')
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
        title = search_args.get('title').strip().lower() if search_args.get('title') else None
        amenities = search_args.get('amenities').strip().lower() if search_args.get('amenities') else None
        price = search_args.get('price')
        location = search_args.get('location').strip().lower() if search_args.get('location') else None


        args = sorting_parser.parse_args()
        sort_order = args.get('sort_order')
        if sort_order is None:
           sort_order = 'asc'  # Default to ascending order if not specified

        if (title and len(title.strip()) < 3) or (amenities and len(amenities.strip()) < 3) or (location and len(location.strip()) < 3) :
             return {"message": "Please provide at least three letters for the specified fields"}, 400
        if location is None:
             return {"message": "Location cannot be Empty"}, 400
        
        if price is not None:
         try:
          price = float(price)
          if price < 0:
            return {"message": "Price must be a non-negative numeric value"}, 400
         except ValueError:
            return {"message": "Price must be a valid numeric value"}, 400
        

        # Build the search query based on the provided parameters
        search_body = {
            "query": {
                "bool": {
                    "must": [],
                }
            }
        }

        if title:
            search_body["query"]["bool"]["must"].append({"wildcard": {"title": { "value": "*"+title+"*"}}})
        if amenities:
            search_body["query"]["bool"]["must"].append({"wildcard": {"amenities": {"value": "*"+amenities+"*"}}})
        if price:
            search_body["query"]["bool"]["must"].append({"range": {"price": {"lte": price}}})
        if location:
            search_body["query"]["bool"]["must"].append({"wildcard": {"location": {"value": "*"+location+"*"}}})

        response = es.search(index='property', size=10000, body=search_body, sort=[{"price": {"order": sort_order}}])
        hits = response['hits']['hits']

        if hits:
            # Search results found
            properties = [PropertySearch(**hit['_source']) for hit in hits]
            return {"message": "Search results found:  Order - " + sort_order, "results": [property.to_dict() for property in properties]}, 200
        else:
            # No results found
            return {"message": "No search results found"}, 404
