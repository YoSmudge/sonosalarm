import yaml
import sonosalarm.discovery
from datetime import datetime
import time
import logging


class Alarm():
    """
    Play an alarm
    """

    def __init__(self,config):
        self.__config = config
        self.loadConfig()
        self.players = sonosalarm.discovery.Discover(self.config.get('zone_ip'))
        self.players.selectZone(self.config['zone'])

    def loadConfig(self):
        with open(self.__config) as f:
            self.config = yaml.safe_load(f.read())

    def saveSettings(self):
        """
        Save the current state of the group
        """

        return self.players.settings

    def restoreSettings(self, settings):
        """
        Reset the settings of the group
        """

        for z in self.players.groupZones:
            # Volume
            z.volume = settings['volume'][z._uid]

        # Set queue position
        if settings['current_playing_state'] == 'PLAYING':
            self.players.groupMaster.play_from_queue(settings['current_queue_position'])
        elif self.players.groupMaster.get_current_transport_info()['current_transport_state'] == 'PLAYING':
            self.players.groupMaster.pause()

    def play(self):
        """
        Play an alarm
        """

        settings = self.saveSettings()

        # Decrease volume to zero if playing
        if not self.players.groupMaster.get_current_transport_info()['current_transport_state'] == 'STOPPED':
            fadeOutStart = datetime.utcnow()
            fadedVolume = settings['volume']
            fadeOut = int(self.config['fadeout'])
            while True:
                fadeDuration = (datetime.utcnow()-fadeOutStart).total_seconds()
                percentageFaded = float(fadeDuration)/float(fadeOut)
                logging.debug("Faded at %f" % (percentageFaded*100))

                for z in self.players.groupZones:
                    startVolume = settings['volume'][z._uid]
                    targetVolume = int(float(startVolume)*(1-percentageFaded))

                    if targetVolume < 0:
                        targetVolume = 0

                    logging.debug("Target volume for %s is now %d (from %d)" % (z._player_name, targetVolume, startVolume))
                    z.volume = targetVolume

                if fadeDuration > fadeOut:
                    break
                time.sleep(0.5)

            self.players.groupMaster.pause()

        for z in self.players.groupZones:
            z.volume = self.config['volume']

        # Add the alarm file to the end of the queue
        # FUN FACT 2: add_uri_to_queue returns the correct playlist index, play_from_queue adds 1 to the index
        queuePos = self.players.groupMaster.add_uri_to_queue(self.config['file'])
        logging.info("Added in queue position %d" % queuePos)
        self.players.groupMaster.play_from_queue(queuePos-1)

        time.sleep(5)
        while True:
            if not int(self.players.groupMaster.get_current_track_info()['playlist_position']) == int(queuePos)\
                or self.players.groupMaster.get_current_transport_info()['current_transport_state'] != 'PLAYING':
                break
            logging.info("Waiting for play to finish")
            time.sleep(0.5)
        self.players.groupMaster.remove_from_queue(queuePos-1)

        self.restoreSettings(settings)
