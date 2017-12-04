import pandas as pd
from metadata import *
import json,csv
from feature_util import *
from sklearn.cross_validation import StratifiedKFold #http://scikit-learn.org/0.17/modules/cross_validation.html#stratified-k-fold
from sklearn.cross_validation import train_test_split #http://machinelearningmastery.com/xgboost-python-mini-course/
from sklearn.cross_validation import LabelKFold
from xgboost import XGBClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import minmax_scale
import numpy as np
from imblearn.combine import SMOTEENN

def df2list(path,col):
	df = pd.read_csv(filepath_or_buffer = path,header = 0)
	return df[col].tolist()

def get_train_user_merchant(path):
	user_merchant = df2list(path,'user_id#merchant_id')
	users = set()
	merchants = set()
	for each in user_merchant:
		user,merchant = each.split('#')
		users.add(user)
		merchants.add(merchant)
	return users,merchants

########################### get feature database ###########################

def get_user_profile():
	# read user profile
	f = open(pre_path + 'user.json','r')
	line = f.readline()
	f.close()
	user_profile = json.loads(line)
	return user_profile

def get_merchant_profile():
	f = open(pre_path + 'merchant.json','r')
	line = f.readline()
	f.close()
	merchant_profile = json.loads(line)
	return merchant_profile

def get_UM_profile():
	# read user profile
	f = open(pre_path + 'user_merchant.json','r')
	line = f.readline()
	f.close()
	UM_profile = json.loads(line)
	return UM_profile


def get_training_data():
	df = pd.read_csv(f_train,header = 0)
	features = []
	labels = []
	user_profile = get_user_profile()
	merchant_profile = get_merchant_profile()
	UM_profile = get_UM_profile()
	for row_num,each in df.iterrows():
		feature = []
		UM,label = each.tolist()
		user,merchant = UM.split('#')
		#user profile feature
		feature = np.concatenate((feature,combo_user_feature(user,user_profile)))
		#merchant profile feature
		feature = np.concatenate( (feature,combo_merchant_feature(merchant,merchant_profile) ) )
		#UM profile feature
		feature =  np.concatenate( (feature,combo_UM_feature(UM,UM_profile)) )
		features.append(feature)
		labels.append(label)
		print "finished {0} of {1}, {2}%".format(row_num,len(df),100*float(row_num)/len(df))
	features = np.array(features)
	features = preprocessing.minmax_scale(features)
	return features,labels

def get_testing_data():
	test_df = pd.read_csv(f_test,header = 0)
	test_features = []
	user_profile = get_user_profile()
	merchant_profile = get_merchant_profile()
	UM_profile = get_UM_profile()
	ids = []
	for row_num,each in test_df.iterrows():
		test_feature = []
		UM,label = each.tolist()
		user,merchant = UM.split('#')
		#user profile feature
		test_feature = np.concatenate((test_feature,combo_user_feature(user,user_profile)))
		#merchant profile feature
		test_feature = np.concatenate( (test_feature,combo_merchant_feature(merchant,merchant_profile) ) )
		#UM profile feature
		test_feature =  np.concatenate( (test_feature,combo_UM_feature(UM,UM_profile)) )
		ids.append(UM)
		test_features.append(test_feature)
		print "finished {0} of {1}, {2}%".format(row_num,len(test_df),100*float(row_num)/len(test_df))
	test_features = np.array(test_features)
	test_features = preprocessing.minmax_scale(test_features)
	return ids,test_features

def write_results(ids,probs,fname='rs.csv'):
	headers = ['user_id#merchant_id','prob']
	csvfile = file(fname, 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(headers)
	for i in range(len(ids)):
		writer.writerow([ids[i],probs[i]])
	csvfile.close()


########### main ############
if __name__ == '__main__':
	features,labels = get_training_data()

	model = XGBClassifier(learning_rate =0.1, max_depth=7,
	min_child_weight=200, gamma=0, subsample=0.8,             colsample_bytree=0.8,
	 objective= 'binary:logistic',     scale_pos_weight=1.0, seed=27)

	learning_rate = [0.001, 0.01, 0.1]
	scale_pos_weight = [3.0/5,1,2]
	param_grid = dict(max_depth=[5,6,7,8],min_child_weight=[5,100,200],learning_rate = learning_rate,scale_pos_weight=scale_pos_weight,)
	kfold = StratifiedKFold(labels, n_folds=10, shuffle=True, random_state=7)
	grid_search = GridSearchCV(model, param_grid, scoring="log_loss", n_jobs=-1, cv=kfold)
	result = grid_search.fit(np.array(features), labels)
	# summarize results
	print("Best: %f using %s" % (result.best_score_, result.best_params_))
	means, stdevs = [], []
	for params, mean_score, scores in result.grid_scores_:
		stdev = scores.std()
		means.append(mean_score)
		stdevs.append(stdev)
		print("%f (%f) with: %r" % (mean_score, stdev, params))



	### final training 
	#features,labels = get_training_data()
	model = XGBClassifier(learning_rate =0.1, max_depth=8,
	min_child_weight=200, gamma=0, subsample=0.8,             colsample_bytree=0.8,
	 objective= 'binary:logistic',     scale_pos_weight=1.0, seed=27)
	model.fit(np.array(features), labels)


	### final prediction
	ids,test_x = get_testing_data()
	predicted_y = model.predict_proba(np.array(test_x))
	predicted_is = predicted_y[:,1]
	write_results(ids,predicted_is,fname = 'rs4.csv')
