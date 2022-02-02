from ast import arg


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def change_priority(self, last_number, priority):
        if last_number == priority - 1:
            return True
        self.current_items[last_number + 1] = self.current_items.pop(last_number)
        self.change_priority((last_number - 1), priority)

    def add(self, args):
        if len(args) == 2:
            priority = int(args[0])
            while priority in self.current_items.keys():
                priority += 1
            last_consecutive_number = priority - 1
            if len(self.current_items) != 0:
                self.change_priority(last_consecutive_number, int(args[0]))
            self.current_items[int(args[0])] = args[1]
            self.write_current()
            print(f'Added task: "{args[1]}" with priority {args[0]}')
        else:
            print("Missing arguments see help")

    def done(self, args):
        priority = int(args[0])
        if priority in self.current_items.keys():
            completed_task = self.current_items.pop(priority)
            self.completed_items.append(completed_task)
            self.write_completed()
            self.write_current()
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        if priority in self.current_items.keys():
            self.current_items.pop(priority)
            self.write_current()
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted."
            )

    def ls(self):
        for index, item in enumerate(sorted(self.current_items.keys())):
            print(f"{index+1}. {self.current_items[item]} [{item}]")

    def report(self):
        print(f"Pending : {len(self.current_items)}")
        self.ls()
        print()
        print(f"Completed : {len(self.completed_items)}")
        for index, item in enumerate(self.completed_items):
            print(f"{index+1}. {item}")
