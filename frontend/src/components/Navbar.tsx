import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { Button } from './common';

export default function Navbar() {
  const router = useRouter();
  const { isAuthenticated, user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    router.push('/auth/login');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-blue-600 cursor-pointer" onClick={() => router.push('/')}>
          AI Interview
        </div>
        
        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <span className="text-gray-700">{user?.email}</span>
              <Button onClick={handleLogout} variant="outline" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button onClick={() => router.push('/auth/login')} variant="outline" size="sm">
                Login
              </Button>
              <Button onClick={() => router.push('/auth/register')} size="sm">
                Register
              </Button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
