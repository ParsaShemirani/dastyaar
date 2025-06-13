file_functions.scp_copy(
    local_path='/Users/parsashemirani/Main/Inbox/testingests/DSC00871-v3-04b4b8f408e8809e59637006a7870f69dc516eedca0f34e855316738744eb064.jpg',
    remote_user='parsa',
    remote_host='192.168.1.4',
    remote_path='/home/parsa/baseman'
)

b'\xca}\xdf\x9e\xfft\x11\xdb\xdb\xa6\x08\x8f\xfe\xcb X\xa2\x18\xd96!\xb9\xf0]\x92\xae\x80\xfc\xa2\xe4\x19\xb7'


from app.tools.file_functions import scp

scp(
    local_path='/Users/parsashemirani/Main/Inbox/cambriatrim_proxy_quarter.mp4',
    remote_user='parsa',
    remote_host='192.168.1.4',
    remote_path='/home/parsa/',
    upload=True
)

ffmpeg -i C0079-v1-ee2b5b1e5374fe9827317cdc14383a9318d6dd8fad112df3583eea2915efa40c.mp4 -vf "scale=-2:480" -c:v libx264 -preset slower -crf 40 -c:a aac -b:a 128k 40_480p.mp4
ffmpeg -i C0079-v1-ee2b5b1e5374fe9827317cdc14383a9318d6dd8fad112df3583eea2915efa40c.mp4 -ac 1 -ar 8000 -q:a 9 output_8k_mono9man.mp3
