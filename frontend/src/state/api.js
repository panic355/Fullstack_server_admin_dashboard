import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:5001" }),
  reducerPath: "adminApi",
  tagTypes: [
    "User",
    "Products",
    "Customers",
    "Transactions",
    "Geography",
    "Sales",
    "Admins",
    "Service",
    "Dashboard",
    "Performance",
    "Logs",
  ],
  endpoints: (build) => ({
    getUser: build.query({
      query: (id) => `general/user/${id}`,
      providesTags: ["User"],
    }),
    getTransactions: build.query({
      query: ({ page, pageSize, sort, search }) => ({
        url: "client/transactions",
        method: "GET",
        params: { page, pageSize, sort, search },
      }),
      providesTags: ["Transactions"],
    }),
    getGeography: build.query({
      query: () => "client/geography",
      providesTags: ["Geography"],
    }),
    getAdmins: build.query({
      query: () => "management/admins",
      providesTags: ["Admins"],
    }),
    getUserPerformance: build.query({
      query: () => `management/performance`,
      providesTags: ["Performance"],
    }),
    getDashboard: build.query({
      query: () => "general/dashboard",
      providesTags: ["Dashboard"],
    }),
    getEntity: build.query({
      query: () => "general/entity",
      providesTags: ["Entity"],
    }),
    getService: build.query({
      query: () => "general/services",
      providesTags: ["Service"],
    }),
    getLogs: build.query({
      query: () => "general/logs",
      providesTags: ["Logs"],
    }),
    getSystem: build.query({
      query: () => "general/system",
      providesTags: ["System"],
    }),
    getAccounts: build.query({
      query: () => "general/accounts",
      providesTags: ["Accounts"],
    }),
  }),
});

export const {
  useGetUserQuery,
  useGetTransactionsQuery,
  useGetGeographyQuery,
  useGetAdminsQuery,
  useGetUserPerformanceQuery,
  useGetDashboardQuery,
  useGetEntityQuery,
  useGetServiceQuery,
  useGetLogsQuery,
  useGetSystemQuery,
  useGetAccountsQuery,
} = api;
