/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <fstream>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

using namespace ns3;

//NS_LOG_COMPONENT_DEFINE ("FifthScriptExample");

// ===========================================================================
//
//         node 0                 node 1
//   +----------------+    +----------------+
//   |    ns-3 TCP    |    |    ns-3 TCP    |
//   +----------------+    +----------------+
//   |    10.1.1.1    |    |    10.1.1.2    |
//   +----------------+    +----------------+
//   | point-to-point |    | point-to-point |
//   +----------------+    +----------------+
//           |                     |
//           +---------------------+
//                5 Mbps, 2 ms
//
//
// We want to look at changes in the ns-3 TCP congestion window.  We need
// to crank up a flow and hook the CongestionWindow attribute on the socket
// of the sender.  Normally one would use an on-off application to generate a
// flow, but this has a couple of problems.  First, the socket of the on-off 
// application is not created until Application Start time, so we wouldn't be 
// able to hook the socket (now) at configuration time.  Second, even if we 
// could arrange a call after start time, the socket is not public so we 
// couldn't get at it.
//
// So, we can cook up a simple version of the on-off application that does what
// we want.  On the plus side we don't need all of the complexity of the on-off
// application.  On the minus side, we don't have a helper, so we have to get
// a little more involved in the details, but this is trivial.
//
// So first, we create a socket and do the trace connect on it; then we pass 
// this socket into the constructor of our simple application which we then 
// install in the source node.
// ===========================================================================
//
class MyApp : public Application 
{
public:

  MyApp ();
  virtual ~MyApp();

  void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);

private:
  virtual void StartApplication (void);
  virtual void StopApplication (void);

  void ScheduleTx (void);
  void SendPacket (void);

  Ptr<Socket>     m_socket;
  Address         m_peer;
  uint32_t        m_packetSize;
  uint32_t        m_nPackets;
  DataRate        m_dataRate;
  EventId         m_sendEvent;
  bool            m_running;
  uint32_t        m_packetsSent;
};

MyApp::MyApp ()
  : m_socket (0), 
    m_peer (), 
    m_packetSize (0), 
    m_nPackets (0), 
    m_dataRate (0), 
    m_sendEvent (), 
    m_running (false), 
    m_packetsSent (0)
{
}

MyApp::~MyApp()
{
  m_socket = 0;
}

int drops = 0;

void
MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
{
  m_socket = socket;
  m_peer = address;
  m_packetSize = packetSize;
  m_nPackets = nPackets;
  m_dataRate = dataRate;
}

void
MyApp::StartApplication (void)
{
  m_running = true;
  m_packetsSent = 0;
  m_socket->Bind ();
  m_socket->Connect (m_peer);
  SendPacket ();
}

void 
MyApp::StopApplication (void)
{
  m_running = false;

  if (m_sendEvent.IsRunning ())
    {
      Simulator::Cancel (m_sendEvent);
    }

  if (m_socket)
    {
      m_socket->Close ();
    }
}

void 
MyApp::SendPacket (void)
{
  Ptr<Packet> packet = Create<Packet> (m_packetSize);
  m_socket->Send (packet);

  if (++m_packetsSent < m_nPackets)
    {
      ScheduleTx ();
    }
}

void 
MyApp::ScheduleTx (void)
{
  if (m_running)
    {
      Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
      m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
    }
}

static void
CwndChange (uint32_t oldCwnd, uint32_t newCwnd)
{
  NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);
}

/*static void
RxDrop (Ptr<const Packet> p)
{
  NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
  
}*/

int 
main (int argc, char *argv[])
{

  CommandLine cmd;  
  cmd.Parse (argc, argv);
  
  std::string transport_prot = "ns3::TcpVegas";
  Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue (TypeId::LookupByName (transport_prot)));

  NodeContainer nodes;
  nodes.Create(5);

  NodeContainer n0n1 = NodeContainer (nodes.Get (0), nodes.Get (1));
  NodeContainer n1n2 = NodeContainer (nodes.Get (1), nodes.Get (2));
  NodeContainer n2n3 = NodeContainer (nodes.Get (2), nodes.Get (3));
  NodeContainer n2n4 = NodeContainer (nodes.Get (2), nodes.Get (4));
  
  InternetStackHelper stack;
  stack.Install (nodes);

  PointToPointHelper p2p;
  p2p.SetDeviceAttribute ("DataRate", StringValue ("500Kbps"));
  p2p.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer d0d1 = p2p.Install (n0n1);
  NetDeviceContainer d1d2 = p2p.Install (n1n2);
  NetDeviceContainer d2d3 = p2p.Install (n2n3);
  NetDeviceContainer d2d4 = p2p.Install (n2n4);
  
  p2p.EnablePcapAll("PacketsCapturedPart3");

  //NS_LOG_INFO ("Assign IP Addresses....");
  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.0.0", "255.255.255.0"); //n0,n1
  Ipv4InterfaceContainer i0i2 = ipv4.Assign (d0d1);
  ipv4.SetBase ("10.1.1.0", "255.255.255.0"); //n1, n2
  Ipv4InterfaceContainer i1i2 = ipv4.Assign (d1d2);
  ipv4.SetBase ("10.1.2.0", "255.255.255.0"); //n2, n3
  Ipv4InterfaceContainer i2i3 = ipv4.Assign (d2d3); 
  ipv4.SetBase ("10.1.3.0", "255.255.255.0"); //n2, n4
  Ipv4InterfaceContainer i2i4 = ipv4.Assign (d2d4);  


  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  uint16_t sinkPort = 8080;
  Address sinkAddress (InetSocketAddress (i2i3.GetAddress (1), sinkPort)); //yahan change karna padd sakta //chng
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), sinkPort));
  ApplicationContainer sinkApps = packetSinkHelper.Install(nodes.Get (3));
  sinkApps.Start (Seconds (1.));
  sinkApps.Stop (Seconds (100.));

   Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (nodes.Get (0), TcpSocketFactory::GetTypeId ());
  Ptr<MyApp> app1 = CreateObject<MyApp> ();
  app1->Setup (ns3TcpSocket, sinkAddress, 3000, 1000000, DataRate ("250Kbps"));
  nodes.Get (0)->AddApplication (app1);
  app1->SetStartTime (Seconds (1.));
  app1->SetStopTime (Seconds (100.));

 
  ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&CwndChange));

  
  //NS_LOG_INFO ("Create Applications.");
  uint16_t port = 40000;
  OnOffHelper onoff ("ns3::UdpSocketFactory", Address (InetSocketAddress (i2i4.GetAddress(1), port)));
  onoff.SetConstantRate (DataRate ("250Kbps"));
  ApplicationContainer apps = onoff.Install(nodes.Get(1));
  apps.Start (Seconds (20.0));
  apps.Stop (Seconds (30.0));
  
  PacketSinkHelper sink ("ns3::UdpSocketFactory",
                         Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
  apps = sink.Install (nodes.Get(4));
  apps.Start (Seconds (20.0));
  apps.Stop (Seconds (30.0)); 


  //NS_LOG_INFO ("Create Applications.");
  uint16_t port2 = 40001;   
  OnOffHelper onoff2 ("ns3::UdpSocketFactory", Address (InetSocketAddress (i2i4.GetAddress(1), port2)));
  onoff2.SetConstantRate (DataRate ("500Kbps"));
  ApplicationContainer apps4 = onoff2.Install(nodes.Get(1));
  apps4.Start (Seconds (30.0));
  apps4.Stop (Seconds (100.0));

  // Create a packet sink to receive these packets
  //PacketSinkHelper sink ("ns3::UdpSocketFactory", Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
  apps4 = sink.Install (nodes.Get(4));
  apps4.Start (Seconds (30.0));
  apps4.Stop (Seconds (100.0)); 
  
  

  std::cout << drops << " hi " << "\n";

  Simulator::Stop (Seconds (100));
  Simulator::Run ();
  Simulator::Destroy ();

  return 0;
}
