pre_path = '/home/zhc415/myspace/447/datasets/'

f_train = pre_path + 'train_label.csv'
f_test = pre_path + 'test_label.csv'
f_user_log = pre_path + 'user_log.csv'
f_user_info = pre_path + 'user_info.csv'
f_sample = pre_path + 'sample_submission.csv' 

#derived files
f_train_log = pre_path + 'train/' + 'train_log.csv'
f_test_log = pre_path + 'test/' + 'test_log.csv'


#features
count_features = [u'action_counts_month', u'day_counts_month', u'action_ratio_month']