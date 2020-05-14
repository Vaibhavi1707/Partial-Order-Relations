import itertools as it, os
from sys import argv 

GREATER, LESSER, NOT_COMPARABLE = ">", "<", "#"

def process_marks(marksheet):
    rollnos_marks = {}
    
    for line in open(marksheet):
        records = line.strip().split()
        rollnos_marks[records[0]] = [int(marks) for marks in records[1:]]
    
    return rollnos_marks

def relation_in(mark_list1, mark_list2):
    
    if all(marks1 > marks2 for marks1, marks2 in zip(mark_list1, mark_list2)):
        return GREATER
    
    if all(marks1 < marks2 for marks1, marks2 in zip(mark_list1, mark_list2)):
        return LESSER
    
    return NOT_COMPARABLE

def get_order(students):
    relations = set()

    def get_pairs():
    return it.combinations([student for student in students.keys()], 2)

    for student1, student2 in get_pairs(students):
        relation = relation_in(students[student1], students[student2])
        
        if relation == GREATER:
            relations.add(student1 + student2)
        
        elif relation == LESSER:
            relations.add(student2 + student1)
    
    return relations



def get_removables(relations):

    def get_medium_students():
    return set(relation[0] for relation in relations) & set(relation[1] for relation in relations)

    medium_students = get_medium_students(relations) 
    better = [relation[0] for relation in relations]
    inferior = [relation[1] for relation in relations]
    
    return {better + inferior for relation in relations for medium in medium_students 
        if better + medium in relations and medium + inferior in relations}

def maintain_transitivity(relations):
    return (relations ^ get_removables(relations))

def create_png(final_order):
    with open("vanchi.dot", "w") as dot_file:
        print("digraph vanchi {", file = dot_file)

        for relation in final_order:
            print("\t%s -> %s;" %(relation[0], relation[1]), file=dot_file)
        
        print("}", file=f)

    os.system("dot -T png -o vanchi.png vanchi.dot")

# def find_ranking(final_order):
    # ordered = ''.join(order for order in final_order)
    # 


final_order = maintain_transitivity(get_order(process_marks(argv[1])))
create_png(sorted(final_order))
#print("Final ranking in students is", find_ranking(final_order))