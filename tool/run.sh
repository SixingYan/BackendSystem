#!/bin/bash
ps aux | grep "flask run -p 8003" | awk '{print $2}' | xargs kill -9
export FLASK_APP=api/cli.py
flask run -p 8003
