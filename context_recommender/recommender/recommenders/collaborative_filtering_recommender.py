from scipy.stats import pearsonr
from numpy import average

from django.utils.datastructures import SortedDict


class CollaborativeFilteringRecommender(object):
    KNN_LIMIT = 3

    def recommend(self, user_id, ratings, recommendation_context):
        all_users_ratings = self.__get_users_ratings(ratings, user_id)
        similarities = self.__get_users_similarities(user_id, all_users_ratings)

        context_predictions = self.__predict_user_ratings(user_id, ratings, similarities, recommendation_context)
        context_recommended_item = self.__get_recommended_item(context_predictions)
        if context_recommended_item:
            return context_recommended_item

    def __predict_user_ratings(self, user_id, ratings, similarities, cont=None):

        predictions = {}
        for rating in list(ratings.exclude(user_id=user_id)):

            if rating.movie_id not in predictions:
                prediction = self.__estimate_rating(user_id, rating.movie_id, ratings, similarities)
                if prediction:
                    predictions[rating.movie_id] = prediction

        return predictions

    def __get_users_similarities(self, user_id, user_ratings):
        positive_sims = {}
        for u_id in user_ratings:
            if u_id != user_id:
                sim = pearsonr(user_ratings[user_id].values(), user_ratings[u_id].values())[0]
                if sim > 0:
                    positive_sims[u_id] = sim

        return positive_sims # TODO: return KNN
        # return self.__get_KNN(positive_sims)

    def __get_users_ratings(self, all_ratings, user_id):

        user_ratings = {}
        user_movies = SortedDict([(rating.movie_id, rating.rating) for rating in all_ratings.filter(user_id=user_id)])

        for rating in all_ratings:
            if rating.movie_id in user_movies:
             user_ratings.setdefault(rating.user_id, SortedDict([(m, 0) for m in user_movies]))[rating.movie_id] = rating.rating

        return user_ratings

    def __get_recommended_item(self, predictions):
        max_rating = 0
        best_recommendation = None
        for movie_id in predictions:
            if predictions[movie_id] > max_rating:
                max_rating = predictions[movie_id]
                best_recommendation = movie_id
        return best_recommendation

    def __estimate_rating(self, user_id, movie_id, ratings, similarities):
        movie_ratings = ratings.filter(movie_id=movie_id, user_id__in=similarities)
        if movie_ratings.count() < 3:
            return None

        movie_users_ratings = {}
        for r in movie_ratings:
            movie_users_ratings[r.user_id] = r.rating
        sims_ratings = SortedDict([(similarities[u], movie_users_ratings[u]) for u in movie_users_ratings
                                   if u != user_id and u in similarities])

        if sims_ratings:
            return average(sims_ratings.values(), weights=sims_ratings.keys())

        return None

    def __get_KNN(self, similarities):
        return dict(sorted(similarities.items, lambda(k, v): v)[:self.KNN_LIMIT])