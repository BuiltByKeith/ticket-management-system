import api from "./axios";

export const getSystems = () => api.get("/systems/");
export const getSystem = (ulid) => api.get(`/systems/${ulid}/`);
export const createSystem = (data) => api.post("/systems/", data);
export const updateSystem = (ulid, data) => api.patch(`/systems/${ulid}`, data);
export const deleteSystem = (ulid) => api.delete(`/systems/${ulid}/`);
