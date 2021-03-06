import sys
import glob
import serial


def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith ('linux'):
        temp_list = glob.glob ('/dev/tty[A-Za-z]*')
        result = []
        for a_port in temp_list:
            try:
                s = serial.Serial (a_port)
                s.close ()
                result.append (a_port)
            except serial.SerialException:
                pass
        return result

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(serial_ports())
