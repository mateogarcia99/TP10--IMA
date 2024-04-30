import numpy as np
from scipy import signal
from acoustics.signal import bandpass
from acoustics.bands import (octave_low, octave_high, third_low, third_high, octave, third)

def inv_sine_sweep(T,f1,f2,fs=48000):
    
    # T = duracion del Sine sweep
    # f1 = frecuencia inicial del barrido
    # f2 = frecuencia final del barrido
    # fs = frecuencia de muestreo
    
    t = np.arange(0, T*fs)/fs # vector temporal
    w1 = 2*np.pi*f1 # frecuencia angular inferior
    w2 = 2*np.pi*f2 # frecuencia angular superior
    R = np.log(w2/w1)
    K = T*w1/R
    L = T/R
    
    w=(K/L)*np.exp(t/L)
    m=w1/(2*np.pi*w)

    # Generacion de audio_data del filtro inverso
    inv_sine_sweep = m*np.sin(K*(np.exp(-t/L)-1))
    
    # Normalizado
    valor_max = max(abs(max(inv_sine_sweep)),abs(min(inv_sine_sweep)))
    inv_sine_sweep_norm = inv_sine_sweep / valor_max
    
    return inv_sine_sweep_norm


def mmfilt(audio_data,N):
    
    # aplica la tecnica de filtrado promedio movil utilizando scipy.signal.medfilt
    filtro_movil=signal.medfilt(audio_data,N)
    
    # aplica la transformada de hilbert utilizando scipy.signal.hilbert
    hilbert=signal.hilbert(filtro_movil)
    
    # obtiene la envolvente de la señal
    envolvente = np.abs(hilbert)
    
    #devuelve la señal suavizada
    return envolvente

def Escala_log(audio_data):
    # Valor maximo de la señal
    valor_max = max(abs(max(audio_data)),abs(min(audio_data)))
    # Conversion de los valores a dB
    normalizado=20*np.log10(audio_data/valor_max)
    return normalizado

def schroeder(señal,audio_fs,t=0):
    # genera un vector de ceros con la longitud de la cantidad de muestras del audio que contendra lo valores arrojados por la integral
    sch=np.zeros(len(señal))
    # Calcula los valores de la integral y los guarda en sch
    sch[::-1]=10*np.log10(np.cumsum(señal[::-1]**2)/np.sum(señal[::]**2))

    return sch

def schroeder_por_banda(audio_data,audio_fs): 
    audio_data=Escala_log(audio_data)
    señal_sch=[]# se inicializa el vector que contendra a todas las señales de schroeder
    # se genera un bucle for que aplica la integral de schroeder a todas las señales
    for i in range(len(audio_data)):
        señal=audio_data[i]
     #   señal_i=señal[0:t*audio_fs]
        sch=schroeder(señal,audio_fs)
        señal_sch.append(sch)
    # devuelve un vector que contiene todas las señales de schroeder
    return señal_sch

def ajuste_lineal(y,audio_fs):
    
    # y = valores de los puntos a los cuales se desea aplicar el ajuste
    # audio_fs = frecuecia de muestreo de los puntos
    
    n=len(y) # cantidad de puntos
    x=np.linspace(0,len(y)/audio_fs,len(y)) # genera un vector temporal al cual se ajustaran los puntos
    sxx=np.sum(x**2) # suma de todos los valores del vector x eleveados al cuadrado
    syy=np.sum(y**2) # suman de todos los valores del vector y eleveados al cuadrado
    sx=np.sum(x) # suma de todos los valores del vector x
    sy=np.sum(y) # suma de todos los valores del vector y
    sxy=np.sum(x*y) # suma todos los valores del vector x por los del vector y

    # calculo del valor de la pendiente
    a=(n*sxy-sx*sy)/(n*sxx-(sx)**2)
    # calculo del valor de la ordenada al origen
    b=(sxx*sy-sx*sxy)/(n*sxx-(sx)**2)
    # generacion de la recta
    recta=a*x+b
    # calculo del valor del indice de correlacion
    r=(n*sxy-sx*sy)/np.sqrt((n*sxx-sx*sx)*(n*syy-sy*sy))
    
    # devuelve el vector con la recta, el valor de la pendiente, el de la ordenada y el el de r 
    return recta , a , b , r

def mmfilt_band(audio_data,N):   
    señal_suavizada=[] # se inicializa el vector que contendra a todas las señales suavizadas
    # se genera un bucle for que aplica el suavizado a todas las señales
    for i in range(len(audio_data)):
        señal=mmfilt(audio_data[i],N)
        señal_suavizada.append(señal) 
    # devuelve un vector con todas las señales suavizadas
    señal_suavizada=Escala_log(señal_suavizada)
    return señal_suavizada

def filtro(audio_data,audio_fs,bandwidth="octave"):
    # se define el tipo de filtro a partir del ancho de banda introducido
    if bandwidth =="octave":
        bands=octave(31.25,16000) # acoustics.bands.octave genera las frecuencias centrales de un filtro de octava
        low = octave_low(bands[0], bands[-1]) # acoustics.bands.octave_low genera las frecuencias de corte inferior de un filtro de octava
        high = octave_high(bands[0], bands[-1]) # acoustics.bands.octave_high genera las frecuencias de corte superior de un filtro de octava
    elif bandwidth =="third":
        bands=third(12.5,20000) # acoustics.bands.third genera las frecuencias centrales de un filtro de tercio de octava
        low = third_low(bands[0], bands[-1]) # acoustics.bands.third_low genera las frecuencias de corte inferior de un filtro de tercio de octava
        high = third_high(bands[0], bands[-1]) # acoustics.bands.third_high genera las frecuencias de corte superior de un filtro de tercio de octava
    
    # se genera un vector que contendra a todas las señales filtradas
    señal_filtrada=[]
    for band in range(len(bands)):
        
        # se aplica el filtrado de la señal utilizando acoustic.signal.bandpass
        filtered_signal = bandpass(audio_data, low[band], high[band], audio_fs, order=4)
        # se agrega la señal filtrada en la banda i a el vector señal_filtrada
        señal_filtrada.append(filtered_signal)
    
    # devuelve un vector que contiene a todas las señales filtradas 
    return señal_filtrada


def suaviazado(data,tipo,fs,N=0):

    if tipo =="sch":
        señal_suavizada=schroeder_por_banda(data,fs)
    elif tipo == "mmf":  
        señal_suavizada=mmfilt_band(data,N)

    return señal_suavizada
