import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import os
import sys
import math
import webbrowser
import pickle
import pandas as pd


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text="Movie Revenue Prediction",
                              font=('Arial', 18, 'bold italic'),
                              width=20, height=2)

        logo_file = tk.PhotoImage(file='./UI_supporting_files/logo.gif')
        self.logo_l = tk.Label(self, image=logo_file)
        self.logo_l.photo = logo_file
        self.logo_l2 = tk.Label(self, image=logo_file)
        self.logo_l2.photo = logo_file

        image_file = tk.PhotoImage(
                    file='./UI_supporting_files/Frontpage_image.gif')
        self.image_l = tk.Label(self, image=image_file)
        self.image_l.photo = image_file

        self.help = tk.Button(self, text="Help", font=('Arial', 12),
                              width=20, height=2, bd=5,
                              command=self.get_help)

        self.report = tk.Button(self, text="Researcher Use",
                                font=('Arial', 12),
                                width=20, height=2, bd=5,
                                command=self.print_report)

        self.start_p = tk.Button(self, text="Your Movie Prediction",
                                 font=('Arial', 12),
                                 width=20, height=2, bd=5,
                                 command=self.run_program)
        self.quit = tk.Button(self, text="Quit program", font=('Arial', 10),
                              fg='red',
                              width=15, height=2, bd=5,
                              command=root.destroy)

        # final value of prediction====================
        self.revenue = tk.StringVar()
        self.revenue.set('N/A')
        # Layout=======================================
        self.title.grid(row=0, column=1)
        self.logo_l.grid(row=0, column=0)
        self.logo_l2.grid(row=0, column=2)
        self.image_l.grid(row=1, column=0, columnspan=3)
        self.report.grid(row=3, column=0, pady=20)
        self.start_p.grid(row=3, column=1)
        self.help.grid(row=3, column=2)
        self.quit.grid(row=4, column=1)

    def get_help(self):
        helpinfo = "In this system, user can predict the revenue of" \
                    "a movie with customized parameters. Researchers can" \
                    "check more details using our modules and even build" \
                    "their own prediction models."
        tk.messagebox.showinfo(
            title="Movie Revenue Prediction - User Help", message=helpinfo)

    def print_report(self):
        # open the file report on google drive
        os.system("start cmd /c jupyter notebook ..\\example\\demo.ipynb")
        # url_project = "https://drive.google.com/file/d/" \
        #                "1VvI4h8u0aof57OnSwIPhDbwV-t5Kcgex/view"
        # webbrowser.open(url_project)

    def normalization(self, a, min_v, max_v):
        a = float(a)
        nor = (a - min_v) / (max_v - min_v)
        return nor

    # prediction function which collects all the input data
    def prediction(self, budget, imdb_rating, imdb_voting, runtime,
                   weekend_var, month_var,
                   rating, genre1_var, genre2_var, genre3_var,
                   model_selection):
        # log and normalization
        budget_v = math.log10(int(budget))
        IMDBvoting_v = math.log10(int(imdb_voting))
        imdb_rating = self.normalization(imdb_rating, 1.2, 9.0)
        IMDBvoting_v = self.normalization(IMDBvoting_v, 1.041, 6.2667)
        runtime = self.normalization(runtime, 41, 321)
        budget_v = self.normalization(budget_v, 2.69897, 8.579783597)

        if weekend_var == 'YES':
            weekend_v = 1
        else:
            weekend_v = 0

        if month_var in ['Jan', 'Feb', 'Sept', 'Oct']:
            month_v = 1
        else:
            month_v = 0

        Rating_v = [0] * 6  # G,PG,PG-13,R,NC-17,Unrated
        if rating == 'G':
            Rating_v[0] = 1
        elif rating == 'PG':
            Rating_v[1] = 1
        elif rating == 'PG-13':
            Rating_v[2] = 1
        elif rating == 'R':
            Rating_v[3] = 1
        elif rating == 'NC-17':
            Rating_v[4] = 1
        else:
            Rating_v[5] = 1

        genre123_var = [genre1_var, genre2_var, genre3_var]
        genre_v = [0] * 13
        for x in genre123_var:
            if x == 'action':
                genre_v[0] = 1
            elif x == 'adventure':
                genre_v[1] = 1
            elif x == 'animation':
                genre_v[2] = 1
            elif x == 'biography':
                genre_v[3] = 1
            elif x == 'comedy':
                genre_v[4] = 1
            elif x == 'crime':
                genre_v[5] = 1
            elif x == 'darama':
                genre_v[6] = 1
            elif x == 'family':
                genre_v[7] = 1
            elif x == 'fantasy':
                genre_v[8] = 1
            elif x == 'mystery':
                genre_v[9] = 1
            elif x == 'romance':
                genre_v[10] = 1
            elif x == 'thriller':
                genre_v[11] = 1
            else:
                genre_v[12] = 1

        features = []
        features.append(float(imdb_rating))
        features.append(IMDBvoting_v)
        features.append(0)  # language
        features.append(float(runtime))
        features.append(budget_v)
        features.append(0)  # actor_plpularity
        features.append(0)  # director_popularity
        features.append(weekend_v)
        features.append(month_v)
        features.extend(genre_v)
        features.extend(Rating_v)
        # print(features)
        if model_selection == 1:
            with open('./UI_supporting_files/lr_model.pkl',
                      'rb') as model:
                new_model = pickle.load(model)
        elif model_selection == 2:
            with open('./UI_supporting_files/lasso_model.pkl',
                      'rb') as model:
                new_model = pickle.load(model)
        elif model_selection == 3:
            with open('./UI_supporting_files/ridge_model.pkl',
                      'rb') as model:
                new_model = pickle.load(model)
        elif model_selection == 4:
            with open('./UI_supporting_files/tree_model.pkl',
                      'rb') as model:
                new_model = pickle.load(model)

        temp = new_model.predict([features])
        # print(temp)
        final_result = int(round(10**temp[0]))
        self.revenue.set(str(final_result))

    def run_program(self):
        window = tk.Toplevel(self)
        window.geometry("900x450")
        title2 = tk.Label(window, text="Your Moive Prediction",
                          font=('Arial', 18, 'bold italic'),
                          width=25, height=2)
        # CLOSE PREDICTION PROGRAM
        close_b = tk.Button(window, text="Close", font=('Arial', 8),
                            width=10, height=2, bd=3, fg='red',
                            command=window.destroy)
        # BUDGET================================
        budget_t = tk.Label(window, text="Budget", width=20, height=2)
        budget_e = tk.Entry(window, width=12)
        budget_e.insert(0, '10000')
        # IMDB RATING===========================
        IMDBrating_t = tk.Label(
            window, text="IMDB Rating (0.0-9.9)", width=20, height=2)
        IMDBrating_e = tk.Entry(window, width=12)
        IMDBrating_e.insert(0, '6.5')
        # IMDE VOTING===========================
        IMDBvoting_t = tk.Label(window, text="IMDB Voting", width=20, height=2)
        IMDBvoting_e = tk.Entry(window, width=12)
        IMDBvoting_e.insert(0, '10000')
        # MOVIE RATING==========================
        Rating_var = tk.StringVar()
        Rating_list = ('G', 'PG', 'PG-13', 'R', 'NC-17', 'Unrated')
        Rating_t = tk.Label(window, text="Moive Rating", width=20)
        Rating_e = ttk.Combobox(
            window, width=10, textvariable=Rating_var, value=Rating_list)
        Rating_e.current(0)
        # GENRE SELECTION========================
        genre_list = ('N/A', 'action', 'adventure', 'animation', 'biography',
                      'comedy', 'crime', 'drama',
                      'family', 'fantasy', 'mystery',
                      'romance', 'thriller', 'other')
        genre1_var = tk.StringVar()
        genre1_t = tk.Label(window, text="Genre 1", width=20)
        genre1_e = ttk.Combobox(
            window, width=10, textvariable=genre1_var, value=genre_list)
        genre1_e.current(0)

        genre2_var = tk.StringVar()
        genre2_t = tk.Label(window, text="Genre 2 (optional)", width=20)
        genre2_e = ttk.Combobox(
            window, width=10, textvariable=genre2_var, value=genre_list)
        genre2_e.current(0)

        genre3_var = tk.StringVar()
        genre3_t = tk.Label(window, text="Genre 3 (optional)", width=20)
        genre3_e = ttk.Combobox(
            window, width=10, textvariable=genre3_var, value=genre_list)
        genre3_e.current(0)
        # RUNTIME===============================
        runtime_t = tk.Label(window, text="Runtime(min)", width=20, height=2)
        runtime_e = tk.Entry(window, width=12)
        runtime_e.insert(0, '120')
        # RELEASE DATE==========================
        weekend_var = tk.StringVar()
        weekend_list = ('YES', 'NO')
        weekend_t = tk.Label(window, text="Release on weekend", width=20)
        weekend_e = ttk.Combobox(
            window, width=10, textvariable=weekend_var, value=weekend_list)
        weekend_e.current(0)

        month_var = tk.StringVar()
        month_list = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
        month_t = tk.Label(window, text="Release month", width=20)
        month_e = ttk.Combobox(
            window, width=10, textvariable=month_var, value=month_list)
        month_e.current(0)
        # MODEL SELECTION========================
        model_var = tk.IntVar()
        model_group = tk.LabelFrame(
            window, text='Model Selection', font=('Arial', 10, 'bold'))
        model_1 = tk.Radiobutton(model_group, text='Linear Regression',
                                 font=('Arial', 10),
                                 variable=model_var, value=1)
        model_2 = tk.Radiobutton(model_group, text='Lasso Model',
                                 font=('Arial', 10),
                                 variable=model_var, value=2)
        model_3 = tk.Radiobutton(model_group, text='Ridge Model',
                                 font=('Arial', 10),
                                 variable=model_var, value=3)
        model_4 = tk.Radiobutton(model_group, text='Tree Model',
                                 font=('Arial', 10),
                                 variable=model_var, value=4)
        # RUN PREDICTION=========================
        run = tk.Button(window, text="Predict", font=('Arial', 12),
                        width=15, height=2, bd=5,
                        command=lambda: self.prediction(budget_e.get(),
                                                        IMDBrating_e.get(),
                                                        IMDBvoting_e.get(),
                                                        runtime_e.get(),
                                                        weekend_var.get(),
                                                        month_var.get(),
                                                        Rating_var.get(),
                                                        genre1_var.get(),
                                                        genre2_var.get(),
                                                        genre3_var.get(),
                                                        model_var.get()))
        # Print prediction=======================
        prediction_t = tk.Label(window,
                                text='Estimated Revenue (In US Dollar):',
                                font=('Arial', 12, 'bold'))
        prediction_l = tk.Label(window,
                                textvariable=self.revenue,
                                width=20, font=('Arial', 14))
        # LAYOUT=================================
        title2.grid(row=0, column=1, columnspan=4)
        close_b.grid(row=0, column=0)
        budget_t.grid(row=1, column=0)
        budget_e.grid(row=2, column=0)
        IMDBrating_t.grid(row=1, column=1)
        IMDBrating_e.grid(row=2, column=1)
        IMDBvoting_t.grid(row=1, column=2)
        IMDBvoting_e.grid(row=2, column=2)
        runtime_t.grid(row=1, column=3)
        runtime_e.grid(row=2, column=3)
        weekend_t.grid(row=1, column=4)
        weekend_e.grid(row=2, column=4)
        month_t.grid(row=1, column=5)
        month_e.grid(row=2, column=5)
        Rating_t.grid(row=3, column=0)
        Rating_e.grid(row=4, column=0)
        genre1_t.grid(row=3, column=1)
        genre1_e.grid(row=4, column=1)
        genre2_t.grid(row=3, column=2)
        genre2_e.grid(row=4, column=2)
        genre3_t.grid(row=3, column=3)
        genre3_e.grid(row=4, column=3)
        model_group.grid(row=5, column=1, columnspan=4, pady=30)
        model_1.grid(row=5, column=0, padx=20)
        model_2.grid(row=5, column=1, padx=20)
        model_3.grid(row=5, column=2, padx=20)
        model_4.grid(row=5, column=3, padx=20)
        run.grid(row=6, column=2, columnspan=2)
        prediction_t.grid(row=7, column=2, columnspan=2, pady=20)
        prediction_l.grid(row=8, column=2, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TEAM MOIVE BADGERS")
    root.geometry("800x320")
    app = App(root)
    app.mainloop()
