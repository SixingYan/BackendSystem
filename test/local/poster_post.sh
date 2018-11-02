#!/usr/bin/env bash
curl -H "Content-Type:application/json" \
-X POST -d '{"order_no":1603745934,"content": "5555","videos_info_private":[] "pictures_info_private":[{"cloud":"qiniu","bucket":"image-public","key":"test/2018/03/123456.jpg","etag":"Fqe2rcRvLIaPCWy3FCKw2Qw9kL7o","mimeType":"image/jpeg","size":2048}]' \
http://127.0.0.1:8998/v1/moretime/poster\?nosig=1




seller_id: 25165827

http POST http://127.0.0.1:8998/v1/moretime/poster\?nosig=1 \
x-user-id:25165827 \
order_no:=1829645382 \
content='你说我一个上海市委书记怎么就到了北京' \
videos_info_private:='[{"cloud":"qiniu","bucket":"video-private","key":"postervideo.mp4","etag":"Fqe2rcRvLIaPw9kL7o","mimeType":"video/mp4","size":2048}]' \
pictures_info_private:='[{"cloud":"qiniu","bucket":"image-private","key":"posterpicture.jpg","etag":"Fqe2rcRvLCKwL7o","mimeType":"image/jpeg","size":2048}]' \






seller_id: 22020100  buyer_id: 25165827

http POST http://127.0.0.1:8998/v1/moretime/poster\?nosig=1 \
x-user-id:22020100 \
order_no:=1505645796 \
content='我说你另请高明吧' \
videos_info_private:='[{"order":1,"media":{"cloud":"qiniu","bucket":"video-private","key":"postervid.mp4","etag":"F","mimeType":"video/mp4","size":2048}}]' \
pictures_info_private:='[{"order":1,"media":{"cloud":"qiniu","bucket":"image-private","key":"posterpic.jpg","etag":"F","mimeType":"image/jpeg","size":2048}}]' \



9

