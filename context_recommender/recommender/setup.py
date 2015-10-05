from distutils.core import setup
import sys, os

setup(
    name='context_recommender',
    version='',
    packages=['', 'tests', 'tests.data_readers_tests', 'tests.recommenders_tests',
              'tests.recommenders_tests.content_based_recommenders_tests',
              'tests.recommenders_tests.non_personalized_recomenders_tests',
              'tests.recommenders_tests.collaborative_filtering_recommenders_tests', 'tests.user_scenarios_tests',
              'data_parsers', 'data_parsers.movielens_parsers', 'rabbit_mq_modules', 'rabbit_mq_modules.scripts',
              'rabbit_mq_modules.queue_workers', 'system_components', 'system_components.data_filters',
              'system_components.data_parsers', 'system_components.data_parsers.movielens_parsers',
              'system_components.recommenders', 'system_components.recommenders.content_based_recommenders',
              'system_components.recommenders.non_personalized_recommenders',
              'system_components.recommenders.collaborative_filtering_recommenders',
              'system_components.text_generators'],
    package_dir={'': 'recommender'},
    url='',
    license='',
    author='asia',
    author_email='',
    description=''
)

sys.path.append(os.path.join(os.path.dirname('__file__'), "~/PycharmProjects/django_Recommender/recommender"))
