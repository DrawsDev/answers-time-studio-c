import os
import json
import random

VER = "answers-time-studio-c-1-1-0"
UTF8 = "utf-8"
EXIT = ("end", "exit", "quit", "kill")
TRUE = ("yes", "y", "true", "t", "1")
CMDLIST = ("help [..]  -  Print the commands.",
           "end [..]  -  Exit from studio.",
           "test.new [..]  -  Create a new test.",
           "test.load [filename <str>]  -  Load the test from file. (*.json)",
           "test.save [..]  -  Save the test to file. (in the directory of the project)",
           "test.tree [..]  -  Prints the test tree, i.e. title and questions.",
           "test.title [title <str|..>]  -  Set (or print) the test title.",
           "test.qs [..]  -  Print the test questions.",
           "test.selq [index <int|..>]  -  Select a question from the test to edit. Or print the selected question number.",
           "test.newq [..]  -  Create a new question.",
           "test.remq [index <int>]  -  Remove the selected question from the test.",
           "q.title [title <str|..>]  -  Set (or print) the question title.",
           "q.d [duration <int|..>]  -  Set (or print) the question duration (in seconds).",
           "q.input [enabled <bool|..>]  -  Set (or print) the question inputtable.",
           "q.expl [explain <str|..>]  -  Set (or print) the question explain.",
           "q.as [..]  -  Print the question answers.",
           "q.rema [index <int>]  -  Remove the selected question answer.",
           "q.newa [correct_incorrect <bool>] [answer <str>]  -  Create a new answer for question.",
           "q.tree [..]  -  Print the question tree, i.e. title and answers.")

print(VER)

cmdbar = ""
test = None
selq = 0


def str2bool(value: str) -> bool:
    return value.lower() in TRUE


def no_questions() -> bool:
    result = (test is None or len(test.get("questions", [])) <= 0)
    if result: print("error: questions don't exist.")
    return result


def in_range_questions(index) -> bool:
    return (test is not None and 0 <= index <= len(test.get("questions", [])) - 1)


def load_test_file(filename: str | list[str]) -> dict:
    path = f"./{' '.join(filename)}.json"
    if os.path.exists(path):
        with open(path, "r", encoding=UTF8) as file:
            return json.load(file)
    return {}


def save_test_file() -> str:
    name = random.randint(0, 99999999)
    with open(f"{name}.json", "w", encoding=UTF8) as file:
        json.dump(test, file)
    return name


def new_q(**params) -> dict:
    title = params.get("title")
    answers = params.get("answers")
    duration = params.get("duration")
    explain = params.get("explain")
    inputtable = params.get("inputtable")
    return {
        "title": title if isinstance(title, str) else "question",
        "answers": answers if isinstance(answers, dict) else {"right": [], "wrong": []},
        "duration": duration if isinstance(duration, int) else 60,
        "explain": explain if isinstance(explain, str) else "explain",
        "inputtable": inputtable if isinstance(inputtable, bool) else False
    }


def new_test(**params) -> dict:
    title = params.get("title")
    questions = params.get("questions")
    return {
        "title": title if isinstance(title, str) else "new_test",
        "questions": questions if isinstance(questions, list) else []
    }
test = new_test()


def output_test_tree() -> None:
    print(test["title"], "\n")
    for index in range(len(test["questions"])):
        output_question_tree(index)
        print("")


def output_question_tree(index: int) -> None:
    if no_questions(): return
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

        case "help":
            for cmd in CMDLIST: print(cmd)

        case "test.load" if len(params) >= 2:
            source = load_test_file(params[1:])

            if source == {}:
                return print("file doesn't exists.")

            loaded_test = new_test(**{"title": source.get("title")})

            for q in source.get("questions", {}):
                loaded_test["questions"].append(new_q(**{
                    "title": q.get("title"), "answers": q.get("answers"),
                    "duration": q.get("duration"), "explain": q.get("explain"),
                    "inputtable": q.get("inputtable")}))

            global test
            test = loaded_test

        case "test.save":
            filename = save_test_file()
            print(f"saved as './{filename}.json'.")

        case "test.title" if len(params) >= 2:
            new_title = " ".join(params[1:])
            test["title"] = new_title
            print(f"new test title: {new_title!r}.")

        case "test.title":
            print(test["title"])

        case "test.qs":
            if no_questions(): return
            for i, q in enumerate(test["questions"]):
                title = q["title"]
                print(f"#{i+1} > {title}")

        case "test.selq" if len(params) == 2:
            if no_questions(): return
            index = int(params[1]) - 1 if params[1].isdigit() else -1
            if in_range_questions(index):
                global selq
                selq = index
                print(f"question #{selq+1} selected.")
        
        case "test.selq":
            print(f"question #{selq+1}")

        case "test.remq" if len(params) == 2:
            if no_questions(): return
            index = int(params[1]) - 1 if params[1].isdigit() else -1
            if in_range_questions(index):
                test["questions"].pop(index)
                print(f"question #{index+1} has been removed.")
            else:
                print("error: index out of range.")

        case "test.newq":
            test["questions"].append(new_q())
            print("new question added.")

        case "test.tree":
            output_test_tree()
        
        case "test.new":
            print("create a new test? (the current one won't be saved)")
            if str2bool(input("[y/n] >> ")): 
                test = new_test()
                print("new test created.")

        case "q.title" if len(params) >= 2:
            if no_questions(): return
            new_title = " ".join(params[1:])
            test["questions"][selq]["title"] = new_title
            print(f"new question title: {new_title!r}.")

        case "q.title":
            if no_questions(): return
            print(test["questions"][selq]["title"])
        
        case "q.d" if len(params) == 2:
            if no_questions(): return
            if params[1].isdigit():
                test["questions"][selq]["duration"] = int(params[1])
                print(f"new question duration: {params[1]} sec.")
        
        case "q.d":
            if no_questions(): return
            print(test["questions"][selq]["duration"], "sec.")

        case "q.input" if len(params) == 2:
            if no_questions(): return
            if str2bool(params[1]):
                test["questions"][selq]["inputtable"] = True
                print("question requires input.")
            else:
                test["questions"][selq]["inputtable"] = False
                print("question doesn't require input.")
        
        case "q.input":
            if no_questions(): return
            print(test["questions"][selq]["inputtable"])
        
        case "q.expl" if len(params) >= 2:
            if no_questions(): return
            new_explain = " ".join(params[1:])
            test["questions"][selq]["explain"] = new_explain
            print(f"new question explain: {new_explain!r}.")

        case "q.expl":
            if no_questions(): return
            print(test["questions"][selq]["explain"])

        case "q.as":
            answers = test["questions"][selq]["answers"]
            for i in answers["right"]: print(f"{i} (right)")
            for i in answers["wrong"]: print(f"{i}")
        
        case "q.rema" if len(params) == 2:
            if no_questions(): return
            
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
                    print(f"answer {needrem!r} has been removed.")

        case "q.newa" if len(params) >= 3:
            if no_questions(): return
            if len(test["questions"][selq]["answers"]["right"] + test["questions"][selq]["answers"]["wrong"]) == 4:
                return print("error: number of answers out of range (> 4).")
            test["questions"][selq]["answers"]["right" if str2bool(params[1]) else "wrong"].append(" ".join(params[2:]))
            print("new answer added.")

        case "q.tree":
            output_question_tree(selq)


while not cmdbar.lower() in EXIT:
    cmdbar = input("\n >> ")

    handle_command(cmdbar.split(" "))
