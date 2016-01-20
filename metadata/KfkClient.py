#!/usr/bin/python
import logging
import time

from kafka.client import KafkaClient, FetchRequest, ProduceRequest, OffsetRequest

DEBUG = True

def debug(var):
    if DEBUG is True:
        print(var)

class KfkClient(object):

    def __init__(self, ip):
        self.client = KafkaClient(ip, 9092)
        self.fd = None
        self.topic = None
        self.partition = None
        self.offset = None

    def send(self, topic, partition, data):
        message = self.client.create_message(data)
        request = ProduceRequest(topic, partition, [message])
        self.client.send_message_set(request)

    def _check_offset(self, topic, partition):
        if (self.topic != topic or self.partition != partition):
            self.topic = topic
            self.partition = partition
            self._get_new_offset()

    def receive(self, topic, partition):
        self._check_offset(topic, partition)

        while True:
            request = FetchRequest(topic, partition, self.offset, 2048)
            debug(request)
            try:
                (messages, nextRequest) = self.client.get_message_set(request)
            except e:
                self._check_offset(topic, partition)
                continue
                
            if len(messages) > 0:
                self.offset = nextRequest.offset
                self._write_offset()
                return messages
            else:
                time.sleep(1)

    def get_line(self, topic, partition):
        while True:
            messages = self.receive(topic, partition)
            for message in messages:
                yield message.payload

    def close(self):
        if self.fd is not None:
            self.fd.close()
        self.client.close()


    def _get_new_offset(self):
        file_name = "%s-%s.offset" % (self.topic, self.partition)

        if self.fd is not None:
            self.fd.close()

        try:
            self.fd = open(file_name, 'r+')
            file_offset = self.fd.readline()
        except IOError:
            self.fd = open(file_name, 'w+')
            file_offset = -1

        self.fd.seek(0,0)
        self.fd.truncate()

        try:
            file_offset = int(file_offset)
        except:
            file_offset = 0

        minoffsetreq = OffsetRequest(self.topic, self.partition, -2, 1)
        results = self.client.get_offsets(minoffsetreq)
        minoffset = results[0]

        maxoffsetreq = OffsetRequest(self.topic, self.partition, -1, 1)
        results = self.client.get_offsets(maxoffsetreq)
        maxoffset = results[0]


        if file_offset == -1:
            self.offset = minoffset
        elif file_offset >= minoffset and file_offset <= maxoffset:
            self.offset = file_offset
        else:
            self.offset = maxoffset

        debug ("file%d min%d max%d using%d" % (file_offset, minoffset, maxoffset, self.offset))
        self._write_offset()


    def _write_offset(self):
        self.fd.seek(0,0)
        self.fd.write("%d" % self.offset)

def main():
    DEBUG = True
    client = KfkClient("10.110.0.40")
    #client.send("module_log", 0, "big dog")

    for message in client.get_line("va_result", 0):
        print message
    client.close()

if __name__ == '__main__':
    main()
