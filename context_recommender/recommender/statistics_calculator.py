from scipy.stats import pearsonr, ttest_ind


class StatisticsCalculator(object):
    SIGNIFICANCE_THRESHOLD = 0.1

    @classmethod
    def get_significance(cls, ratings_1, ratings_2):

        (t_test, p_value) = ttest_ind(ratings_1, ratings_2, equal_var=False)
        return True if t_test > 0 and p_value < cls.SIGNIFICANCE_THRESHOLD else False