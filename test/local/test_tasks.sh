#!/usr/bin/env bash
seller_id: 25165827


http POST http://127.0.0.1:8998/v1/moretime/poster\?nosig=1 \
x-user-id:25165827 \
order_no:=1829645382 \
content='你说我一个上海市委书记怎么就到了北京' \
videos_info_private:='[{"order":1,"media":{"cloud":"qiniu","bucket":"video-private","key":"postervideo.mp4","etag":"Fqe2rcRvLIaPw9kL7o","mimeType":"video/mp4","size":2048}}]' \
pictures_info_private:='[{"order":1,"media":{"cloud":"qiniu","bucket":"image-private","key":"posterpicture.jpg","etag":"Fqe2rcRvLCKwL7o","mimeType":"image/jpeg","size":2048}}]' \

