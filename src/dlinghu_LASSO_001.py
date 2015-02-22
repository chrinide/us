# this file implements LASSO

import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn import linear_model, decomposition
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import accuracy_score
from dlinghu_SVM_001 import output, read_data, print_cv_scores


# find the best threshold
def find_reg_threshold(clf, x_train, y_train):
    threshold_list = np.arange(start=0.1, stop=1.0, step=0.05)
    threshold_best = 0
    accuracy_best = 0
    y_train_predict = clf.predict(x_train)
    for threshold in threshold_list:
        y_train_predict_binary = np.array(y_train_predict)
        y_train_predict_binary[y_train_predict_binary < threshold] = 0
        y_train_predict_binary[y_train_predict_binary >= threshold] = 1
        tmp_score = accuracy_score(y_train_predict_binary, y_train)
        # print '%s\t%s' % (threshold, tmp_score)
        print '{:>8} {:>8}'.format(*[threshold, tmp_score])
        if tmp_score > accuracy_best:
            accuracy_best = tmp_score
            threshold_best = threshold
            y_train_predict_binary_best = y_train_predict_binary
    print 'best threshold = %s' % threshold_best
    return threshold_best


# tune parameters for LASSO
def lasso_tune_parameters(x_train, y_train):
    lasso = linear_model.Lasso()
    alpha_list = np.logspace(-8, 5, num=11)
    print "Entering GridSearchCV..."
    param_grid = dict(alpha=alpha_list)
    cv = StratifiedKFold(y=y_train, n_folds=3)
    grid = GridSearchCV(lasso, param_grid=param_grid, cv=cv)
    grid.fit(x_train, y_train)
    print("The best classifier is: ", grid.best_estimator_)
    clf = grid.best_estimator_
    return clf


def lasso_001():
    x_train, y_train, x_test = read_data()
    clf = lasso_tune_parameters(x_train, y_train)
    threshold = find_reg_threshold(clf, x_train, y_train)
    y_test_predict_raw = clf.predict(x_test)
    y_test_predict = np.array(y_test_predict_raw)
    y_test_predict[y_test_predict < threshold] = 0
    y_test_predict[y_test_predict >= threshold] = 1
    # output(y_test_predict, 'LASSO_001.csv')  # alpha=1e-8, threshold=0.4


if __name__ == "__main__":
    lasso_001()