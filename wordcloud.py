import falcon, json, pymongo


MONGO_DB_USER_FILE = '/home/frank/word_cloud-backend/config/mongodb-user'
mongo_db_user_config = open(MONGO_DB_USER_FILE, 'r').read()


user_name = mongo_db_user_config.split(':')[0]
password = mongo_db_user_config.split(':')[1]


mongo_db_client = pymongo.MongoClient('wordcloud-mongo.home.franks-reich.net', 27017)
mongo_db_client.admin.authenticate(user_name, password)
wordcloud_database = mongo_db_client.wordcloud


class WordCloudResource:
    def on_get(self, request, response, name):
        """Handles GET requests"""
        wordcloud = {
            'name': name,
            'wordcloud' : {
                'blub' : 40,
                'blah' : 34,
                'derp' : 57
            }
        }
        response.body = json.dumps(wordcloud)


app = falcon.API()
app.add_route('/wordcloud/{name}', WordCloudResource())
