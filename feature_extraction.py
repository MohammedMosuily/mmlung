import numpy as np
from scipy.stats import kurtosis, skew
from pipe_scripts.input_parser import get_rms, get_normalized_channels, get_best_channel

from scipy.io import wavfile
import numpy as np
from librosa.util import frame
from pyAudioAnalysis import ShortTermFeatures

feature_dictionary_pyAudio = {
    'Zero_Crossing_Rate': 0,
    'Energy': 1,
    'Energy_Entropy': 2,
    'Spectral_Centroid': 3,
    'Spectral_Spread': 4,
    'Spectral_Entropy': 5,
    'Spectral_Flux': 6,
    'Spectral_Rolloff': 7,
    'Chroma': slice(21,34)
}

aggregate_dictionary_pyAudio = {
    'mean': np.mean, 'std': np.std, 'skew': skew, 'kurtosis': kurtosis
}

def get_feature_names(options):

    whole_signal_features = options['whole_signal']

    ws_columns = [f'whole_signal_{statistic}' for statistic in whole_signal_features]

    pyAudio_columns = get_pyAudio_featurelist(options['pyAudio']['features'], options['pyAudio']['aggregates'])

    coefficient_columns = get_coefficients_feature_list(options['coefficients'])

    wavelet_columns = get_wavelet_feature_list(options['wavelets']['features'], options['wavelets']['aggregates'])

    return ['selected_channel'] + ws_columns + pyAudio_columns + coefficient_columns + wavelet_columns

def get_pyAudio_featurelist(features, aggregates): 
    feature_list = []
    for feature in features:
        if isinstance(feature_dictionary_pyAudio[feature], slice):
            s = feature_dictionary_pyAudio[feature]
            l = len(range(s.stop)[s])
            feature_list = feature_list + [f'{feature}_{i+1}' for i in range(l)]
        else:
            feature_list.append(feature)
    feature_list

    column_list = [f'{feature}_{aggregate}' for aggregate in aggregates for feature in feature_list] 
    return column_list
    
whole_signal_statistics_dictionary = {
    'mean': np.mean, 'std': np.std, 'skew': skew, 'kurtosis': kurtosis, 'rms': get_rms
}

def get_coefficients_feature_list(selected_coefficients):
    coefficient_names = []

    for coefficient in selected_coefficients:
        for i in range(1,14):
            coefficient_names.append(f'{coefficient}_{i}')

    return coefficient_names

def extract_features_from_file(row, task_name, options, window_length = 6, hop = 0.3):

    samplerate, data = wavfile.read(row[f'{task_name}_file'])
    channel_data = get_normalized_channels(data)


    _, _, selected_channel = get_best_channel(channel_data)
    selected_data = channel_data[:, selected_channel]

    print("samplerat:", samplerate)
    print("--------------------------")
    print("data shape[0]:", data.shape)
    print("--------------------------")
    print("data shape[0]:", data.shape[0])
    

    windows = [selected_data]
    window = windows[0]

    whole_signal_features = get_whole_signal_features(selected_data, options['whole_signal'])


    pyaudio_features = get_pyAudio_features(window, samplerate, options['pyAudio']['aggregates'], options['pyAudio']['features'])

    coefficients = get_coefficient_features(window, samplerate, options['coefficients'])


    wavelet_features = get_wavelet_features(window, samplerate, options['wavelets']['features'], options['wavelets']['aggregates'])

    row_values = [selected_channel] + whole_signal_features + pyaudio_features + coefficients + wavelet_features
    return tuple(row_values)


def get_whole_signal_features(data, statistics):
    feature_list = []

    for statistic in statistics:
        statistic_function = whole_signal_statistics_dictionary[statistic]
        feature_list.append(statistic_function(data))

    return feature_list

def get_pyAudio_features(data, samplerate, selected_aggregates, selected_features):

    F, f_names = ShortTermFeatures.feature_extraction(data, samplerate, 0.01*samplerate, 0.01*samplerate, deltas=False)


    feature_list = []
    for aggreate in selected_aggregates:
        aggreate_function = aggregate_dictionary_pyAudio[aggreate]
        for feature in selected_features:
            index = feature_dictionary_pyAudio[feature]
            extracted = F[index, :]
            if(extracted.ndim ==2):
                for i in range(extracted.shape[0]):
                    feature_list.append(aggreate_function(extracted[i])) 

            else:
                feature_list.append(aggreate_function(extracted)) 

    return feature_list

from spafe.features.bfcc import bfcc
from spafe.features.cqcc import cqcc
from spafe.features.gfcc import gfcc
from spafe.features.lfcc import lfcc
from spafe.features.lpc import lpcc
from spafe.features.mfcc import mfcc
from spafe.features.msrcc import msrcc
from spafe.features.rplp import rplp

spectral_coefficient_dictionary = {
    'BFCC' : bfcc,
    'CQCC' : cqcc,
    'GFCC' : gfcc,
    'LFCC' : lfcc,
    'LPCC' : lpcc,
    'MFCC' : mfcc,
    'MSRCC': msrcc,
    'RPLP' : rplp
}

def get_coefficient_features(data, samplerate, selected_coefficients):
    all_coefficients = []

    for coefficient in selected_coefficients:
        coef_function = spectral_coefficient_dictionary[coefficient]
        coefficients  = coef_function(data,
                fs=samplerate, win_len=0.01, win_hop=0.01)
        coefficients = np.mean(coefficients, axis=0).tolist()
        all_coefficients = all_coefficients + coefficients

    return all_coefficients

feature_dictionary_wavelets = {
    'Zero_Crossing_Rate': 0,
    'Energy': 1,
    'Energy_Entropy': 2,
    'Spectral_Centroid': 3,
    'Spectral_Spread': 4,
    'Spectral_Entropy': 5,
    'Spectral_Flux': 6,
    'Spectral_Rolloff': 7
}

import pywt

def get_wavelet_features(data, samplerate, features, aggregates):

    coeff_list = pywt.wavedec(data, 'db2', level=4)
    all_features = []

    for i,level_data in enumerate(coeff_list):
        level_features = get_pyAudio_features(level_data, samplerate, aggregates, features)
        all_features = all_features + level_features

    return all_features


def get_wavelet_feature_list(features, aggregates):
    all_levels = []

    for level in range(1,6):
        column_list = [f'Level_{level}_{feature}_{aggregate}' for aggregate in aggregates for feature in features] 
        all_levels = all_levels + column_list

    return all_levels
