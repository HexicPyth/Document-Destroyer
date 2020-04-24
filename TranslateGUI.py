import random as insecure_random
import textwrap
import tkinter
import TranslateAPI

random = insecure_random.SystemRandom()  # make random() Cryptographically-Secure just 'cuz why not?


def select_all(event):
    """ Overwrite the tkinter CTRL-A action so CTRL-A actually does a 'select-all'"""
    event.widget.tag_add("sel", "1.0", "end")


background_window_color = "#003366"
background_logging_color = "#4c5975"
background_IO_color = "#e4edd9"
foreground_text_color = "white"
foreground_title_font = ("Ubuntu", 12, "bold")

UI = tkinter.Tk()
UI.bind_class("Text", "<Control-a>", select_all)
UI.title('Text Screw-er-up-er')
UI.configure(background=background_window_color)

layers_value = tkinter.StringVar()

title_label = tkinter.Label(text="Document Destroyer 2.3 Revision 3", font=("Ubuntu", 13, "italic", "underline"),
                            fg=foreground_text_color, bg=background_window_color)

title_label.pack()
input_dialog = tkinter.Text(UI, height=60, width=60, wrap=tkinter.WORD, font=("ubuntu", 10), fg="green")

output_dialog = tkinter.Text(UI, height=60, width=60, wrap=tkinter.WORD, font=("ubuntu", 10), fg="green")
output_dialog.configure(background=background_IO_color)


progress_label = tkinter.Label(text="Progress")
progress_label.configure(font=foreground_title_font, bg=background_window_color, fg=foreground_text_color)
progress_label.pack()

progress_text = tkinter.Text(height=2, width=50, borderwidth=0)
progress_text.configure(background=background_logging_color)
progress_text.pack()


def update_logs(message):
    progress_text.delete(1.0, tkinter.END)
    progress_text.insert(tkinter.END, message)
    UI.update()


mode = tkinter.StringVar()
mode.set("Slow")  # initialize


def destroy_text():
    """ Helper function to call make_my_text_weird when the "Destroy my text" button is clicked."""
    global mode
    global progress_label

    output_dialog.delete(1.0, tkinter.END)
    UI.update()

    try:
        layers = int(layers_value.get())
    except ValueError:
        layers = random.randint(1, 20)

    in_text = input_dialog.get("1.0", tkinter.END)
    progress_label.pack()

    try:
        # slow_translate(in_text, layer_count, intermediate=False, verbose=False, wimpiness=False)

        update_logs("Translating...")
        if str(mode.get()) == "Slow":
            print("Translating slowly...")
            raw_weird_text = TranslateAPI.slow_translate(in_text, layers, intermediate=False,
                                                         verbose=True, wimpiness=False,
                                                         progress_text=progress_text, UI=UI)
        else:
            print("Translating quickly...")
            raw_weird_text = TranslateAPI.make_my_text_weird(in_text, layers, show_intermediate_translations=False,
                                                             verbose=True, i_am_a_wimp=False,
                                                             progress_text=progress_text, UI=UI, fast_mode=True)
        update_logs("Translation Complete!")

        update_logs("Formatting...")
        formatted_weird_text = '\n'.join(textwrap.wrap(raw_weird_text, 60, break_long_words=False))
        formatted_weird_text = formatted_weird_text.replace("[", "")
        formatted_weird_text = formatted_weird_text.replace("]", "").encode('ascii', 'ignore').decode('ascii', 'ignore')
        update_logs("Formatting Complete!")

        output_dialog.insert(tkinter.END, formatted_weird_text)
        print(formatted_weird_text)
        UI.update()

    except AttributeError:
        pass


# Local Tkinter stuff.

in_label = tkinter.Label(text="Enter a boring document.",
                         font=("Ubuntu", 12, "bold", "underline"),
                         fg=foreground_text_color, bg=background_window_color)

out_label = tkinter.Label(text="Share an entertaining document.",
                          font=("Ubuntu", 12, "bold", "underline"),
                          fg=foreground_text_color, bg=background_window_color)

in_label.pack(side=tkinter.TOP, anchor='w')

# I/O
input_dialog.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1,)
input_dialog.configure(bg=background_IO_color)
input_dialog.insert(tkinter.END, "Type Fancy document here")
output_dialog.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)

control_location = tkinter.TOP

# Layers control
layers_label = tkinter.Label(UI, text="• Layer Count", bg=background_window_color, fg=foreground_text_color,
                             font=("Ubuntu", 11, "bold"))
layers_label.pack(side=control_location, fill=tkinter.BOTH)
layers_string = tkinter.Entry(UI, textvariable=layers_value)
layers_string.pack(side=control_location, fill=tkinter.BOTH)

mode_select_label = tkinter.Label(text="Select a translation mode:")


def set_mode():
    translation_mode = str(mode.get())
    print(translation_mode)


b = tkinter.Radiobutton(UI, text="Slow Mode(new!)", variable=mode, value="Slow", command=set_mode)
b.pack(anchor='s')

b = tkinter.Radiobutton(UI, text="Fast Mode", variable=mode, value="Fast", command=set_mode)
b.pack(anchor='s')

# Destroy My Text button
translate_button = tkinter.Button(text="Destroy my text", command=destroy_text)
translate_button.pack(side=control_location)

tkinter.mainloop()
