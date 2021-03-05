from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import random

# @login_required(login_url="/login/")
problem_list = []
problem_list_2 = []
current_q_number = 0
q_count = 0

def index(request):
    global problem_list, problem_list_2, q_count, current_q_number

    problem_list.clear()
    problem_list_2.clear()

    data_file = "example.txt"
    q_count = 2
    f = open(data_file, "r")
    
    problem = {}
    options = []
    for row in f.readlines():
        if row.strip() == "": continue
        row = row[:-1]
        head = row.split(":")
        if len(head) == 1: continue
        if head[0].strip() == "Q":
            problem.clear()
            options.clear()
            problem["q"] = row
        elif head[0].strip() == "A":
            problem["a"] = head[1].strip()
            problem["o"] = options
            problem_list.append(problem)
        else:
            print(row)
            options.append(head[1].strip())
    
    
    problem_list_2 = problem_list[:]
    print(len(problem_list))
    print(len(problem_list_2))
    
    context = {}
    context["data_file"] = data_file
    context["total_q_count"] = len(problem_list)
    context["q_count"] = q_count
    context["p_list"] = problem_list
    current_q_number = 0
    print("cur = " + str(current_q_number))
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


def exam(request):
    global problem_list_2, current_q_number
    
    n = random.randint(0, len(problem_list_2)-1)
    current_q_number += 1
    print(str(n) + " : " + str(len(problem_list_2)))

    context = {}
    context["q"] = problem_list_2[n]["q"]
    context["a"] = problem_list_2[n]["a"]
    context["o"] = problem_list_2[n]["o"]
    if current_q_number < q_count:
        context["btn_name"] = "Next"
    else:
        context["btn_name"] = "Finish"
    print("cur = " + str(current_q_number))
    html_template = loader.get_template( 'exam.html' )
    return HttpResponse(html_template.render(context, request))    


    

