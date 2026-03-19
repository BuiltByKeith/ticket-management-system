import api from "./axios";

export const getConcernTypes = () => api.get("/concern-types/");
export const getConcernType = (ulid) => api.get(`/concern-types/${ulid}/`);
export const createConcernType = (data) => api.post("/concern-types/", data);
export const updateConcernType = (ulid, data) =>
  api.patch(`/concern-types/${ulid}/`, data);
export const deleteConcernType = (ulid) => api.delete(`/concern-types/${ulid}`);
