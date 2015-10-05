import recommender.context as context
from scipy.stats import pearsonr, wilcoxon


class ContextRatingsFilter(object):
    SIGNIFICANCE_THRESHOLD = 0.1
    CONTEXTS = [context.Time, context.Weather, context.DayType, context.Season, context.Social]

    def calculate_user_preferences(self, ratings, movies_data, user):
        self.all_ratings = ratings
        self.movies_data = movies_data
        self.genres_dependence = self.__get_types_contexts_dependence(ratings.filter(user_id=user.id))
        print self.genres_dependence

    def filter_by_context(self, user, recommendation_context):
        if not isinstance(recommendation_context, context.NoContext):
            genres = self.genres_dependence[recommendation_context.context][recommendation_context.value]
            return self.all_ratings.filter(genre__in=genres)

        return self.all_ratings

    def __get_types_contexts_dependence(self, all_ratings):
        types_contexts = {c_type.context: {c_value: None for c_value in c_type.names} for c_type in self.CONTEXTS}

        for cont in self.CONTEXTS:

            for context_value in cont.names:
                context_ratings = self.__filter_by_context(cont.context, context_value, all_ratings)
                non_context_ratings = self.__exclude_by_context(cont.context, context_value, all_ratings)
                genre_c_r = {}
                genre_nc_r = {}

                for cr in context_ratings:
                    genre_c_r.setdefault(cr.movie.genre, []).append(cr.rating)
                for ncr in non_context_ratings:
                    genre_nc_r.setdefault(ncr.movie.genre, []).append(ncr.rating)

                types_contexts[cont.context][context_value] = []
                for genre in genre_c_r:
                    if genre in genre_nc_r and genre > 0:
                        significance = self.__get_significance(genre_c_r[genre], genre_nc_r[genre])
                        if significance:
                            types_contexts[cont.context][context_value].append(genre)

        return types_contexts

    def __get_significance(cls, ratings_1, ratings_2):
        (t_test, p_value) = wilcoxon(ratings_1, ratings_2)
        return True if t_test > 0 and p_value < cls.SIGNIFICANCE_THRESHOLD else False

    def __filter_by_context(self, context_type, context_value, all_ratings):
        return all_ratings.filter(**{context_type: context_value})

    def __exclude_by_context(self, context_type, context_value, all_ratings):
        return all_ratings.exclude(**{context_type: context_value})