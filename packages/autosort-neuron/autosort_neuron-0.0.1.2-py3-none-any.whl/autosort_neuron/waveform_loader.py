
import numpy as np

from torch.utils import data
import pickle
# import pickle5 as pickle

def location_cal(sensor_positions, batch_features):
    NumChannels = batch_features.shape[1]
    location_day = []

    b_max = batch_features.max(-1)
    b_min = batch_features.min(-1)
    amplitudes = b_max-b_min
    # amplitudes_multi = np.multiply(amplitudes,amplitudes)
    # amplitudes = np.multiply(amplitudes_multi,amplitudes)
    amplitudes =np.square(amplitudes)
    amplitudes = np.square(amplitudes)
    sum_square_amplitute=np.sum(amplitudes,axis=1)

    location_day=[]
    for ij in range(sensor_positions.shape[1]):
        x=np.dot(sensor_positions[:, ij] , amplitudes.T)
        x=np.divide(x, sum_square_amplitute)
        location_day.append(x)
    # y=np.dot(sensor_positions[:, 1] , amplitudes.T)
    # y=np.divide(y, sum_square_amplitute)
    #
    # # location_day = [x, y]
    # z=np.dot(sensor_positions[:, 2] , amplitudes.T)
    # z=np.divide(z, sum_square_amplitute)
    # location_day=[x,y,z]
    location_day=np.array(location_day).T
    return location_day


def location_cal_group(sensor_positions, batch_features,group_id):
    group_batch = sensor_positions[:,-1]
    location_day=np.zeros((batch_features.shape[0],3))
    for i in np.unique(group_batch):
        care_loc = np.where(group_batch==i)[0]
        look_spike_loc = np.nonzero(np.in1d(group_id, care_loc))[0]
        location_day_batch = location_cal(sensor_positions[care_loc,:], batch_features[look_spike_loc,:,:][:,care_loc,:])
        location_day[look_spike_loc,:] = location_day_batch
    return location_day



class waveformLoader(data.Dataset):
    def __init__(self, root, Keep_id , shank_channel ,
                 sensor_positions, splitgroup=False):
        with (open(root + "X_waveform.pkl", "rb")) as openfile:
            datafile = pickle.load(openfile)
        with (open(root + "Y_spike_id.pkl", "rb")) as openfile:
            GT = pickle.load(openfile)
        with (open(root + "Y_spike_id_noise.pkl", "rb")) as openfile:
            channel_id = np.array(pickle.load(openfile))

        ### datafile = datafile[:, shank_channel, :]
        for i in Keep_id:
            if i not in GT:
                keep_index = np.in1d(GT, Keep_id + [-1])
                datafile = datafile[keep_index, :, :]
                channel_id = channel_id[keep_index]
                GT = np.array(GT)[keep_index]
                break
        #
        # datafile = datafile[[ij in shank_channel for ij in channel_id], :, :]
        # GT = GT[[ij in shank_channel for ij in channel_id]]
        # channel_id = channel_id[[ij in shank_channel for ij in channel_id]]

        mask = ~np.isin(GT, Keep_id)
        GT = np.array(GT)

        GT_binary = np.zeros((GT.shape[0], 2))
        GT_binary[list(mask), 0] = 1
        GT_binary[~mask, 1] = 1

        self.GT_unique = Keep_id + [-1]
        self.GT_binary = GT_binary

        # for ind, i in enumerate(shank_channel):
        #     channel_id[channel_id == i] = ind
        self.Img_single = datafile[np.arange(datafile.shape[0]), np.array(channel_id).astype('int'), :]


        self.GT_LIST = GT

        GT_array = np.zeros((len(GT), len(self.GT_unique)))
        for idx, unique_id in enumerate(self.GT_unique):
            rmv_list = np.where(np.array(GT) == unique_id)[0]
            GT_array[rmv_list, idx] = 1

        self.GT = GT_array

        self.Img = datafile

        if splitgroup:
            pred_location = location_cal_group(sensor_positions, datafile, channel_id)
        else:
            pred_location = location_cal(sensor_positions, datafile)
        self.pred_location = pred_location
        print('pred_location',pred_location.shape)
        self.n_classes = len(set(self.GT_unique))


        # # if ch_group!=None:
        # #     test = np.array([ch_group[i] for i in channel_id])
        # #     pred_location = np.append(pred_location,test.reshape(-1,1),1)





        # i=0909
        # GT1=np.argmax(self.GT,axis=1)
        # for yichun_j in np.unique(GT1):
        #     plt.figure(figsize=(10,1))
        #     test = np.where(GT1==yichun_j)[0]
        #     plt.plot(np.arange(900),np.mean(self.Img[test,:],axis=0).flatten())
        #     for i in range(0,900,30):
        #         plt.vlines(i, -150, +150, linestyles='solid', colors='k', alpha=0.2)
        #
        #     plt.vlines(30*int(channel_id[test[0]]), -100, +100, linestyles='solid', colors='red')
        #     plt.title(yichun_j)
        #     plt.show()
        #
        # #
        # # plt.figure(figsize=(10,3))
        # # test = np.where(GT==yichun_j)[0]
        # # for yichun_i in range(5000):
        # #     plt.plot(np.arange(30), datafile[test[yichun_i],int(channel_id[test[yichun_i]]), :, ])
        # #     # break
        # # plt.show()
        #
        # # return self.Img[index, ...] ,  self.GT[index, ...], self.GT_binary[index, ...], self.Img_single[index, ...],self.pred_location[index,...]
        #
        # GT1 = np.argmax(self.GT, axis=1)
        # for yichun_j in set(GT1):
        #     plt.figure()
        #     test = np.where(GT1==yichun_j)[0]
        #     for yichun_i in range(1000):
        #         plt.plot(np.arange(30), self.Img_single[test[yichun_i],:, ])
        #         # break
        #     plt.title(yichun_j)
        #     plt.show()

        # sensor_positions
        ##### plot prediction spike
        # spike_id=np.argmax(GT_array,axis=1)
        #
        # plt.figure(figsize=(5,7))
        # color_list=np.random.rand(30,3)
        # # color_list=[[0,166,81],[236,0,140],[0,174,239],[241,90,41],[141,198,63],[102,45,145]]
        # # color_list=np.array(color_list)/255
        # for i in range(30):
        #     plt.scatter(sensor_positions[i,0],sensor_positions[i,1],c='lightgrey',
        #                 edgecolors=color_list[i],linewidths=10,
        #                 s=50)
        #
        # for i, txt in enumerate(range(30)):
        #     plt.annotate(txt, (sensor_positions[i,0], sensor_positions[i,1]))
        #
        # for i in range(30):
        #     idx = np.where(spike_id == i)
        #     plt.scatter(np.mean(self.pred_location[idx, 0]),
        #             np.mean(self.pred_location[idx, 1]), edgecolors='black',
        #             c=color_list[i], s=5)
        # # for i in range(6, 7):
        # #     idx = np.where(spike_id == i)
        # #     plt.scatter(self.pred_location[idx, 0],
        # #                 self.pred_location[idx, 1],
        # #                 c='k', s=0.0001)
        # # plt.xlim([-10,60])
        # # plt.ylim([-20, 120])
        # plt.axis('off')
        #
        # # plt.savefig('mouse6_shank1.png',dpi=300,transparent=True)
        # plt.show()



        # for ind, i in enumerate(shank_channel):
        #     channel_id[channel_id==i]=ind
        # self.GT_LIST = GT
        # self.n_classes = len(set(self.GT_unique))


    def __len__(self):
        return len(self.GT)



    def __getitem__(self, index):

        # img = self.Img[index, ...]
        # lbl = self.GT[index, ...]
        # lbl_binary = self.GT_binary[index, ...]


        return self.Img[index, ...] ,  self.GT[index, ...], self.GT_binary[index, ...], self.Img_single[index, ...],self.pred_location[index,...]


        ##### plot prediction spike
        # spike_id=np.argmax(GT_array,axis=1)
        #
        # plt.figure(figsize=(5,7))
        # color_list=[[0,166,81],[236,0,140],[0,174,239],[241,90,41],[141,198,63],[102,45,145]]
        # color_list=np.array(color_list)/255
        # for i in range(6):
        #     plt.scatter(sensor_positions[i,0],sensor_positions[i,1],c='lightgrey',
        #                 edgecolors=color_list[i],linewidths=10,
        #                 s=5000)
        #
        # for i in range(6):
        #     idx=np.where(spike_id==i)
        #     plt.scatter(self.pred_location[idx,0],
        #                 self.pred_location[idx,1],
        #                 c=color_list[i],s=0.001)
        # for i in range(6):
        #     idx = np.where(spike_id == i)
        #     plt.scatter(np.mean(self.pred_location[idx, 0]),
        #             np.mean(self.pred_location[idx, 1]), edgecolors='black',
        #             c=color_list[i], s=500)
        # # for i in range(6, 7):
        # #     idx = np.where(spike_id == i)
        # #     plt.scatter(self.pred_location[idx, 0],
        # #                 self.pred_location[idx, 1],
        # #                 c='k', s=0.001)
        # plt.xlim([-10,60])
        # plt.ylim([-20, 120])
        # plt.axis('off')
        #
        # plt.savefig('mouse6_shank1.png',dpi=300,transparent=True)
        # # plt.savefig('mouse6_shank1_noise.png',dpi=300,transparent=True)
        # plt.show()