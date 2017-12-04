# kaggle-project: Loyal Customer Prediction



# Project Link

https://inclass.kaggle.com/c/loyal-customer-prediction 

1. run 'count_features.py' to build entity profiles (features)
2. run 'util.py' to train the model and write the results


# Questions

## 1. what is the ratio of positive and negative instances.

positive: 7885
negative: 122479

ratio = 15



## 2. Statistics

train_label.csv:                              
        # of users:      106031  # of merchants:        1992

test_label.csv:
        # of users:      106031  # of merchants:        1991

user_log.csv:
        # of users:      212062
        # of items:      916773
        # of categories:         1581
        # of merchants:  4995
        # of brands:     8161

user_info.csv:
        # of users:      212062

sample_submission.csv:
        # of users:      106031  # of merchants:        1991

date range:

511 - 1112




# About preprocessing 

* Does the data include crawlers ?


* Missing values ? (all 0)

# How to manage features

split user_log.csv by training set and testing set for convinience.
So that we could generate features for training set and testing set seperately.

Two types of features:

## Entity features 

each entity has a file. 

For users,

    file structure
    user.json :
    {
        user_id:
            {
            feature_id:
                {
                    action_type: [0,0,0,0,0,0,0,0] #(7 months + sum)
                }
            } ,
        ...
    }
    '''

## Interative features



## imbalanced learning: 

https://github.com/scikit-learn-contrib/imbalanced-learn#id27

http://contrib.scikit-learn.org/imbalanced-learn/auto_examples/combine/plot_smote_enn.html


