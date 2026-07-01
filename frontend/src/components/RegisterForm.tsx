'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button, Input, showNotification } from './common';
import { authAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const login = useAuthStore((state) => state.login);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await authAPI.register(formData);
      showNotification('Registration successful!');
      router.push('/auth/login');
    } catch (error: any) {
      showNotification(error.response?.data?.detail || 'Registration failed', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-900">Register</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <Input
          label="First Name"
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
        />
        <Input
          label="Last Name"
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
        />
        <Input
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <Button type="submit" isLoading={isLoading} className="w-full">
          Register
        </Button>
      </form>
      <p className="text-center mt-4 text-gray-600">
        Already have an account?{' '}
        <Link href="/auth/login" className="text-blue-600 hover:underline">
          Login
        </Link>
      </p>
    </div>
  );
}
