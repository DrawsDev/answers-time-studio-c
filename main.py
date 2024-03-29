import os
import json
import random

print("answers-time-studio-c-1-0-0")

input_line = ""
test = None
selq = 0 

def new_q(**params) -> dict:
    return {
        "title": params.get("title", "question"),
        "answers": params.get("answers", {"right": ["y"], "wrong": ["n"]}),
        "duration": params.get("duration", 60),
        "explain": params.get("explain", "explain"),
        "inputtable": params.get("inputtable", False)
    }

def new_test(**params) -> dict:
    return {
        "title": params.get("title", "NewTest"),
        "questions": params.get("questions", [new_q()])
    }
test = new_test()

def str2bool(value: str) -> bool:
    return value.lower() in ["yes", "y", "true", "t", "1"]

def test_tree() -> None:
    title = test["title"]
    print(f"{title}\n")
    for index in range(len(test["questions"])):
        q_tree(index)
        print("")

def q_tree(index: int) -> None:
    question = test["questions"][index]
    title = question["title"]
    answers = question["answers"]
    right, wrong = answers["right"], answers["wrong"]
    if question["inputtable"]:
        print(f"Question {index + 1} (input) - {title}")
        for i in right: print(f"- {i} (right)")
    else:
        print(f"Question {index + 1} - {title}")
        for i in right: print(f"- {i} (right)")
        for i in wrong: print(f"- {i}")

def handle_command(params: list) -> None:
    match params[0]:
        case "dev":
            print("yes")

        case "test.load" if len(params) >= 2:
            path = f"./{' '.join(params[1:])}.json"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    test_title = data.get("title", "NewTest")
                    test_questions = data.get("questions", [])

                    loaded_test = {
                        "title": test_title,
                        "questions": []
                    }

                    for question in test_questions:
                        loaded_test["questions"].append({
                            "title": question.get("title", "question"),
                            "answers": question.get("answers", {"right": [], "wrong": []}),
                            "duration": question.get("duration", 60),
                            "explain": question.get("explain", "explain"),
                            "inputtable": question.get("inputtable", False)
                        })

                    global test
                    test = loaded_test
            else:
                print("file doesn't exists.")

        case "test.save":
            name = random.randint(0, 99999999)
            with open(f"{name}.json", "w", encoding="utf-8") as file:
                json.dump(test, file,)
            print(f"saved as ' ./{name}.json '")

        case "test.title" if len(params) >= 2:
            test["title"] = " ".join(params[1:])
            print("new test title is '", test["title"], "'")

        case "test.title" if len(params) == 1:
            print(test["title"])
        
        case "test.qs" if len(params) == 1:
            for i, q in enumerate(test["questions"]):
                print(i+1, "|", q["title"])
            if len(test["questions"]) <= 0:
                print("empty")

        case "test.selq" if len(params) == 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            if params[1].isdigit():
                if 0 <= int(params[1]) - 1 <= len(test["questions"]) - 1:
                    global selq
                    selq = int(params[1]) - 1
                    print("selected question #", selq + 1)

        case "test.remq" if len(params) == 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            if params[1].isdigit():
                if 0 <= int(params[1]) - 1 <= len(test["questions"]) - 1:
                    test["questions"].pop(int(params[1]) - 1)
                    print("question #", int(params[1]), "has been removed.")

        case "test.newq":
            print("new question added")
            test["questions"].append(new_q())

        case "test.tree":
            test_tree()
        
        case "test.new":
            print("create a new test? (the current one won't be saved)")
            if str2bool(input("[y/n] >> ")): 
                print("new test created.")
                test = new_test()

        case "q.title" if len(params) >= 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            test["questions"][selq]["title"] = " ".join(params[1:])
            print("new question title is '", test["questions"][selq]["title"], "'")

        case "q.title" if len(params) == 1:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            print(test["questions"][selq]["title"])
        
        case "q.d" if len(params) == 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            if params[1].isdigit():
                test["questions"][selq]["duration"] = int(params[1])
                print("new question duration is", int(params[1]), "sec")
        
        case "q.d" if len(params) == 1:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            print(test["questions"][selq]["duration"])

        case "q.input" if len(params) == 1:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            print(test["questions"][selq]["inputtable"])
        
        case "q.input" if len(params) == 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            if str2bool(params[1]):
                test["questions"][selq]["inputtable"] = True
                print("question requires input")
            else:
                test["questions"][selq]["inputtable"] = False
                print("question doesn't require input")

        case "q.expl" if len(params) >= 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            test["questions"][selq]["explain"] = " ".join(params[1:])
            print("new question explain is '", test["questions"][selq]["explain"], "'")

        case "q.expl" if len(params) == 1:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            print(test["questions"][selq]["explain"])

        case "q.as":
            answers = test["questions"][selq]["answers"]
            for i in answers["right"]:
                print(f"{i} +")
            for i in answers["wrong"]:
                print(f"{i}")
        
        case "q.rema" if len(params) == 2:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            
            answers = test["questions"][selq]["answers"]
            right = answers["right"]
            wrong = answers["wrong"]
            right_wrong = right + wrong

            if params[1].isdigit():
                index = int(params[1]) - 1
                if 0 <= index <= len(right_wrong) - 1:
                    needrem = right_wrong[index]
                    if needrem in right:
                        right.remove(needrem)
                    elif needrem in wrong:
                        wrong.remove(needrem)
                    print(f"answer ' {needrem} ' has been removed")

        case "q.newa" if len(params) >= 3:
            if len(test["questions"]) <= 0: 
                print("questions don't exists.")
                return
            if len(test["questions"][selq]["answers"]["right"] + test["questions"][selq]["answers"]["wrong"]) == 4:
                print("too many answers.")
                return
            test["questions"][selq]["answers"]["right" if str2bool(params[1]) else "wrong"].append(" ".join(params[2:]))
            print("new answer added")

        case "q.tree":
            q_tree(selq)
        
while input_line != "end":
    input_line = input("\n >> ")

    handle_command(input_line.split(" "))
