'''
Set of helper functions to use 
'''
import numpy as np
import pandas as pd
import math



def extract_timestamp_cutouts(trace_to_extr:np.ndarray, uncor_timestamps:np.ndarray, baseline:float, posttime=None,sampling=1,offset=0.0, z_scored=False, dff=False)->pd.DataFrame:
    """
        Arguments:
        trace_to_extract: an array containing values of interest (e.g. dF/F trace), ASSUMES CONSTANT SAMPLING FREQUENCY!!

        timestamps: array containing timepoints of the events, points from trace_to_extract will be taken around each timestamp

        baseline: time before the timepoint (in seconds) to be extracted

        posttime: time after the timepoint (in seconds) to be extracted, by default equals baseline

        sampling: acquisition rate of the trace_to-extract, in Hz (by default 1)

        offset: shift in time in seconds between timestamps and trace_to_extract (if, for example photometry acqusition starts 5 seconds before behavior video 
            from which timepoints were annotated offset = 5)

        z-scored: returns cutouts as z-score values computed on baseline

        dff: returns cutouts as deltaF/F values computed on baseline

        Returns:
        DataFrame with signal cutouts around each trigger, organized in columns
    """
    #Copy the input trace
    trace_to_extract = trace_to_extr.copy()
    #if time after the trigger is not specified, make it equal to baseline
    if not posttime:
        posttime=baseline
    #Make "result" dataframe
    result=pd.DataFrame()
    #Apply offset to trigger timestamps
    timestamps = uncor_timestamps+offset
    #Define length of the cutout (in points)
    cutout_length =  round((posttime+baseline)*sampling)
    #Define time points of the cutouts relative to the trigger
    #result.index=np.round(np.arange(-baseline,posttime,1/sampling),round(math.log10(sampling)+2))

    cutouts = []
    #Extract cutouts around each trigger in a loop
    for i,timestamp in enumerate(timestamps):
        indfrom = round((timestamp-baseline)*sampling)
        if indfrom<0 or indfrom+cutout_length>len(trace_to_extract)-1:
            continue
        cutouts.append(pd.Series(trace_to_extract[indfrom:indfrom+cutout_length]))
        #result["Cutout{}".format(i)]=trace_to_extract[indfrom:indfrom+cutout_length]

    result = pd.concat(cutouts, axis=1)
    result.index=np.round(np.arange(-baseline,posttime,1/sampling),round(math.log10(sampling)+2))
    
    #Apply deltaF/F0 transformation to all cutouts (columns of results
    if dff:
        for col in result:
            base_mean = result.loc[:0,col].mean()
            result[col]-=base_mean
            result[col]/=base_mean
    #Apply deltaF/F0 transformation to the cutout (columns of results)
    if z_scored:
        for col in result:
            std = result.loc[:0,col].std()
            result[col]-=result.loc[:0,col].mean()
            result[col]/=std
            
    return result



def locate_onsets_offsets(annotated_trace:np.ndarray, time_trace:np.ndarray = None, thresh=0.5, on_dur_thresh=0, off_dur_thresh=0, return_dur = False)->pd.DataFrame:
    '''
    
    '''
    if time_trace is None:
        time_trace = np.arange(len(annotated_trace))
    onsets = time_trace[(annotated_trace>thresh) & (np.roll(annotated_trace,1)<=thresh)]
    offsets = time_trace[(annotated_trace<thresh) & (np.roll(annotated_trace,1)>=thresh)]

    
    if onsets[-1] == time_trace[-1]:
        onsets = onsets[:-1]
    if offsets[-1]==time_trace[-1]:
        offsets = offsets[:-1]


    if offsets[0]<onsets[0]:
        offsets = np.roll(offsets,-1)

    
    if len(onsets)< len(offsets):
            onsets=np.append(onsets,float("nan"))
    elif len(onsets)> len(offsets):
        offsets=np.append(offsets,float("nan"))

    if off_dur_thresh>0:
        off_durations=onsets-np.roll(offsets,1)
        indices_to_remove=np.arange(len(onsets))
        indices_to_remove = indices_to_remove[off_durations<off_dur_thresh][1:]
        onsets=np.delete(onsets,indices_to_remove)
        offsets=np.delete(offsets,indices_to_remove-1)

    if on_dur_thresh>0:
        on_durations=offsets-onsets
        indices_to_remove=np.arange(len(onsets))
        indices_to_remove = indices_to_remove[on_durations<on_dur_thresh]
        onsets=np.delete(onsets,indices_to_remove)
        offsets=np.delete(offsets,indices_to_remove)

    results = pd.concat([pd.Series(onsets), pd.Series(offsets)],axis=1)
    results.columns = ["on","off"]
    if return_dur:
        results["duration"] = results.off-results.on
    return results


def create_timestamp_aligned_video(video:np.ndarray, timestamps:np.ndarray, FPS:int, baseline:float, posttime:float, bin_factor=1, z_scored=False):
    excerpts = []
    omitted_count = 0
    for timestamp in timestamps:
        if timestamp>=baseline and timestamp<=len(video)/FPS-posttime:
            from_frame = int((timestamp-baseline)*FPS)
            to_frame = int((timestamp+posttime)*FPS)
            excerpts.append(video[from_frame:to_frame,:,:])

    if omitted_count:
        print("{} timestamps omitted due to being too close to the start/end of the video, shorten baseline/posttime parameters to reinclude them.".format(omitted_count))

    if len(excerpts):
        aligned_video = np.array(excerpts).mean(axis=0)
        if bin_factor>1:
            aligned_video = space_bin(aligned_video,bin_factor)
        if z_scored:
            aligned_video = (aligned_video-aligned_video[:int(baseline*FPS)].mean(axis=0))/aligned_video[:int(baseline*FPS)].std(axis=0)
        return aligned_video


    
def bin_trace(trace:np.ndarray, binwidth=1, just_smooth=False):
    if binwidth>1:
        numpnts = (len(trace)//binwidth) *binwidth
        trace = np.insert(trace, 0 , [trace[0] for _ in range(binwidth)])
        trace = np.append(trace, [trace[-1] for _ in range(binwidth)])
        new_trace = trace.copy()
        
        for i in range(1,binwidth):
            new_trace+=np.roll(trace,-i)
        if just_smooth:
            return np.roll(new_trace/binwidth,binwidth//2)[binwidth:-binwidth]
        else:
            return new_trace[binwidth:-binwidth][0:numpnts:binwidth]/binwidth
    else:
        return trace
    


def space_bin(video, bin=2):
    binrate = bin
    binned_video = video.copy()
    for i in range(1,bin):
        binned_video+=np.roll(binned_video,-i,axis=1)
        binned_video+= np.roll(binned_video,-i,axis=2)  
    return binned_video[:,::binrate,::binrate]/(bin**2)