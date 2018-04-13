import cv2
import numpy as np
import re
TOURFRANCE_NOSPAM_PATH = "../LNK2018_data/tweets/visualstories_tourfrance_2016_twitter_nospam_images+videos.csv"
TOURFRANCE_PATH = "../LNK2018_data/tweets/visualstories_tourfrance_2016_twitter_images+videos.csv"
URL_REGEX = r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
class DataHandler:


    def readVideoData(self, file):
        data = open(file,"r")
        result = {}
        for num,line in enumerate(data.readlines()):
            data = line.split()
            if len(data) == 2:
                id, url = data[0], data[1]
                result[id] = url
                # print(id,url)
            else:
                print("Error" + data)
        return result


    def parseImage(self,url,id,path):
        vidcap = cv2.VideoCapture(url)
        success, image = vidcap.read()
        frame = 0
        count = 0

        fps = vidcap.get(cv2.CAP_PROP_FPS)
        #take a shot every 0.5 sec
        gap = int(fps/2)
        while success:
            success, image = vidcap.read()
            if (frame % gap == 0) & (type(image) is np.ndarray):
                cv2.imwrite("{}{}_{}f.jpg".format(path,id,count), image)
                count += 1
                # save frame as JPEG file
            frame += 1
        vidcap.release()

    def readTweets(self,file):
        f = open(file,'r')
        tweetsInfo = []
        noiseInfo = []
        videos_num = 0
        total_tweets = 0
        images_num = 0
        noise_num = 0
        for num, line in enumerate(f.readlines()):
            if num == 0:
                continue
            total_tweets +=1
            data = line.split(";")
            try:
                id = int(data[0])
                obj_image = re.match(URL_REGEX,data[6])
                obj_video = re.search(URL_REGEX, data[8])

                if (obj_image!=None) & (obj_video!=None):
                    #match success, tweets contains url

                    if data[6][-3:] not in ["jpg","png"]:
                        print("not ending with jpg: " + data[6])
                    # print("potential video url found: " + obj_video.group())
                    #TODO ADD EXTRACTED URL TO RESULT
                    data[7] = obj_video.group()

                    images_num += 1
                    if ("youtu.be" in data[8]) | ("youtube" in data[8]):
                        videos_num += 1
                    tweetsInfo.append(data)

                elif obj_video:
                    # print("potential video url found: " + obj_video.group())
                    data[7] = obj_video.group()
                    if ("youtu.be" in data[8]) | ("youtube" in data[8]):
                        videos_num += 1
                elif obj_image:
                    if data[6][-3:] not in ["jpg", "png"]:
                        print("not ending with jpg: " + data[6])

                    tweetsInfo.append(data)
                    images_num += 1



                else:
                    noise_num += 1
                    noiseInfo.append(data)




            except ValueError:
                noise_num += 1
                noiseInfo.append(data)
            except IndexError:
                noise_num += 1
                noiseInfo.append(data)

        print("- Total images URL's for tourfrance_2016: {}".format(images_num))
        print("- Total videos URL's for tourfrance_2016: {}".format(videos_num))

        return tweetsInfo



if __name__ == "__main__":
    dh = DataHandler()
    dh.readTweets(TOURFRANCE_PATH)
    # result = dh.readVideoData("../vtt2016/vines.url.testingSet.txt")
    # for id, url in result.items():
    #     dh.parseImage(url,id,"../vtt2016/images/")
