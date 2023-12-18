# Credit: @therealOri - (GitHub)
import beaupy
import os
import json
from termcolor import colored
import ast
import re
from pystyle import Colors, Colorate


dash = 60


def clear():
    os.system("clear||cls")


def banner():
    banner = """


    ████████╗ ██████╗ ██████╗  ██████╗
    ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
       ██║   ██║   ██║██║  ██║██║   ██║
       ██║   ██║   ██║██║  ██║██║   ██║
       ██║   ╚██████╔╝██████╔╝╚██████╔╝
       ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝

    Made by https://github.com/therealOri


"""
    colored_banner = Colorate.Horizontal(Colors.purple_to_blue, banner, 1)
    return colored_banner



# Load tasks from json
with open('tasks.json') as f:
    tasks = json.load(f)




def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)



def add_task():
    global tasks


    task_ids = []
    for task in tasks.keys():
        t_id = re.search(r"Task(\d+)", task)
        if t_id:
            task_ids.append(int(t_id.group(1)))


    next_id = max(task_ids) + 1
    task_id = "Task" + str(next_id)


    last_task = list(tasks)[-1]
    if not list(tasks[last_task])[-1].endswith(','):
        tasks[last_task][list(tasks[last_task])[-1]] += ','

    title = beaupy.prompt(colored("Enter new task title: ", "yellow"))
    if not title:
        clear()
        return

    desc = beaupy.prompt(colored("Enter new task description: ", "green"))
    if not desc:
        clear()
        return

    date = beaupy.prompt(colored("Enter due date (mm-dd-yyyy): ", "red"))
    if not date:
        clear()
        return


    # Create new task
    new_task = {
        f"{task_id}": {
            "Title": title,
            "Description": desc,
            "Due-by-date": date,
            "Completed": "False"
        }
    }

    # Update data with new task
    tasks.update(new_task)
    save_tasks()

    input(colored(f'Todo list has been updated!.\n\nPress "enter" to continue...', 'blue', attrs=['bold']))
    clear()
    return





def remove_task():
    global tasks

    while True:
        print("Existing Tasks:\n")
        for id, task in tasks.items():
            print(f"{id}: {task['Title']} (Completed: {task['Completed']})")

        task_id = beaupy.prompt("\n\nEnter ID of task to remove: ")
        if not task_id:
            clear()
            return
        if task_id in tasks:
            clear()
            tasks.pop(task_id)
            input(f'Removed task {task_id}.\n\nPress "enter" to continue...')
            save_tasks()
            return
        else:
            clear()
            input('Invalid task ID.\n\nPress "enter" to continue...')
            clear()
            continue






def update_tasks():
    global tasks

    msg_list = []
    print("Please select a task or multiple tasks that you would like to modify. (Mark as complete or incomplete)")
    print("-=-" * 40 + "\n")
    for t_id, task_name in tasks.items():
        msg = f'{t_id} | {task_name["Completed"]}'
        msg_list.append(msg)

    t_options = beaupy.select_multiple(msg_list, tick_style="#ed1dd3", cursor_style="#ffa533", tick_character="x")
    if not t_options:
        clear()
        return


    for option in t_options:
        task_id = option.split(' ', 1)[0]
        if task_id in tasks:
            task = tasks[task_id]
            if task["Completed"] == "True":
                task["Completed"] = "False"
            else:
                task["Completed"] = "True"
        else:
            pass

    save_tasks()
    input('Tasks have been update successfully!\n\nPress "enter" to continue...')
    clear()
    return




def show_completed():
    global tasks
    print("Completed Tasks:")
    print(colored("=" * 40 + "\n", "magenta"))

    for task_id, task in tasks.items():
        if task['Completed'] == "True":
            print(f"{task_id}")
            print(colored(f" - Title: {task['Title']}", "blue"))
            print(colored(f" - Description: {task['Description']}", 'green'))
            print(colored(f" - Due Date: {task['Due-by-date']}", "red"))
            print()

    print(colored("=" * 40 + "\n", "magenta"))
    total_completed = len([t for t in tasks.values() if t['Completed'] == "True"])
    input(f"You have completed {total_completed} tasks out of {len(tasks)} total.\n\nPress enter to continue...")
    clear()
    return




def show_incomplete():
    global tasks
    print("Incomplete Tasks:")
    print(colored("=" * 40 + "\n", "magenta"))

    for task_id, task in tasks.items():
        if task['Completed'] == "False":
            print(f"{task_id}")
            print(colored(f" - Title: {task['Title']}", "blue"))
            print(colored(f" - Description: {task['Description']}", 'green'))
            print(colored(f" - Due Date: {task['Due-by-date']}", "red"))
            print()

    print(colored("=" * 40 + "\n", "magenta"))
    total_incomplete = len([t for t in tasks.values() if t['Completed'] == "False"])
    input(f"You have not completed {total_incomplete} tasks out of {len(tasks)} total.\n\nPress enter to continue...")
    clear()
    return




def show_tasks():
    TASKS_PER_PAGE = 3
    global tasks
    num_tasks = len(tasks)
    num_pages = -(-num_tasks//TASKS_PER_PAGE)
    while True:
        #print(colored(f"Total Tasks: {num_tasks}, Pages: {num_pages}", "blue"))
        for page in range(1, num_pages+1):
            print(colored(f"Total Tasks: {num_tasks}, Pages: {num_pages}", "blue"))
            print(colored(f"Page {page}/{num_pages}", "magenta"))
            print(colored('Type "/help" to show more commands.\n', 'yellow'))

            start = (page-1)*TASKS_PER_PAGE
            end = start + TASKS_PER_PAGE

            for i, task in enumerate(list(tasks.keys())[start:end], start=start):
                literal = ast.literal_eval(tasks[task]['Completed'])

                print(colored("=" * 40 + "\n", "magenta"))
                print(colored(f"Title: {tasks[task]['Title']}", "blue"))
                print(colored(f"Description: {tasks[task]['Description']}", 'green'))
                print(colored(f"Due Date: {tasks[task]['Due-by-date']}", "red"))
                print(colored(f"Completed: {literal}\n", "yellow"))


            print(colored("=" * 40 + "\n", "magenta"))
            choice = beaupy.prompt("Menu: (N)ext page (P)revious page (E)xit\nEnter command: ")
            clear()

            if not choice:
                return

            choice = choice.lower()
            if choice == "/help":
                while True:
                    print('Press "ctrl+c" to go back or type "B" to go back.')
                    print(colored("=" * 40 + "\n", "magenta"))
                    print("More Commands;\n\n/show_completed\n/show_incomplete\n/update_tasks\n")
                    print(colored("=" * 40 + "\n", "magenta"))

                    help_cmd = beaupy.prompt("Please enter a command:")
                    if not help_cmd:
                        clear()
                        break
                    if help_cmd.lower() == 'b':
                        clear()
                        break
                    elif help_cmd == "/show_completed":
                        clear()
                        show_completed()
                    elif help_cmd == "/show_incomplete":
                        clear()
                        show_incomplete()
                    elif help_cmd == "/update_tasks":
                        clear()
                        update_tasks()


            if num_pages == 1:
                if choice in {"n","p"}:
                    continue
                elif choice in {"e", "exit"}:
                    return
            else:
                if choice == "n":
                    page += 1
                elif choice == "p":
                    if page > 1:
                        page -= 1
                    else:
                        page = num_pages
                elif choice in {"e", "exit"}:
                    return



def main():
    global tasks

    while True:
        clear()
        options = ['Show TODO list?', 'Add a task?', 'Remove a task?', 'Exit?']


        print(f'{banner()}\n\nWhat would you like to do?\n{"-"*dash}\n')
        option = beaupy.select(options, cursor_style="#ffa533")

        if not option:
            clear()
            quit("Keyboard Interuption Detected!\nGoodbye <3")


        if options[0] in option:
            clear()
            if not tasks:
                pass
            else:
                show_tasks()


        if options[1] in option:
            clear()
            if not tasks:
                clear()
                continue
            else:
                add_task()


        if options[2] in option:
            clear()
            if not tasks:
                clear()
                continue
            else:
                remove_task()

        #exit should always be th elast option in the list.
        if options[-1] in option:
            clear()
            quit("Goodbye! <3")







if __name__ == '__main__':
    clear()
    main()
