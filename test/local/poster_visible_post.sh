#!/usr/bin/env bash

buyer : 22020100 设置多媒体不可见
http POST http://127.0.0.1:8998/v1/moretime/poster/visible\?nosig=1 \
x-user-id:22020100 \
poster_id:=8 \
is_content:=false \
set_visible:=0

buyer : 22020100 设置多媒体可见
http POST http://127.0.0.1:8998/v1/moretime/poster/visible\?nosig=1 \
x-user-id:22020100 \
poster_id:=8 \
is_content:=false \
set_visible:=1




buyer : 25165827 设置多媒体不可见
http POST http://127.0.0.1:8998/v1/moretime/poster/visible\?nosig=1 \
x-user-id:25165827 \
poster_id:=9 \
is_content:=false \
set_visible:=0

buyer : 25165827 设置多媒体可见
http POST http://127.0.0.1:8998/v1/moretime/poster/visible\?nosig=1 \
x-user-id:25165827 \
poster_id:=9 \
is_content:=false \
set_visible:=1




