import api from "./axios";

export const getOffices = () => api.get("/offices/");
export const getOffice = (ulid) => api.get(`/offices/${ulid}/`);
export const createOffice = (data) => api.post("/offices/", data);
export const updateOffice = (ulid, data) => api.patch(`/offices/${ulid}`, data);
export const deleteOffice = (ulid) => api.delete(`/offices/${ulid}/`);
