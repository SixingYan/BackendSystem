#!/usr/bin/env bash

http POST http://127.0.0.1:8998/v1/moretime/reply\?nosig=1 \
poster_id:=6 \
prior_id:=-1 \
to_user_id:=25165827 \
content='这是坠吼的' \
rate:=5 \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"replyreplyvideo.jpg","etag":"Fqe2rcRvLIaPCWy3FCKw2QwkL7o","mimeType":"image/jpeg","size":2048}]'  \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"replyreplypicture.jpg","etag":"Fqe2rcRvLIaPCWy3FC2Qw9kL7o","mimeType":"image/jpeg","size":2048}]'




buyer : 22020100
http POST http://127.0.0.1:8998/v1/moretime/reply\?nosig=1 \
x-user-id:22020100 \
poster_id:=8 \
prior_id:=-1 \
to_user_id:=25165827 \
content='这是坠吼的' \
set_visible:=1 \
rate:=5 \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"buyerreplyvideo.mp4","etag":"cRvLIaPCWy3FCKw2QwkL7o","mimeType":"video/mp4","size":2048}]'  \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"buyerreplypicture.jpg","etag":"RvLIaPCWy3FC2Qw9kL7o","mimeType":"image/jpeg","size":2048}]'

reply_id: 31


seller : 25165827
http POST http://127.0.0.1:8998/v1/moretime/reply\?nosig=1 \
x-user-id:25165827 \
poster_id:=8 \
prior_id:=31 \
to_user_id:=22020100 \
content='很惭愧只做了一点微小的工作' \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"sellerreplyvideo.mp4","etag":"cRvLIaPCsdWy3FCKw2QwkL7o","mimeType":"video/mp4","size":2048}]'  \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"sellerreplypicture.jpg","etag":"RvLIWysssssFC2Qw9kL7o","mimeType":"image/jpeg","size":2048}]'





buyer : 25165827
http POST http://127.0.0.1:8998/v1/moretime/reply\?nosig=1 \
x-user-id:25165827 \
poster_id:=9 \
prior_id:=-1 \
to_user_id:=22020100  \
content='苟利国家生死以' \
set_visible:=1 \
rate:=5 \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"buyerreplyvideoxxx.mp4","etag":"cRvLIaPCWy3FCKw2QwkL7o","mimeType":"video/mp4","size":2048}]'  \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"buyerreplypicturexxx.jpg","etag":"RvLIaPCWy3FC2Qw9kL7o","mimeType":"image/jpeg","size":2048}]'

reply_id: 39


seller : 22020100
http POST http://127.0.0.1:8998/v1/moretime/reply\?nosig=1 \
x-user-id:22020100 \
poster_id:=9 \
prior_id:=39 \
to_user_id:=25165827 \
content='岂因祸福避趋之' \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"sellerreplyvideoxxx.mp4","etag":"cRvLIaPCsdWy3FCKw2QwkL7o","mimeType":"video/mp4","size":2048}]'  \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"sellerreplypicturexxx.jpg","etag":"RvLIWysssssFC2Qw9kL7o","mimeType":"image/jpeg","size":2048}]'

