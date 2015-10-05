from random import choice
from recommender.data_reader import DataReader


class ExplanationsGenerator(object):

    EXPLANATIONS = ['Maybe you feel like watching a {genre} like {movie} because {context}?',
                    '{context} so what about watching a {genre} like {movie}?',
                    'You might like a {genre} such as {movie} as {context}.',
                    '{context}, so what about watching a {genre}  such as {movie}?']

    def __init__(self, movies_data):
        self.movies_data = movies_data

    def get_explanations(self, user, recommendations):
        descriptions = []
        for movie_id in recommendations:
            movie = self.movies_data.get(id=movie_id)
            explanation = choice(self.EXPLANATIONS)
            descriptions.append(explanation.format(genre=movie.genre,
                            movie=movie.title.capitalize(),
                            context=' and '.join([r.get_description()
                            for r in recommendations[movie_id]])))

        return'Hi {}! {}'.format(user.name, '\n'.join(descriptions))