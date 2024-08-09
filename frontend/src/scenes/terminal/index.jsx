import React, { useState } from 'react';
import { Box, useTheme } from "@mui/material";
import { useGetAdminsQuery } from "state/api";
import Header from "components/Header";
import { ReactTerminal } from "react-terminal";

const Terminal = () => {

  const [terminalOutput, setTerminalOutput] = useState([]);
  const [connected, setConnected] = useState(false);
  const [connectionInfo, setConnectionInfo] = useState({
    host: '192.168.0.11',
    username: 'panic',
    password: '35512',
  });

  const connectToSSH = async () => {
    const response = await fetch('http://localhost:5001/ssh/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(connectionInfo),
    });

    const result = await response.json();
    if (result.success) {
      setConnected(true);
      setTerminalOutput([...terminalOutput, 'Connected to SSH server.']);
    } else {
      setTerminalOutput([...terminalOutput, 'Failed to connect: ' + result.error]);
    }
  };

  const handleCommand = async (command) => {
    console.log('Executing command:');
    if (!connected) {
      setTerminalOutput([...terminalOutput, 'Not connected to any SSH session.']);
      return;
    }

    const response = await fetch('http://localhost:5001/ssh/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command }),
    });

    const result = await response.json();
    setTerminalOutput([...terminalOutput, result.output]);
    return result.output;
  };

  const commands = {
    ssh: () => connectToSSH(),
    help: () => {
      return 'Available commands: ssh, help';
    },
    '*': handleCommand,
  };


  return (
    <Box m="1.5rem 2.5rem">
      <Header title="Terminal" subtitle="Managing your system though SSH" />
      <Box
        mt="40px"
        height="75vh"
      >
        <ReactTerminal
          showControlBar={false}
          commands={commands}
          welcomeMessage="Type 'ssh' to connect to the server."
          prompt=">"
          commandCallback={handleCommand}
          output={terminalOutput.join('\n')}
          themes={{
            "my-custom-theme": {
              themeBGColor: "#272B36",
              themeToolbarColor: "#DBDBDB",
              themeColor: "#FFFEFC",
              themePromptColor: "#a917a8",
            },
          }}
          theme="my-custom-theme"
        />
      </Box>
    </Box>
  );
};

export default Terminal;
