import xlrd
from recommender.models import User, Movie, Rating
import recommender.context as context


class DataReader(object):

    def __init__(self, data_file= './data/LDOS/LDOS-CoMoDa.xls'):
        self.data_file = data_file
        self.wb = xlrd.open_workbook(filename=self.data_file)

    def save_data(self):
        self.save_ratings_data()
        self.save_movies()

    def save_ratings_data(self):
        rating_columns = {'user_id': 0, 'movie_id': 1, 'rating': 2, 'time': 7, 'daytype': 8, 'season': 9, 'location': 10,
                          'weather': 11, 'social': 12, 'end_emotion': 13, 'dominant_emotion': 14, 'mood': 15, 'physical':16,
                          'decision': 17, 'interaction': 8}
        # user_columns = {'id': 0, 'age': 3, 'gender': 4, 'city': 5, 'country': 6, }
        # movie_columns = {'id': 1, 'director': 19, 'country': 20, 'language': 21, 'year': 22, 'genre':23, 'budget': 27}

        ws = self.wb.sheet_by_name('Sheet1')
        users = []
        movies = []
        ratings = []
        for row in range(1, ws.nrows):
            # users.append(self.__read_columns(ws, row, user_columns))
            # movies.append(self.__read_columns(ws, row, movie_columns))
            ratings.append(self.__read_columns(ws, row, rating_columns))
        # User.objects.bulk_create([User(**data) for data in users])
        #
        Rating.objects.bulk_create([Rating(**data) for data in ratings])

    def get_movies_titles(self):
        ws = self.wb.sheet_by_name('Sheet2')
        movies_titles = {}
        for row in range(0, ws.nrows):
            movies_titles[ws.cell_value(row, 0)] = ws.cell_value(row, 1)
        return movies_titles

    def save_movies(self):
        movies_titles = self.get_movies_titles()
        fields_names = {1: 'director',
                        2:  'country',
                        3:	'language',
                        4:	'year',
                        5:	'genre',
                        11: 'budget'
                        }

        ws = self.wb.sheet_by_name('Sheet3')
        movies_data = {}
        for movie_id in movies_titles:
            movies_data.setdefault(movie_id, {'id': movie_id})['title'] = movies_titles[movie_id]
        for row in range(0, ws.nrows):
            item_id = ws.cell_value(row, 0)
            field_id = ws.cell_value(row, 1)
            if field_id in fields_names:
                field_name = fields_names[field_id]
                if item_id in movies_data:
                    movies_data[item_id][field_name] = ws.cell_value(row, 2)
        # print movies_data

        Movie.objects.bulk_create([Movie(**movies_data[data]) for data in movies_data])
        print Movie.objects.all()

    def get_movies_genres(self, all_ratings):
        movies_genres = {}
        for r in all_ratings:
            if r not in movies_genres and r.genre > 0:
                movies_genres[r.movie_id] = context.Genre.names[r.genre]
        return movies_genres

    def __read_columns(self, worksheet, row, columns_names):
        fields = {col_name: worksheet.cell_value(row, columns_names[col_name]) for col_name in columns_names}

        return fields


