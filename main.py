from flask import Flask
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
api = Api(app)

# connect to database
# x's not in real app, just place holders here.
database = mysql.connector.connect(
    host="xxxx (host address)",
    user="xxxx (Username)", 
    passwd="xxxx (password)",
    database="xxxx (database name)")

# Add dictionary true to get the table headers.
# Else it just prints out each row as a list without the mapped (header -> body).
# eg: WANT {Title: "Harry Potter", Id: 27} NOT [Harry Potter, 27]
databaseCursor = database.cursor(dictionary=True)   

#TEST SQL QUERY CALL
class MoviesByCategoryWithLimitMaxOrderedByAudienceScore(Resource):
    #return all the movie titles from a category in the database
    def get(self, category, limitMax):
        query = "SELECT * FROM Movies WHERE Primary_Category = \'" + category  + "\' ORDER BY Audience_Score DESC LIMIT " + str(limitMax)
        return ExecuteQuery(query)

#PRODUCTION
class MoviesByCategory(Resource):
    #return all the movie titles from a category in the database
    def get(self, category):
        query = "SELECT * FROM Movies WHERE Primary_Category = \'" + category  + "\' "
        return ExecuteQuery(query)

#PRODUCTION
class MovieReviews(Resource):
    #return all the movie Reviews for a titles id
    def get(self, movieId):
        query = "SELECT * FROM MovieReviews WHERE Movie_Id = " + str(movieId)
        return ExecuteQuery(query)


# Execute query and return the result with a 200 success code.
def ExecuteQuery(query):
    databaseCursor.execute(query)
    result = databaseCursor.fetchall()

    return result, 200  # return data and 200 OK



#End Points
api.add_resource(MovieReviews, '/<int:movieId>/moviereviews')  # this is our url entry point
api.add_resource(MoviesByCategory, '/<string:category>/movies')  # this is our url entry point

if __name__ == '__main__':
    app.run()  # run our Flask app
