tasks = []

while True:
    print("\nTo-Do List Menu:")
    print("1. View tasks")
    print("2. Add task")
    print("3. Remove task")
    print("4. Quit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        if len(tasks) == 0:
            print("Your to-do list is empty!")
        else:
            print("Your tasks:")
            for i in range(len(tasks)):
                print(f"{i + 1}. {tasks[i]}")

    elif choice == "2":
        task = input("Enter a new task: ")
        tasks.append(task)
        print("Task added!")

    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks to remove.")
        else:
            print("Tasks:")
            for i in range(len(tasks)):
                print(f"{i + 1}. {tasks[i]}")
            task_num = input("Enter task number to remove: ")
            if task_num.isdigit():
                task_index = int(task_num) - 1
                if 0 <= task_index < len(tasks):
                    removed = tasks.pop(task_index)
                    print(f"Removed task: {removed}")
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid number.")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Please enter 1, 2, 3 or 4.")
