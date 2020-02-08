import operator

import numpy as np
from knn import KNN
import numpy.linalg as LA


############################################################################
# DO NOT MODIFY ABOVE CODES
############################################################################


# TODO: implement F1 score
def f1_score(real_labels, predicted_labels):
    """
    Information on F1 score - https://en.wikipedia.org/wiki/F1_score
    :param real_labels: List[int]
    :param predicted_labels: List[int]
    :return: float
    """
    assert len(real_labels) == len(predicted_labels)
    tp = 0
    fp = 0
    fn = 0
    for i in range(len(real_labels)):
        if real_labels[i] == 1 and predicted_labels[i] == 1:
            tp += 1
        elif real_labels[i] == 0 and predicted_labels[i] == 1:
            fp += 1
        elif real_labels[i] == 1 and predicted_labels[i] == 0:
            fn += 1
    if tp == 0 and fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)

    if tp == 0 and fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    if precision == 0 and recall == 0:
        f1 = 0
    else:
        f1 = (2 * precision * recall) / (precision + recall)
    return f1
    raise NotImplementedError


class Distances:
    @staticmethod
    # TODO
    def canberra_distance(point1, point2):
        """
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        dist = 0
        for i in range(len(point1)):
            sep = (abs(point1[i] - point2[i])) / (point1[i] + point2[i])
            if np.isnan(sep):
                dist = dist + 0
            else:
                dist += sep

        return dist
        raise NotImplementedError

    @staticmethod
    # TODO
    def minkowski_distance(point1, point2):
        """
        Minkowski distance is the generalized version of Euclidean Distance
        It is also know as L-p norm (where p>=1) that you have studied in class
        For our assignment we need to take p=3
        Information on Minkowski distance - https://en.wikipedia.org/wiki/Minkowski_distance
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        dist = 0
        for i in range(len(point1)):
            dist = dist + (abs((point1[i] - point2[i]) ** 3))
        dist = dist ** (1 / 3)
        return dist
        raise NotImplementedError

    @staticmethod
    # TODO
    def euclidean_distance(point1, point2):
        """
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        dist = 0
        for i in range(len(point1)):
            dist += ((point1[i] - point2[i]) ** 2)
        dist = np.sqrt(dist)
        return dist
        raise NotImplementedError

    @staticmethod
    # TODO
    def inner_product_distance(point1, point2):
        """
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        dist = 0
        for i in range(len(point1)):
            dist = dist + (point1[i] * point2[i])

        return dist
        raise NotImplementedError

    @staticmethod
    # TODO
    def cosine_similarity_distance(point1, point2):
        """
       :param point1: List[float]
       :param point2: List[float]
       :return: float
       """
        num = 0
        p1 = 0
        p2 = 0
        for i in range(len(point1)):
            num = num + (point2[i] * point1[i])
            p1 = p1 + (point1[i] ** 2)
            p2 = p2 + (point2[i] ** 2)
        dist = num / (np.sqrt(p1) * np.sqrt(p2))
        return 1 - dist
        raise NotImplementedError

    @staticmethod
    # TODO
    def gaussian_kernel_distance(point1, point2):
        """
       :param point1: List[float]
       :param point2: List[float]
       :return: float
       """
        dist = 0
        for i in range(len(point1)):
            dist += ((point1[i] - point2[i]) ** 2)
        d = -(np.exp(-0.5 * dist))
        return d
        raise NotImplementedError


class HyperparameterTuner:
    def __init__(self):
        self.best_k = None
        self.best_distance_function = None
        self.best_scaler = None
        self.best_model = None

    # TODO: find parameters with the best f1 score on validation dataset
    def tuning_without_scaling(self, distance_funcs, x_train, y_train, x_val, y_val):
        """
        In this part, you should try different distance function you implemented in part 1.1, and find the best k.
        Use k range from 1 to 30 and increment by 2. Use f1-score to compare different models.

        :param distance_funcs: dictionary of distance functions you must use to calculate the distance.
            Make sure you loop over all distance functions for each data point and each k value.
            You can refer to test.py file to see the format in which these functions will be
            passed by the grading script
        :param x_train: List[List[int]] training data set to train your KNN model
        :param y_train: List[int] train labels to train your KNN model
        :param x_val:  List[List[int]] Validation data set will be used on your KNN predict function to produce
            predicted labels and tune k and distance function.
        :param y_val: List[int] validation labels

        Find(tune) best k, distance_function and model (an instance of KNN) and assign to self.best_k,
        self.best_distance_function and self.best_model respectively.
        NOTE: self.best_scaler will be None

        NOTE: When there is a tie, choose model based on the following priorities:
        Then check distance function  [canberra > minkowski > euclidean > gaussian > inner_prod > cosine_dist]
        If they have same distance fuction  , choose model which has a less k.
        """
        f1 = []
        distance_rankings = {
            'euclidean': 5,
            'minkowski': 4,
            'gaussian': 3,
            'inner_prod': 2,
            'cosine_dist': 1
        }
        for i in distance_funcs:

            print(i)
            for k in range(1, 30, 2):
                obj = KNN(k, distance_funcs[i])
                obj = obj.train(x_train, y_train)
                predict = obj.predict(x_val)
                f1.append([k, f1_score(y_val, predict), distance_rankings[i], obj])

        f1.sort(key=operator.itemgetter(1, 2), reverse=True)
        # You need to assign the final values to these variables
        # index = max(best, key=(lambda x:x[1]))
        self.best_k = f1[0][0]
        for name, val in distance_rankings.items():
            if val == f1[0][2]:
                self.best_distance_function = name

        self.best_model = f1[0][3]

        # raise NotImplementedError

    # TODO: find parameters with the best f1 score on validation dataset, with normalized data
    def tuning_with_scaling(self, distance_funcs, scaling_classes, x_train, y_train, x_val, y_val):
        """
        This part is similar to Part 1.3 except that before passing your training and validation data to KNN model to
        tune k and disrance function, you need to create the normalized data using these two scalers to transform your
        data, both training and validation. Again, we will use f1-score to compare different models.
        Here we have 3 hyperparameters i.e. k, distance_function and scaler.

        :param distance_funcs: dictionary of distance funtions you use to calculate the distance. Make sure you
            loop over all distance function for each data point and each k value.
            You can refer to test.py file to see the format in which these functions will be
            passed by the grading script
        :param scaling_classes: dictionary of scalers you will use to normalized your data.
        Refer to test.py file to check the format.
        :param x_train: List[List[int]] training data set to train your KNN model
        :param y_train: List[int] train labels to train your KNN model
        :param x_val: List[List[int]] validation data set you will use on your KNN predict function to produce predicted
            labels and tune your k, distance function and scaler.
        :param y_val: List[int] validation labels

        Find(tune) best k, distance_funtion, scaler and model (an instance of KNN) and assign to self.best_k,
        self.best_distance_function, self.best_scaler and self.best_model respectively

        NOTE: When there is a tie, choose model based on the following priorities:
        For normalization, [min_max_scale > normalize];
        Then check distance function  [canberra > minkowski > euclidean > gaussian > inner_prod > cosine_dist]
        If they have same distance function, choose model which has a less k.
        """
        f1 = []
        for name in scaling_classes:
            obj = scaling_classes[name]()
            xtrain = obj(x_train)
            xval = obj(x_val)
            print(name)
            for i in distance_funcs:
                j = 0
                print(i)
                for k in range(1, 30, 2):
                    obj = KNN(k, distance_funcs[i])
                    obj = obj.train(xtrain, y_train)
                    predict = obj.predict(xval)
                    f1.append([k, f1_score(y_val, predict), i, name])
                    #f1[k] = f1_score(y_val, predict)
                    #print(k, "  ", f1.get(k))
        f1 = sorted(f1, key=operator.itemgetter(1), reverse=True)

        # You need to assign the final values to these variables
        #index = max(best, key=(lambda x: x[2]))
        self.best_k = f1[0][0]
        self.best_distance_function = f1[0][2]
        self.best_scaler = f1[0][3]
        self.best_model = obj
        # raise NotImplementedError


class NormalizationScaler:
    def __init__(self):
        pass

    # TODO: normalize data
    def __call__(self, features):
        """
        Normalize features for every sample

        Example
        features = [[3, 4], [1, -1], [0, 0]]
        return [[0.6, 0.8], [0.707107, -0.707107], [0, 0]]

        :param features: List[List[float]]
        :return: List[List[float]]
        """
        np.seterr(divide='ignore', invalid='ignore')
        data = np.array(features)
        d = LA.norm(data, axis=1)
        new = data / d[:, np.newaxis]
        np.nan_to_num(new, copy=False)
        return new
        raise NotImplementedError


class MinMaxScaler:
    counter = 0
    min, max = [], []
    """
    Please follow this link to know more about min max scaling
    https://en.wikipedia.org/wiki/Feature_scaling
    You should keep some states inside the object.
    You can assume that the parameter of the first __call__
    will be the training set.

    Hints:
        1. Use a variable to check for first __call__ and only compute
            and store min/max in that case.

    Note:
        1. You may assume the parameters are valid when __call__
            is being called the first time (you can find min and max).

    Example:
        train_features = [[0, 10], [2, 0]]
        test_features = [[20, 1]]

        scaler1 = MinMaxScale()
        train_features_scaled = scaler1(train_features)
        # train_features_scaled should be equal to [[0, 1], [1, 0]]

        test_features_scaled = scaler1(test_features)
        # test_features_scaled should be equal to [[10, 0.1]]

        new_scaler = MinMaxScale() # creating a new scaler
        _ = new_scaler([[1, 1], [0, 0]]) # new trainfeatures
        test_features_scaled = new_scaler(test_features)
        # now test_features_scaled should be [[20, 1]]

    """

    def __init__(self):
        pass

    def __call__(self, features):
        self.counter += 1
        data = np.array(features)
        if self.counter == 1:
            self.min = data.min(axis=0)
            self.max = data.max(axis=0)
        """
        normalize the feature vector for each sample . For example,
        if the input features = [[2, -1], [-1, 5], [0, 0]],
        the output should be [[1, 0], [0, 1], [0.333333, 0.16667]]

        :param features: List[List[float]]
        :return: List[List[float]]

        """
        new = (data - self.min) / (self.max - self.min)
        return new
        raise NotImplementedError
