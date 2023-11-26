/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2015 Natale Patriciello <natale.patriciello@gmail.com>
 *
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
 *
 */
#include "TcpNewRenoPlus.h"
#include "tcp-socket-base.h"
#include "ns3/log.h"
#include <math.h>

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("TcpNewRenoPlus");
NS_OBJECT_ENSURE_REGISTERED (TcpNewRenoPlus);

/*
TypeId
TcpCongestionOps::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::TcpNewRenoPlus")
    .SetParent<Object> ()
    .SetGroupName ("Internet")
  ;
  return tid;
}

TcpCongestionOps::TcpCongestionOps () : Object ()
{
}

TcpCongestionOps::TcpCongestionOps (const TcpCongestionOps &other) : Object (other)
{
}

TcpCongestionOps::~TcpCongestionOps ()
{
}

*/

// RENO

//NS_OBJECT_ENSURE_REGISTERED (TcpNewRenoPlus);

TypeId
TcpNewRenoPlus::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::TcpNewRenoPlus")
    .SetParent<TcpNewReno> ()
    .SetGroupName ("Internet")
    .AddConstructor<TcpNewRenoPlus> ()
  ;
  return tid;
}

TcpNewRenoPlus::TcpNewRenoPlus (void) : TcpNewReno ()
{
  NS_LOG_FUNCTION (this);
}

TcpNewRenoPlus::TcpNewRenoPlus (const TcpNewRenoPlus& sock)
  : TcpNewReno (sock)
{
  NS_LOG_FUNCTION (this);
}

TcpNewRenoPlus::~TcpNewRenoPlus (void)
{
}



uint32_t
TcpNewRenoPlus::SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  NS_LOG_FUNCTION (this << tcb << segmentsAcked);

  if (segmentsAcked >= 1)
    {
      //tcb->m_cWnd += tcb->m_segmentSize;
      tcb->m_cWnd += static_cast<uint32_t> (pow((tcb->m_segmentSize), 1.91)/(tcb->m_cWnd));
      NS_LOG_INFO ("In SlowStart, updated to cwnd " << tcb->m_cWnd << " ssthresh " << tcb->m_ssThresh);
      return segmentsAcked - 1;
    }

  return 0;
}


void
TcpNewRenoPlus::CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  NS_LOG_FUNCTION (this << tcb << segmentsAcked);

  if (segmentsAcked > 0)
    {
      //double adder = static_cast<double> (tcb->m_segmentSize * tcb->m_segmentSize) / tcb->m_cWnd.Get ();
      //adder = std::max (1.0, adder);
      //tcb->m_cWnd += static_cast<uint32_t> (adder);
      tcb->m_cWnd += static_cast<uint32_t> (0.51* tcb->m_segmentSize);
      NS_LOG_INFO ("In CongAvoid, updated to cwnd " << tcb->m_cWnd <<
                   " ssthresh " << tcb->m_ssThresh);
    }
}


void
TcpNewRenoPlus::IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked)
{
  NS_LOG_FUNCTION (this << tcb << segmentsAcked);

  if (tcb->m_cWnd < tcb->m_ssThresh)
    {
      segmentsAcked = SlowStart (tcb, segmentsAcked);
    }

  if (tcb->m_cWnd >= tcb->m_ssThresh)
    {
      CongestionAvoidance (tcb, segmentsAcked);
    }

}

std::string
TcpNewRenoPlus::GetName () const
{
  return "TcpNewRenoPlus";
}

uint32_t
TcpNewRenoPlus::GetSsThresh (Ptr<const TcpSocketState> state,
                         uint32_t bytesInFlight)
{
  NS_LOG_FUNCTION (this << state << bytesInFlight);

  return std::max (2 * state->m_segmentSize, bytesInFlight / 2);
}

Ptr<TcpCongestionOps>
TcpNewRenoPlus::Fork ()
{
  return CopyObject<TcpNewRenoPlus> (this);
}

}
 // namespace ns3

