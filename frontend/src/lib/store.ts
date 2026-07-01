import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  login: (token, user) =>
    set({
      token,
      user,
      isAuthenticated: true,
    }),
  logout: () =>
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    }),
  setUser: (user) => set({ user }),
}));
