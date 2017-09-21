from collections import Counter, defaultdict

doc_1 = ['Madam', 'I', 'I', 'am', 'Adam']
doc_2 = ['Adam', 'love', 'Madam']
doc_3 = ['I', 'am', 'banana']

collection = [doc_1, doc_2, doc_3]

def reverse_id(collection):
    
    dic = defaultdict(set) # wont create key duplicates
    
    for i, doc in enumerate(collection):

        for item in doc:
            dic[item].add(i)

    return dic

print(reverse_id(collection))

