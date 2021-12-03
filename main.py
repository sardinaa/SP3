import subprocess
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class codecs_converssion:
    def __init__(self, variables):
        self.name = variables["name"]
        self.time_start = variables["start"]
        self.time_finish = variables["finish"]

    def cut_v(self):
        subprocess.getstatusoutput(
            "ffmpeg -ss " + self.time_start + " -i " + self.name + " -to "
            + self.time_finish + " -c copy test.mp4")

    def downsample(self):
        subprocess.getstatusoutput("ffmpeg -i test.mp4 -vf scale=1280:720 "
                                   "-preset slow -crf 18 bbb_720.mp4")
        subprocess.getstatusoutput("ffmpeg -i test.mp4 -vf scale=854:480 "
                                   "-preset slow -crf 18 bbb_480.mp4")
        subprocess.getstatusoutput("ffmpeg -i test.mp4 -vf scale=360:240 "
                                   "-preset slow -crf 18 bbb_360.mp4")
        subprocess.getstatusoutput("ffmpeg -i test.mp4 -vf scale=160:120 "
                                   "-preset slow -crf 18 bbb_160.mp4")

    def change_to_vp9(self):
        subprocess.getstatusoutput("ffmpeg -i bbb_720.mp4 -c:v libvpx-vp9 "
                                   "-c:a libopus vp9_720.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_480.mp4 -c:v libvpx-vp9 "
                                   "-c:a libopus vp9_480.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_360.mp4 -c:v libvpx-vp9 "
                                   "-c:a libopus vp9_360.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_160.webm -c:v libvpx-vp9 "
                                   "-c:a libopus vp9_160.webm")
        subprocess.getstatusoutput("mkdir vp9_vresized")
        subprocess.getstatusoutput("mv vp9_160.webm vp9_360.webm vp9_480.webm "
                                   "vp9_720.webm ./vp9_vresized")

    def change_to_vp8(self):
        subprocess.getstatusoutput("ffmpeg -i bbb_720.mp4 -b:v 1M -c:v libvpx "
                                   "-c:a libvorbis vp8_720.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_480.mp4 -b:v 1M -c:v libvpx "
                                   "-c:a libvorbis vp8_480.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_360.mp4 -b:v 1M -c:v libvpx "
                                   "-c:a libvorbis vp8_360.webm")
        subprocess.getstatusoutput("ffmpeg -i bbb_160.mp4 -b:v 1M -c:v libvpx "
                                   "-c:a libvorbis vp8_160.webm")
        subprocess.getstatusoutput("mkdir vp8_vresized")
        subprocess.getstatusoutput("mv vp8_160.webm vp8_360.webm vp8_480.webm "
                                   "vp8_720.webm ./vp8_vresized")
        subprocess.getstatusoutput("ffprobe -v quiet -print_format json "
                                   "-show_format -show_streams vp8_720.webm "
                                   "> vp8_720.mp4.json")

    def change_to_h265(self):
        subprocess.getstatusoutput("ffmpeg -i bbb_720.mp4 -c:v libx265 -crf "
                                   "26 -preset fast -c:a aac -b:a 128k "
                                   "h265_720.mp4")
        subprocess.getstatusoutput("ffmpeg -i bbb_480.mp4 -c:v libx265 -crf "
                                   "26 -preset fast -c:a aac -b:a 128k "
                                   "h265_480.mp4")
        subprocess.getstatusoutput("ffmpeg -i bbb_360.mp4 -c:v libx265 -crf "
                                   "26 -preset fast -c:a aac -b:a 128k "
                                   "h265_360.mp4")
        subprocess.getstatusoutput("ffmpeg -i bbb_160.mp4 -c:v libx265 -crf "
                                   "26 -preset fast -c:a aac -b:a 128k "
                                   "h265_160.mp4")
        subprocess.getstatusoutput("mkdir h265_vresized")
        subprocess.getstatusoutput("mv h265_160.mp4 h265_360.mp4 h265_480.mp4 "
                                   "h265_720.mp4 ./h265_vresized")

    def change_to_av1(self):
        subprocess.getstatusoutput("ffmpeg -i bbb_720.mp4 -c:v libaom-av1 "
                                   "-crf 30 -b:v 0 av1_720.mkv")
        subprocess.getstatusoutput("ffmpeg -i bbb_480.mp4 -c:v libaom-av1 "
                                   "-crf 30 -b:v 0 av1_480.mkv")
        subprocess.getstatusoutput("ffmpeg -i bbb_360.mp4 -c:v libaom-av1 "
                                   "-crf 30 -b:v 0 av1_360.mkv")
        subprocess.getstatusoutput("ffmpeg -i bbb_160.mp4 -c:v libaom-av1 "
                                   "-crf 30 -b:v 0 av1_160.mkv")
        subprocess.getstatusoutput("mkdir av1_vresized")
        subprocess.getstatusoutput("mv av1_160.mkv av1_360.mkv av1_480.mkv "
                                   "av1_720.mkv ./av1_vresized")

    def comparassion(self, value):
        if value == "1":
            subprocess.getstatusoutput(
                "ffmpeg -i vp9_vresized/vp9_720.webm "
                "-i vp8_vresized/vp8_720.webm "
                "-filter_complex hstack "
                "comparassion_vp8_vp9.webm")
            subprocess.getstatusoutput("ffplay comparassion_vp8_vp9.webm")

        elif value == "2":
            subprocess.getstatusoutput(
                "ffmpeg -i vp9_vresized/vp9_720.webm "
                "-i h265_vresized/h265_720.mp4 "
                "-filter_complex hstack "
                "comparassion_vp9_h265.mp4")
            subprocess.getstatusoutput("ffplay comparassion_vp9_h265.mp4")

        elif value == "3":
            subprocess.getstatusoutput("ffmpeg -i h265_vresized/h265_720.mp4 "
                                       "-i vp8_vresized/vp8_720.webm "
                                       "-filter_complex hstack "
                                       "comparassion_vp8_h265.mp4")
            subprocess.getstatusoutput("ffplay comparassion_vp8_h265.mp4")

        elif value == "4":
            subprocess.getstatusoutput("ffmpeg -i h265_vresized/h265_720.mp4 "
                                       "-i av1_vresized/av1_720.mkv "
                                       "-filter_complex hstack "
                                       "comparassion_vp8_h265.mp4")
            subprocess.getstatusoutput("ffplay comparassion_av1_h265.mp4")

    def stream(self):
        subprocess.getstatusoutput("ffmpeg -i vp8_vresized/vp8_480.webm -f "
                                   "mpegts udp://@127.0.0.1:8008")

    def change_ip(self, ip):
        subprocess.getstatusoutput("ffmpeg -i vp8_vresized/vp8_480.webm -f "
                                   "mpegts udp://" + ip + ":8008")

    def clean(self):
        subprocess.getstatusoutput("unlink test.mp4")
        subprocess.getstatusoutput("unlink bbb_720.mp4")
        subprocess.getstatusoutput("unlink bbb_480.mp4")
        subprocess.getstatusoutput("unlink bbb_360.mp4")
        subprocess.getstatusoutput("unlink bbb_160.mp4")
        subprocess.getstatusoutput("rm -d vp9_vresized")
        subprocess.getstatusoutput("rm -d vp8_vresized")
        subprocess.getstatusoutput("rm -d h265_vresized")


if __name__ == '__main__':
    variables = {
        "name": "BBB.mp4",  # complete video of big buck bunny
        "start": "00:00:21",
        "finish": "00:00:6"
    }
    cc = codecs_converssion(variables)
    print("Renderitzant el fragment tallat i reescalat...")
    # cc.clean()
    # cc.cut_v()
    # cc.downsample()

    on = True

    while on:
        print(
            "Benvingut a la SP3, a continuació es mostren les següents "
            "opcions a executar: ")
        print(
            "\n 1) Canviar codec \n 2) Comparar codecs \n 3) Live Streaming "
            "\n 4) Canviar IP Streaming \n 5) Exit")
        var = input("\n  Seleccioneu el número per executar: ")
        if var == "1":
            print("Convertint a codec VP8...")
            cc.change_to_vp8()
            print("Convertint a codec VP9...")
            cc.change_to_vp9()
            print("Convertint a codec h265...")
            cc.change_to_h265()
            print("Convertint a codec av1...")
            cc.change_to_av1()

        elif var == "2":
            print(
                "\n 1) VP8 vs VP9 \n 2) VP8 vs h.265 \n 3) VP9 vs h.265 \n 4) "
                "AV1 vs h.265")
            var_2 = input("Trieu quins codecs voleu comparar: ")
            print(var_2)
            if var_2 == "1":
                cc.comparassion(var_2)
            elif var_2 == "2":
                cc.comparassion(var_2)
            elif var_2 == "3":
                cc.comparassion(var_2)
            elif var_2 == "4":
                cc.comparassion(var_2)
        elif var == "3":
            cc.stream()
        elif var == "4":
            var_2 = input("Escriviu la ip host: ")
            cc.change_ip(var_2)
        elif var == "5":
            print("Fins la pròxima")
            on = False
        else:
            print("No existeix aquesta opció.")
