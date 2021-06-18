import struct
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

import struct
import sys
import math

import numpy as np
from utils.data_utils import *
from utils.mmWave_parse_utils import *

#
# TODO 1: (NOW FIXED) Find the first occurrence of magic and start from there
# TODO 2: Warn if we cannot parse a specific section and try to recover
# TODO 3: Remove error at end of file if we have only fragment of TLV
#


magic = b'\x02\x01\x04\x03\x06\x05\x08\x07'

range_bin_num = 256
fileName = 'C:/Users/HaowenWeiJohn/Desktop/CWINS/mmWave_WIFI_inter/Range_test_data_4_25/Step1[' \
           '1349]/Step1/40cm.dat'

# fileName = 'C:/Users/HaowenWeiJohn/Desktop/ProjectCWINS/mmWave_WIFI_inter/Range_test_data_4_25/Radar_data_4_26[' \
#            '1359]/Radar_data_4_26/160cm_4_26.dat '

if __name__ == '__main__':
    print("John")
    rawDataFile = open(fileName, "rb")
    rawData = rawDataFile.read()
    rawDataFile.close()
    offset = rawData.find(magic)
    rawData = rawData[offset:]

    processing_data = rawData
    # rawData = rawData[]
    current_offset = 0
    success = False

    frame_num = 0

    log_range_profile_total = np.zeros(range_bin_num)
    log_noise_profile_total = np.zeros(range_bin_num)

    while rawData.find(magic) != -1:

        if frame_num >= 150:
            break
        print(frame_num)

        success, processing_data, detected_points, range_profile, noise_profile, rd_heatmap, azi_heatmap, statistics = decode_iwr_tlv(
            processing_data)
        # TODO: range_profile = converting(range_profile)

        # plt.plot(range_profile)
        # plt.scatter(21, range_profile[21])
        # # plt.plot(noise_profile)
        # plt.xlabel('Range bins')
        # plt.ylabel('Power')
        # plt.show()
        if success:
            log_range_profile = log10xto10(range_profile)
            log_noise_profile = log10xto10(noise_profile)

            log_range_profile_total += log_range_profile
            log_noise_profile_total += log_noise_profile
            frame_num += 1

    log_ave_range_profile = log_range_profile_total / frame_num
    log_ave_noise_profile = log_noise_profile_total / frame_num

    plt.plot(log_ave_range_profile)
    plt.plot(log_ave_noise_profile)
    plt.xlabel('Range bins')
    plt.ylabel('Power(10log10X)')
    plt.show()
