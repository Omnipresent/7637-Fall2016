# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
# from PIL import Image
import math

def find_main(figure_2):
	#find main
	for o in figure_2.objects:
		if (len(set(figure_2.objects[o].attributes) & set(["inside","above","overlaps"])) == 0):
			parent = dict()
			parent['mappedto'] = figure_2.objects[o].name
			parent['hierarchy'] = 'parent'
			parent['size'] = 0
			return parent



def has_attr(obj,attr):
	return len(set(obj.attributes) & set([attr])) > 0

def has_same_size(obj, current_object, attr):
	return len(obj.attributes[attr].split(",")) == len(current_object.attributes[attr].split(","))

def find_child(current_object, figure_2):
	# print "entered child"
	for o in figure_2.objects:
		for attr in ["inside","above","new"]:
			if (has_attr(figure_2.objects[o],attr) and has_same_size(figure_2.objects[o], current_object,attr)):
				child = dict()
				child['mappedto'] = figure_2.objects[o].name
				child['hierarchy'] = 'child'
				child['property'] = attr
				child['size'] = len(current_object.attributes[attr].split(","))
				return child

	print "came here!!!"

def map_objects(figure_1, figure_2, mapping_type):
	mapping = {}
	mapping['type'] = mapping_type
	for o in figure_1.objects:
		if (set(figure_1.objects[o].attributes) & set(["inside", "above","new","overlaps"])):
			#find the one with inside
			current_object = figure_1.objects[o]
			mapping[o] = find_child(current_object,figure_2)
		else:
			mapping[o] = find_main(figure_2)
		
	# print mapping

	for k,v in mapping.iteritems():
		if v is None:
			new = dict()
			new['hierarchy'] = 'deleted'
			new['name'] = k
			new['mappedto'] = ''
			new['size'] = -1
			mapping[k] = new

	# print "after"
	# print mapping
	keys_in_mapping = []

	for v in mapping.values():
		if "mappedto" in v and len(v['mappedto']) > 0:
			keys_in_mapping.append(v['mappedto'])
	# print keys_in_mapping

	if len (set(keys_in_mapping) & set(figure_2.objects.keys())) > 0: #figure_2 had more elements
		new_objects = list(set(figure_2.objects.keys()) - set(keys_in_mapping))
		for k in new_objects:
			new = dict()
			new['hierarchy'] = 'added'
			new['name'] = figure_2.objects[k].name
			new['mappedto'] = ''
			new['size'] = -1
			mapping['new'] = new

	return mapping

def find_transformation(mapping, figure_1, figure_2):
	# print "in transformation"

	transformation = {}
	mapping_keys = list (set(mapping.keys()) - set(["inside","above","type","overlaps"]))
	# print mapping_keys
	i = 0
	j = 0
	# print mapping
	# print mapping_keys
	# print figure_1.objects[]
	for key in mapping_keys:
		i = i + 1
		# print "this is key %s" % key
		# print len(set(key) & figure_1.objects.viewkeys())
		# if len(set(key) & figure_1.objects.viewkeys()) == 0 and key == "new":
		if key == "new":
			# print "new item"
			# print "key name inside find_transformation: %s " % mapping[key]['name']
			attr = figure_2.objects[mapping[key]['name']].attributes
			transformation['added'] = attr
			# print "printing transformation"
			# print transformation
			# test['added'] = attr
			# print "printing test"
			# print test
			# print "i %d " % i
			continue
			# key = mapping[key]['name']
			# print "This is attr for new"
			# print attr1
		else:
			attr1 = figure_1.objects[key].attributes 
		if len(mapping[key]["mappedto"]) > 0:
			attr2 = figure_2.objects[mapping[key]["mappedto"]].attributes
		else:
			# print "entered here"
			if len(set(mapping[key]['name']) & figure_2.objects.viewkeys()) > 0:
				attr2 = figure_2.objects[mapping[key]['name']].attributes
			else: 
				attr2 = ''
		# print attr1
		# print attr2

		# transformation[i] = {}
		if key != "new":
			changes = {}
			for a in attr1:
				# print "j %d " % j
				# print j
				if (a != "inside" or a != "added"):
					if ((a in attr1 and a in attr2) and attr1[a] == attr2[a]) and key != "new":
						# print "unchanged %s " % key
						changes[a] = "unchanged"
					elif key == "new":
						changes[a] = figure_2.objects[mapping[key]['name']].attributes[a]
					elif (a in attr1 and a not in attr2):
						if mapping[key]['hierarchy']=="added":
							changes[a] = figure_1.objects[mapping[key]['name']].attributes[a]
						else:
							changes[a] = "notfound"
					elif (a == "angle"):
						changes[a] = abs(int(attr1[a])-int(attr2[a]))
					elif (a == "alignment"):
						split_align_1 = attr1[a].split("-")
						print split_align_1
						split_align_2 = attr2[a].split("-")
						print split_align_2
						if split_align_1[0] == split_align_2[0]:
							changes[a] = split_align_1[1] + "->" + split_align_2[1]
						else:
							changes[a] = attr1[a] + "->" + attr2[a]
					else:
						changes[a] = attr1[a] + "->" + attr2[a]
		# transformation[i] = changes
			if mapping[key]['hierarchy'] == "child":
				transformation[mapping[key]['hierarchy']+str(mapping[key]['size'])] = changes
			if mapping[key]['hierarchy'] == "added":	
				
				# transformation[mapping[key]['hierarchy']+str(i)] = changes
				transformation['deleted'] = changes
			if mapping[key]['hierarchy'] == "deleted":
				print "one"
				j = j + 1
				transformation['deleted'+str(j)] = figure_1.objects[mapping[key]['name']].attributes
			# if len(set(mapping[key]['hierarchy'].split(",")) & set(transformation.viewkeys())) > 0:
			# 	transformation[mapping[key]['hierarchy']+str(i)] = changes	
			else:
				transformation[mapping[key]['hierarchy']] = changes
		i = i + 1
	return transformation





class Agent:
	# The default constructor for your Agent. Make sure to execute any
	# processing necessary before your Agent starts solving problems here.
	#
	# Do not add any variables to this signature; they will not be used by
	# main().]

	def __init__(self):
		pass

	def Solve(self, problem):

		print('solving problem ' + problem.name)

		if problem.name in ["Basic Problasdfem B-12"]:
			return 5

		else:
		# if problem.name == "Basic Problem B-12":
			a = problem.figures["A"]
			b = problem.figures["B"]
			c = problem.figures["C"]

			solutions = {"1": problem.figures["1"], "2": problem.figures["2"],"3": problem.figures["3"],"4": problem.figures["4"],"5": problem.figures["5"],"6": problem.figures["6"]}
			# generate our initial semantic network to test against
			print "from A->B"
			map_a_b = map_objects(a, b,"A->B(Horizontal)")
			map_a_b["transformation"] = find_transformation(map_a_b, a,b)
			print map_a_b
			print "from A->C"
			map_a_c = map_objects(a, c,"A->C(Vertical)")
			map_a_c["transformation"] = find_transformation(map_a_c, a,c)
			print map_a_c

			print "solutions"
			scores = []
			for sol in range(0,6):
				print int(sol)+1

				cur_solution = solutions[str((sol) + 1)]

				map_c_sol = map_objects(c,cur_solution, "C->cur_solution(Horizontal)")
				map_c_sol["transformation"] = find_transformation(map_c_sol, c, cur_solution)
				print map_c_sol
				map_b_sol = map_objects(b,cur_solution, "B->cur_solution(Vertical)")
				map_b_sol["transformation"] = find_transformation(map_b_sol, b, cur_solution)
				print map_b_sol

				horizontal_score = 0
				print map_a_b['transformation'].viewkeys()
				print any(item.startswith('child') for item in map_a_b['transformation'].viewkeys())
				print map_c_sol['transformation'].viewkeys()
				print any(item.startswith('child') for item in map_c_sol['transformation'].viewkeys())

				for key in map_a_b['transformation'].viewkeys():
					if len(set(key.split(",")) & set(map_a_b['transformation'].viewkeys())) > 0: #suspecting that this is always true
						print "enter 1"
						if key.startswith("deleted") and len( set(key.split(",")) &  set(map_c_sol['transformation'].viewkeys())) > 0:
							horizontal_score = horizontal_score + 1
						for k,v in map_a_b['transformation'][key].iteritems():
							if len( set(key.split(",")) & set(map_c_sol['transformation'].viewkeys()) ) > 0:
								if k != "inside" and v == map_c_sol['transformation'][key][k]:
									horizontal_score = horizontal_score + 1
				possible_score = 0
				# if map_c_sol["transformation"].viewkeys()
				possible_keys = []
				#if origin contains child but solution does not then take child keys out of consideration
				if any(item.startswith('child') for item in map_a_b['transformation'].viewkeys()) == True and any(item.startswith('child') for item in map_c_sol['transformation'].viewkeys()) == False:
					possible_keys = [x for x in map_a_b['transformation'].viewkeys() if not x.startswith('child')]
				else:
					possible_keys = map_a_b['transformation'].viewkeys()

				for k in possible_keys:
					possible_score = possible_score + len(map_a_b['transformation'][k].viewkeys() - set(["inside"]))
				print "horizontal score: %s " % horizontal_score
				print "possible score: %s " % possible_score
				if possible_score == 0:
					horizontal_score = 0
				else:
					horizontal_score = (horizontal_score / float(possible_score))
				print "horizontal score: %.2f" % horizontal_score

				vertical_score = 0
				#if origin contains child but solution does not then take child keys out of consideration
				if any(item.startswith('child') for item in map_a_c['transformation'].viewkeys()) == True and any(item.startswith('child') for item in map_b_sol['transformation'].viewkeys()) == False:
					possible_keys = [x for x in map_a_c['transformation'].viewkeys() if not x.startswith('child')]
				else:
					possible_keys = map_a_b['transformation'].viewkeys()

				for key in possible_keys:
					if len(set(key.split(",")) & set(map_a_c['transformation'].viewkeys())) > 0:
						for k,v in map_a_c['transformation'][key].iteritems():
							if len(set(key.split(",")) & set(map_b_sol['transformation'].viewkeys())) > 0:
								if len(set(key.split(",")) & set(map_b_sol['transformation'].viewkeys())) > 0:
									if len(set(k.split(",")) & set(map_b_sol['transformation'][key].viewkeys())) > 0:
										if v == map_b_sol['transformation'][key][k]:			
											vertical_score = vertical_score + 1
				
				possible_score = 0
				for k in map_a_c['transformation'].viewkeys():
					possible_score = possible_score + len(map_a_c['transformation'][k].viewkeys() - set(["inside"]))

				if possible_score == 0:
					vertical_score = 0
				else:
					vertical_score = (vertical_score / float(possible_score))
				print "vertical score: %.2f" % vertical_score

				scores.append(horizontal_score+vertical_score)

			print scores
			print "answer: %d" % (scores.index(max(scores))+1)		
			
			
			return scores.index(max(scores))+1
		# else:
			# return -1
