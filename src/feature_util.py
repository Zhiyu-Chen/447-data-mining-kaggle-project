from metadata import *
from util import *
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import preprocessing

def combo_count_features(feature,feature_book):
	'''
	actually this should be called as action count features ...
	'''
	for each in count_features:
		each_feature = feature_book[each]
		for each_action in ['0','1','2','3']:
			if each_feature.has_key(each_action):
				feature += each_feature[each_action]
			else:
				feature += [0 for i in range(8)]
	return feature

def combo_diversity_features(feature,feature_book):
	diversity = feature_book['diversity']
	for each_prod in diversity:
		feature += diversity[each_prod]
	return feature

def combo_user_feature(user_id,user_profile):
	feature_book = user_profile[user_id]
	all_feature = []
	#for count feature
	all_feature = combo_count_features(all_feature,feature_book)
	#for diversity feature
	all_feature = combo_diversity_features(all_feature,feature_book)
	# process NaN
	all_feature = np.nan_to_num(all_feature)
	return all_feature


def combo_merchant_feature(merchant_id,merchant_profile):
	feature_book = merchant_profile[merchant_id]
	all_feature = []
	#for count feature
	all_feature = combo_count_features(all_feature,feature_book)
	#for diversity feature
	all_feature = combo_diversity_features(all_feature,feature_book)
	# process NaN
	all_feature = np.nan_to_num(all_feature)

	return all_feature


def combo_UM_feature(UM,UM_profile):
	feature_book = UM_profile[UM]
	all_feature = []
	#for count feature
	all_feature = combo_count_features(all_feature,feature_book)
	#for diversity feature
	all_feature = combo_diversity_features(all_feature,feature_book)
	# process NaN
	all_feature = np.nan_to_num(all_feature)
	return all_feature