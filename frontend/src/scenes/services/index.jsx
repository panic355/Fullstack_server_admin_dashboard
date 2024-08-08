import React, { useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Box, useTheme, useMediaQuery } from "@mui/material";
import Header from "components/Header";
import { useGetServiceQuery } from "state/api";

const Services = () => {
  const theme = useTheme();
  const { data, isLoading } = useGetServiceQuery();
  const isNonMobile = useMediaQuery("(min-width: 1000px)");

  const columnsDash = [
    {
      field: "unit",
      headerName: "Unit",
      flex: 2,
    },
    {
      field: "description",
      headerName: "description",
      flex: 2,
    },
    {
      field: "load",
      headerName: "load",
      flex: 0,
    },
    {
      field: "active",
      headerName: "active",
      flex: 0,
    },
    {
      field: "sub",
      headerName: "sub",
      flex: 0,
    },
  ];

  return (
    <Box m="1.5rem 2.5rem">
      <Header title="Services" subtitle="Shows list of services." />
      <Box
        gridColumn="span 5"
        gridRow="span 10"
        backgroundColor={theme.palette.background.alt}
        p="0.6rem 1.5rem"
        borderRadius="0.55rem"
        height={700}
      >
        <DataGrid
          loading={isLoading || !data}
          getRowId={(row) => row._id}
          rows={data || []}
          columns={columnsDash}
        />
      </Box>
    </Box>
  );
};

export default Services;
