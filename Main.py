# BEGINNING OF SCRIPT

import pandas as pd
import os
import pathlib
import moviepy.editor as mvp
import json
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class Main:
    def __init__(self, master):
        """
            Implements a Tkinter GUI to enable splitting operation

            Arguments:
            master -- Tkinter window instance

            Returns:
            Null.

        """

        self.master = master

        global excel_link
        excel_link = ""

        global videobaselink
        videobaselink = ""

        global default_dir_link
        default_dir_link = ""

        global p
        p = pathlib.Path(os.path.expanduser("~"))

        mainframe = tk.Frame(self.master, width=650, height=550, bg="#f8f8f8")
        mainframe.pack(fill=tk.BOTH)

        # --------------- Labels ---------- #

        default_dir_label = tk.Label(mainframe, text="Destination: ", font="Times 15 bold", bg="#f8f8f8", fg="#101010")
        default_dir_label.place(x=30, y=50)
        self.ent_show_dir = tk.Entry(mainframe, font="Times 15 bold", width=35)
        self.ent_show_dir.insert(0, p)
        self.ent_show_dir.place(x=170, y=52)

        default_excel_label = tk.Label(mainframe, text="Excel Link: ", font="Times 15 bold", bg="#f8f8f8", fg="#101010")
        default_excel_label.place(x=30, y=150)
        self.ent_show_excel = tk.Entry(mainframe, font="Times 15 bold", width=35)
        self.ent_show_excel.insert(0, p)
        self.ent_show_excel.place(x=170, y=152)

        default_video_label = tk.Label(mainframe, text="Video Link: ", font="Times 15 bold", bg="#f8f8f8", fg="#101010")
        default_video_label.place(x=30, y=250)
        self.ent_show_video = tk.Entry(mainframe, font="Times 15 bold", width=35)
        self.ent_show_video.insert(0, p)
        self.ent_show_video.place(x=170, y=252)

        default_sheet_label = tk.Label(mainframe, text="Sheet Name: ", font="Times 15 bold", bg="#f8f8f8",
                                       fg="#101010")
        default_sheet_label.place(x=30, y=350)

        self.selection_combo = tk.StringVar()
        self.sheet_combo = ttk.Combobox(mainframe, textvariable=self.selection_combo, state='readonly')
        self.sheet_combo.place(x=170, y=350)


# ----------- Buttons ----------- #

        button_excel = tk.Button(mainframe, text="Choose", font="Arial 12 bold", width=7, command=self.openexcel)
        button_excel.place(x=530, y=150)
        button_video = tk.Button(mainframe, text="Choose", font="Arial 12 bold", width=7, command=self.openvideo)
        button_video.place(x=530, y=250)
        button_split = tk.Button(mainframe, text="Split", font="Arial 12 bold", width=15, command=self.button_split)
        button_split.place(x=240, y=420)
        button_dir = tk.Button(mainframe, text="Choose", font="Arial 12 bold", width=7, command=self.opendir)
        button_dir.place(x=530, y=49)

    def button_split(self):

        """
            Implements a function to call split function.

            Arguments:
                self

            Returns:
                Null.

        """

        global excel_link, videobaselink
        sheetname = self.selection_combo.get()
        classlist, datadictionary = self.read(excel_name=excel_link, sheet_name=sheetname)
        self.split(classlist=classlist, datadictionary=datadictionary)

    def openvideo(self):

        """
            Implements a function to open filedialog and to facilitate user input(Video Directory Link).

            Arguments:
                self

            Returns:
                Null.

        """

        global p
        global videobaselink
        videobaselink = filedialog.askdirectory(initialdir=p, title="choose the video directory")
        self.ent_show_video.delete(0, 'end')
        self.ent_show_video.insert(0, videobaselink)

    def openexcel(self):

        """
            Implements a function to open filedialog and to facilitate user input(Excel sheet Link).

            Arguments:
                self

            Returns:
                Null.

        """

        global excel_link
        global p
        excel_link = filedialog.askopenfilename(initialdir=p, title="choose your excel sheet")
        self.ent_show_excel.delete(0, 'end')
        self.ent_show_excel.insert(0, excel_link)
        data = pd.ExcelFile(excel_link)
        sheetnames = data.sheet_names
        self.sheet_combo.config(values=sheetnames)

    def opendir(self):

        """
            Implements a function to open filedialog and to facilitate user input(Directory Link).

            Arguments:
                self

            Returns:
                Null.

        """

        global default_dir_link
        global p
        default_dir_link = filedialog.askdirectory(initialdir=p, title="choose the destination directory")
        self.ent_show_dir.delete(0, 'end')
        self.ent_show_dir.insert(0, default_dir_link)

    def read(self, excel_name, sheet_name):

        """
            Implements a function to read the excel sheet using pandas
            and to convert the data into dictionaries and list

            Arguments:
                self

            Returns:
                classlist -- List containing the names of the classes(actions) in that particular sheet
                datadictionary -- Dictionary that encapsulates the entire information about Excel sheet
                                      keys -- "video_des + str(index)", "timeline + str(index)",
                                              "actions + str(index)" , "subline" + str(index)

        """

        data = pd.read_excel(excel_name, sheet_name)

        video_index = []
        videoname_index = []
        videospecs_index = []
        datetime_index = []
        viewpoint_index = []
        optype_index = []
        videolength_index = []
        class_index = []
        sub_index = []

        for j in data.columns:
            for i in data.index:

                if data[j][i] == "Main":
                    video_index.append([j, i])
                elif "Working type list <Verb + Object>" in str(data[j][i]):
                    class_index.append([j, i])
                elif "Operator No" in str(data[j][i]):
                    optype_index.append([j, i+1])
                elif "View points" in str(data[j][i]):
                    viewpoint_index.append([j, i+1])
                elif "Manual annotated video name :" in str(data[j][i]):
                    videoname_index.append([j, i])
                elif data[j][i] == "The data time":
                    datetime_index.append([j, i + 1])
                elif data[j][i] == "Video Length":
                    videolength_index.append([j, i + 1])
                elif "Video spec :" in str(data[j][i]):
                    if "25Mbps" in str(data[j][i]):
                        videospecs_index.append([j, i])
                elif "sub" in str(data[j][i]).lower():
                    sub_index.append([j, i])

        classdata = data[class_index[0][0]].values.tolist()

        classlist = []
        for i in range(class_index[0][1] + 1, len(classdata)):
            if str(classdata[i]) != 'nan':
                classlist.append(classdata[i].split(".")[0])

        # converting data to create data dictionary for annotations as output (output variable: datadictionary)

        datadictionary = {}

        for j in range(len(video_index)):

            name_col1 = video_index[j][0].split(' ')[0] + " " + str(int(video_index[j][0].split(' ')[1]) - 1)
            name_col2 = video_index[j][0]
            name_col3 = sub_index[j][0]
            column_1 = data[name_col1].values.tolist()
            column_2 = data[name_col2].values.tolist()
            column_3 = data[name_col3].values.tolist()

            base_video_description = {"Videoname": data[videoname_index[j][0]][videoname_index[j][1]].split(": ")[1],
                                      "Videospecs": data[videospecs_index[j][0]][videospecs_index[j][1]].split(": ")[1],
                                      "datetime": data[datetime_index[j][0]][datetime_index[j][1]],
                                      "Operatorno": data[optype_index[j][0]][optype_index[j][1]],
                                      "ViewPoints": data[viewpoint_index[j][0]][viewpoint_index[j][1]],
                                      "Videolength": str(data[videolength_index[j][0]][videolength_index[j][1]])}

            timeline = []
            actionline = []
            subline = []
            for i in range(int(video_index[j][1] + 1), len(column_1), 2):
                if str(column_1[i]) != 'nan':
                    timeline.append(self.convert_to_seconds(time=column_1[i]))

            for i in range(int(video_index[j][1] + 2), len(column_2) - 1, 2):
                if str(column_2[i]) != 'nan':
                    actionline.append(str(column_2[i].split('.')[0]))

            for i in range(int(video_index[j][1] + 2), len(column_3) - 1, 2):
                if str(column_3[i]) != 'nan':
                    subline.append(str(column_3[i].split('.')[0]))
                else:
                    subline.append("null")

            datadictionary["video_des" + str(j)] = base_video_description
            datadictionary["timeline" + str(j)] = timeline
            datadictionary["actions" + str(j)] = actionline
            datadictionary["subline" + str(j)] = subline

        return classlist, datadictionary

    def split(self, classlist, datadictionary):

        """
            Implements a function to enable the splitting of video along with the creation of JSON files.

            Arguments:
                self
                classlist      -- List containing the names of the classes(actions) in that particular sheet
                datadictionary -- Dictionary that encapsulates the entire information about Excel sheet
                              keys -- "video_des + str(index)", "timeline + str(index)",
                                      "actions + str(index)" , "subline" + str(index)
            Returns:
                Null


        """

        global videobaselink
        global default_dir_link

        dictionary, dictionary2 = self.create_directory(classlist=classlist)
        tempdictionary = self.extractjson(end=len(dictionary), dictionary2=dictionary2)
        templist = tempdictionary.keys()
        jsondictionary = {}

        for i in range(len(classlist)):
            jsondictionary[str(classlist[i])] = []

        for i in templist:
            jsondictionary[str(i)] = tempdictionary[str(i)]

        print(datadictionary.keys())
        for j in range(0, len(datadictionary), 4):

            video_des = datadictionary["video_des"+str(int(j/3))]
            annotations = datadictionary["timeline"+str(int(j/3))]
            actions = datadictionary["actions"+str(int(j/3))]
            subclass = datadictionary["subline" + str(int(j / 3))]
            video_link = os.path.join(videobaselink, video_des["Videoname"])
            video_des["path"] = str(os.path.join(video_link.split('/')[-2], video_link.split('/')[-1]))
            videojson = []

            looplength = len(actions)

            for i in range(looplength):

                try:
                    destination = str(os.path.join(default_dir_link, dictionary[str(actions[i])]))
                    existing_elements = int(len(os.listdir(destination))/2)
                    split_video_name = "instance" + str(existing_elements + 1) + ".mp4"
                    final_video_link = str(os.path.join(destination, split_video_name))
                    relative_path = str(os.path.join(destination.split('/')[-2],
                                                     destination.split('/')[-1], split_video_name))
                    diff = str(float(annotations[i+1]) - float(annotations[i]))+" Secs"
                    video = mvp.VideoFileClip(video_link).subclip(float(annotations[i]), float(annotations[i + 1]))
                    # to change the fps add eg: fps=50
                    video.write_videofile(final_video_link)
                    frames = int(video.fps * video.duration)

                    data = {"videoname": split_video_name,
                            "duration": diff,
                            "frames": frames,
                            "path": relative_path,
                            "class": str(actions[i]),
                            "classid": dictionary[str(actions[i])],
                            "subclass": str(subclass[i]),
                            "operatorno": video_des["Operatorno"],
                            "viewpoints": video_des["ViewPoints"],
                            "basevideodes": {
                                "videoname": video_des["Videoname"],
                                "duration": video_des["Videolength"],
                                "videospecs": video_des["Videospecs"],
                                "datetime": video_des["datetime"],
                                "path": video_des["path"]
                            }
                            }

                    try:
                        videojson.append(data)
                        dirname = os.path.join(default_dir_link, "Videojson")
                        if not os.path.exists(dirname):
                            os.mkdir(dirname)
                        jsonpath2 = os.path.join(dirname, str(video_des["Videoname"]).split(".")[0] + ".json")
                        self.create_json(data=videojson, path=jsonpath2)
                    except Exception as e:
                        message = "Exception : " + str(e) + " Comments:" + "Cannot create Video JSON File " + \
                                  annotations[i] + " " + annotations[i + 1] + " " + actions[i] + " "
                        print(message)
                        self.create_log_file(message)

                    try:
                        textfilename = split_video_name.split(".")[0] + ".json"
                        jsonpath = os.path.join(destination, textfilename)
                        self.create_json(data=data, path=jsonpath)
                    except Exception as e:
                        message = "Exception : " + str(e) + " Comments:" + "Cannot create Clip JSON File " + \
                                  annotations[i] + " " + annotations[i + 1] + " " + actions[i] + " "
                        print(message)
                        self.create_log_file(message)

                    try:
                        jsondictionary[str(actions[i])].append(data)
                        path2 = os.path.join(default_dir_link, str(dictionary[str(actions[i])] + ".json"))
                        self.create_json(data=jsondictionary[str(actions[i])], path=path2)
                    except Exception as e:
                        message = "Exception : " + str(e) + " Comments:" + "Cannot create Class JSON File " + \
                                  annotations[i] + " " + annotations[i + 1] + " " + actions[i] + " "
                        print(message)
                        self.create_log_file(message)

                except Exception as e:
                    message = "Exception : " + str(e) + " Comments:" + "cannot be clipped " + annotations[i]+" " + \
                              annotations[i+1] + " " + actions[i]+" "
                    print(message)
                    self.create_log_file(message)

    def create_json(self, data, path):
        """
            Implements a function to create a JSON file.

            Arguments:
                self
                data -- Json Data that has to be displayed in the JSON file
                path -- path link where the json file has to be created

            Returns:
                       Null


        """

        with open(path, 'w') as outfile:
            json.dump(data, outfile)

    def create_directory(self, classlist):
        """
            Implements a function to create a class directories.

            Arguments:
            self
            classlist -- List containing the names of the classes(actions) in that particular sheet

            Returns:
            Null


        """

        global default_dir_link
        sheetname = "Work type"
        dictionary, dictionary2 = self.classnametoindex(excel_name=excel_link, sheet_name=sheetname)

        for list1 in classlist:

            list1 = dictionary[str(list1)]
            dirname = os.path.join(default_dir_link, list1)

            if not os.path.exists(dirname):
                os.mkdir(dirname)

        return dictionary, dictionary2

    def convert_to_seconds(self, time):
        """
            Implements a function to convert minutes:seconds:milli-seconds to seconds

            Arguments:
                self
                time -- Variable containing the annotations in (minutes:seconds:milli-seconds)

            Returns:
                a string that contains time in seconds


        """

        minute = time.hour
        second = time.minute
        milli = time.second

        return str(((minute*60 + second)*1000+milli)/1000)

    def classnametoindex(self, excel_name, sheet_name):

        """
            Implements a function to create index to classname dictionary and vice-versa

            Arguments:
                        self
                        time -- Variable containing the annotations in (minutes:seconds:milli-seconds)

            Returns:
            dictionary  -- dictionary that contains classname to index mapping
            dictionary2 -- dictionary that contains index to classname mapping


        """
        data = pd.read_excel(excel_name, sheet_name)

        dictionary = {}
        dictionary2 = {}
        column1 = data["Unnamed: 8"]
        column2 = data["Unnamed: 7"]

        for i in range(len(column1)):
            if str(column1[i]) != 'nan':
                dictionary[str(column2[i]).split(".")[0]] = str(i - 1)
                dictionary2[str(i - 1)] = str(column2[i]).split(".")[0]

        return dictionary, dictionary2

    def extractjson(self, end, dictionary2):

        """
            Implements a function to create index to classname dictionary and vice-versa

            Arguments:
                self
                end -- Variable containing the annotations in (minutes:seconds:milli-seconds)
                dictionary2 -- dictionary that contains index to classname mapping

            Returns:
                dictionary -- dictionary that contains the extracted data in JSON files

        """
        global default_dir_link
        dictionary = {}
        for i in range(1, end + 1):
            temp = str(i) + ".txt"
            link = os.path.join(default_dir_link, temp)

            try:
                f = open(link, "r")
                jsoncontents = f.read()
                contents = eval(jsoncontents)
                dictionary[str(dictionary2[str(i)])] = contents
                f.close()
            except Exception as e:
                message = "Exception : " + str(e) + " Comments:" + "Cannot parse File name " + str(temp)
                self.create_log_file(message)

        return dictionary

    def create_log_file(self, string):

        global default_dir_link
        link = os.path.join(default_dir_link, "log.txt")
        time = datetime.datetime.now()
        new_contents = str(time) + " : " + string
        new_contents = new_contents + '\n'

        try:
            f = open(link, "a")
            f.write(new_contents)
            f.close()
        except Exception as e:
            print("Exception : " + str(e) + " Comments:" + "Cannot write into Log file ")


def main():
    """
       Implements a main function for the Class Main

    """
    root = tk.Tk()
    root.geometry("650x550+300+250")
    root.resizable(False, False)
    root.title("Video Splitter")
    Main(root)
    root.mainloop()


if __name__ == '__main__':
    main()

# END OF SCRIPT