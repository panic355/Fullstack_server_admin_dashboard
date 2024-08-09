import React from "react";
import { Box, useTheme } from "@mui/material";
import { useGetAccountsQuery } from "state/api";
import { DataGrid } from "@mui/x-data-grid";
import Header from "components/Header";
import CustomColumnMenu from "components/DataGridCustomColumnMenu";
import { ReactTerminal } from "react-terminal";

const Accounts = () => {
    const theme = useTheme();
    const { data: accountsData, isLoading: accountsIsLoading } = useGetAccountsQuery();


    const columnsAccs = [
        {
            field: "uid",
            headerName: "ID",
            flex: 1,
        },
        {
            field: "username",
            headerName: "User Name",
            flex: 1,
        },
        {
            field: "fullName",
            headerName: "Full Name",
            flex: 1,
        },
        {
            field: "lastActive",
            headerName: "Last Active",
            flex: 1,
        },
        {
            field: "description",
            headerName: "Description",
            flex: 1,
        },
        {
            field: "groups",
            headerName: "Groups",
            flex: 1,
        },
    ];

    return (
        <Box m="1.5rem 2.5rem">
            <Box sx={{ border: '1px solid rgba(0, 0, 0, 0.3)', padding: '5px', borderRadius: '16px', boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.25)', }}>
                <Header title="Accounts" subtitle="Managing user acounts" />
                <Box
                    mt="40px"
                    height="75vh"
                    sx={{
                        "& .MuiDataGrid-root": {
                            border: "none",
                        },
                        "& .MuiDataGrid-cell": {
                            borderBottom: "none",
                        },
                        "& .MuiDataGrid-columnHeaders": {
                            backgroundColor: theme.palette.background.alt,
                            color: theme.palette.secondary[100],
                            borderBottom: "none",
                        },
                        "& .MuiDataGrid-virtualScroller": {
                            backgroundColor: theme.palette.primary.light,
                        },
                        "& .MuiDataGrid-footerContainer": {
                            backgroundColor: theme.palette.background.alt,
                            color: theme.palette.secondary[100],
                            borderTop: "none",
                        },
                        "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
                            color: `${theme.palette.secondary[200]} !important`,
                        },
                    }}
                >
                    <DataGrid
                        loading={accountsIsLoading || !accountsData}
                        rows={(accountsData) || []}
                        columns={columnsAccs}
                        getRowId={(accountsData) => accountsData.uid}
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default Accounts;