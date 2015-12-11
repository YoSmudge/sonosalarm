import soco
from texttable import Texttable
import sys
import logging


class Discover(object):
    """
    Discover and link nearby sonos units
    """

    _zones = None

    def __init__(self,zone_ip=None):
        self.__zone_ip = zone_ip

    def printZones(self):
        t = Texttable()
        t.add_row(['Zone Name', 'UID', 'Group', 'IP', 'Current Volume'])

        for z in self.zones:
            t.add_row([z.player_name, z.uid, z.group.coordinator.player_name, z.ip_address, z.volume])

        sys.stdout.write(t.draw())
        sys.stdout.write("\n")
        sys.stdout.flush()

    def selectZone(self, zoneName):
        self.__selectedZone = None
        for z in self.zones:
            if z.player_name == zoneName:
                self.__selectedZone = z

        if not self.__selectedZone:
            raise Exception("Zone named %s is not found!" % (zoneName))

        if self.__selectedZone.group.coordinator != self.__selectedZone:
            raise Exception("Zone %s is part of a group (%s). Target zone should be the coordinator node" % (self.__selectedZone.playerName, self.__selectedZone.group.coordinator.player_name))


    @property
    def zones(self):
        if not self.__zone_ip:
            if not self._zones:
                self._zones = soco.discover(timeout=5)
        else:
            logging.info("Discovering with custom IP")
            self._zones = [soco.SoCo(self.__zone_ip)]
        return self._zones

    @property
    def groupMaster(self):
        return self.groupZones[0].group.coordinator

    __groupZones = None
    @property
    def groupZones(self):
        if not self.__groupZones:
            self.__groupZones = []

            # FUN FACT! Asking for the player name or UID sends a GET request to Sonos, every. time.
            # I have no idea why
            for z in self.__selectedZone.group.members:
                z._uid = str(z.uid)
                z._player_name = str(z.player_name)
                self.__groupZones.append(z)
        return self.__groupZones

    @property
    def settings(self):
        settings = {
            'volume':{},
            'current_queue_position':int(self.groupMaster.get_current_track_info()['playlist_position']),
            'current_playing_state':self.groupMaster.get_current_transport_info()['current_transport_state']
        }

        for z in self.groupZones:
            settings['volume'][z.uid] = int(z.volume)
        return settings
