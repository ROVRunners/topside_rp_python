import cv2
import tkinter as tk
from PIL import Image, ImageTk
from config.dashboard import DashboardConfig


class Dashboard(tk.Frame):

    def __init__(self, master, config: DashboardConfig, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.scales = {}
        self.labels = {}
        self.entries = {}
        self.images = {}

        self.displays = {}

        self._config = config

        # Labels
        for i in self._config.labels:
            self.put_label(i.name, i.row, i.column, i.text, i.rspan, i.cspan)

        # Slider bars
        for i in self._config.scales:
            self.put_scale(i.name, i.row, i.column, i.min_, i.max_, i.default, i.rspan, i.cspan)

        # Orientation markers
        for i in self._config.images:
            self.put_image(i.name, i.row, i.column, i.width, i.height, i.filename, i.rspan, i.cspan)

        self.pack()
        # Cameras
        # self.put_display("frame0", 1, 0, rspan=5)
        # self.put_display("frame1", 6, 0, rspan=5)

    def put_scale(self, name, row, column, min_, max_, default, rspan=1, cspan=1):
        scale = tk.Scale(self, from_=min_, to=max_, orient=tk.HORIZONTAL, length=300)
        scale.set(default)
        scale.grid(row=row, column=column, rowspan=rspan, columnspan=cspan)
        self.scales[name] = scale

    def get_scale(self, name):
        return self.scales[name].get()

    def put_entry(self, name, row, column, converter, default="", rspan=1, cspan=1):
        def validator_fn(x):
            if x == "":
                return True
            try:
                converter(x)
                return True
            except:
                return False

        vcmd = (self.register(validator_fn), "%P")

        entry = tk.Entry(self, validate="all", validatecommand=vcmd)
        entry.insert(0, default)
        entry.grid(row=row, column=column, rowspan=rspan, columnspan=cspan)

        self.entries[name] = (converter, entry)

    def get_entry(self, name, default):
        converter, entry = self.entries[name]

        text = entry.get()
        try:
            return converter(text)
        except:
            return default

    def put_label(self, name, row, column, text, rspan=1, cspan=1):
        label = tk.Label(self, text=text)
        label.grid(row=row, column=column, rowspan=rspan, columnspan=cspan)
        self.labels[name] = label

    def set_label(self, name, text):
        self.labels[name].config(text=text)

    def put_image(self, name, row, column, width, height, filename, rspan=1, cspan=1):
        hypotenuse = (width ** 2 + height ** 2) ** 0.5

        coord = hypotenuse / 2

        canvas = tk.Canvas(self, width=hypotenuse, height=hypotenuse)

        canvas.grid(row=row, column=column, rowspan=rspan, columnspan=cspan)

        image = Image.open(filename)
        image.thumbnail((width, height), Image.LANCZOS)

        tkimage = ImageTk.PhotoImage(image)

        image_id = canvas.create_image(coord, coord, image=tkimage)

        self.images[name] = (image, tkimage, image_id, coord, canvas)

    def rotate_image(self, name, angle):
        image, tkimage, image_id, coord, canvas = self.images[name]
        tkimage = ImageTk.PhotoImage(image.rotate(angle, expand=True))
        canvas.delete(image_id)
        image_id = canvas.create_image(coord, coord, image=tkimage)
        self.images[name] = (image, tkimage, image_id, coord, canvas)

    def put_display(self, name, row, column, rspan=1, cspan=1):
        display = tk.Label(self)
        display.grid(row=row, column=column, rowspan=rspan, columnspan=cspan)

        self.displays[name] = display

    def update_display(self, name, frame):
        display = self.displays[name]
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        display.imgtk = imgtk
        display.configure(image=imgtk)
        self.displays[name] = display

    def update_images(self, images: dict[str, float]):
        for name, value in images.items():
            if name in self.images:
                self.rotate_image(name, value)


# if __name__ == "__main__":
#     root = tk.Tk()
#
#     dashboard = Dashboard(root)
#
#     dashboard.put_label("Label", 1, 2, "Hi!")
#     dashboard.put_scale("Scale1", 1, 3, 0, 359, 50)
#
#     dashboard.put_entry("Place", 2, 1, float, "23")
#
#     dashboard.put_image("topview", 3, 1, 200, 200, "assets/topview.png")
#     dashboard.put_image("sideview", 3, 2, 200, 200, "assets/sideview.png")
#
#     dashboard.pack()
#
#     while 1:
#         dashboard.rotate_image("topview", dashboard.get_entry("Place", 0))
#         dashboard.rotate_image("sideview", dashboard.get_scale("Scale1"))
#
#         root.update_idletasks()
#         root.update()
