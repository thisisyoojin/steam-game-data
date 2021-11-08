from stem import Signal
from stem.control import Controller
from selenium import webdriver
from utils import read_config

#https://boredhacking.com/tor-webscraping-proxy/
# signal TOR for a new connection
def switchIP():
    with Controller.from_port(port = 9051) as controller:
        tor_passwd = read_config("./utils/db_config.yaml", ["TOR"])
        controller.authenticate(password='tor_passwd')
        controller.signal(Signal.NEWNYM)

# get a new selenium webdriver with tor as the proxy
def proxy_driver(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", PROXY_HOST)
    fp.set_preference("network.proxy.socks_port", int(PROXY_PORT))
    fp.update_preferences()

    return webdriver.Firefox(firefox_profile=fp)    

