from recommender.models import User, Movie, Rating
from recommender.statistics_calculator import StatisticsCalculator
from recommender.recommenders.collaborative_filtering_recommender import CollaborativeFilteringRecommender
from recommender.filters.context_filters import ContextRatingsFilter
from recommender.explanations_generator import ExplanationsGenerator


class RecommenderSystem(object):

    def __init__(self):

        self.calculator = StatisticsCalculator()
        self.all_ratings = Rating.objects.all()
        self.all_movies = Movie.objects.all()
        self.context_filter = ContextRatingsFilter()
        self.recommender = CollaborativeFilteringRecommender()
        self.explanation_generator = ExplanationsGenerator(self.all_movies)
        #TODO: precalculations in each module for all users

    def recommend(self, user, recommendation_context):
        #input
        self.user = user
        self.recommendation_context = recommendation_context
        #precalculations
        self.context_filter.calculate_user_preferences(self.all_ratings, self.all_movies, self.user)

        #recommending
        recommendations = self.__get_recommendations(self.user.id, self.recommendation_context)

        #generating explanation
        explanations = self.explanation_generator.get_explanations(self.user, recommendations)
        return explanations

    def __get_recommendations(self, user_id, recommendation_context):
        recommendations_reasons = {}

        for c in recommendation_context:
            context_ratings = self.context_filter.filter_by_context(self.user, c)
            context_recommended_item = self.recommender.recommend(user_id, context_ratings, c)
            if context_recommended_item:
                recommendations_reasons.setdefault(context_recommended_item, []).append(c)

        return recommendations_reasons








