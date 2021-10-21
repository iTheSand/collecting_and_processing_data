# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
import requests
import json


def repos_for_user():
    while True:
        print(
            'Команды:\n'
            'exit - выход из программы;\n'
            'repo - получить список публичных репозиториев пользователя')
        command = input('')
        if command == 'repo':
            username = input('Введите имя пользователя GitHub: ')
            repos = requests.get(f'https://api.github.com/users/{username}/repos')
            with open(f'lesson_1_hw_1_{username}.json', 'w') as file:
                print(f'Список репозиториев пользователя {username}: ')
                for rep in repos.json():
                    print(rep['html_url'])
                json.dump(repos.json(), file, skipkeys=True, sort_keys=True, indent=4)
                print(f"JSON-вывод записан в файл - 'lesson_1_hw_1_{username}.json'")
                continue
        elif command == 'exit':
            print('До свидания!')
            break
        else:
            print('Введите корректную команду!')


if __name__ == '__main__':
    repos_for_user()
