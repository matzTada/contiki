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
    <randomseed>generated</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>org.contikios.cooja.radiomediums.DirectedGraphMedium</radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.Z1MoteType
      <identifier>z11</identifier>
      <description>Z1 Mote Type receiver</description>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/nodes_REALSIM/node-receiver-leapfrog.z1</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDefaultSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <motetype>
      org.contikios.cooja.mspmote.Z1MoteType
      <identifier>z12</identifier>
      <description>Z1 Mote Type sender</description>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/nodes_REALSIM/node-sender-leapfrog-replicate.z1</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDefaultSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>0.6309702065965581</x>
        <y>71.83942531741528</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>1</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>53.512341499486524</x>
        <y>72.84565070183504</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>2</id>
      </interface_config>
      <motetype_identifier>z12</motetype_identifier>
    </mote>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.SimControl
    <width>280</width>
    <z>6</z>
    <height>160</height>
    <location_x>400</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.DGRMVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <viewport>3.6118582284019114 0.0 0.0 3.6118582284019114 108.75435038406056 -107.81321339576489</viewport>
    </plugin_config>
    <width>400</width>
    <z>4</z>
    <height>400</height>
    <location_x>1</location_x>
    <location_y>1</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <width>935</width>
    <z>3</z>
    <height>240</height>
    <location_x>400</location_x>
    <location_y>160</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <mote>0</mote>
      <mote>1</mote>
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <width>1335</width>
    <z>2</z>
    <height>146</height>
    <location_x>9</location_x>
    <location_y>1004</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <width>655</width>
    <z>5</z>
    <height>160</height>
    <location_x>680</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <scriptfile>[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/scenario/realsim_test_script.js</scriptfile>
      <active>false</active>
    </plugin_config>
    <width>600</width>
    <z>0</z>
    <height>700</height>
    <location_x>702</location_x>
    <location_y>282</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.realsim.RealSimFile
    <plugin_config>
      <Filename>[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/scenario/realsim_test.realsimfile</Filename>
      <Load>false</Load>
      <SimEvent time="500">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>1</ID>
        <MoteType>z11</MoteType>
      </SimEvent>
      <SimEvent time="500">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventAddNode
        <ID>2</ID>
        <MoteType>z12</MoteType>
      </SimEvent>
      <SimEvent time="1000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>1.0</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="1000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>1.0</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="600000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>1.0</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="600000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>1.0</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="1200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.9</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="1200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.9</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="1800000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.8</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="1800000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.8</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="2400000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.7</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="2400000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.7</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="3000000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.6</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="3000000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.6</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="3600000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.5</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="3600000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.5</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="4200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.4</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="4200000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.4</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="4800000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.3</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="4800000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.3</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="5400000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.2</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="5400000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.2</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="6000000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>1</src>
          <dst>2</dst>
          <ratio>0.1</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
      <SimEvent time="6000000">
        de.fau.cooja.plugins.realsim.RealSimFile$SimEventSetEdge
        <RSE>
          <src>2</src>
          <dst>1</dst>
          <ratio>0.1</ratio>
          <rssi>-10.0</rssi>
          <delay>0</delay>
          <lqi>105</lqi>
        </RSE>
      </SimEvent>
    </plugin_config>
    <width>396</width>
    <z>1</z>
    <height>657</height>
    <location_x>298</location_x>
    <location_y>342</location_y>
  </plugin>
</simconf>

