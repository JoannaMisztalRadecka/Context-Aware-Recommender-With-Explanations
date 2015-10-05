from unittest import TestCase
import os
from django.utils.datastructures import SortedDict
from django.conf import settings
import xlrd
from scipy.stats import pearsonr, ttest_ind
from django.db.models import Count
import numpy as np
from random import choice

from recommender.models import User, Movie, Rating
import recommender.context as context


import django
django.setup()


class TestUserScenario(TestCase):

    def save_data(self):

        rating_columns = {'user_id': 0, 'movie_id': 1, 'rating': 2, 'time': 7, 'daytype': 8, 'season': 9, 'location': 10,
                          'weather': 11, 'social': 12, 'end_emotion': 13, 'dominant_emotion': 14, 'mood': 15, 'physical':16,
                          'decision': 17, 'interaction': 8, 'genre': 23}
        user_columns = {'id': 0, 'age': 3, 'gender': 4, 'city': 5, 'country': 6, }
        movie_columns = {'id': 1, 'director': 19, 'country': 20, 'language': 21, 'year': 22, 'genre':23, 'budget': 27}

        wb = xlrd.open_workbook(filename= './data/LDOS/LDOS-CoMoDa.xls')
        ws = wb.sheet_by_name('Sheet1')
        users = []
        movies = []
        ratings = []
        for row in range(1, ws.nrows):
            users.append(self.read_columns(ws, row, user_columns))
            movies.append(self.read_columns(ws, row, movie_columns))
            ratings.append(self.read_columns(ws, row, rating_columns))

        # User.objects.bulk_create([User(**data) for data in users])
        # Movie.objects.bulk_create([Movie(**data) for data in movies])
        Rating.objects.bulk_create([Rating(**data) for data in ratings])

        print User.objects.all()
        print Movie.objects.all()
        print Rating.objects.all()
        self.assertEqual(1,2)

    def get_movies_titles(self):
        wb = xlrd.open_workbook(filename='./data/LDOS/LDOS-CoMoDa.xls')
        ws = wb.sheet_by_name('Sheet2')
        movies_titles = {}
        for row in range(1, ws.nrows):
            movies_titles[ws.cell_value(row, 0)] = ws.cell_value(row, 1)
        return movies_titles

    def get_movies_genres(self):
        movies_genres = {}
        for r in self.all_ratings:
            if r not in movies_genres and r.genre > 0:
                movies_genres[r.movie_id] = context.Genre.names[r.genre]

        return movies_genres

    def read_columns(self, worksheet, row, columns_names):
        return {col_name: worksheet.cell_value(row, columns_names[col_name]) for col_name in columns_names}

    def compare_emotions_for_context(self, context_feature):
        print context_feature
        for name in context_feature.names:
            ratings = self.filter_by_context(context_feature.context, name)
            print '\n{}: {}'.format(context_feature.names[name], ratings.count())
            max_diff = 0
            max_emotion = None

            for emotion in context.Emotion.names:
                ### test correlation with emotional states
                wr_emotion = ratings.filter(dominant_emotion=emotion)
                not_emotion = ratings.exclude(dominant_emotion=emotion)
                try:
                    avg_emotion = wr_emotion.count()
                    avg_not_emotion = not_emotion.count()
                    diff = float(avg_emotion)/avg_not_emotion
                    print diff

                    if diff > max_diff:
                        max_diff = diff
                        max_emotion = emotion

                    print '{0}: total:{1}, {2}/{3}'.format(context.Emotion.names[emotion], wr_emotion.count(),
                                                   avg_emotion, avg_not_emotion)
                except (TypeError, KeyError):
                    print 'Value is None {}'.format(context.Emotion.names[emotion])

            print 'Max emotion: {}, diff: {}'.format(context.Emotion.names[max_emotion], max_diff)

    def test_user_based_CF(self):
        #input
        self.user = User(name='John', age=25, id=55)
        self.recommendation_context = [context.Season(context.Season.SUMMER), context.Weather(context.Weather.SUNNY),
                                  context.DayType(context.DayType.WORKING_DAY), context.Time(context.Time.EVENING)]

        #precalculations
        self.all_ratings = Rating.objects.all()
        self.movies_titles = self.get_movies_titles()
        self.movies_genres = self.get_movies_genres()
        # self.movies_contexts = self.get_movies_contexts_dependence(self.all_ratings)

        self.genres_dependence = self.get_types_contexts_dependence(self.all_ratings.filter(user_id=self.user.id))
        print self.genres_dependence

        self.all_users_ratings = self.get_users_ratings(self.all_ratings, self.user.id)
        self.similarities = self.get_user_similarity(self.user.id, self.all_users_ratings)

        #recommending
        self.recommendations = self.get_recommendations(self.user.id, self.similarities, self.recommendation_context, self.all_ratings)

        #generating explanation
        self.explanations = self.get_explanations(self.user, self.recommendations)
        print self.explanations
        self.assertEqual(1, 2)

    def get_recommendations(self, user_id, similarities, recommendation_context, all_ratings):
        recommendations = {}

        for c in recommendation_context:
            context_predictions = self.predict_user_ratings(user_id, all_ratings, similarities, c)
            context_recommended_item = self.get_recommended_item(context_predictions)
            if context_recommended_item:
                recommendations.setdefault(context_recommended_item, []).append(c)

        predictions = self.predict_user_ratings(user_id, all_ratings, similarities)
        recommended_item = self.get_recommended_item(predictions)

        if recommended_item:
            recommendations.setdefault(recommended_item, []).append(context.NoContext())
        return recommendations

    def get_explanations(self, user, recommendations):
        explanations = ['Maybe you feel like watching a {genre} like {movie} because {context}?',
                        '{context} so what about watching a {genre} like {movie}?',
                        'You might like a {genre} such as {movie} as {context}.',
                        '{context}, so what about watching a {genre}  such as {movie}?']

        descriptions = []
        for movie in recommendations:
            explanation = choice(explanations)
            descriptions.append(explanation.
                            format(genre=self.movies_genres[movie],
                                   movie=self.movies_titles[movie].capitalize(),
                            context=' and '.join([r.get_description()
                            for r in recommendations[movie]])))

        return'Hi {}! {}'.format(user.name, '\n'.join(descriptions))

    def get_recommended_item(self, predictions):
        max_rating = 0
        best_recommendation = None
        for movie_id in predictions:
            if predictions[movie_id] > max_rating:
                max_rating = predictions[movie_id]
                best_recommendation = movie_id
        return best_recommendation

    def get_significance(self, ratings_1, ratings_2):
        SIGNIFICANCE_THRESHOLD = 0.1
        (t_test, p_value) = ttest_ind(ratings_1, ratings_2, equal_var=False)
        return True if t_test > 0 and p_value < SIGNIFICANCE_THRESHOLD else False

    def get_movies_contexts_dependence(self, all_ratings):
        contexts = [context.Time, context.Weather, context.DayType, context.Season]
        all_movies = []
        for r in all_ratings:
            if r.movie_id not in all_movies:
                all_movies.append(r.movie_id)
        movies_contexts = {c_type.context: {c_value: None for c_value in c_type.names} for c_type in contexts}

        for cont in contexts:
            for context_value in cont.names:
                context_ratings = self.filter_by_context(cont.context, context_value, all_ratings)
                non_context_ratings = self.exclude_by_context(cont.context, context_value, all_ratings)
                movie_c_r = {}
                movie_nc_r = {}

                for cr in context_ratings:
                    movie_c_r.setdefault(cr.movie_id, []).append(cr.rating)
                for ncr in non_context_ratings:
                    movie_nc_r.setdefault(ncr.movie_id, []).append(ncr.rating)

                movies_contexts[cont.context][context_value] = {movie_id: self.get_significance(movie_c_r[movie_id], movie_nc_r[movie_id])
                                                                for movie_id in movie_c_r if movie_id in movie_nc_r}
        return movies_contexts

    def get_types_contexts_dependence(self, all_ratings):

        contexts = [context.Time, context.Weather, context.DayType, context.Season]
        all_types = []
        for r in all_ratings:
            if r.genre not in all_types:
                all_types.append(r.genre)

        types_contexts = {c_type.context: {c_value: None for c_value in c_type.names} for c_type in contexts}

        for cont in contexts:

            for context_value in cont.names:
                context_ratings = self.filter_by_context(cont.context, context_value, all_ratings)
                non_context_ratings = self.exclude_by_context(cont.context, context_value, all_ratings)
                genre_c_r = {}
                genre_nc_r = {}

                for cr in context_ratings:
                    genre_c_r.setdefault(cr.genre, []).append(cr.rating)
                for ncr in non_context_ratings:
                    genre_nc_r.setdefault(ncr.genre, []).append(ncr.rating)

                types_contexts[cont.context][context_value] = []
                for genre in genre_c_r:
                    if genre in genre_nc_r and genre > 0:
                        significance = self.get_significance(genre_c_r[genre], genre_nc_r[genre])
                        if significance:
                            types_contexts[cont.context][context_value].append(genre)
        return types_contexts

    def predict_user_ratings(self, user_id, all_ratings, similarities, cont=None):

        predictions = {}
        if cont:
            genres = self.genres_dependence[cont.context][cont.value]
            print cont.context
            print [context.Genre.names[g] for g in genres]
            all_ratings = all_ratings.filter(genre__in=genres)

        for rating in list(all_ratings.exclude(user_id=user_id)):

            if rating.movie_id not in predictions:
                prediction = self.estimate_rating(user_id, rating.movie_id, similarities)
                if prediction:
                    predictions[rating.movie_id] = prediction

        return predictions

    def get_users_ratings(self, all_ratings, user_id):

        user_ratings = {}
        user_movies = SortedDict([(rating.movie_id, rating.rating) for rating in all_ratings.filter(user_id=user_id)])

        for rating in all_ratings:
            if rating.movie_id in user_movies:
             user_ratings.setdefault(rating.user_id, SortedDict([(m, 0) for m in user_movies]))[rating.movie_id] = rating.rating

        return user_ratings

    def get_user_similarity(self, user_id, user_ratings):
        positive_sims = {}
        for u_id in user_ratings:
            if u_id != user_id:
                sim = pearsonr(user_ratings[user_id].values(), user_ratings[u_id].values())[0]
                if sim > 0:
                    positive_sims[u_id] = sim

        return positive_sims

    def estimate_rating(self, user_id, movie_id, similarities):
        movie_ratings = Rating.objects.filter(movie_id=movie_id, user_id__in=similarities)
        if movie_ratings.count() < 3:
            return None

        movie_users_ratings = {}
        for r in movie_ratings:
            movie_users_ratings[r.user_id] = r.rating
        sims_ratings = SortedDict([(similarities[u], movie_users_ratings[u]) for u in movie_users_ratings if u != user_id and u in similarities])

        if sims_ratings:
            return np.average(sims_ratings.values(), weights=sims_ratings.keys())

        return None

    def filter_by_context(self, context_type, context_value, all_ratings):
        return all_ratings.filter(**{context_type: context_value})

    def exclude_by_context(self, context_type, context_value, all_ratings):
        return all_ratings.exclude(**{context_type: context_value})

