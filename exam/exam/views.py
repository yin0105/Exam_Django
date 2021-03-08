from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import random, os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

problem_list = []
problem_list_2 = []
current_q_number = 0
q_count = int(os.environ.get('QUESTIONS_COUNT'))
correct_number = 0

def index(request):
    global problem_list, problem_list_2, q_count, current_q_number

    problem_list.clear()
    problem_list_2.clear()

    data_file = os.environ.get('DATA_FILE')
    f = open(data_file, "r")
    
    problem = {}
    options = []
    q = ""

    for row in f.readlines():
        row = row[:-1]
        
        if q != "":
            if row.strip() == "":
                problem["q"] = q
                q = ""
            else :
                q += row
                continue
        
        head = row.split(":")
        if len(head) == 1: continue
        if head[0].strip() == "Q":
            problem.clear()
            options.clear()
            # problem["q"] = row
            q = row
        elif head[0].strip() == "A":
            problem["a"] = head[1].strip()
            problem["o"] = options[:]
            problem_list.append(problem.copy())
        else:
            print(row)
            options.append(head[1].strip())
            print("OPtion")
            print(options)

    # for row in f.readlines():
    #     if row.strip() == "": continue
    #     row = row[:-1]
    #     head = row.split(":")
    #     if len(head) == 1: continue
    #     if head[0].strip() == "Q":
    #         problem.clear()
    #         options.clear()
    #         problem["q"] = row
    #     elif head[0].strip() == "A":
    #         problem["a"] = head[1].strip()
    #         problem["o"] = options[:]
    #         problem_list.append(problem.copy())
    #     else:
    #         print(row)
    #         options.append(head[1].strip())
    #         print("OPtion")
    #         print(options)
    
    
    problem_list_2 = problem_list[:]
    print(len(problem_list))
    print(problem_list)
    print(len(problem_list_2))
    print(problem_list_2)
    
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
    global problem_list, problem_list_2, current_q_number, correct_number, q_count
    context = {}

    if "correct" in request.GET:
        correct_number += int(request.GET["correct"])
    else:
        current_q_number = 0
        problem_list_2 = problem_list[:]
        correct_number = 0
    
    current_q_number += 1
    if current_q_number > q_count:
        context["total"] = q_count
        context["correct"] = correct_number
        context["score"] = "{:.2f}".format(correct_number/q_count*5)
        html_template = loader.get_template( 'evaluate.html' )
        return HttpResponse(html_template.render(context, request))
    n = random.randint(0, len(problem_list_2)-1)
    print(str(n) + " : " + str(len(problem_list_2)))

    
    context["q"] = problem_list_2[n]["q"]
    context["a"] = problem_list_2[n]["a"]
    context["o"] = problem_list_2[n]["o"]
    del problem_list_2[n]
    print("len = " + str(len(problem_list_2)))
    print(problem_list_2)
    if current_q_number < q_count:
        context["btn_name"] = "Next"
    else:
        context["btn_name"] = "Finish"
    print("cur = " + str(current_q_number))
    print(context["o"])

    context["total"] = q_count
    context["cur"] = current_q_number
    html_template = loader.get_template( 'exam.html' )
    return HttpResponse(html_template.render(context, request))    


    

