'use client';

import React from 'react';
import { useAuthStore } from '@/lib/store';
import { useRouter } from 'next/navigation';
import ResumeUploader from '@/components/ResumeUploader';

export default function ResumePage() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  if (!isAuthenticated) {
    router.push('/auth/login');
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Resume Analysis</h1>
      <ResumeUploader />
    </div>
  );
}
