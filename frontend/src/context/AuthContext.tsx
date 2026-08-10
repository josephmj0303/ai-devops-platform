import {
  createContext,
  useContext,
  useState,
} from "react";

import type { ReactNode } from "react";

interface AuthContextType {
  token: string | null;

  login: (token: string) => void;

  logout: () => void;

  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  const login = (token: string) => {
    localStorage.setItem("token", token);
    setToken(token);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within AuthProvider"
    );
  }

  return context;
}
