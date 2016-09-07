<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <project EXPORT="discard">[APPS_DIR]/mrm</project>
  <project EXPORT="discard">[APPS_DIR]/mspsim</project>
  <project EXPORT="discard">[APPS_DIR]/avrora</project>
  <project EXPORT="discard">[APPS_DIR]/serial_socket</project>
  <project EXPORT="discard">[APPS_DIR]/collect-view</project>
  <project EXPORT="discard">[APPS_DIR]/powertracker</project>
  <project EXPORT="discard">[APPS_DIR]/realsim</project>
  <simulation>
    <title>My simulation</title>
    <randomseed>123456</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>org.contikios.cooja.radiomediums.DirectedGraphMedium</radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.SkyMoteType
      <identifier>sky1</identifier>
      <description>Sky Mote Type #sky1</description>
      <source EXPORT="discard">[CONTIKI_DIR]/examples/hello-world/hello-world.c</source>
      <commands EXPORT="discard">make hello-world.sky TARGET=sky</commands>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/hello-world/hello-world.sky</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyFlash</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyCoffeeFilesystem</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.SkyTemperature</moteinterface>
    </motetype>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.SimControl
    <width>290</width>
    <z>1</z>
    <height>192</height>
    <location_x>811</location_x>
    <location_y>431</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <viewport>0.9090909090909091 0.0 0.0 0.9090909090909091 134.76363636363638 118.41818181818184</viewport>
    </plugin_config>
    <width>300</width>
    <z>2</z>
    <height>300</height>
    <location_x>806</location_x>
    <location_y>68</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <width>962</width>
    <z>5</z>
    <height>150</height>
    <location_x>77</location_x>
    <location_y>656</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <width>962</width>
    <z>6</z>
    <height>150</height>
    <location_x>85</location_x>
    <location_y>866</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.springlayout.SpringLayout
    <width>520</width>
    <z>4</z>
    <height>320</height>
    <location_x>24</location_x>
    <location_y>311</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.realsim.RealSimFile
    <plugin_config>
      <Filename>[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/realsim_test/realsim_example.realsimfile</Filename>
      <Load>true</Load>
      <SimEvent time="6000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>34640</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="6000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>12306</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="26000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>26005</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="31000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>34851</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="56000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>63270</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="56000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>13075</ID>
        <MoteType>sky1</MoteType>
      </SimEvent>
      <SimEvent time="56000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>12306</dst>
          <ratio>0.0</ratio>
          <rssi>71.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="61000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>70.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="68000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>12306</dst>
          <ratio>0.5</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="72000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>73.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="75000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>12306</dst>
          <ratio>0.9</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="76000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.9</ratio>
          <rssi>45.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="76000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="76000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.8</ratio>
          <rssi>52.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="76000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>81.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="78000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34851</dst>
          <ratio>0.0</ratio>
          <rssi>76.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="81000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>26005</dst>
          <ratio>0.0</ratio>
          <rssi>62.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="81000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>79.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="83000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>34851</dst>
          <ratio>1.0</ratio>
          <rssi>42.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="87000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>13075</dst>
          <ratio>0.9</ratio>
          <rssi>40.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="88000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>26005</dst>
          <ratio>0.9</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="90000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34851</dst>
          <ratio>0.9</ratio>
          <rssi>70.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="93000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>26005</dst>
          <ratio>1.1</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="94000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>13075</dst>
          <ratio>1.1</ratio>
          <rssi>82.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="96000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>39.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="99000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>26005</dst>
          <ratio>1.0</ratio>
          <rssi>78.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="100000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>13075</dst>
          <ratio>1.0</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="106000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>13075</dst>
          <ratio>0.8</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="106000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>26005</dst>
          <ratio>0.7</ratio>
          <rssi>54.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="150000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="150000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>50.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="150000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.5</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="150000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>44.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="150000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34640</dst>
          <ratio>0.2</ratio>
          <rssi>58.0</rssi>
          <delay>0</delay>
          <lqi>103</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="151000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>73.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="157000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>12306</dst>
          <ratio>0.7</ratio>
          <rssi>49.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="164000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>12306</dst>
          <ratio>1.2</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="169000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34851</dst>
          <ratio>0.4</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="169000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>78.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="176000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>12306</dst>
          <ratio>0.4</ratio>
          <rssi>76.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="176000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>34851</dst>
          <ratio>1.2</ratio>
          <rssi>43.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="182000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>26005</dst>
          <ratio>0.9</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="182000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>13075</dst>
          <ratio>1.2</ratio>
          <rssi>81.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="183000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34851</dst>
          <ratio>0.6</ratio>
          <rssi>72.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="187000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>26005</dst>
          <ratio>1.3</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="187000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>35.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="189000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>13075</dst>
          <ratio>0.5</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="193000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>26005</dst>
          <ratio>0.6</ratio>
          <rssi>78.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="193000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34851</dst>
          <ratio>0.9</ratio>
          <rssi>73.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="194000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>13075</dst>
          <ratio>0.9</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>26005</dst>
          <ratio>0.7</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>13075</dst>
          <ratio>0.9</ratio>
          <rssi>33.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="205000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>26005</dst>
          <ratio>0.9</ratio>
          <rssi>61.0</rssi>
          <delay>0</delay>
          <lqi>102</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="206000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>13075</dst>
          <ratio>0.9</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="211000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>63270</dst>
          <ratio>1.1</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="212000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.3</ratio>
          <rssi>52.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="212000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.3</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="212000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.4</ratio>
          <rssi>45.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="212000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>49.0</rssi>
          <delay>0</delay>
          <lqi>103</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="212000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.4</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="218000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>63270</dst>
          <ratio>0.6</ratio>
          <rssi>44.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="224000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>63270</dst>
          <ratio>0.8</ratio>
          <rssi>57.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="230000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>63270</dst>
          <ratio>0.9</ratio>
          <rssi>77.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="236000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>63270</dst>
          <ratio>0.8</ratio>
          <rssi>72.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="258000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="264000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>12306</dst>
          <ratio>1.2</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="267000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>34851</dst>
          <ratio>1.1</ratio>
          <rssi>44.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="268000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="268000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>45.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="268000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34640</dst>
          <ratio>0.4</ratio>
          <rssi>50.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="268000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.5</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="268000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="271000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>79.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="274000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34851</dst>
          <ratio>0.9</ratio>
          <rssi>72.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="278000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>12306</dst>
          <ratio>1.0</ratio>
          <rssi>75.0</rssi>
          <delay>0</delay>
          <lqi>103</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="279000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34851</dst>
          <ratio>0.8</ratio>
          <rssi>34.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="281000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>13075</dst>
          <ratio>0.8</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="281000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>26005</dst>
          <ratio>1.1</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="284000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="286000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>73.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="286000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>13075</dst>
          <ratio>0.7</ratio>
          <rssi>51.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="287000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>26005</dst>
          <ratio>0.7</ratio>
          <rssi>79.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="291000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>13075</dst>
          <ratio>0.7</ratio>
          <rssi>31.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="292000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34851</dst>
          <ratio>0.9</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="293000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>26005</dst>
          <ratio>0.8</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="297000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>13075</dst>
          <ratio>0.8</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="300000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>26005</dst>
          <ratio>0.8</ratio>
          <rssi>61.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="303000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>13075</dst>
          <ratio>1.2</ratio>
          <rssi>82.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="306000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>26005</dst>
          <ratio>0.8</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="311000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>63270</dst>
          <ratio>0.8</ratio>
          <rssi>43.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="317000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>63270</dst>
          <ratio>0.7</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="323000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>63270</dst>
          <ratio>0.7</ratio>
          <rssi>78.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="330000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>63270</dst>
          <ratio>0.6</ratio>
          <rssi>72.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="335000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>63270</dst>
          <ratio>1.3</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="336000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.5</ratio>
          <rssi>43.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="336000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34640</dst>
          <ratio>0.5</ratio>
          <rssi>50.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="336000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>51.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="336000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.3</ratio>
          <rssi>51.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="336000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>81.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="359000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>12306</dst>
          <ratio>1.1</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="365000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>12306</dst>
          <ratio>0.7</ratio>
          <rssi>79.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="367000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>72.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="372000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>75.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="373000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34851</dst>
          <ratio>0.9</ratio>
          <rssi>34.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="376000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>13075</dst>
          <ratio>0.8</ratio>
          <rssi>52.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="378000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>12306</dst>
          <ratio>0.8</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="379000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34851</dst>
          <ratio>0.8</ratio>
          <rssi>73.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="383000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>13075</dst>
          <ratio>0.8</ratio>
          <rssi>31.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="384000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>12306</dst>
          <ratio>0.9</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="385000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34851</dst>
          <ratio>0.7</ratio>
          <rssi>80.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="386000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>26005</dst>
          <ratio>0.7</ratio>
          <rssi>79.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="389000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>13075</dst>
          <ratio>0.6</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="390000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>34851</dst>
          <ratio>1.1</ratio>
          <rssi>44.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="393000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>26005</dst>
          <ratio>0.9</ratio>
          <rssi>53.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="394000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>13075</dst>
          <ratio>1.0</ratio>
          <rssi>81.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="399000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>13075</dst>
          <ratio>0.6</ratio>
          <rssi>47.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="400000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>26005</dst>
          <ratio>0.8</ratio>
          <rssi>61.0</rssi>
          <delay>0</delay>
          <lqi>104</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>63270</src>
          <dst>34640</dst>
          <ratio>0.7</ratio>
          <rssi>49.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>12306</src>
          <dst>34640</dst>
          <ratio>0.2</ratio>
          <rssi>52.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>34640</dst>
          <ratio>0.6</ratio>
          <rssi>52.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>13075</src>
          <dst>34640</dst>
          <ratio>0.5</ratio>
          <rssi>81.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>34640</dst>
          <ratio>0.4</ratio>
          <rssi>48.0</rssi>
          <delay>0</delay>
          <lqi>103</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="406000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34851</src>
          <dst>26005</dst>
          <ratio>0.8</ratio>
          <rssi>74.0</rssi>
          <delay>0</delay>
          <lqi>107</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="412000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>34640</src>
          <dst>26005</dst>
          <ratio>1.3</ratio>
          <rssi>55.0</rssi>
          <delay>0</delay>
          <lqi>106</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="414000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>26005</src>
          <dst>63270</dst>
          <ratio>0.8</ratio>
          <rssi>54.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
    </plugin_config>
    <width>552</width>
    <z>3</z>
    <height>294</height>
    <location_x>54</location_x>
    <location_y>-3</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <script>/*
 * Example Contiki test script (JavaScript).
 * A Contiki test script acts on mote output, such as via printf()'s.
 * The script may operate on the following variables:
 *  Mote mote, int id, String msg
 */

/* Make test automatically fail (timeout) after 100 simulated seconds */
//TIMEOUT(100000); /* milliseconds. no action at timeout */
TIMEOUT(100000, log.log("last msg: " + msg + "\n")); /* milliseconds. print last msg at timeout */

log.log("first mote output: '" + msg + "'\n");

YIELD(); /* wait for another mote output */

log.log("second mote output: '" + msg + "'\n");

log.log("waiting for hello world output from mote 1\n");
WAIT_UNTIL(id == 1 &amp;&amp; msg.equals("Hello, world"));

write(mote, "Hello, mote\n"); /* Write to mote serial port */

GENERATE_MSG(15000, "continue");
YIELD_THEN_WAIT_UNTIL(msg.equals("continue"));

log.log("ok, reporting success now\n");
log.testOK(); /* Report test success and quit */
//log.testFailed(); /* Report test failure and quit */</script>
      <active>false</active>
    </plugin_config>
    <width>600</width>
    <z>0</z>
    <height>700</height>
    <location_x>207</location_x>
    <location_y>412</location_y>
  </plugin>
</simconf>

