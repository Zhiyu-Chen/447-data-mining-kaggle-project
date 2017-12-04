from metadata import *
import pandas as pd
import os
from util import *

def get_statistics(path):
	df = pd.read_csv(filepath_or_buffer = path,header = 0)
	print path + ':'

	if 'user_id#merchant_id' in df.columns:
		user_merchant = df['user_id#merchant_id'].tolist()
		users = set()
		merchants = set()
		for each in user_merchant:
			user,merchant = each.split('#')
			users.add(user)
			merchants.add(merchant)
		print '\t' + "# of users:\t " + str(len(users)) + '\t # of merchants: \t' + str(len(merchants))

	#Index([u'user_id', u'item_id', u'cat_id', u'merchant_id', u'brand_id',u'time_stamp', u'action_type']
	if 'user_id' in df.columns:
		print '\t' + "# of users:\t " + str(len(df['user_id'].drop_duplicates()))


	if 'item_id' in df.columns:
		print '\t' + "# of items:\t " + str(len(df['item_id'].drop_duplicates()))

	if 'cat_id' in df.columns:
		print '\t' + "# of categories:\t " + str(len(df['cat_id'].drop_duplicates()))

	if 'merchant_id' in df.columns:
		print '\t' + "# of merchants:\t " + str(len(df['merchant_id'].drop_duplicates()))

	if 'brand_id' in df.columns:
		print '\t' + "# of brands:\t " + str(len(df['brand_id'].drop_duplicates()))

def get_all_statistics():
	paths = [f_train,f_test,f_user_log,f_user_info,f_sample]
	for each in paths:
		get_statistics(each)


def split_log():
	'''
	split user_log.csv by training set and testing set for convinience.
	'''
	if not os.path.exists( pre_path + 'train'):
		os.mkdir(pre_path + 'train')
	if not os.path.exists(pre_path + 'test'):
		os.mkdir(pre_path + 'test')

	train_users, train_merchants = get_train_user_merchant(f_train)
	log_df = pd.read_csv(f_user_log,header = 0)
	train_log = log_df[log_df['user_id'].isin(train_users)]

	test_users, test_merchants = get_train_user_merchant(f_test)
	test_log = log_df[log_df['user_id'].isin(test_users)]

	train_log.to_csv(pre_path + 'train/train_log.csv',index = False)
	test_log.to_csv(pre_path + 'test/test_log.csv',index = False)


def main():
	#get_all_statistics()
	split_log()

if __name__ == '__main__':
	main()