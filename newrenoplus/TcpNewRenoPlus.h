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
#ifndef TCPNEWRENOPLUS_H
#define TCPNEWRENOPLUS_H

#include "ns3/tcp-socket-state.h"
#include "ns3/tcp-congestion-ops.h"

namespace ns3 {

/**
 * \ingroup tcp
 * \defgroup congestionOps Congestion Control Algorithms.
 *
 * The various congestion control algorithms, also known as "TCP flavors".
 */

/**
 * \ingroup congestionOps
 *
 * \brief Congestion control abstract class
 *
 * The design is inspired on what Linux v4.0 does (but it has been
 * in place since years). The congestion control is split from the main
 * socket code, and it is a pluggable component. An interface has been defined;
 * variables are maintained in the TcpSocketState class, while subclasses of
 * TcpCongestionOps operate over an instance of that class.
 *
 * Only three methods has been utilized right now; however, Linux has many others,
 * which can be added later in ns-3.
 *
 * \see IncreaseWindow
 * \see PktsAcked
 */
 
 /*
class TcpCongestionOps : public Object
{
public:
  static TypeId GetTypeId (void);

  TcpCongestionOps ();
  TcpCongestionOps (const TcpCongestionOps &other);

  virtual ~TcpCongestionOps ();
  virtual std::string GetName () const = 0;
  virtual uint32_t GetSsThresh (Ptr<const TcpSocketState> tcb,
                                uint32_t bytesInFlight) = 0;
  virtual void IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked) = 0;
  virtual void PktsAcked (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked,
                          const Time& rtt)
  {
    NS_UNUSED (tcb);
    NS_UNUSED (segmentsAcked);
    NS_UNUSED (rtt);
  }
  virtual void CongestionStateSet (Ptr<TcpSocketState> tcb,
                                   const TcpSocketState::TcpCongState_t newState)
  {
    NS_UNUSED (tcb);
    NS_UNUSED (newState);
  }
  virtual void CwndEvent (Ptr<TcpSocketState> tcb,
                          const TcpSocketState::TcpCAEvent_t event)
  {
    NS_UNUSED (tcb);
    NS_UNUSED (event);
  }
  virtual Ptr<TcpCongestionOps> Fork () = 0;
};


*/
class TcpNewRenoPlus : public TcpNewReno
{
public:
  /**
   * \brief Get the type ID.
   * \return the object TypeId
   */
  static TypeId GetTypeId (void);

  TcpNewRenoPlus ();

  /**
   * \brief Copy constructor.
   * \param sock object to copy.
   */
  TcpNewRenoPlus (const TcpNewRenoPlus& sock);

  ~TcpNewRenoPlus ();

  std::string GetName () const;

  virtual void IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual uint32_t GetSsThresh (Ptr<const TcpSocketState> tcb,
                                uint32_t bytesInFlight);

  virtual Ptr<TcpCongestionOps> Fork ();

protected:
  virtual uint32_t SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual void CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
};

} // namespace ns3

#endif // TCPCONGESTIONOPS_H
