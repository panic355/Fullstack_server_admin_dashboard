import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

// Create a reusable WebSocket component
const WebSocketComponent = ({ url, onMessage }) => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState('');
  const [serverMessage, setServerMessage] = useState('');

  useEffect(() => {
    // Establish WebSocket connection
    const socketIo = io(url);

    setSocket(socketIo);

    // Handle incoming messages
    socketIo.on('response', (data) => {
      console.log('Message from server:', data);
      setServerMessage(data);
      if (onMessage) {
        onMessage(data); // Callback to parent component
      }
    });

    // Clean up on component unmount
    return () => {
      socketIo.off('response');
      socketIo.close();
    };
  }, [url, onMessage]);

  // Function to send a message to the server
  const sendMessage = () => {
    
    if (socket) {
      alert('is connected');
      socket.send(message);
      console.info('Sent message to server:', message);
      setMessage('');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter message"
        style={{ padding: '10px', width: '300px' }}
      />
      <button onClick={sendMessage} style={{ padding: '10px', marginLeft: '10px' }}>
        Send
      </button>
      <h2>Message from Server: {serverMessage}</h2>
    </div>
  );
};

export default WebSocketComponent;