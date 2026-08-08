import api from "./axios";
import type { LoginRequest, LoginResponse } from "../types/auth";

export const login = async (
  credentials: LoginRequest
): Promise<LoginResponse> => {
  const formData = new URLSearchParams();

  formData.append("username", credentials.email);
  formData.append("password", credentials.password);

  const response = await api.post<LoginResponse>(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};
