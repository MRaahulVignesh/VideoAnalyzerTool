# VideoAnalyzerTool


#### Graphical User Interface to visualize and analyze the data

This GUI was a part of the project "Activity Recognition to detect actions in industries using Deep Learning"
The training data provided by the company was in Excel (xlsv) format where the annotations and the respective class label (the actions performed by the operator) were mentioned as the field variables. The name of the base video clip along with few other specifications (like date & time, video quality, video length) about the video were also specified in the Excel sheet. In order to make the process of splitting the video clips into respective class directories more advantageous and time-saving, we employed the benefits of python and few other open source packages (like Numpy, Scipy, Moviepy) to create a custom automated program.

There were also few other extra features that were added to the GUI Video Splitter. One such notable feature is the generation of JSON (JavaScript Object Notation) structure for each video sub-clips. This JSON file will help the user to analyze the data in a much different format other than visualizing it as a video file. By the generation of JSON file, we mean to generate clip wise JSON file, class wise JSON as well as video level JSON file. The clip wise JSON file is local to a particular clip inside the class directory and contains the information specific to that particular instance of the class label. Each time a sub-video is clipped from a base video file, the python program will call to automatically generate a JSON file structure that will be local to that particular clip as well as generate a class wise JSON file along with the video level JSON file. These three types JSON file can help us to analyze and visualize the data in a much border perspective.

The three level JSON files also gives us the flexibility to analyze the data in three different dimensions. Data analytics can be performed on the JSON scripts to capture few critical informations like maximum, minimum and average time taken by an action to be completed. These data analytics will help us in data processing, which can substantially improve the efficiency of the training the deep learning algorithm.

Overall, This GUI will import the Excel data and split the videos into sub clips that will be pushed into the respective directories (name of the directories are the respective class labels) along with the creation of clip wise ,class wise and video wise JSON files. In the end, an interactive user friendly graphical user interface (GUI) was built with the help of python Tkinter library to facilitate the process of video splitting and JSON file creation. Illustrations of the GUI has been portrayed in the next page. 

