import csv
from tree.test.cart import *

football = open("football.csv", "rb")
f_reader = csv.DictReader(football)
years = ["VII", "VIII", "IX", "X", "XI", "XII", "XIII"]
variables = ["Age", "Att", "YA", "Rec", "YR", "RRTD", "Fmb"]
labels = {0: "Age", 1: "Att", 2: "YA", 3: "Rec", 4: "YR", 5: "RRTD", 6: "Fmb"}
train_dict = {}
test_dict = {}
test_year = "XII"

# Construct a dictionary with entries of the form
# (x1, ..., xd) : y where x1, ..., xd are the parameter values and 
#  y is the response value.
for row in f_reader:
    for i in range(len(years) - 1):
        if row[years[i] + "Att"] == "":
            continue
        dat = []
        for var in variables:
            if row[years[i] + var] == "":
                dat.append(0)
            else:
                dat.append(float(row[years[i] + var]))
        res = row[years[i + 1] + "Fantasy"]
        if res == "":
            res = 0
        if years[i] == test_year:
            test_dict[row["Name"]] = [tuple(dat), float(res)]
        else:
            train_dict[tuple(dat)] = float(res)

# Build tree.
# 6-fold cross validation.
tree = cvt(train_dict, 6, max_depth = 500, Nmin = 5, labels = labels)
tree.display_tree(save = True, filename = "football_tree_new.jpg", view=False)


f = open("football_predictions_new.txt", "wb")
error = []
for i in test_dict:
    predict = tree.lookup(test_dict[i][0])
    act_val = test_dict[i][1]
    f.write(i + "     predicted: " + str(predict) + "    actual: " + str(act_val) + "\n")
    error.append(abs(act_val - predict))
    
f.close()
print numpy.mean(numpy.array(error))
    

        
        
         
    
    
