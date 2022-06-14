__To Get Started__

To start using VIR-Atlas you will need to clone or download the source code. Using the terminal navigate to the directory you want to place the repository containing VIR-Atlas and run the following command:

```git clone git@github.com:tygoetsch/vir-atlas.git```

If you don't have git and feel like it's ~~too complicated~~ beneath you then just download the source code using the download button. You will have options. 

After you have a copy of the repository on your local computer make sure to have the following libraries installed. VIR-Atlas depends on these to operate:

- python3
- tkinter
- numpy
- PIL
- scipy.spatial
- pickle
- satsearch


__To Run VIR-Atlas__

VIR-Atlas is a GUI-based application, however to start using it you'll need the terminal (command prompt for Windows users). 

Open the terminal and navigate to the repository containing VIR-Atlas. Run the following command:
```python3 main.py```

Once the application window opens ***do not close it.*** If you do you'll need to repeat the "To Run VIR-Atlas" section. Just minimize the terminal window to get it out of the way.


__To Use VIR-Atlas__

When the application window appears you will be greeted with the prompt "Welcome to VIR-Atlas! To get started, go to Files -> Open New File". Contrary to what you may be thinking, this *is* in fact what you should do to start using VIR-Atlas.

There are three buttons on the left-hand side of the menu-bar at the top of the main window: "File", "View", and "Satellite".

**File:**

File allows you to Open, Save, and Load data files associated with VIR-Atlas. You'll need to be a little patient with VIR-Atlas when you initially load data files into the application. It will take a few seconds for the maps to load on the screen and during this period the application will be unresponsive. This is because VIR-Atlas is currently processing the data and generating all of the maps. It's fine, just look out the window and remember to blink a few times while this is happening. Look at the section titled **Data Files** for more information about the types of files that VIR-Atlas supports. 

**File->Open New Files:**

Open New Files will present two screens to you. The first prompts you for the STELLA data file. The second prompts you for the drone flight data. 

**File->Load Previous File:**

Load Previous File presents you with a screen that prompts you for a VMAP file.

**File->Save File:**

Save File allows you to save the currently loaded map to a VMAP file.


**View:**

View is the way you swap between maps. When the data files have been loaded (see previous section **File**) you will notice the area of the screen which originally greeted you will update and display your specified data using the default map, Temp. There are currently 8 different kinds of maps to peruse through, Visual, NIR, Temp, Surface vs Air Temp, NDVI, EVI, SAVI, MSAVI. 

**Satellite:**

Satellite has two features at the moment. One involves satellites, the other doesn't. You can decide which is which. For the satellite functionality you'll see that the top right area of the main window has a mini-window, that is the satellite image window.

**Satellite->Get Satellite Image:**

Get Satellite Image will pull a satellite image from an external source that is mapped to the bounding box of the area the drone traversed. This image will appear in the satellite image window.

**Satellite->Upload Aerial Image**

Upload Aerial Image lets you load your own custom image to VIR-Atlas in the circumstance that your drone was capable of taking some snazzy aerial pictures during the flight, or if you like to have pictures of your ~~cats~~ children right next to your forestry work. The choice is yours.

__Using Annotations__

Annotations are a groovy feature we added that allow you to make a note about a specific point on the map. To use annotations you just right click on the map and you will be presented with a dialogue box. Depending on whether you clicked near a map point (visually represented by a black arrow on the flight path of the drone) you may be presented with data we have decided may be relevant for you to view. At the bottom of the dialogue box is a text entry field where you can jot down notes or complain about your coworkers. You will be able to save this annotation and see that a little pin has appeared on the screen where the annotation was made. 

There is also an annotations box on the right, underneath the ~~cat~~ satellite image. This box will update with a new line representing each annotation that you place on the screen. From this box you can edit or delete annotations that have been made.

__Directory Structure__

Right now there are a lot of files for VIR-Atlas, but you can ignore most of those unless you are tired of the fact that the greeting says "Files -> Open New File" but the button in question says "File". You're welcome.

The only folder you are likely going to be interested in is the **Data Files** folder. As it sounds, this is where you are *suggested* to keep your STELLA, drone, and VMAP files. There are already some in this folder that you can use to play around with the application before you start doing whatever you plan on doing with it.

__Data Files__

If you didn't get confused by the fact that we have a folder titled "Data Files" as well as a section in this User Guide titled __Data Files__, then you likely noticed that the greeting when you start VIR-Atlas says "Files -> Open New File", but the button in question says "File". Good for you. The files that VIR-Atlas works with come in three forms: TXT, CSV, and VMAP. The TXT and CSV files are used together whereas the VMAP file is a standalone. Read further for reasons.

**TXT, CSV, STELLA, Drone, Hakuna, Matata**

When you select the **FILE->Open New Files** option in the menu bar, VIR-Atlas prompts for two data files. The first prompt is for the TXT file produced by STELLA. The second prompt is for a CSV file produced by the drone. During development we used the **DJI Phantom 4** drone to conduct our test flights. There are several example files in the "Data Files" directory which you can use to compare with the output from *your* drone. If your drone's output file is formatted differently the recommendation is to convert your file into the appropriate format and column placement. If your drone **doesn't produce** any output files you will need to get a new drone. We use the longitude, latitude, and timestamp from the drone data file to generate our maps. Sorry.

**VMAP**

When you save a VIR-Atlas map to file it generates a VMAP file. This is just a [pickle dump](https://docs.python.org/3/library/pickle.html), so those of you that like pickles will like this. We place a ".vmap" extension on the filename for ease of finding in the future.

Saving your generated map to a VMAP file makes it easy for the next time you want to start up VIR-Atlas and look at some data set you already accessed in the past. When you select the **FILE->Load Previous File** option in the menu bar, VIR-Atlas prompts for the aforementioned VMAP file type. If you try to load something else you *will* be met with the fact that no other file type will appear in the browser window.

### Contributors:
* Sophia Novo-Gradac
* Marisa Loraas
* Franklin Keithley
* Brynn Charity
* Tenise Stansfield
* Timothy Goetsch
