import os
import subprocess

executed_commands = set()

def execute_commands_from_file(file_path):
    global executed_commands
    with open(file_path, 'r') as file:
        content = file.read()
        local_vars = {}
        exec(content, {}, local_vars)
        if 'CMDS' in local_vars:
            for cmd in local_vars['CMDS']:
                if cmd not in executed_commands:
                    try:
                        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                        print(result.stdout.strip())
                        executed_commands.add(cmd)
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing command '{cmd}': {e}")
                else:
                    print(f"команда \"{cmd}\" уже выполнялась")

def main():
    files_with_cmds = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'test.py':
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    local_vars = {}
                    exec(content, {}, local_vars)
                    if 'CMDS' in local_vars:
                        files_with_cmds.append((file_path, local_vars['CMDS']))

    files_with_cmds.sort(key=lambda x: (-x[0].count(os.sep), x[0]))

    for file_path, _ in files_with_cmds:
        execute_commands_from_file(file_path)

if __name__ == "__main__":
    main()