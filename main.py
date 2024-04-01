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
           "q.newa [correct <bool>] [answer <str>]  -  Create a new answer for question.",
           "q.repa [index <int>] [correct <bool>] [text <str>]  -  Overwrite the selected answer.",
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
    return in_range(index, 0, len(test.get("questions", [])) - 1)


def in_range(index: int, min_index: int, max_index: int) -> bool:
    result = min_index <= index <= max_index
    if not result: print("error: index out of range.")
    return result


def get_answers() -> tuple[list, list]:
    """Return a right and wrong answers"""
    answers = test["questions"][selq]["answers"]
    right = answers["right"]
    wrong = answers["wrong"]
    return right, wrong


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


def remove_answer(index: int) -> None:
    if no_questions(): return
    right, wrong = get_answers()
    merge = right + wrong
    if in_range(index, 0, len(merge) - 1):
        target = merge[index]
        if target in right: right.remove(target)
        elif target in wrong: wrong.remove(target)
        print(f"answer {target!r} has been removed.")


def append_answer(correct: bool, text: str) -> None:
    if no_questions(): return
    right, wrong = get_answers()

    if len(right + wrong) >= 4:
        return print("error: number of answers out of range (> 4).")
    
    right.append(text) if correct else wrong.append(text)    
    print("new answer added.")


def handle_command(params: list) -> None:
    global test
    match params[0]:
        case "dev":
            print("yes")

        case "help":
            for cmd in CMDLIST: print(cmd)

        case "test.new":
            print("create a new test? (the current one won't be saved)")
            if str2bool(input("[y/n] >> ")):
                test = new_test()
                print("new test created.")

        case "test.load" if len(params) >= 2:
            source = load_test_file(params[1:])

            if source == {}:
                return print("file doesn't exists.")

            test = new_test(**{"title": source.get("title")})

            for q in source.get("questions", {}):
                test["questions"].append(new_q(**{
                    "title": q.get("title"), "answers": q.get("answers"),
                    "duration": q.get("duration"), "explain": q.get("explain"),
                    "inputtable": q.get("inputtable")}))

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
            if no_questions(): return
            right, wrong = get_answers()
            for i in right: print(f"{i} (right)")
            for i in wrong: print(f"{i}")
        
        case "q.rema" if len(params) == 2:
            index = int(params[1]) - 1 if params[1].isdigit() else -1
            remove_answer(index)
            
        case "q.newa" if len(params) >= 3:
            correct = str2bool(params[1])
            text = " ".join(params[2:])
            append_answer(correct, text)
        
        case "q.repa" if len(params) >= 4:
            index = int(params[1]) - 1 if params[1].isdigit() else -1
            correct = str2bool(params[2])
            text = " ".join(params[3:])
            remove_answer(index)
            append_answer(correct, text)

        case "q.tree":
            output_question_tree(selq)


while not cmdbar.lower() in EXIT:
    cmdbar = input("\n >> ")

    handle_command(cmdbar.split(" "))
