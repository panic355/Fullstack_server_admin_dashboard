import React from "react";
import FlexBetween from "components/FlexBetween";
import Header from "components/Header";
import {
  DownloadOutlined,
  MemoryOutlined,
  PersonAdd,
  Traffic,
  DeveloperBoardOutlined,
  StorageOutlined,
  LockOutlined
} from "@mui/icons-material";
import {
  Box,
  Button,
  Typography,
  useTheme,
  useMediaQuery,
  Tooltip,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import OverviewChart from "components/OverviewChart";
import { useGetDashboardQuery, useGetEntityQuery, useGetServiceQuery, useGetSystemQuery } from "state/api";
import StatBox from "components/StatBox";
import RealtimeGraph from 'components/RealtimeGraph';




const Dashboard = () => {
  const theme = useTheme();
  const isNonMediumScreens = useMediaQuery("(min-width: 1200px)");
  const { data: serviceData, isLoading: serviceIsLoading } = useGetServiceQuery();
  const { data: DashData, isLoading: DashIsLoading } = useGetDashboardQuery();
  const { data: systemData, isLoading: systemIsLoading } = useGetSystemQuery();

  const cpuNetworkSeries = [
    { id: 'Upload', key: 'net_io_sent' },
    { id: 'Download', key: 'net_io_recv' }
  ];

  const yAxisRange = { min: 0, max: 200 }


  const columnsDash = [
    {
      field: "unit",
      headerName: "Unit",
      flex: 1,
      renderCell: (params) => (
        <Tooltip title={params.value} arrow>
          <span>{params.value.length > 20 ? `${params.value.substring(0, 20)}...` : params.value}</span>
        </Tooltip>
      ),
    },
    {
      field: "load",
      headerName: "Load",
      flex: 1,
    },
    {
      field: "active",
      headerName: "Active",
      flex: 1,
    },
    {
      field: "sub",
      headerName: "Sub",
      flex: 1,
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1,
      renderCell: (params) => (
        <Tooltip title={params.value} arrow>
          <span>{params.value.length > 20 ? `${params.value.substring(0, 20)}...` : params.value}</span>
        </Tooltip>
      ),
    },
  ];


  return (
    <Box m="1.5rem 2.5rem">
      <FlexBetween>
        <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />

        <Box>
          <Button
            sx={{
              backgroundColor: theme.palette.secondary.light,
              color: theme.palette.background.alt,
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            <LockOutlined sx={{ mr: "10px" }} />
            Autherize SUDO - TODO
          </Button>
        </Box>
      </FlexBetween>

      <Box
        mt="20px"
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="160px"
        gap="20px"
        sx={{
          "& > div": { gridColumn: isNonMediumScreens ? undefined : "span 12" },
        }}
      >
        {/* ROW 1 */}
        <StatBox
          title="CPU Load (TODO)"
          icon={
            <DeveloperBoardOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "26px" }}
            />
          }
        />
        <StatBox
          title="CPU Load (TODO)"
          icon={
            <DeveloperBoardOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "26px" }}
            />
          }
        />

        <Box
          gridColumn="span 8"
          gridRow="span 2"
          backgroundColor={theme.palette.background.alt}
          p="1rem"
          borderRadius="0.55rem"
        >
        </Box>
        <StatBox
          title="Storage usage (TODO)"
          //value={data }
          increase="+5%"
          description="In procentage"
          icon={
            <StorageOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "26px" }}
            />
          }
        />
        <StatBox
          title="RAM Usage (TODO)"
          isDashboard={true}
          description="In procentage"
          icon={
            <MemoryOutlined
              sx={{ color: theme.palette.secondary[300], fontSize: "26px" }}
            />
          }
        />


        {/* ROW 2 */}
        <Box
          gridColumn="span 9"
          gridRow="span 3"
          sx={{
            "& .MuiDataGrid-root": {
              border: "none",
              borderRadius: "5rem",
            },
            "& .MuiDataGrid-cell": {
              borderBottom: "none",
            },
            "& .MuiDataGrid-columnHeaders": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderBottom: "1px solid",
            },
            "& .MuiDataGrid-virtualScroller": {
              backgroundColor: theme.palette.background.alt,
            },
            "& .MuiDataGrid-footerContainer": {
              backgroundColor: theme.palette.background.alt,
              color: theme.palette.secondary[100],
              borderTop: "none",
            },
            "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
              color: `${theme.palette.secondary[200]} !important`,
            },
            border: '1px solid rgba(0, 0, 0, 0.3)',
            borderRadius: '16px',
            boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.25)',
          }}
        >
          <DataGrid
            loading={serviceIsLoading || !serviceData}
            rows={(serviceData) || []}
            columns={columnsDash}
          />
        </Box>
        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={theme.palette.background.alt}
          p="1.5rem"
          borderRadius="0.55rem"
          sx={{ border: '1px solid rgba(0, 0, 0, 0.3)', borderRadius: '16px', boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.25)', }}
        >
          <Typography variant="h4" sx={{ color: theme.palette.secondary[100] }}>
            System information
          </Typography>
          <Typography
            variant="h6"
            p="0.6rem 0.6rem"
            sx={{ color: theme.palette.secondary[100] }}
          >
            CPU: {(systemData && systemData["CPU Info"].Modelnavn) || []}
          </Typography>
          <Typography
            variant="h6"
            p="0.6rem 0.6rem"
            sx={{ color: theme.palette.secondary[100] }}
          >
            BIOS Version: {(systemData && systemData["BIOS Version"]) || ["unknown"]}
          </Typography>
          <Typography
            variant="h6"
            p="0.6rem 0.6rem"
            sx={{ color: theme.palette.secondary[100] }}
          >
            RAM Capacity: {(systemData && systemData["RAM Info"].Total) || []}
          </Typography>
          <Typography
            variant="h6"
            p="0.6rem 0.6rem"
            sx={{ color: theme.palette.secondary[100] }}
          >
            Storage Devices present:{" "}
            {(systemData && systemData["Storage Devices"].length) || []}
          </Typography>
          <Typography
            //p="0 0.6rem"
            fontSize="0.8rem"
            sx={{ color: theme.palette.secondary[200] }}
          >
            Basic Information about system setup.
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
