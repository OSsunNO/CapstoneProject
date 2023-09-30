import axios from "axios";

const useApi = axios.create({
    headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Access-Control-Allow-Origin": "http://localhost:5001",
        "Access-Control-Allow-Credentials": "true",
    },
});

const useApi_file = axios.create({
    headers: {
        "Content-Type": "multipart/form-data",
    },
});

useApi.interceptors.response.use((response) => response);
useApi_file.interceptors.response.use((response) => response);

export { useApi as default, useApi_file };
