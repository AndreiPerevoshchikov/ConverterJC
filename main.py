import json
from customtkinter import *
from customtkinter import filedialog as fd
import pathlib
from PIL import Image, ImageTk
from itertools import count, cycle


class ImageLabel(CTkLabel):
    def load(self, im):
        """
        Загружает и отображает анимированное изображение в виджете Label.
        Параметры:
            im (str): Путь к изображению.
        """
        im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        self.frames = cycle(frames)
        self.delay = im.info['duration']

        if len(frames) == 1:
            self.configure(image=next(self.frames))
        else:
            self.next_frame()

    def next_frame(self):
        """
        Отображает следующий кадр анимированного изображения.
        """
        if self.frames:
            self.configure(image=next(self.frames))
            self.after(self.delay, self.next_frame)


def callback():
    """
    Обработчик события нажатия кнопки "Выбрать json файл".
    Открывает диалоговое окно выбора файла и записывает путь к файлу в поле ввода.
    """
    name = fd.askopenfilename()
    ePath.configure(state='normal')
    ePath.delete('1', 'end')
    ePath.insert('1', name)
    ePath.configure(state='readonly')


def convert():
    """
    Конвертирует json файл в csv формат.
    Читает данные из json файла, формирует csv строку и сохраняет в новый csv файл.
    """
    json_file = ePath.get()
    csv_file = pathlib.Path(json_file)
    csv_file = csv_file.stem + '.csv'
    try:
        with open(json_file, 'r') as f:
            data = json.loads(f.read())
        output = ','.join([*data[0]])
        print(output)
        for obj in data:
            output += f'\n{obj["id"]},{obj["first_name"]},{obj["last_name"]}'
        print(output)
        with open(csv_file, 'w') as f:
            f.write(output)
    except Exception as ex:
        print(f'Error: {str(ex)}')

    CTkLabel(root, text='Конвертация завершена', font=('Arial', 15)).pack(pady=10)


if __name__ == '__main__':
    root = CTk()
    root.title('Конвертер json в csv')
    root.geometry('800x400+400+400')
    root.resizable(width=False, height=False)

    CTkButton(root, text='Выбрать json файл', font=('Arial', 15), command=callback).pack(pady=10)

    lbPath = CTkLabel(root, text='Путь к файлу:', font=('Arial', 15))
    lbPath.pack()

    ePath = CTkEntry(root, width=400, state='readonly')
    ePath.pack(pady=10)

    btnConvert = CTkButton(root, text='Конвертировать', font=('Arial', 15), command=convert).pack(pady=10)

    lb = ImageLabel(root)
    lb.pack()
    lb.load('test.gif')
    root.mainloop()
