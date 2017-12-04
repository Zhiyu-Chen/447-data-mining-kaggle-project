'''
	file structure e.g. user profile
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
from metadata import *
import pandas as pd
from util import *
import json
import time
from util import *
import numpy as np
############################################### Init ###############################################

def init_user_features():
	#use this function before generating the 1st user profile feature
	f = open(pre_path + 'user.json','w')
	user_log = pd.read_csv(f_user_log,header  = 0)
	users = user_log['user_id'].drop_duplicates()
	user_profile = dict()
	for user in users:
		user_profile[user] = dict() # for {user_id: feature_dict}
	f.write(json.dumps(user_profile))
	f.close()

def init_merchant_features():
	#use this function before generating the 1st merchant profile feature
	f = open(pre_path + 'merchant.json','w')
	user_log = pd.read_csv(f_user_log,header  = 0)
	merchants = user_log['merchant_id'].drop_duplicates()
	merchant_profile = dict()
	for merchant in merchants:
		merchant_profile[merchant] = dict() # for {user_id: feature_dict}
	f.write(json.dumps(merchant_profile))
	f.close()

def init_UM_features():
	#use this function before generating the 1st user-merchant profile feature
	f = open(pre_path + 'user_merchant.json','w')
	user_log = pd.read_csv(f_user_log,header  = 0)
	user_merchant = user_log[['user_id','merchant_id']].drop_duplicates()
	user_merchant_profile = dict()
	for pair in user_merchant.iterrows():
		um_pair = tuple(pair[1].tolist())
		user_merchant_profile[str(um_pair[0]) + '#' + str(um_pair[1])] = dict() # for {user_id: feature_dict}
	f.write(json.dumps(user_merchant_profile))
	f.close()

############################################### Count Features ###############################################
def store_user_action_counts():
	'''
	Description: # of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_counts_month
	
	Path: pre_path + 'user.json'

	'''

	# read user profile
	f = open(pre_path + 'user.json','r')
	line = f.readline()
	f.close()
	user_profile = json.loads(line)

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['user_id'])
	## for each user
	for user,each_log in groups:
		action_vector = dict()
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not action_vector.has_key(action):
				action_vector[action] = [0 for i in range(8)]
			
			month = record['time_stamp']/100 - 5
			action_vector[action][month] += 1

		## monthly vector has been created, compute the sum of each actions
		for each_action in action_vector:
			action_vector[each_action][-1] = sum(action_vector[each_action])

		## write this feature to user profile
		user_profile[str(user)]['action_counts_month'] = action_vector
		print "user action count features: {0}".format(action_vector)

	# update user profile
	f = open(pre_path + 'user.json','w')
	f.write(json.dumps(user_profile))
	f.close()

def store_merchant_action_counts():
	'''
	Description: # of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_counts_month
	
	Path: pre_path + 'merchant.json'

	'''
	# read user profile
	f = open(pre_path + 'merchant.json','r')
	line = f.readline()
	f.close()
	merchant_profile = json.loads(line)

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['merchant_id'])
	## for each merchant
	for merchant,each_log in groups:
		action_vector = dict()
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not action_vector.has_key(action):
				action_vector[action] = [0 for i in range(8)]
			
			month = record['time_stamp']/100 - 5
			action_vector[action][month] += 1

		## monthly vector has been created, compute the sum of each actions
		for each_action in action_vector:
			action_vector[each_action][-1] = sum(action_vector[each_action])

		## write this feature to user profile
		merchant_profile[str(merchant)]['action_counts_month'] = action_vector
		print "merchant action count features: {0}".format(action_vector)
	# update user profile
	f = open(pre_path + 'merchant.json','w')
	f.write(json.dumps(merchant_profile))
	f.close()

def store_UM_action_counts():
	'''
	Description: # of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_counts_month
	
	Path: pre_path + 'user_merchant.json'

	'''
	# read user profile
	f = open(pre_path + 'user_merchant.json','r')
	line = f.readline()
	f.close()
	UM_profile = json.loads(line)

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	total = len(UM_profile)
	## for each user-merchant pair
	count = 0
	groups =  user_log.groupby(['user_id','merchant_id'])
	for (user_id,merchant_id),each_log in groups:
		start = time.clock()

		action_vector = dict()
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not action_vector.has_key(action):
				action_vector[action] = [0 for i in range(8)]

			month = record['time_stamp']/100 - 5
			action_vector[action][month] += 1

		## monthly vector has been created, compute the sum of each actions
		for each_action in action_vector:
			action_vector[each_action][-1] = sum(action_vector[each_action])

		## write this feature to user profile
		UM_profile[str(user_id) + '#' + str(merchant_id)]['action_counts_month'] = action_vector

		## log
		elapsed = (time.clock() - start)
		count += 1
		print "action_vector of {0} # {1} : {2}".format(user_id,merchant_id,action_vector)
		print "finish {0} of {1}, {2}, {3} hours left ".format(count,total, 1.0*count/total*100,elapsed*(total-count)/3600.0 )

	# update user profile
	f = open(pre_path + 'user_merchant.json','w')
	f.write(json.dumps(UM_profile))
	f.close()

############################################### Ratio Features ###############################################

def store_user_action_ratio():
	'''
	Description: ratio of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_ratio_month
	
	Path: pre_path + 'user.json'

	'''

	# read user profile
	user_profile = get_user_profile()

	## for each user
	for user in user_profile:
		action_ratio_vector = dict()
		## calculate the sum of all actions 
		action_vector = user_profile[user]['action_counts_month']
		action_sum = np.array([0 for i in range(8)],dtype=np.float64)
		for action in action_vector:
			action_sum += np.array(action_vector[action],dtype=np.float64)

		for action in action_vector:
			action_ratio_vector[action] = list(action_vector[action]/action_sum)
		## write this feature to user profile
		user_profile[user]['action_ratio_month'] = action_ratio_vector
		print "user action ratio features: {0}".format(action_ratio_vector)

	# update user profile
	f = open(pre_path + 'user.json','w')
	f.write(json.dumps(user_profile))
	f.close()

def store_merchant_action_ratio():
	'''
	Description: ratio of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_ratio_month
	
	Path: pre_path + 'merchant.json'

	'''

	# read merchant profile
	merchant_profile = get_merchant_profile()

	## for each merchant
	for merchant in merchant_profile:
		action_ratio_vector = dict()
		## calculate the sum of all actions 
		action_vector = merchant_profile[merchant]['action_counts_month']
		action_sum = np.array([0 for i in range(8)],dtype=np.float64)
		for action in action_vector:
			action_sum += np.array(action_vector[action],dtype=np.float64)

		for action in action_vector:
			action_ratio_vector[action] = list(action_vector[action]/action_sum)
		## write this feature to user profile
		merchant_profile[merchant]['action_ratio_month'] = action_ratio_vector
		print "merchant action ratio features: {0}".format(action_ratio_vector)

	# update user profile
	f = open(pre_path + 'merchant.json','w')
	f.write(json.dumps(merchant_profile))
	f.close()

def store_UM_action_ratio():
	'''
	Description: ratio of clicks, purchases, add-to-favourite actions in each month or overall count

	Feature ID : action_ratio_month
	
	Path: pre_path + 'user_merchant.json'

	'''

	# read user merchant profile
	UM_profile = get_UM_profile()

	## for each merchant
	for UM in UM_profile:
		action_ratio_vector = dict()
		## calculate the sum of all actions 
		action_vector = UM_profile[UM]['action_counts_month']
		action_sum = np.array([0 for i in range(8)],dtype=np.float64)
		for action in action_vector:
			action_sum += np.array(action_vector[action],dtype=np.float64)

		for action in action_vector:
			action_ratio_vector[action] = list(action_vector[action]/action_sum)
		## write this feature to user profile
		UM_profile[UM]['action_ratio_month'] = action_ratio_vector
		print "user-merchant action ratio features: {0}".format(action_ratio_vector)

	# update user profile
	f = open(pre_path + 'user_merchant.json','w')
	f.write(json.dumps(UM_profile))
	f.close()


############################################### Day Counts Features ###############################################

def store_user_day_counts():
	'''
	Description: # of days with a particular action type in each month or overall count

	Feature ID : day_counts_month
	
	Path: pre_path + 'user.json'

	'''

	# read user profile
	user_profile = get_user_profile()

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['user_id'])
	## for each user
	for user,each_log in groups:
		day_count_vector = dict() # {'0':[[],[],[],[],[],[],[]]}
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not day_count_vector.has_key(action):
				day_count_vector[action] = [set() for i in range(8)]
			
			month = record['time_stamp']/100 - 5
			day = record['time_stamp']%100
			day_count_vector[action][month].add(day)

		## monthly vector has been created, compute the sum of each actions
		for each_action in day_count_vector:
			for each_month in day_count_vector[each_action]:
				day_count_vector[each_action][-1] = day_count_vector[each_action][-1] | each_month

		for each_action in day_count_vector:
			day_count_vector[each_action] = [len(day_count_vector[each_action][i]) for i in range(8) ]
		## write this feature to user profile
		user_profile[str(user)]['day_counts_month'] = day_count_vector
		print "user day count features: {0}".format(day_count_vector)

	# update user profile
	f = open(pre_path + 'user.json','w')
	f.write(json.dumps(user_profile))
	f.close()


def store_merchant_day_counts():
	'''
	Description: # of days with a particular action type in each month or overall count

	Feature ID : day_counts_month
	
	Path: pre_path + 'merchant.json'

	'''

	# read user profile
	merchant_profile = get_merchant_profile()

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['merchant_id'])
	## for each user
	for merchant,each_log in groups:
		day_count_vector = dict() # {'0':[[],[],[],[],[],[],[]]}
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not day_count_vector.has_key(action):
				day_count_vector[action] = [set() for i in range(8)]
			
			month = record['time_stamp']/100 - 5
			day = record['time_stamp']%100
			day_count_vector[action][month].add(day)

		## monthly vector has been created, compute the sum of each actions
		for each_action in day_count_vector:
			for each_month in day_count_vector[each_action]:
				day_count_vector[each_action][-1] = day_count_vector[each_action][-1] | each_month

		for each_action in day_count_vector:
			day_count_vector[each_action] = [len(day_count_vector[each_action][i]) for i in range(8) ]
		## write this feature to user profile
		merchant_profile[str(merchant)]['day_counts_month'] = day_count_vector
		print "merchant day count features: {0}".format(day_count_vector)

	# update user profile
	f = open(pre_path + 'merchant.json','w')
	f.write(json.dumps(merchant_profile))
	f.close()


def store_UM_day_counts():
	'''
	Description: # of days with a particular action type in each month or overall count

	Feature ID : day_counts_month
	
	Path: pre_path + 'user_merchant.json'

	'''

	# read user profile
	UM_profile = get_UM_profile()

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['user_id','merchant_id'])
	## for each user
	for (user_id,merchant_id),each_log in groups:
		day_count_vector = dict() # {'0':[[],[],[],[],[],[],[]]}
		for index, record in each_log.iterrows():
			action = record['action_type']
			if not day_count_vector.has_key(action):
				day_count_vector[action] = [set() for i in range(8)]
			
			month = record['time_stamp']/100 - 5
			day = record['time_stamp']%100
			day_count_vector[action][month].add(day)

		## monthly vector has been created, compute the sum of each actions
		for each_action in day_count_vector:
			for each_month in day_count_vector[each_action]:
				day_count_vector[each_action][-1] = day_count_vector[each_action][-1] | each_month

		for each_action in day_count_vector:
			day_count_vector[each_action] = [len(day_count_vector[each_action][i]) for i in range(8) ]
		## write this feature to user profile
		UM_profile[str(user_id) + '#' + str(merchant_id)]['day_counts_month'] = day_count_vector
		print "UM day count features: {0}".format(day_count_vector)

	# update user profile
	f = open(pre_path + 'user_merchant.json','w')
	f.write(json.dumps(UM_profile))
	f.close()


###############################################  Diversity Features ###############################################
def store_user_diversity():
	'''
	Description: # of unique items, brands and categories that the user clicked, purchased or added to favourites
				in each month or over the whole data period.

	Feature ID : diversity
	
	Path: pre_path + 'user_merchant.json'
	{
		user_id:
			{
			diversity:
				{
					items: [0,0,0,0,0,0,0,0] #(7 months + overall)
					brands:...
					cat:...
				}

			} ,
		...
	}
	'''	
	user_profile = get_user_profile()

	# begin to extract monthly diversity features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['user_id'])
	## for each user
	for user,each_log in groups:
		diversity = dict()
		for index, record in each_log.iterrows():
			item_id = record['item_id']
			cat_id = record['cat_id']
			brand_id = record['brand_id']

			if not diversity.has_key('items'):
				diversity['items'] = [[] for i in range(8)]
			if not diversity.has_key('brands'):
				diversity['brands'] = [[] for i in range(8)]
			if not diversity.has_key('cats'):
				diversity['cats'] = [[] for i in range(8)]

			month = record['time_stamp']/100 - 5
			diversity['items'][month].append(item_id)
			diversity['brands'][month].append(brand_id)
			diversity['cats'][month].append(cat_id)


		## monthly vector has been created, compute the sum over the whole period
		for each_action in diversity:
			for i in range(7):
				diversity[each_action][-1] += diversity[each_action][i]

		## convert items to number of unique items
		for each_prod in diversity:
			for i in range(8):
				diversity[each_prod][i] = len(set(diversity[each_prod][i]))

		## write this feature to user profile
		user_profile[str(user)]['diversity'] = diversity
		print "user diversity features: {0}".format(diversity)
	# update user profile
	f = open(pre_path + 'user.json','w')
	f.write(json.dumps(user_profile))
	f.close()



def store_merchant_diversity():

	merchant_profile = get_merchant_profile()

	# begin to extract monthly diversity features
	user_log = pd.read_csv(f_user_log,header  = 0)
	groups =  user_log.groupby(['merchant_id'])
	## for each user
	for merchant,each_log in groups:
		diversity = dict()
		for index, record in each_log.iterrows():
			item_id = record['item_id']
			cat_id = record['cat_id']
			brand_id = record['brand_id']

			if not diversity.has_key('items'):
				diversity['items'] = [[] for i in range(8)]
			if not diversity.has_key('brands'):
				diversity['brands'] = [[] for i in range(8)]
			if not diversity.has_key('cats'):
				diversity['cats'] = [[] for i in range(8)]

			month = record['time_stamp']/100 - 5
			diversity['items'][month].append(item_id)
			diversity['brands'][month].append(brand_id)
			diversity['cats'][month].append(cat_id)


		## monthly vector has been created, compute the sum over the whole period
		for each_action in diversity:
			for i in range(7):
				diversity[each_action][-1] += diversity[each_action][i]

		## convert items to number of unique items
		for each_prod in diversity:
			for i in range(8):
				diversity[each_prod][i] = len(set(diversity[each_prod][i]))

		## write this feature to user profile
		merchant_profile[str(merchant)]['diversity'] = diversity
		print "merchant diversity features: {0}".format(diversity)
	# update user profile
	f = open(pre_path + 'merchant.json','w')
	f.write(json.dumps(merchant_profile))
	f.close()


def store_UM_diversity():
	# read user merchant profile
	UM_profile = get_UM_profile()

	# begin to extract monthly action count features
	user_log = pd.read_csv(f_user_log,header  = 0)
	total = len(UM_profile)
	## for each user-merchant pair
	count = 0
	groups =  user_log.groupby(['user_id','merchant_id'])
	for (user_id,merchant_id),each_log in groups:
		start = time.clock()

		diversity = dict()
		for index, record in each_log.iterrows():
			item_id = record['item_id']
			cat_id = record['cat_id']
			brand_id = record['brand_id']

			if not diversity.has_key('items'):
				diversity['items'] = [[] for i in range(8)]
			if not diversity.has_key('brands'):
				diversity['brands'] = [[] for i in range(8)]
			if not diversity.has_key('cats'):
				diversity['cats'] = [[] for i in range(8)]

			month = record['time_stamp']/100 - 5
			diversity['items'][month].append(item_id)
			diversity['brands'][month].append(brand_id)
			diversity['cats'][month].append(cat_id)


		## monthly vector has been created, compute the sum over the whole period
		for each_action in diversity:
			for i in range(7):
				diversity[each_action][-1] += diversity[each_action][i]

		## convert items to number of unique items
		for each_prod in diversity:
			for i in range(8):
				diversity[each_prod][i] = len(set(diversity[each_prod][i]))
		## write this feature to user profile
		UM_profile[str(user_id) + '#' + str(merchant_id)]['diversity'] = diversity

		## log
		elapsed = (time.clock() - start)
		count += 1
		print "diversity of {0} # {1} : {2}".format(user_id,merchant_id,diversity)
		print "finish {0} of {1}, {2}, {3} hours left ".format(count,total, 1.0*count/total*100,elapsed*(total-count)/3600.0 )

	# update user profile
	f = open(pre_path + 'user_merchant.json','w')
	f.write(json.dumps(UM_profile))
	f.close()



if __name__ == '__main__':
	init_user_features()
	init_merchant_features()
	init_UM_features()
	store_user_action_counts()
	store_merchant_action_counts()
	store_UM_action_counts()
	print "begin to store user action ratio:"
	store_user_action_ratio()
	print "begin to store merchant action ratio"
	store_merchant_action_ratio()
	print "begin to store UM action ratio"
	store_UM_action_ratio()
	store_user_day_counts()
	store_merchant_day_counts()
	store_UM_day_counts()