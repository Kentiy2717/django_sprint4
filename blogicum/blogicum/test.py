from termcolor import cprint

from blogicum.blog.views import stream_file

count_test = 1

DETAIL_REPORT_ON = True


def write_to_file(message):
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')


def write_to_file_num(count_test):
    with open('logs.txt', 'a', encoding='utf-8') as f:
        f.write(str(count_test) + ') ')


def print_title(message):
    global count_test
    print('_____________________________________________________\n')
    cprint(f'{count_test})', end=' ', color='grey')
    cprint(message, color='yellow', attrs=['underline'])
    write_to_file_num(count_test)
    count_test += 1
    write_to_file(message)


def print_failed_test(message):
    print('')
    cprint(message, on_color='on_red')
    print('')
    write_to_file(message)


def print_error(message):
    cprint(message, color='red')
    write_to_file(message)


def print_passed(message):
    cprint(message, color='green')
    write_to_file(message)


def print_text_grey(message):
    if DETAIL_REPORT_ON is True:
        cprint(message, color='grey')
        write_to_file(message)


def print_text_grey_start(message):
    cprint(message, color='grey')
    write_to_file(message)


def print_text_white(message):
    cprint(message, color='white')
    write_to_file(message)

from time import sleep


print_title('Здравствуйте!')
for i in range(10, 20):
    print_error(f'Приветствую тебя пользователь {i}')
    # sleep(1)
print_passed('Поздаровались!')
