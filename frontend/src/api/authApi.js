import api from "./axios";

// Endpoint to target the django login API
export const login = (credentials) => api.post("/auth/login/", credentials);

// End point to call the logout function that has a parameter of the current users refresh token
export const logout = (refresh) => api.post("/auth/logout/", refresh);

export const getMe = () => api.get("/auth/me/");
