from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox

class util:
    def toCenterScreen(self, width, height):

        root = Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.destroy()
        
        pos_x = float(screen_width)/2 - width/2
        pos_y = float(screen_height)/2 - height/2
        
        if pos_x < 0:
            pos_x = pos_x * -1

        if pos_y < 0:
            pos_y = pos_y * -1

        return f'{width}x{height}+{pos_x:.0f}+{pos_y:.0f}'

class Convert:
    def __init__(self, multiplication_factor : float = 1.5) -> None:
        self.multiplication_factor = multiplication_factor
        self.list_data_dimens = []

    def getFormatedDimen(self, dimen_id: str, value: int, type_dimen: str) -> str:
        return f'<dimen name="{dimen_id}">{round(value)}{type_dimen}</dimen>\n'.replace(".0", "")

    def filter(self, list_values: str):
        pos_init = 0
        pos_end = 0
        
        pos_init_id = 0
        pos_end_id = 0
        
        is_first_aspa = False
        for pos, letter in enumerate(list_values):
            if letter == '"':
                if is_first_aspa == True:
                    pos_end_id = pos
                    is_first_aspa = False
                else:
                    pos_init_id = pos + 1
                    is_first_aspa = True

                pos_init = pos + 2
            elif letter == '/':
                pos_end = pos - 1

                #Add objeto a lista
                dimen = list_values[pos_init : pos_end]
                self.list_data_dimens.append(
                    {
                        "new_dimen":  int(dimen.replace("dp", "").replace("sp", "")) * self.multiplication_factor,
                        "id": list_values[pos_init_id : pos_end_id],
                        "type": "dp" if "dp" in dimen else "sp"
                    }
                )

    def convert(self):
        news_dimens = ""
        for dimen in self.list_data_dimens:
            news_dimens += self.getFormatedDimen(dimen["id"], dimen["new_dimen"], dimen["type"])

        self.list_data_dimens.clear()
        return news_dimens
        
class Graph:
    def __init__(self) -> None:
        self.window = Tk()
        self.convert = Convert()
        self.onCreate()

    def onCreate(self) -> None:
        self.window.title("Dimens convert")
        self.window.geometry(util().toCenterScreen(600, 450))

        self.setupEntrys()
        self.setupButtons()

        self.window.mainloop()

    def setupEntrys(self):
        self.stDimensSource = scrolledtext.ScrolledText(self.window, width=70, height=10)
        self.stDimensSource.place(x=10, y=50)

        self.stDimensResult = scrolledtext.ScrolledText(self.window, width=70, height=10, state="disabled")
        self.stDimensResult.place(x=10, y=250)

    def setupButtons(self):
        self.btConvert = Button(self.window, text="Convert", command=self.onConvert, width=81)
        self.btConvert.place(x=10, y=220)

        self.btConvert = Button(self.window, text="Copy to Clipboard", command=self.onCopy)
        self.btConvert.place(x=10, y=420)

    def onConvert(self):
        self.convert.filter(
            self.stDimensSource.get("1.0", END)
        )
        self.setResult(
            self.convert.convert()
        )
    
    def setResult(self, news_dimens) -> None:
        self.stDimensResult['state'] = "normal"
        self.stDimensResult.delete("1.0", END)
        self.stDimensResult.insert(INSERT, news_dimens)
        self.stDimensResult['state'] = "disabled"

    def onCopy(self) -> None:
        #LIMPA A AREA DE TRANSFERENCIA E ADICIONA O CÓDIGO FORMATADO
        self.window.clipboard_clear()
        self.window.clipboard_append(
            self.stDimensResult.get("1.0", END)
        )
        messagebox.showinfo("Copy", "Copied to clipboard")

if __name__ == "__main__":
    Graph()