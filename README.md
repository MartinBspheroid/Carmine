![Carmine logo](https://i.ibb.co/tD5c38y/carmine-Logo.png)

Carmine is Ableton user remote script for Ableton Live. It allows you to recall Instrument racks by triggering clips in session view, designed to provide streamlined workflow during both preparation and performance of live sets.


Did you ever wonder how to recall instruments per clip? Sure, there are a couple of ways to do that at the moment.

#### Recall by sending MIDI Program change set via clips:

-   Not much VSTs support
-   program changes are not propagating through device chain,
-   complete lack of support in all Ableton devices

#### ClyphX Pro

-   but you cannot be bothered to write scripts

#### VST host that's acting like VSTi

-   need to save changes to devices anytime you make some changes

#### Reaktor with Program changes

-   I used to do that, but Snapshot managing became a nightmare

That's why I decided to poke around Ableton Live's API and came up with this solution. Initial attempt to use one device per track and just save/restore settings was soon replaced when I discovered that you can load whole Intrument racks, including internal sends/returns & macros (which was essential due to fact that I use Push2 as the main controller).

Now Carmine tries to address these issues by following this rule: 

##### Clip name => Preset name

So it's easy as this: 

 1. Tweak/design your sound with devices way you want
 2. Pack all devices and vsts to Instrument rack and save it to `presets` folder in your current project
 3. Rename clip to match name of that Instrument Rack
 4. Recall this Instrument rack later by triggering it. 

Easy, right? 

You need to change preset settings ? Save it again and overwrite old one. No need to navigate in window of our VST host or menu dive into Intrument rack chains. 
All your settings are persistantly saved within your project folder. No external settings or extra files. 

### Installation
Please refer to [this official article on](https://help.ableton.com/hc/en-us/articles/209072009-Installing-Third-Party-Control-Surfaces) Ableton's website. 
Clear and straight forward instructions, pretty much copy paste one folder to different folder. 
You can confirm that Carmine is working by making a new liveset, there should be yellow message popping at the bottom like 

    Control surface 2 -> CARMINE


### Usage

To load a Script, there has to be a folder called `presets` made in your current project. Make sure there's one, as this is a place where Carmine will pull presets from. 

Once Carmine is active it changes behaviour of clips in couple of certain ways:

 - If clips **has a name, it will automatically try to load Instrument rack** (or any *.adv file so to speak) onto channel once clip starts playing. 
 - This means that **it will replace just Instrument**, *not any effects that are already stacked after current Instrument or Instrument rack.* That way, you can keep all your filters/effects that you might use after Intrument as they are and  only replace instrument.  
 - **If Carmine cannot find  preset in your** `presets` **folder, it will change color of this clip to red to mark that it's unable to perform loading action.** 
 - If clip has **no name at all**, Carmine will **disregard this clip.** 
 - You can store clips store clips in folders, up to 5 levels deep, to better organize presets. **Please keep in mind that in order for loading to work properly, presets should have unique names** (_eg.if presets have same name, Carmine will load first preset it will encounter during search_) 
 
#### DEVELOPMENT:
- Fork, send PR to your hearts desire. I'm not fluid in Python, so this is pretty much hacked version of liveOSC (specificaly [this version](https://github.com/dinchak/node-liveosc).
- Repo contains convinient **websocket.html** file, which might be used to debug script, as it communicate with outside world using websockets (on port 8000). Unfortunately, if things go south, you still have to go to Log.txt, hidden one Ableton folder, hidden in depths of your hard drive. One day, I will be able to somehow redirrect this to websockets as well. Hopefully. 

### TODO: 
- check out how to handle automation on the clips. 
- check all the clips upon project loads and mark all missing presets. 
- scene launching is broken, I need to find out how to schedule loading all instruments one by one. 
- when retriggering already loaded clip, there should be option to change behavour to recall all original parameters, instead of just relaunching the clip. Think: using macros to mess up the sound with distortion, prolong release/reverb/delay into wall of noise and change it into original staccato mode with one push. 

### Thanks to: 

 - Ableton for making Live and all those endless hours of fun I had over
   the years.

 - Luciano for making [this](https://github.com/lucianoiam/live_rpyc), and making my life much easier.
 - [This project](https://github.com/dinchak/node-liveosc) for pushing me towards right direction while poking around Live API (I actually borrowed some of the code as well).
 - [Isotonik's ClyphX Pro](https://isotonikstudios.com/product/clyphx-pro/) for showing me what is possible in Live with user script.

### Credits:
 - Websockets library is slightly modified version of [this library](https://github.com/dpallot/simple-websocket-server) made by [Dave](https://github.com/dpallot)