'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { Button, Card } from '@/components/common';

export default function Home() {
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();

  if (isAuthenticated) {
    router.push('/dashboard');
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-900">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-20">
          <h1 className="text-5xl font-bold text-white mb-4">AI Interview Platform</h1>
          <p className="text-xl text-blue-100 mb-8">
            Master interviews with AI-powered practice and personalized feedback
          </p>
          <div className="flex gap-4 justify-center">
            <Button
              onClick={() => router.push('/auth/register')}
              size="lg"
              className="bg-white text-blue-600 hover:bg-gray-100"
            >
              Get Started
            </Button>
            <Button
              onClick={() => router.push('/auth/login')}
              variant="outline"
              size="lg"
              className="border-white text-white hover:bg-blue-700"
            >
              Login
            </Button>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <Card className="text-center">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-bold mb-2">Mock Interviews</h3>
            <p className="text-gray-600">Practice with AI-generated questions tailored to your role</p>
          </Card>
          <Card className="text-center">
            <div className="text-4xl mb-4">📝</div>
            <h3 className="text-xl font-bold mb-2">Resume Analysis</h3>
            <p className="text-gray-600">Get ATS scoring and actionable feedback on your resume</p>
          </Card>
          <Card className="text-center">
            <div className="text-4xl mb-4">💡</div>
            <h3 className="text-xl font-bold mb-2">Skill Building</h3>
            <p className="text-gray-600">Personalized learning paths to improve your interview skills</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
