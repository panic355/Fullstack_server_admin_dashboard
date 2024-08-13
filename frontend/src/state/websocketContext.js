import React, { createContext, useState, useEffect } from 'react';
import io from 'socket.io-client';

const WebSocketContext = createContext();

const WebSocketProvider = ({ children }) => {
  const [stats, setStats] = useState({
    cpu_load: 0,
    ram_usage: 0,
    storage_usage: 0,
    net_io: {}
  });

  useEffect(() => {
    const socket = io('ws://192.168.0.11:6969');

    socket.on('system_stats', (data) => {
      setStats(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={stats}>
      {children}
    </WebSocketContext.Provider>
  );
};

export { WebSocketContext, WebSocketProvider };