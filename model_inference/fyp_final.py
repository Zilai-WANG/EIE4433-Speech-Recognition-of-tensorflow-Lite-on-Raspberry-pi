
import sounddevice as sd
import numpy as np
import scipy.signal
import timeit
import python_speech_features
import RPi.GPIO as GPIO


import tensorflow as tf
############################
from tuning import Tuning
import usb.core
import usb.util
import time
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
##############################
import copy
#############################
import tkinter
##################
import socket
host = '192.168.1.210' #主机地址
port = 1026   # 自定义端口
print('socket setup')
# Parameters
debug_time = 0
debug_acc = 1
led_pin = 8
word_threshold = 0.9###
word_threshold2 = 0.5###
rec_duration = 0.5
window_stride = 0.5
sample_rate = 16000
resample_rate = 8000
num_channels = 1
num_mfcc = 16

model_path = 'fyp_pooling3.tflite'  #i5: 0 for wowl; 1 for help; 2 for others # i6 the help is collected from micro array instead of usb # i7 array in ic # i8 is scream normalized 
# Sliding window
window = np.zeros(int(rec_duration * resample_rate) * 2)

# GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
print("!!!!!!!!!!!!!!!!!!!!")
# Load model (interpreter)
interpreter = tf.lite.Interpreter(model_path)
#interpreter = Interpreter(model_path)
print("!!!!!!!!!!!!!!!!!!!!")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details)
######################################
def tk(x,y,txt,ss,message):
    root = tkinter.Tk()
    root.title(message)
    root.geometry('500x300+{}+{}'.format(x,y))

    #richText=tkinter.Text(root,height = 8,width=380)
    richText = tkinter.Label(root, text=txt, bg='red', font=('Arial', 12), width=100, height=60)
    richText.place(x=10,y=10,width=250,height=250)

   # richText.pack()
    #richText.insert('1.0',txt)

    root.after(ss,root.destroy)
# Decimate (filter and downsample)
def decimate(signal, old_fs, new_fs):
    
    # Check to make sure we're downsampling
    if new_fs > old_fs:
        print("Error: target sample rate higher than original")
        return signal, old_fs
    
    # We can only downsample by an integer factor
    dec_factor = old_fs / new_fs
    if not dec_factor.is_integer():
        print("Error: can only decimate by integer factor")
        return signal, old_fs

    # Do decimation
    resampled_signal = scipy.signal.decimate(signal, int(dec_factor))

    return resampled_signal, new_fs

# This gets called every 0.5 seconds
def sd_callback(rec, frames, time, status):

    GPIO.output(led_pin, GPIO.LOW)

    # Start timing for testing
    start = timeit.default_timer()
    
    # Notify if errors
    if status:
        print('Error:', status)
    
    # Remove 2nd dimension from recording sample
    rec = np.squeeze(rec)
    #normalization
    xx = copy.deepcopy(rec)
    xx = xx - np.mean(xx)  # 消除直流分量
    x = xx / np.max(np.abs(xx))  # 幅值归一化
    rec = 1.45*x
    #print("after normalization,length = {} samples,  dtype = {}".format(*rec.shape,rec.dtype))
    # Resample
    rec, new_fs = decimate(rec, sample_rate, resample_rate)
    
    # Save recording onto sliding window
    window[:len(window)//2] = window[len(window)//2:]
    window[len(window)//2:] = rec

    # Compute features
    mfccs = python_speech_features.base.mfcc(window, 
                                        samplerate=new_fs,
                                        winlen=0.032,
                                        winstep=0.010,
                                        numcep=num_mfcc,
                                        nfilt=26,
                                        nfft=512,
                                        preemph=0.98,
                                        ceplifter=0,
                                        appendEnergy=False,# noise
                                        winfunc=np.hanning)
    mfccs = mfccs.transpose()

    # Make prediction from model
    in_tensor = np.float32(mfccs.reshape(1, mfccs.shape[0], mfccs.shape[1], 1))
    interpreter.set_tensor(input_details[0]['index'], in_tensor)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    #val = output_data[0][0]
    top_index = np.argmax(output_data[0])
    val = output_data[0][top_index]
    val2 = output_data[0][1] # help word accuracy
    val1 = output_data[0][0] # scream word scream
    #print('val2 is:', val2)
    #print('val3 is:', val3)
    if val2 > word_threshold2 or val1>word_threshold:
        #print('Index is: ',top_index)
        #GPIO.output(led_pin, GPIO.HIGH)
        
             
        if(val2 > word_threshold2 ):
            print("Help detected!")
            #tk(1200,1600,'Content for help!!!',5000,'warning for help')
            #tkinter.mainloop()
            if (dev): 
             Mic_tuning = Tuning(dev)
             print ("DOA is:", Mic_tuning.direction)
             #print(type(Mic_tuning.direction))
             client = socket.socket()
             #print("tst2")
             client.connect((host, port)) #连接主机
             #print("tst")
             s = 'help,'+str(Mic_tuning.direction)
             s = s.encode()
             client.send(s)   #发送给主机信息
             data = client.recv(1024)  #接收主机回复信息
             print ("DOA_sent is:", data.decode())
             
            
                
                 
        elif val1 > word_threshold:
            print("scream detected")
            #tk(60,80,'Content for screaming!!!!',3000,'warning for screaming')
            #tkinter.mainloop()
            if (dev):
             Mic_tuning = Tuning(dev)
             print ("DOA is:", Mic_tuning.direction)
             #print(type(Mic_tuning.direction))
             client = socket.socket()
             #print("tst2")
             client.connect((host, port)) #连接主机
             #print("tst")
             s = 'scream,'+str(Mic_tuning.direction)
             #s = 'help,'+str(Mic_tuning.direction)
             s = s.encode()
             client.send(s)   #发送给主机信息
             data = client.recv(1024)  #接收主机回复信息
             print ("DOA_sent is:", data.decode())
        
    if debug_acc:
        print('matrix:',output_data[0])
    
    if debug_time:
        print(timeit.default_timer() - start)

# Start streaming from microphone
with sd.InputStream(channels=num_channels,
                    samplerate=sample_rate,
                    blocksize=int(sample_rate * rec_duration),
                    callback=sd_callback):
    while True:
        pass