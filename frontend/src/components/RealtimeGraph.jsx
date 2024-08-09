import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ResponsiveLine } from '@nivo/line';
import { Box, useTheme, Typography } from "@mui/material";
import Header from "components/Header";
import FlexBetween from "./FlexBetween";



/**
 * Reusable RealtimeGraph component.
 * 
 * @param {Object} props
 * @param {string} props.url - URL for the HTTP polling.
 * @param {Array} props.series - Array of series configuration objects.
 * @param {number} props.pollingInterval - Interval for polling in milliseconds.
 * @param {boolean} props.loading - Loading state.
 */
const RealtimeGraph = ({ url, series, pollingInterval = 5000, yAxisRange, icon , title}) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const theme = useTheme();

    // Function to fetch data from the server
    const fetchData = async () => {
        try {
            const response = await axios.get(url);
            const newData = response.data;
            const timestamp = new Date().toISOString();

            // Add the new data point to the state
            setData(prevData => {
                const updatedData = [
                    ...prevData,
                    { x: timestamp, ...newData }
                ];

                // Keep only the most recent 'maxPoints' data points
                if (updatedData.length > 10) {
                    updatedData.shift(); // Remove the oldest point
                }

                return updatedData;
            });

            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };
// Polling the server at the specified interval
useEffect(() => {
    const interval = setInterval(fetchData, pollingInterval);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
}, [pollingInterval]);

// Prepare data for Nivo Line Chart
const chartData = series.map(serie => ({
    id: serie.id,
    data: data.map(item => ({ x: item.x, y: item[serie.key] }))
}));

return (
    <Box
    gridColumn="span 2"
    gridRow="span 1"
    display="flex"
    flexDirection="column"
    justifyContent="space-between"
    p="1.25rem 1rem"
    flex="1 1 100%"
    backgroundColor={theme.palette.background.alt}
    borderRadius="0.55rem"
    border="0.5px solid"
  >
    <FlexBetween>
      <Typography variant="h6" sx={{ color: theme.palette.secondary[100] }}>
        {title}
      </Typography>
      {icon}
    </FlexBetween>

    <Typography
      variant="h3"
      fontWeight="600"
      sx={{ color: theme.palette.secondary[200] }}
    >
    <Box m="1.5rem 2.5rem">
        <Box height="75vh">
            {data ? (
                <ResponsiveLine
                    data={chartData}
                    theme={{
                        axis: {
                            domain: {
                                line: {
                                    stroke: theme.palette.secondary[200],
                                },
                            },
                            legend: {
                                text: {
                                    fill: theme.palette.secondary[200],
                                },
                            },
                            ticks: {
                                line: {
                                    stroke: theme.palette.secondary[200],
                                    strokeWidth: 1,
                                },
                                text: {
                                    fill: theme.palette.secondary[200],
                                },
                            },
                        },
                        legends: {
                            text: {
                                fill: theme.palette.secondary[200],
                            },
                        },
                        tooltip: {
                            container: {
                                color: theme.palette.primary.main,
                            },
                        },
                    }}
                    margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                    xScale={{ type: "point" }}
                    yScale={{
                        type: "linear",
                        min: yAxisRange ? yAxisRange.min : 'auto',
                        max: yAxisRange ? yAxisRange.max : 'auto',
                    }}
                    yFormat=" >-.2f"
                    // curve="catmullRom"
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                        orient: "bottom",
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: "Time",
                        legendOffset: 60,
                        legendPosition: "36",
                    }}
                    axisLeft={{
                        orient: "left",
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                        legend: "IO (Bytes) per second",
                        legendOffset: -40,
                    }}
                    enableGridX={false}
                    enableGridY={false}
                    pointSize={0}
                    pointColor={{ theme: "background" }}
                    pointBorderWidth={2}
                    pointBorderColor={{ from: "serieColor" }}
                    pointLabelYOffset={-12}
                    useMesh={true}
                    legends={[
                        {
                            anchor: "top-right",
                            direction: "column",
                            justify: false,
                            translateX: 50,
                            translateY: 0,
                            itemsSpacing: 0,
                            itemDirection: "left-to-right",
                            itemWidth: 80,
                            itemHeight: 20,
                            itemOpacity: 0.75,
                            symbolSize: 12,
                            symbolShape: "circle",
                            symbolBorderColor: "rgba(0, 0, 0, .5)",
                            effects: [
                                {
                                    on: "hover",
                                    style: {
                                        itemBackground: "rgba(0, 0, 0, .03)",
                                        itemOpacity: 1,
                                    },
                                },
                            ],
                        },
                    ]}
                />
            ) : (
                <>Loading...</>
            )}
        </Box>
    </Box>
    </Typography>
      <FlexBetween gap="1rem">
      </FlexBetween>
    </Box>
);
};

export default RealtimeGraph;