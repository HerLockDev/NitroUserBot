FROM erdembey/epicuserbot:latest
RUN git clone https://github.com/HerLockDev/NitroUserBot /root/NitroUserBot
WORKDIR /root/NitroUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
