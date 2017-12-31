import gmusicapi
import logging
import getpass
import gcredentials

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    gmapi = gmusicapi.Mobileclient()
    email = gcredentials.EMAIL_HARDCODE
    logging.info("Attempting login as {} with android ID {}".format(email, gcredentials.AID_HARDCODE))
    success = gmapi.login(email, getpass.getpass(), gcredentials.AID_HARDCODE)
    logging.info('Logged in: {}'.format(success))