import wx
import pandas as pd

def dfrange(df):
    pass

def __realtime_data_to_point(close_list, last_close, xmax, ymax):
    low, high = pd.Series.min(close_list), pd.Series.max(close_list)
    draw_data_height = max(abs(low - last_close), abs(high-last_close))*2
    xstep = xmax/len(close_list)
    ystep = ymax/draw_data_height
    return [ wx.Point(val[0]*xmax/len(close_list), (val[1]-(last_close-draw_data_height/2))*ystep) for val in  enumerate(close_list.values)]
#    for val in enumerate(close_list.values):
#        yield wx.Point(val[0]*xstep, (val[1]-(last_close-draw_data_height/2)*ystep))

    
    
def draw_realtime(dc, df, last_close):
    """ dc: device context
        df: pandas.dataframe
                   open high low close volume
        datetime   xx   xx   xx   xx    xx
    """
    size=dc.GetSize()         
    xmax = size.width-50
    ymax = size.height-50
    dc.SetDeviceOrigin(10, ymax+40)
    dc.SetAxisOrientation(True, True)
    #dc.SetBackground(wx.Brush(wx.WHITE))
    
    close_data = df['close']    
    
    low, high = (pd.Series.min(close_data), pd.Series.max(close_data))  
        
    data_axis = __realtime_data_to_point(close_data, last_close,xmax, ymax)  
    dc.DrawSpline(data_axis)
    #last close
   
    #left axis
    
    data_height = max(abs(low - last_close), abs(high-last_close))
    
    vallist = []
    
    
    #dc.MaxX and dc.MaxY may be changed after dc.drawxxxx, so do not use this when want to draw in specific area
    for i in range(9):
        dc.SetPen(wx.Pen('#d5d5d5'))
        dc.DrawLine(0, i*ymax/8, xmax, i*ymax/8)
        dc.DrawLine(i*xmax/8, 0, i*xmax/8, ymax)
        val = last_close - data_height+i*2*data_height/8
        percent = 100*(val - last_close)/last_close
        dc.DrawText('%.2f' % val, -5, i*ymax/8)
        dc.DrawText('%.2f'%percent+"%", xmax, i*ymax/8)
    

    dc.SetPen(wx.Pen(wx.RED, 3))
    dc.DrawLine(0, ymax/2, xmax, ymax/2)    
    
    
        
        
        
    

    
       

def draw_candle(dc, df):
    """ dc: device context
        df: pandas.dataframe
                   open high low close volume
        datetime   xx   xx   xx   xx    xx
    """
    size=dc.GetSize()         
    windowWidth = size.width-50
    windowHeight = size.height-100
    dc.SetDeviceOrigin(0, windowHeight)
    dc.SetAxisOrientation(True, True)    
    

    stockRange = (pd.Series.min(df['low']), pd.Series.max(df['high']))
    dfindex_len = df.shape[0]   
    recwidth = float(windowWidth)/dfindex_len
    i = 0
    for dt in df.index:
        row = df.ix[i]
        close = row['close']
        high = row['high']
        open = row['open']
        low = row['low']
        pricediff = stockRange[1] - stockRange[0]
        recheight = windowHeight*abs(close - open)/pricediff+1
        x = i*windowWidth/dfindex_len + 1        
        upperlineendY = (high - stockRange[0])*windowHeight/pricediff                 
        lowerlineendY = (low - stockRange[0])*windowHeight/pricediff
        drop = False
        if close >= open:                 
            y = upperlineendY - (high - open)*windowHeight/pricediff       
        else:                
            drop = True             
            y = upperlineendY - (high - close)*windowHeight/pricediff  
                   
        rec = (x, y, recwidth, recheight)
        upperline = (x+recwidth/2, y+recheight, x+recwidth/2, upperlineendY)
        lowerline = (x+recwidth/2, y, x+recwidth/2, lowerlineendY)
           
        if drop:
            dc.SetBrush(wx.BLACK_BRUSH)
        else:                
            dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawRectangle(rec[0], rec[1], rec[2], rec[3])
        dc.DrawLine(upperline[0], upperline[1], upperline[2], upperline[3])
        dc.DrawLine(lowerline[0], lowerline[1], lowerline[2], lowerline[3])
        i = i+1