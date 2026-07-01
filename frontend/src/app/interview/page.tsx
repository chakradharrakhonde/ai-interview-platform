'use client';

import React from 'react';
import { useAuthStore } from '@/lib/store';
import { useRouter } from 'next/navigation';
import MockInterview from '@/components/MockInterview';

export default function InterviewPage() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  if (!isAuthenticated) {
    router.push('/auth/login');
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Mock Interview</h1>
      <MockInterview />
    </div>
  );
}
