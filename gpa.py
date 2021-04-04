import matplotlib.pyplot as plt
import math as m
from msvcrt import getch


from py_librus_api import Librus
from tkinter import filedialog
from tkinter import Tk
from textwrap import wrap
from matplotlib import rcParams
from time import sleep


def get_login_data():
    Tk().withdraw()
    file_path = filedialog.askopenfilename()

    if not file_path:
        exit()

    with open(file_path, 'r') as file:
        data = file.readlines()
    data = [i.strip() for i in data]
    return data

def login(login, password):
    librus = Librus()
    for i in range(10):
        if not librus.login(login, password):
            continue
        else:
            print("Logged in successfully!")
    if not librus.logged_in:

        print('Login Failed!')
        print('Press Any Key To Exit...')
        getch()
        exit()

    return librus

def grades(librus):
    values = {'1' : 1., '1+' : 1.5,
              '2-' : 1.75, '2' : 2., '2+' : 2.5,
              '3-' : 2.75, '3' : 3., '3+' : 3.5,
              '4-' : 3.75, '4' : 4., '4+' : 4.5,
              '5-' : 4.75, '5' : 5., '5+' : 5.5,
              '6-' : 5.75, '6' : 6.,
               }

    _subj = ['Fizyka',
            'Historia i społeczeństwo - p.uzupełniający',
            'Informatyka',
            'Język angielski',
            'Język niemiecki',
            'Język polski',
            'Matematyka',
            'Religia',
            'Wychowanie fizyczne',
            'rys.techniczny',
            ]
    _ignored = ['+', '-', 'np']
    _grades = {}
    data = librus.get_grades()
    for subj in data:
        if subj in _subj:
            _grades[subj] = []
        for grade in data[subj]:
            if grade['To_the_average'] == 'Tak':
                if grade['Grade'] in _ignored:
                    continue
                _grades[subj].append((values[grade['Grade']], grade['Weight']))
    return _grades

def gpa(grades):
    _gpa = {i : None for i in grades}
    for subj, _grades in grades.items():
        try:
            temp = sum([i[0]*i[1] for i in _grades])/sum([i[1] for i in _grades])
        except ZeroDivisionError:
            temp = 0
        _gpa[subj] = round(temp, 2)

    return _gpa

def plot(gpa, ngpa):
    width = .75
    rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots()
    fig.suptitle('Średnie')


    x, y = zip(*gpa.items())
    x =  [ '\n'.join(wrap(i, 16)) for i in x ]
    _gpa = ax.bar(x, y, width=width, label = 'Średnie cząstkowe')

    x, y = zip(*ngpa.items())
    _ngpa = ax.bar(x, y, width=width, label = 'Średnia ocen')

    ax.legend(loc=3)
    ax.set_ylabel('Średnia')
    ax.bar_label(_gpa, padding=0)
    ax.bar_label(_ngpa, padding=0)

    plt.get_current_fig_manager().set_window_title('GPA')
    plt.xticks(rotation=90, fontsize= 'small',)
    fig.savefig('gpa.png')
    plt.show()


def ngpa(gpa):
    _ngpa = 0
    def normalize(x):
        if x - int(x) < 0.75:
            return m.floor(x)
        else:
            return m.ceil(x)
    for name, _gpa in gpa.items():
        _ngpa += normalize(_gpa)
    _ngpa /= len(gpa)
    _ngpa = round(_ngpa, 2)
    _ngpa = {'Ogólna': _ngpa}
    return _ngpa

def main():
    login_, password = get_login_data()
    librus = login(login_, password)
    Grades = grades(librus)
    Gpa = gpa(Grades)
    Ngpa = ngpa(Gpa)
    plot(Gpa, Ngpa)


if __name__=='__main__':
    main()
