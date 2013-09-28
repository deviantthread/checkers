import socket
import checkers

# Using localhost will be faster but only allow accessing locally
# If you want access from other computers use socket.gethostname()
HOST = 'localhost'
PORT = 8080

print('Starting server on host %s port %s' % (HOST, PORT))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(2)

class SocketSource:
  def __init__(self, conn):
    self.conn = conn

  def read(self):
    data = self.conn.recv(1024)
    if data:
      return data.decode()
    return data

# Given a source on which you can call "read" to retrieve some amount
# of data as a string, LineReader provides a simple read_line functionality.
# Source should return None when it is empty. read_line will return when
# the source has indicated it is empty for all subsequent calls.
class LineReader:
  def __init__(self, source):
    self.source = source
    self.remaining = ''
    self.closed = False

  def read_line(self):
    if self.closed:
      return None
    newline_pos = self.remaining.find('\n')
    while newline_pos == -1:
      new_text = self.source.read()
      if not new_text:
        self.closed = True
        if self.remaining == '':
          return None
        return self.remaining
      self.remaining += new_text
      newline_pos = self.remaining.find('\n')
    ret = self.remaining[0:newline_pos]
    if ret[-1] == '\r':
      ret = ret[:-1]
    self.remaining = self.remaining[newline_pos+1:]
    return ret

while 1:
  print('Waiting for connections')
  conn, addr = s.accept()
  print('Connected to from', addr)
  lr = LineReader(SocketSource(conn))
  while 1:
    data = lr.read_line()
    if not data: break
    print(data)
  conn.close()

s.close()
