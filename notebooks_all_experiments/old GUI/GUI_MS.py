import os
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Canvas, BOTH
from tkinter import messagebox, filedialog
from tkinter import *
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import mergedmsdbs
from PIL import ImageTk, Image

gender = 1
OCB_value = 1

class GUI:

    def __init__(self, master):
        # initialize all params in GUI
        self.master = master
        master.geometry("440x250")
        # set GUI title
        master.title("Multiple Sclerosis Prediction")

        # fields for user's patient information
        self.MRI_lesion_mass = ""
        self.primary_EDSS_at_diagnosis = ""
        self.age_at_diagnosis = ""
        self.TIM3_RQ = ""
        self.TIGIT_RQ = ""
        self.LAG3_RQ = ""
        self.PD1_RQ = ""
        self.Male = ""
        self.positive_OCB = ""

        self.MRI_lesion_mass_Label = Label(master, text="Lession mass value:")
        self.primary_EDSS_at_diagnosis_Label = Label(master, text="EDSS at diagnosis:")
        self.age_at_diagnosis_Label = Label(master, text="Age at diagnosis:")
        self.TIM3_RQ_Label = Label(master, text="TIM 3 value:")
        self.TIGIT_RQ_Label = Label(master, text="TIGIT value:")
        self.LAG3_RQ_Label = Label(master, text="LAG 3 value:")
        self.PD1_RQ_Label = Label(master, text="PD1 value:")

        self.MRI_Entry = Entry(master, validate="key")
        self.EDSS_Entry = Entry(master, validate="key")
        self.age_Entry = Entry(master, validate="key")
        self.TIM3_Entry = Entry(master, validate="key")
        self.TIGIT_Entry = Entry(master, validate="key")
        self.LAG3_Entry = Entry(master, validate="key")
        self.PD1_Entry = Entry(master, validate="key")

        global gender
        gender = IntVar()
        gender.set(0)

        R1 = Radiobutton(self.master, text="Male", variable=gender, value=1)
        R2 = Radiobutton(self.master, text="Female", variable=gender, value=2)
        R1.grid(row=10, column=1, sticky=W, ipady=1)
        R2.grid(row=10, column=0, sticky=W, ipady=1)
        R2.select()

        global OCB_value
        OCB_value = IntVar(0)
        OCB_value.set(0)

        R3 = Radiobutton(self.master, text="Positive OCB", variable=OCB_value, value=1)
        R4 = Radiobutton(self.master, text="Negative OCB", variable=OCB_value, value=2)
        R3.select()
        R3.grid(row=11, column=0, sticky=W, ipady=1)
        R4.grid(row=11, column=1, sticky=W, ipady=1)
        import sklearn
        print('The scikit-learn version is {}.'.format(sklearn.__version__))

        # self.train_model_button = Button(master, text="Train Model", command=lambda: self.update("train"), state="disabled")
        self.predict_button = Button(master, text="Execute Prediction", command=lambda: self.update("predict"), state="normal", width=20, height=2, fg='blue')


        # LAYOUT - Grid
        self.MRI_lesion_mass_Label.grid(row=2, column=0, sticky=W)
        self.MRI_Entry.grid(row=2, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.primary_EDSS_at_diagnosis_Label.grid(row=3, column=0, sticky=W)
        self.EDSS_Entry.grid(row=3, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.age_at_diagnosis_Label.grid(row=4, column=0, sticky=W)
        self.age_Entry.grid(row=4, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.TIM3_RQ_Label.grid(row=5, column=0, sticky=W)
        self.TIM3_Entry.grid(row=5, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.TIGIT_RQ_Label.grid(row=6, column=0, sticky=W)
        self.TIGIT_Entry.grid(row=6, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.LAG3_RQ_Label.grid(row=7, column=0, sticky=W)
        self.LAG3_Entry.grid(row=7, column=1, ipadx=100, ipady=1)


        # LAYOUT - Grid
        self.PD1_RQ_Label.grid(row=8, column=0, sticky=W)
        self.PD1_Entry.grid(row=8, column=1, ipadx=100, ipady=1)

        # self.predict_button.grid(row=17, column=1)
        self.predict_button.place(relx=0.5, rely=0.9, anchor=CENTER)





    # check validate path - was entered by user
    def validatePath(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_path = ""
            return True
        try:
            # path need to be to real file and excel file
            if os.path.isfile(new_text) and new_text.endswith('.xlsx'):
                self.entered_path = new_text
                return True
            self.entered_path = ""
            error = messagebox.showerror('K Means Clustering', 'Error file type - Enter path to xlsx file',
                                         parent=self.master)
            return False
        except ValueError:
            self.entered_path = ""
            error = messagebox.showerror('K Means Clustering', 'Error file type - Enter path to xlsx file',
                                         parent=self.master)
            return False

    def validate_MRI(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.MRI_Entry.get()) == 0:
            return result
        if not re.match(regex, self.MRI_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction', 'Incorrect lession mass value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not int(self.MRI_Entry.get()) >= 0:
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect lession mass value - please fill a non-negative value',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_EDSS(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.EDSS_Entry.get()) == 0:
            return result
        if not re.match(regex, self.EDSS_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect EDSS value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if 0 <= getdouble(self.EDSS_Entry.get()) <= 10 and getdouble(self.EDSS_Entry.get()) % 0.5 == 0:
            return result
        else:
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect EDSS value - please fill an EDSS value in range',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_age(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.age_Entry.get()) == 0:
            return result
        if not re.match(regex, self.age_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect age value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not 0 < int(self.age_Entry.get()) < 100:
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect age value - please fill a non-negative value in range',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_TIM3(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.TIM3_Entry.get()) == 0:
            return result
        if not re.match(regex, self.TIM3_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect TIM3 value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not 0 <= getdouble(self.TIM3_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect TIM3 value - please fill a non-negative value',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_TIGIT(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.TIGIT_Entry.get()) == 0:
            return result
        if not re.match(regex, self.TIGIT_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect TIGIT value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not 0 <= getdouble(self.TIGIT_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect TIGIT value - please fill a non-negative value',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_LAG3(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.LAG3_Entry.get()) == 0:
            return result
        if not re.match(regex, self.LAG3_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect LAG3 value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not 0 <= getdouble(self.LAG3_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect LAG3 value - please fill a non-negative value',
                                 parent=self.master)
            result = FALSE
        return result

    def validate_PD1(self):
        result = TRUE
        regex = r'^[+-]{0,1}((\d*\.)|\d*)\d+$'
        if len(self.PD1_Entry.get()) == 0:
            return result
        if not re.match(regex, self.PD1_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect PD1 value - please fill a numeric value',
                                 parent=self.master)
            result = FALSE
            return result
        if not 0 <= getdouble(self.PD1_Entry.get()):
            messagebox.showerror('Multiple Sclerosis Prediction',
                                 'Incorrect PD1 value - please fill a non-negative value',
                                 parent=self.master)
            result = FALSE
        return result

    # open browser window - to choose file

    def choosePath(self):
        filename = askopenfilename()
        entered_path = filename
        return filename

    # update - for every buttons press
    def update(self, method):
        # button - browse
        if method == "browse":
            filename = self.choosePath()

            self.pathEntry.delete(0, END)
            self.pathEntry.insert(0, filename)

        elif method == "predict":
            if self.check_user_data() == FALSE:
                # messagebox.showerror('Multiple Sclerosis Prediction', 'Please fill all the relevant data for prediction', parent=self.master)
                return
            else:
                dictionary_gender = ""
                ocb_val = ""
                if gender.get() == 1:
                    dictionary_gender = 1
                else:
                    dictionary_gender = 0
                if OCB_value.get() == 1:
                    ocb_val = 1
                else:
                    ocb_val = 0
                user_data = {
                    "MRI_lesion_mass": self.MRI_Entry.get(),
                    "primary_EDSS_at_diagnosis": self.EDSS_Entry.get(),
                    "age_at_diagnosis": self.age_Entry.get(),
                    "TIM3_RQ": self.TIM3_Entry.get(),
                    "TIGIT_RQ": self.TIGIT_Entry.get(),
                    "PD-1_RQ": self.PD1_Entry.get(),
                    "LAG3_RQ": self.LAG3_Entry.get(),
                    "Male": dictionary_gender,
                    "positive_OCB": ocb_val
                }
                # changes value in dictionary to match the code that draws information from the model
                missing_values = ""
                if len(self.MRI_Entry.get()) == 0:
                    user_data['MRI_lesion_mass'] = ''
                    missing_values = "lession mass, "
                if len(self.EDSS_Entry.get()) == 0:
                    user_data['primary_EDSS_at_diagnosis'] = ''
                    missing_values = missing_values + "EDSS at diagnosis, "
                if len(self.age_Entry.get()) == 0:
                    user_data['age_at_diagnosis'] = ''
                    missing_values = missing_values + "age at diagnosis, "
                if len(self.TIM3_Entry.get()) == 0:
                    user_data['TIM3_RQ'] = ''
                    missing_values = missing_values + "TIM3, "
                if len(self.TIGIT_Entry.get()) == 0:
                    user_data['TIGIT_RQ'] = ''
                    missing_values = missing_values + "TIGIT, "
                if len(self.PD1_Entry.get()) == 0:
                    user_data['PD-1_RQ'] = ''
                    missing_values = missing_values + "PD1, "
                if len(self.LAG3_Entry.get()) == 0:
                    user_data['LAG3_RQ'] = ''
                    missing_values = missing_values + "LAG3, "
                missing_values = missing_values[:len(missing_values)-2]

                results = mergedmsdbs.predictions(user_data)
                RRMS = results['RRMS']
                EDSS = results['EDSS']
                EDSS_DESC = results['message']

                lines = ["Predicted EDSS after 10 years is: " + str(EDSS),"This level of EDSS means that the patient is " +str(EDSS_DESC), "The patient is classified as " + str(RRMS) + " with a probability of 80%",
                         "The missing values that were filled automatically by the model are: " + missing_values]

                messagebox.showinfo('Multiple Sclerosis Prediction', "\n\n".join(lines), parent=self.master)
                return

    def check_user_data(self):
        # if gender.get() == 0 or OCB_value.get() == 0:
        #     return FALSE
        if self.validate_MRI() == FALSE or self.validate_age() == FALSE or self.validate_EDSS() == FALSE or self.validate_TIGIT() == FALSE:
            return FALSE
        if self.validate_LAG3() == FALSE or self.validate_PD1() == FALSE or self.validate_TIM3() == FALSE:
            return FALSE
        return TRUE


# run GUI
root = Tk()
my_gui = GUI(root)
root.mainloop()
