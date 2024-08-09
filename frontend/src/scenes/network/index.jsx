import React from "react";
import { Box, useTheme } from "@mui/material";
import { useGetAdminsQuery } from "state/api";
import { DataGrid } from "@mui/x-data-grid";
import Header from "components/Header";
import CustomColumnMenu from "components/DataGridCustomColumnMenu";
import { ReactTerminal } from "react-terminal";
import RealtimeGraph from 'components/RealtimeGraph';

const Network = () => {
    const theme = useTheme();
    const cpuNetworkSeries = [
        { id: 'Upload', key: 'net_io_sent' },
        { id: 'Download', key: 'net_io_recv' }
    ];

    const yAxisRange = { min: 0, max: 200 }
    return (
        <Box m="1.5rem 2.5rem">
        <Header title="Network" subtitle="Managing your network" />
        <Box height="75vh">
                <RealtimeGraph
                    url="http://localhost:6789/data"
                    series={cpuNetworkSeries}
                    pollingInterval={1000}
                    yAxisRange={yAxisRange}
                />
            </Box>
        </Box>
    );
};

export default Network;