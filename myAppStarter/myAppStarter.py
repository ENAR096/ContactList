
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import shutil,os

# Global variables section - add variables that are required

path = 'images' # folder with friend's images

# functions and sub-functions to manage the various buttons and user inter-action
# see the coursework sepcification

def showFriends():
    # once show freind button clicked:
    # 1. call function 'friendsFrame()' that will take care the creation of a new frame that will show to the user all the friend buttons
    # 2. call function 'processPath()' that will check the how many images are available in the folder.
    friendsFrame()    
    processPath()  
    # after button clicked, 'Show friend' will be disabled and 'Clear all' button will be enabled.
    # in this way, we will avoid situation where the button gets clicked multiple times and loading the same images every time.
    bFriend['state'] = DISABLED
    bFriend['image'] = imgList[5] 
    bClearAll['state'] = NORMAL
    bClearAll['image'] = imgList[2] 

def friendButton(head, count):
    
    friendFolderPath = path +'\\'+ head # get the unique path for each friend. 'head' variable contains the name of the image (with no extension)   
    
    row = 2 # start placing the items in the second line of the grid
    
    #use the os module and use his method path.exists to check if the specified path exists
    if os.path.exists(friendFolderPath):
        # check if path specified exist
        # if True: show all friends for the specific friend   
        if  len(os.listdir(friendFolderPath))==0:
            messagebox.showinfo('','Folder exists but it is empty')       
        
        for file in os.listdir(friendFolderPath): #get the list of directories
            
            #split name of the file, head= name of the friend, tail= extension of the file
            (head, tail) = os.path.splitext(file)         
            if tail.lower() not in ['.png', '.jpg']: #skip all other file format
                
                continue           
            

            fullFileLoc = friendFolderPath + '\\' + file  #save the image's address into fullFilLoc variable          
            friendPhoto = PhotoImage(file=fullFileLoc) # method photoimage, will take as argument the location of our image. This method will keep the image visible all the time. 
            # avoiding situation where the image is load and mode right after in the garbage collector. 
            
            friendPhoto = friendPhoto.subsample(2,2) #change size of the image

            #the image of the friend of friend, will be shown as Label widget + the name of the friend. Compaund attribute, place the image on top of the friend's name
            friendLabel = ttk.Label(friendLabelFrame, text= head.upper(),image = friendPhoto, compound='top', background='#2C7865', foreground='white',font=('Helvetica', 8,'bold'))
            
            # now placing the friends of friend under the same column. Increase count depending on the button friend clicked
            friendLabel.grid(row=row, column= count+1, padx=6, pady=6, ipadx=1, ipady=2, sticky = N)
            friendLabel.image=friendPhoto # pass the friend image in the label friend
            #increse row, so all friend of friends are place one under the other in order.
            row +=1
            
        # after all images are shown, create a button to close the friend tab
        # lambda function used to call function after button clicked
        clearFriendButton = ttk.Button(friendLabelFrame, text='X', width=1, command= lambda: closeFriendsTab(count+1)) 
        clearFriendButton.grid(row=row, column= count+1) #place the button in the right column, according to which friend button is clicked
           
       # if False: show message on screen for the user  
    else:
        messagebox.showwarning('No friends', f"The folder: {head} is empty, no friends available")
        pass
    
    
    buttonPressed = count//2 #get the index of the button pressed in the list
    x=friendButtonList[buttonPressed] # x contains the button pressed
    x['state']=DISABLED # proceed to disabled the button after it has been clicked 

def clearAll():

    global friendButtonList #get the list of our friends
    friendButtonList.clear() #empty the list of old friend list addresses. 

    bFriend['state'] = NORMAL #enable the show friend button
    bFriend['image'] = imgList [6]
    bClearAll['state'] = DISABLED # disable the clear All button
    bClearAll['image'] = imgList[1]
    friendLabelFrame.destroy() # destroy the friend frame below 

def delFriend():
    # delFile will contain the path of the image we want to delete 
    delFile = filedialog.askopenfilename(
        initialdir='./images',
        title='Select a file to delete',
        filetypes=(('Image files', '*.png'), ('All files', '*.*')))    
    
    if delFile:
        #confirm deletion
        check = messagebox.askyesno(
            title='Delete File?',
            message='Are you sure you want to delete this file?')
        
        if check == True:
            filename = os.path.basename(delFile) #get the file path of image selected
            os.remove(delFile)
            messagebox.showinfo('Delete a file', f"{filename} deleted")
        else:
            messagebox.showinfo('Delete a file', 'Changed your mind, file not deleted')

    
    clearAll() # this will load the friend frame above the menu pannel    
    showFriends() # this function 

def addFriend():
    #get the image we want to add
    filetypes = (('Image files', '*.png;*.jpg;*jpeg;*gif'), ('All files', '*.*'))  
    #get the path of our image 
    selectFile = filedialog.askopenfilename(initialdir='./', title='Select File', filetypes= filetypes)

    if selectFile:
        
        check= messagebox.askquestion('Add a new File', 'Do you want to add a new file?')
        if check == 'yes':
            #check file extension
            (head,tail) = os.path.splitext(selectFile)
            if tail.lower() in ('.png', '.jpeg'):
                shutil.copy(selectFile, './images/')
                #extract the file name from full path
                filename=os.path.basename(selectFile)
                messagebox.showinfo('Add a new File', f"{filename} added")
            else:
                messagebox.showwarning('Add a new File', 'Not an image file, not added')
        else:
            messagebox.showinfo('Add a new File', 'Changed your mind, file not added')
    
    clearAll() # this will load the friend frame above the menu pannel    
    showFriends() # this function 
    
def quitApp():

    answer = messagebox.askquestion('Confirm', 'Are you sure you want to quit?') #create a pop up window, ask user if wants to quit
    #check answer clicked
    if answer =='yes': #close app window if answer is yes
        myApp.destroy()
    else: #show message to user that operation has been cancelled
        messagebox.showinfo('Information','Operation cancelled!')

def friendsFrame():
    # function that will redefined the friend frame widget
    global friendLabelFrame
    style.configure('FriendFrame.TLabelframe', background='#FF9800', borderwidth=5)
    friendLabelFrame= ttk.LabelFrame(myApp, text='Friends List', style='FriendFrame.TLabelframe')
    friendLabelFrame.place(in_=myApp, relx=0.05, rely= 0.15) #place the frame according to relative app window size 

def displayImg(item, count):
    col = count * 2  #get the number of total friends and multiply by 2, it is needed to place the images friends of friend in the same column  
    
    (head, tail)= os.path.splitext(item) # get name and extension of image    
    itemLoc = path + '\\'+ item  # contains image address 
    friendPhoto = PhotoImage(file=itemLoc) # photoimage is used to display the image
    friendPhoto = friendPhoto.subsample(2,2) # reduce image size to half
       
    bFriendOfFriend = ttk.Button(friendLabelFrame, image = friendPhoto, command= lambda: friendButton(head, col-2))
    
    # use lamda function will allow us to show a friends of friend only when the button for that color is clicked
    # the function friendButton take 2 parameters, the name of the friend(head) and the column where the images will be loaded    

    bFriendOfFriend.image = friendPhoto # make sure the image has not been removed by garbage collector, so it keeps a reference
    friendButtonList.append(bFriendOfFriend) #save all button friends created in a list, that we will need it for the function friendButton()   
    bFriendOfFriend.grid(row= 0, column=col-1, padx= 7) #place each button friend in the grid    
    bFriendName = ttk.Label(friendLabelFrame, text= head.upper() + ' Button', width =10, font=('',8,'bold'), background='#2C7865', foreground='white', anchor='center')
    bFriendName.grid(row=1, column = col-1, padx=5, pady=5,ipadx=5, ipady=5, sticky=EW)
    
def processPath():
    global path #it's variable containing the path of images' folder, declared at the beginning     
    if os.path.exists(path): # check if the location exists
        
        if os.path.isdir(path): #check if it is a directory
                       
            count=0 # keep track of how many image files are dealt with
            for item in os.listdir(path): # iterate for every file inside the folder
                
                (head,tail)=os.path.splitext(item) # split the name of file and its extension 
                
                if tail.lower() not in ['.png', 'jpeg']: # check file extension, if not a img then skip step
                    continue
                count +=1 # if it's an image then increase count of images found
                                
                displayImg(item,count) # this function will process the images found and it will show inside the Friends Frame
              
        else:
            print('Path exists but no folders')
    else:
        print('Path does not exist')   

def closeFriendsTab(col):    
    widgets = friendLabelFrame.grid_slaves(column=col) #widgets list will contain all the label of Friends of a specific column
    num_widgets=len(widgets)
   
    #start to iterate from 2nd position of the list of widgets, the loop will remove
    #all friend inside the list, but it will keep the friendButton and its label 

    for widget in widgets[:num_widgets-2]: 
        
        widget.grid_remove()

    buttonPressed = col//2 #get the index of the button pressed in the list   
    x=friendButtonList[buttonPressed] # x contains the button pressed
    x['state']=NORMAL # proceed to disabled the button after it has been clicked


# Basic Window for your app
imgList = [] # contains images of buttons

myApp = Tk()
myApp.title("Image display app by: Enrico Narciso - w19689317")
myApp.geometry("1300x900")
myApp.configure(background='#D9EDBF')
myApp.resizable('true','true') #size of the window can be changed by user

imgPath = 'menuImg'
for file in os.listdir(imgPath):
    fileLoc = imgPath + '/' + file
    menuImg = PhotoImage(file=fileLoc)
    menuImg = menuImg.subsample(1,1)
    imgList.append(menuImg)
    
 

style = ttk.Style() # create instance for widget style
style.theme_use('alt')


# Code to configure styles for your ttk widgets
# write code below to create styles for you buttons, labels, frames, etc

style.configure('mainMenuFrame.TLabelframe', background='#FF9800', borderwidth=5)

style.configure('TButton', background='#2C7865', foreground='white',font=('Helvetica', 12, 'bold'), width=16, borderwidth=2, focusthickness=2, focuscolor='#D9EDBF')
# map style for active state of TButton widgets to change background color 
style.map('TButton', background=[('active','#FFC300')])

# Create a frame(mainMenu) that will hold buttons to manage the app.

mainMenuFrame = ttk.LabelFrame(myApp, text = 'Main Menu', height= 40, width=350, style='mainMenuFrame.TLabelframe')
#mainMenuFrame.grid(row = 0, column= 0, padx= 5, pady=5)
mainMenuFrame.place(in_=myApp, anchor='n', relx=0.5, rely=0.02) #place the frame to the center of the window

# create buttons that have been described in the coursework specification and add to the frame above

bFriend         = ttk.Button(mainMenuFrame, text='Show Friend', style='TButton', image= imgList[6], command= showFriends)
bClearAll       = ttk.Button(mainMenuFrame, text='Clear All', style='TButton', image= imgList[1], state= DISABLED, command=clearAll)
bDeleteFriend   = ttk.Button(mainMenuFrame, text='Delete Friend', style='TButton', image= imgList[3], command=delFriend)
bAddNewFriend   = ttk.Button(mainMenuFrame, text='Add new friend', style='TButton',image= imgList[0], command=addFriend)
bQuit           = ttk.Button(mainMenuFrame, text='Quit', image= imgList[4], command=quitApp)

# place all buttons into the menu frame and adjust padding for all buttons 
i=0
for myButtons in mainMenuFrame.winfo_children():
    myButtons.grid_configure(row=0, column=i, padx= 5, pady= 5)
    i+=1

friendButtonList =[]
friendLabelFrame=ttk.LabelFrame()
bFriendOfFriend=ttk.Button()

myApp.mainloop()