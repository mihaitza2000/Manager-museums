#libraries
import pyautogui
from ttkwidgets.autocomplete import AutocompleteEntry
from tkinter import ttk
from tkinter import *
import ctypes, os, smtplib, mysql.connector, datetime, ssl, decimal, PIL.Image
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import tkinter.font as font
#global variables
museums_list = ["Medieval museum London", "Botanic museum Istambul", "Art museum Rome", 
                "Medieval museum Rome", "Botanic museum Berlin", "Art museum Berlin",
                "Medieval museum Madrid", "Botanic museum Madrid", "Art museum Budapest", 
                "Science museum Budapest", "Science museum Prague", "Science museum Prague"]
museums = ["Medieval", "Botanic", "Art", "Science"]
toggle, toggle2, user32, exception = 0, 1, ctypes.windll.user32, True
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
user_key, password_key =  "", ""
museum_types = os.listdir("./museums")
list_index = [i for i in range(len(museum_types))]
#variable for automatic fill
names_list = ["Andrei", "Alex", "Vlad", "Ana", "Ilie", "Stefan"]
surnames_list = ["Patrolea", "Alucai", "Stoleriu", "Apetrei", "Luchian", "Stolnicescu"]
ages_list = [i for i in range(80)]
genders_list = ["M", "F"]
numbers = "0123456789"
phones_list = ["07"+"".join([choice(numbers) for i in range(8)]) for i in range(100)]
codes_list = ["".join([choice(numbers) for i in range(6)]) for i in range(100)]