from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, List, Schema, Float
from flask_cors import CORS
import requests
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load API key from environment variables
API_KEY = os.getenv("API_KEY")

# Define GraphQL types
class ChunkResult(ObjectType):
    chunkId = Int()
    contentId = Int()
    fileName = String()
    text = String()
    similarityScore = Float()

class Query(ObjectType):
    searchSimilarChunks = List(
        ChunkResult,
        userId=String(required=True),
        query=String(required=True),
        limit=Int(default_value=5)
    )

    def resolve_searchSimilarChunks(parent, info, userId, query, limit):
        print(f"Received request: userId={userId}, query={query}, limit={limit}")
        try:
            # Set up headers with API key
            headers = {'X-API-KEY': API_KEY}
            
            # Make GET request to the external API
            response = requests.get(
                "http://34.207.126.237/api/search",
                params={"user_id": userId, "query": query, "limit": limit},
                headers=headers
            )
            response.raise_for_status()
            
            # Parse and map the response data
            results = response.json().get("results", [])
            return [
                {
                    "chunkId": result["chunk_id"],
                    "contentId": result["content_id"],
                    "fileName": result["file_name"],
                    "text": result["text"],
                    "similarityScore": result["similarity_score"]
                }
                for result in results
            ]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []

# Create schema
schema = Schema(query=Query)

# Add GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

# Add a health check route
@app.route("/")
def index():
    return "GraphQL API is running!"

# Run the Flask app
if __name__ == "__main__":
    # Use environment variable for port or default to 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
