# from __future__ import with_statement
# from __future__ import absolute_import, print_function, unicode_literals
import Live
import sys
# import inspect
# import live_io
import OSC
import RemixNet

from collections import OrderedDict
from functools import partial
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlSurface import ControlSurface
# from _Framework.ControlSurface import ControlSurface
from _Framework.SubjectSlot import Subject
from ableton.v2.control_surface import ControlSurface as CS

from random import randint


from SimpleWebSocketServer import *

connections = []
class SimpleEcho(WebSocket):

    def handleMessage(self):
        self.sendMessage(self.data)

    def handleConnected(self):
        connections.append(self)
        self.sendMessage(u"CARMINE Connected")


    def handleClose(self):
        connections.remove(self)



server = SimpleWebSocketServer('', 8000, SimpleEcho, 0.016)
# server.serveforever()

# oscEndpoint = RemixNet.OSCEndpoint("localhost",9001, "", 9000)
# oscEndpoint = RemixNet.OSCEndpoint("localhost",9001, "", 9000)
def _(msg):
        # server.sendMessage(msg)
        for con in list(connections):
            con.sendMessage(u""+msg)
        # pass

# import OSProxy
class Carmine:
    __module__ = __name__
    def __init__(self, c_instance):
        self.instance = c_instance
        self.slisten = {}
        self.clisten = {}
        self.song = self.instance.song()
        self.app = Live.Application.get_application()
        self.actions = []
        
        _("adding listeners!")
        if self.song.visible_tracks_has_listener(self.addListeners) != 1:
           self.song.add_visible_tracks_listener(self.addListeners)
        
        self.addListeners()
        self.instance.show_message("CARMINE")

    def refresh_state(self):
        pass

    def add_slotlistener(self, slot, tid, cid):
        cb = lambda :self.slot_changestate(slot, tid, cid)

        if self.slisten.has_key(slot) != 1:
            slot.add_has_clip_listener(cb)
            self.slisten[slot] = cb   
    
    def rem_clip_listeners(self):
        for slot in self.slisten:
            if slot != None:
                if slot.has_clip_has_listener(self.slisten[slot]) == 1:
                    slot.remove_has_clip_listener(self.slisten[slot])
    
        self.slisten = {}

    def slot_changestate(self, slot, tid, cid):
        # tmptrack = LiveUtils.getTrack(tid)
        # armed = tmptrack.arm and 1 or 0
        
        # Added new clip
        if slot.clip != None:
            self.add_cliplistener(slot.clip, tid, cid)
            
    # def loadDevice(self, name):
    #     _("Loadig device " + str(name))
    #     FailedToFind = 1
    #     projectFolder = self.app.browser.current_project
    #     _(str(projectFolder))
    #     # print(projectFolder.name)
    #     item_iterator = projectFolder.iter_children
    #     inneritems = [item for item in item_iterator]
    #     for item in inneritems:
    #         if item.name == "presets":
    #             presetsIter = item.iter_children
    #             presets = [preset for preset in presetsIter]
    #             for preset in presets:
    #                 if(preset.name == name + ".adg"):
    #                     _("found item -> attempt to load!")
    #                     self.app.browser.load_item(preset)
    #                     return True
    #     _("could not find preset " + str(name))
    #     return False


    def loadDevice(self,name):
        _("Loadig device " + str(name))
        projectFolder = self.app.browser.current_project
        inneritems = [item for item in projectFolder.iter_children]
        for item in inneritems:
            if item.name == "presets":
                presets = [preset for preset in item.iter_children]
                if self.folderSearch(presets, name, 1):
                    return True

        _("cound not find preset " + name)
        return False

    def folderSearch(self, presets, name, iterCounter):
        # print presets
        if(iterCounter > 5):
            _("reached max recursion level, exiting..")
            return False
        for preset in presets:
            if(preset.is_folder):
                folder_presets = [p for p in preset.iter_children]
                if self.folderSearch(folder_presets,name, iterCounter+1):
                    return True

            if(preset.name == name + ".adg"):
                _("found item " + name + "-> attempt to load!")
                self.app.browser.load_item(preset)
                return True

        return False


    def add_cliplistener(self, clip, tid, cid):
        cb = lambda :self.clip_changestate(clip, tid, cid)
        
        if self.clisten.has_key(clip) != 1:
            clip.add_playing_status_listener(cb)
            self.clisten[clip] = cb

    def clip_changestate(self, clip, x, y):
        _("Listener: x: " + str(x) + " y: " + str(y))

        state = 1
        
        if clip.is_playing == 1:
            state = 2
            
        if clip.is_triggered == 1:
            state = 3
        _(str(clip.name) + " > state:" + str(state))
        
        
          # skip this if names of loaded device is already same as clip we are launching
            
        if(state == 2 and clip.name != ""):
            if(clip.canonical_parent.canonical_parent.devices[0].name != clip.name):
                load_success = self.loadDevice(clip.name)
                if(load_success != True):
                    self.actions.append(lambda: self.loading_failed(clip))
        # self._send_pos[x] = 3
    def loading_failed(self, clip):
        clip.color_index = 14

    def addListeners(self):
        self.rem_clip_listeners()
        
        tracks = self.song.visible_tracks
        clipSlots = []
        for track in tracks:
            clipSlots.append(track.clip_slots)
        tracks = clipSlots
        for track in range(len(tracks)):
            for clip in range(len(tracks[track])):
                c = tracks[track][clip]            
                if c.clip != None:
                    pass
                    # print(c.clip)
                    self.add_cliplistener(c.clip, track, clip)
                
                self.add_slotlistener(c, track, clip)
   
    ######################## ABLETON STUFF @@@@@@@@@@@@
    def update_display(self):

        for action in self.actions:
            action()
        actions = []
        server.serve()

    def refresh_state(self):
        pass
    def build_midi_map(self, midi_map_handle):
        self.refresh_state()            
            
    def disconnect(self):
        # oscEndpoint.shutdown()
        _("Closing session...")
        server.close()
        pass
        
    def connect_script_instances(self, instanciated_scripts):
        """
        Called by the Application as soon as all scripts are initialized.
        You can connect yourself to other running scripts here, as we do it
        connect the extension modules
        """
        return

        def send_midi(self, midi_event_bytes):
            pass

    def receive_midi(self, midi_bytes):
        return

    def can_lock_to_devices(self):
        return False

    def suggest_input_port(self):
        return ''

    def suggest_output_port(self):
        return ''
